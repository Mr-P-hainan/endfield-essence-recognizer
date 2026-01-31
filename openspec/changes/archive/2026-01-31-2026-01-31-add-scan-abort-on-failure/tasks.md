## 1. Add Abort Constants
- [x] 1.1 Add `MAX_CONSECUTIVE_FAILURES = 3` constant
- [x] 1.2 Add `MAX_CONSECUTIVE_LOW_SCORES = 5` constant
- [x] 1.3 Add `LOW_SCORE_THRESHOLD = 0.6` constant
- [x] 1.4 Add `MAX_CONSECUTIVE_DUPLICATE_RESULTS = 2` constant

## 2. Modify recognize_essence() to Return Scores
- [x] 2.1 Modify function signature to return attribute scores along with results
- [x] 2.2 Collect scores from each attribute recognition
- [x] 2.3 Return tuple: (stats, deprecated_str, locked_str, attribute_scores)
- [x] 2.4 Update `recognize_once()` to handle new return value

## 3. Add Abort Logic in EssenceScanner.run()
- [x] 3.1 Initialize `consecutive_failures` counter variable
- [x] 3.2 Initialize `consecutive_low_scores` counter variable
- [x] 3.3 Add `consecutive_duplicate_results` counter variable
- [x] 3.4 Add `last_recognized_stats` tracking variable
- [x] 3.5 Add button failure check after recognize_essence() call
- [x] 3.6 Add low score check after recognize_essence() call
- [x] 3.7 Add duplicate result check after recognize_essence() call
- [x] 3.8 Implement abort with warning message when thresholds exceeded
- [x] 3.9 Reset counters on successful recognitions

## 4. Integration and Testing
- [x] 4.1 Update `recognize_once()` to unpack new return value correctly
- [x] 4.2 Ensure finally block still executes after abort
- [x] 4.3 Verify summary report displays correctly after abort
- [x] 4.4 Verify duplicate result detection works correctly
- [ ] 4.5 Test abort on 3 consecutive button failures
- [ ] 4.6 Test abort on 5 consecutive low scores
- [ ] 4.7 Test abort on 2 consecutive duplicate results
- [ ] 4.8 Test counter reset on successful recognition
- [ ] 4.9 Test that intermittent failures don't trigger abort

## 5. Validation
- [x] 5.1 Run `openspec validate 2026-01-31-add-scan-abort-on-failure --strict`
- [x] 5.2 Resolve any validation errors
- [x] 5.3 Review warning messages for clarity
