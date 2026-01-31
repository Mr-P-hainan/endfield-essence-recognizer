## 1. Data Structure and Collection
- [x] 1.1 Define `treasure_summary` data structure in `essence_scanner.py`
- [x] 1.2 Add `treasure_summary` parameter to `judge_essence_quality()` function
- [x] 1.3 Modify `judge_essence_quality()` to update summary when weapon-matched treasure found
- [x] 1.4 Ensure trash weapons are excluded from treasure summary

## 2. Summary Report Generation
- [x] 2.1 Implement `format_summary_report()` function
- [x] 2.2 Format weapon treasures section with weapon names, rarity, type, and counts
- [x] 2.3 Apply color formatting (bold, colors) for readability
- [x] 2.4 Handle edge cases: empty summary

## 3. Integration with Scanner
- [x] 3.1 Call `format_summary_report()` in `recognize_once()` after single recognition
- [x] 3.2 Call `format_summary_report()` in `EssenceScanner.run()` after full scan loop
- [x] 3.3 Ensure summary is logged even when scan is interrupted
- [x] 3.4 Initialize empty `treasure_summary` dict at start of scans
- [x] 3.5 Test that summary logging doesn't break existing functionality

## 4. Testing
- [ ] 4.1 Test single essence recognition with `[` key - verify summary appears
- [ ] 4.2 Test full scan with `]` key - verify complete summary
- [ ] 4.3 Test scan interruption - verify partial summary appears
- [ ] 4.4 Test with no treasures found - verify zero count shown correctly
- [ ] 4.5 Test with multiple essences matching same weapon - verify grouping works
- [ ] 4.6 Test trash weapons are excluded from summary
- [ ] 4.7 Test recognition failures (None stats) - verify not counted

## 5. Validation
- [x] 5.1 Run `openspec validate 2026-01-31-add-scan-summary --strict`
- [x] 5.2 Resolve any validation errors
- [ ] 5.3 Review summary output for clarity and formatting
