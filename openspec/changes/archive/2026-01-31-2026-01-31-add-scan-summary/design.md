## Context
The `judge_essence_quality()` function already determines if an essence is a "treasure" by matching:
1. User-defined treasure conditions (`config.treasure_essence_stats`)
2. Implemented weapons from `weapon_basic_table` and `weapon_stats_dict`

When a treasure is found, the function logs which weapon it matches. However, this information is scattered across individual logs and not aggregated for easy review.

## Goals / Non-Goals
**Goals:**
- Collect treasure essence information during scanning
- Display a consolidated summary after scan completion showing implemented weapons with matching treasures
- Group treasures by the weapons they match

**Non-Goals:**
- Persist summary data to files or database
- Display summary in Web UI (log output only)
- Real-time summary updates during scanning
- Summary for trash essences
- Summary for user-defined treasure conditions (only implemented weapons)
- List weapons without matching treasures
- Historical tracking of scans

## Decisions

### Summary Data Structure
- **Decision:** Use a dictionary to track treasures by weapon ID
- **Reason:** Multiple essences can match the same weapon; need to count them; only track implemented weapons
- **Implementation:**
  ```python
  treasure_summary: dict[str, dict] = {
      "weapon_id": {
          "name": str,
          "rarity": int,
          "weapon_type": str,
          "count": int
      }
  }
  ```
- **Alternative considered:** Flat list of treasure records - harder to aggregate

### Summary Collection Point
- **Decision:** Collect data in `judge_essence_quality()` function, report in scanner after loop
- **Reason:** `judge_essence_quality()` already has all the matching logic and weapon info
- **Implementation details:**
  - Pass a mutable `treasure_summary` dict to `judge_essence_quality()`
  - Update dict when treasure is found
  - Log summary at end of `EssenceScanner.run()` or `recognize_once()`
- **Alternative considered:** Post-processing logs - fragile and inaccurate

### Summary Report Format
- **Decision:** Use formatted log output with color and structure, showing only implemented weapons
- **Reason:** Consistent with existing log style; easy to read in console; focus on what matters most
- **Format:**
  ```
  ==================== 扫描总结 ====================
  共找到 <bold>N</bold> 个宝藏基质

  【已实装武器】
  - 武器名 (5★ 枪械): x 个
  - 武器名 (6★ 近战): x 个
  =================================================
  ```
- **Alternative considered:** JSON or table format - less human-readable

### Modes of Operation
- **Decision:** Support both single recognition and full scan modes
- **Reason:** User may use `[` key for one essence, still wants to know if it's a treasure
- **Implementation:**
  - `recognize_once()`: Report summary after single essence
  - `EssenceScanner.run()`: Report summary after full scan completes
- **Alternative considered:** Summary only for full scan - less useful

### Handling Interruption
- **Decision:** Always report summary even if scan is interrupted
- **Reason:** User may stop scan early; partial summary is still valuable
- **Implementation:** Log summary in `finally` block or after loop

## Risks / Trade-offs

### Risk: Summary Inaccuracy on Recognition Failure
- **Risk:** If recognition fails (None values), essence not counted correctly
- **Mitigation:** Only count essences with complete, recognized stats; skip incomplete recognitions

### Risk: Performance Overhead
- **Risk:** Dictionary updates on every essence recognition adds minimal overhead
- **Mitigation:** O(1) dictionary operations; negligible compared to screenshot processing

### Risk: Weapon Name Not Found
- **Risk:** `get_item_name()` or translation may fail for some weapon IDs
- **Mitigation:** Use weapon ID as fallback; log error for missing translations

### Trade-off: Verbose Summary vs Compact Summary
- Choose moderately detailed summary with grouped stats and counts
- Accept longer log output for better readability

## Migration Plan
1. Add `treasure_summary` parameter to `judge_essence_quality()` function
2. Modify `judge_essence_quality()` to update summary dict when treasure found
3. Add `format_summary_report()` function to generate formatted summary string
4. Call `format_summary_report()` and log result in:
   - `recognize_one()` after single recognition
   - `EssenceScanner.run()` after full scan loop (even if interrupted)
5. No breaking changes to existing behavior; summary is additive output

## Open Questions
- Should summary include which specific essences (by position) are treasures? (Probably too verbose)
- Should we exclude "trash weapons" from treasure summary? (Yes, already excluded in `judge_essence_quality()`)
