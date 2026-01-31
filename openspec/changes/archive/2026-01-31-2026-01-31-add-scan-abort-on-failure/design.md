## Context
The `EssenceScanner.run()` method currently scans through all essence positions on all pages, only stopping when:
1. User manually interrupts with `]` key
2. Game window loses focus
3. Bottom of essence list is detected

However, if the user is not on the essence inventory screen (e.g., switched to character screen, inventory, or a different game), the scanner will:
- Still click on essence icon positions
- Fail to recognize deprecated/locked button states (return None)
- Log confusing messages
- Waste time scanning non-existent essences

Similarly, if recognition scores are consistently low, it indicates the templates are not matching well, which could mean wrong screen or corrupted recognition.

## Goals / Non-Goals
**Goals:**
- Detect when recognition is consistently failing
- Abort scanning early with clear explanation
- Save user time and reduce confusing log output
- Still show summary report even if aborted early

**Non-Goals:**
- Configurable thresholds via settings file (use code constants)
- Adaptive thresholds based on success rate
- Retry logic with different recognition parameters
- Abort based on treasure/trash ratio

## Decisions

### Failure Type 1: Button Recognition Failure
- **Decision:** Track consecutive failures where deprecated_str or locked_str is None
- **Threshold:** 3 consecutive failures → abort
- **Reason:** If button states can't be recognized 3 times in a row, user is likely not on essence screen
- **Implementation:**
  ```python
  consecutive_failures = 0
  if deprecated_str is None or locked_str is None:
      consecutive_failures += 1
      if consecutive_failures >= 3:
          abort("连续 3 次无法识别按钮状态，可能未在基质界面")
  else:
      consecutive_failures = 0  # reset on success
  ```

### Failure Type 2: Low Recognition Score
- **Decision:** Track consecutive attribute recognitions with scores below threshold
- **Threshold:** 5 consecutive low scores → abort
- **Score threshold:** All 3 attributes have score < 0.6
- **Reason:** If all attributes score very low consistently, recognition is not working properly
- **Implementation:**
  ```python
  # Need to modify recognize_essence() to return scores
  scores = [...]
  low_score_count = sum(1 for s in scores if s < 0.6)
  if low_score_count == 3:
      consecutive_low_scores += 1
      if consecutive_low_scores >= 5:
          abort("连续多次识别分数过低，识别可能存在异常")
  else:
      consecutive_low_scores = 0
  ```

### Abort Behavior
- **Decision:** When abort condition met, break loop and log warning, still show summary
- **Reason:** User should know why scanning stopped early; partial summary is still useful
- **Implementation:**
  ```python
  logger.warning("扫描已中止：{reason}")
  # Still execute finally block to show summary
  ```

### Abort Message Format
- **Decision:** Use clear, actionable Chinese messages
- **Reason:** Users need to understand what went wrong and how to fix it
- **Messages:**
  - "连续 3 次无法识别按钮状态，可能未在基质界面。请按 'N' 键打开贵重品库后切换到武器基质页面。"
  - "连续多次识别分数过低，可能不在正确页面或识别异常。请检查游戏界面。"

### Counter Reset Behavior
- **Decision:** Reset counters on successful recognition
- **Reason:** Intermittent failures are OK; only abort on consistent failures
- **Implementation:** Reset counter when deprecated_str/locked_str are not None and scores are acceptable

## Risks / Trade-offs

### Risk: False Positive Aborts
- **Risk:** Legitimate essences might temporarily fail recognition, causing early abort
- **Mitigation:** Set thresholds high enough (3-5 consecutive failures) to tolerate intermittent issues
- **Acceptable Trade-off:** Better to abort early with clear message than waste 10 minutes scanning nothing

### Risk: Recognition Score Threshold Too Strict
- **Risk:** Valid essences with slightly poor matching could trigger abort
- **Mitigation:** Use relatively low threshold (0.6) and require 5 consecutive occurrences
- **Acceptable Trade-off:** If recognition is consistently that poor, it's not working reliably anyway

### Risk: Breaking Existing Workflow
- **Risk:** Users who expect scanner to run regardless might be surprised
- **Mitigation:** Clear warning messages explain why abort happened; no change to manual interrupt
- **Acceptable Trade-off**: Improved user experience outweighs rare edge cases

## Migration Plan
1. Add constants to essence_scanner.py:
   - `MAX_CONSECUTIVE_FAILURES = 3`
   - `MAX_CONSECUTIVE_LOW_SCORES = 5`
   - `LOW_SCORE_THRESHOLD = 0.6`
2. Modify `recognize_essence()` to return recognition scores along with results
3. Add counter variables in `EssenceScanner.run()`: `consecutive_failures`, `consecutive_low_scores`
4. Add abort logic after each essence recognition in the scan loop
5. Add warning log messages when abort conditions are triggered
6. Ensure finally block still executes to show summary report
7. No breaking changes to public API or behavior

## Open Questions
- Should low score threshold be configurable? (Probably not needed; 0.6 is reasonable)
- Should we track failures per page or globally? (Global is simpler and sufficient)
- Should abort message include statistics (e.g., "5/10 essences failed")? (Nice to have but not required)
