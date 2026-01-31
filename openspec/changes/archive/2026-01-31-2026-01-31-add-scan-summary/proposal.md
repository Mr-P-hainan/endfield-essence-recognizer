# Change: Add Scan Summary Report

## Why
Currently, after scanning all essences, the tool only logs individual essence recognition results without providing a consolidated summary. Users cannot easily see:
- Which weapons have found matching treasure essences
- How many treasures were found for each weapon
- Which weapons are still missing suitable essences

Adding a summary report at the end of scanning will help users quickly understand their essence inventory status and make informed decisions about which weapons need essences.

## What Changes
- Add a summary tracker to collect treasure essence information during scanning
- Implement a summary report generator that logs statistics after scan completion
- Display a formatted summary showing:
  - Total treasures found
  - List of implemented weapons with matching treasures (grouped by weapon)
- Support both single-essence recognition (`[` key) and full scan (`]` key) modes

## Impact
- Affected specs: N/A (new capability)
- Affected code:
  - `src/endfield_essence_recognizer/essence_scanner.py` (add summary tracking and reporting)
  - No changes to configuration or user interface
- Breaking changes: None

## Scope Clarification
- **Included**: Summary logging for treasure essences grouped by matching implemented weapons
- **Excluded**: Summary for user-defined treasure conditions (only implemented weapons)
- **Excluded**: Summary for trash essences (not user-relevant)
- **Excluded**: List of weapons without matching treasures
- **Excluded**: Persistent storage of summary data (log output only)
- **Excluded**: Web UI display of summary (logs only for now)
