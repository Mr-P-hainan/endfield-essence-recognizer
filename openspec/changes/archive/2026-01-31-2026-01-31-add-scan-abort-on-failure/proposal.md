# Change: Add Scan Abort on Recognition Failure

## Why
Currently, the essence scanner continues scanning even when recognition is consistently failing (e.g., user switched to a different game screen, recognition templates are mismatched, or very few essences exist). This leads to:
- Wasted time clicking and scanning empty/invalid positions
- Confusing logs filled with failed recognition attempts
- No clear indication that scanning is not working properly

Adding intelligent abort logic will improve user experience by detecting failure patterns and stopping early with clear feedback.

## What Changes
- Add consecutive failure counter to track recognition failures
- Add low recognition score counter to track poor quality matches
- Add duplicate result counter to detect when clicking empty positions
- Modify `recognize_essence()` to return recognition scores along with results
- Implement abort thresholds:
  - Stop after 3 consecutive recognition failures (button states return None)
  - Stop after 5 consecutive low-score recognitions (all attributes < 0.6)
  - Stop after 2 consecutive duplicate recognition results (indicates empty position)
- Log warning message explaining why scanning stopped
- Still display summary report even when aborted early

## Impact
- Affected specs: New spec `scan-abort` created
- Affected code:
  - `src/endfield_essence_recognizer/essence_scanner.py` (EssenceScanner.run method, recognize_essence function)
- Breaking changes: None

## Scope Clarification
- **Included**: Abort on consecutive button recognition failures (deprecated/locked state None)
- **Included**: Abort on consecutive low recognition scores (attribute recognition)
- **Included**: Abort on consecutive duplicate recognition results (clicking empty positions)
- **Included**: Clear warning messages explaining abort reason
- **Included**: Return recognition scores for abort detection
- **Excluded**: Configurable thresholds via config file (use constants for now)
- **Excluded**: Retry logic or adaptive thresholds (simple fixed thresholds)
- **Excluded**: Abort based on treasure/trash ratio (focus on recognition quality)
