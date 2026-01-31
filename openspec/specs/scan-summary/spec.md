# scan-summary Specification

## Purpose
TBD - created by archiving change 2026-01-31-add-scan-summary. Update Purpose after archive.
## Requirements
### Requirement: Collect Treasure Information During Scanning
The system SHALL collect and track treasure essence information during the scanning process, grouping treasures by the implemented weapons they match.

#### Scenario: Collect weapon-matched treasure essence
- **GIVEN** the system is scanning essences
- **WHEN** an essence's stats match an implemented weapon from `weapon_stats_dict`
- **AND** the weapon ID is NOT in `config.trash_weapon_ids`
- **THEN** the system SHALL increment the count for that weapon
- **AND** SHALL store the weapon name, rarity, and type

#### Scenario: Skip trash weapon essence
- **GIVEN** the system is scanning essences
- **WHEN** an essence matches a weapon that IS in `config.trash_weapon_ids`
- **THEN** the system SHALL NOT add it to the treasure summary
- **AND** SHALL log it as trash (existing behavior)

#### Scenario: Handle recognition failure
- **GIVEN** the system is scanning essences
- **WHEN** essence recognition fails (returns None for any stat)
- **THEN** the system SHALL NOT add this essence to the treasure summary
- **AND** SHALL continue processing other essences

### Requirement: Generate and Log Summary Report
The system SHALL generate a formatted summary report and log it after scanning completes or is interrupted.

#### Scenario: Summary after full scan completion
- **GIVEN** the system has completed a full scan of all essence pages
- **WHEN** the scan loop finishes (bottom detected or interruption)
- **THEN** the system SHALL log a formatted summary containing:
  - Total count of treasure essences found
  - List of implemented weapons with matching treasures, showing:
    - Weapon name (Chinese)
    - Rarity (star rating)
    - Weapon type (Chinese)
    - Count of matching essences
- **AND** SHALL use color formatting for readability (bold, colors)

#### Scenario: Summary after single essence recognition
- **GIVEN** the user pressed `[` key to recognize a single essence
- **WHEN** the recognition completes
- **THEN** the system SHALL log a summary report for that single essence
- **AND** SHALL show count as 1 if treasure, or indicate no treasures if trash

#### Scenario: Summary after scan interruption
- **GIVEN** the system is scanning multiple pages
- **WHEN** the user presses `]` key to interrupt the scan
- **THEN** the system SHALL log a summary report for all essences processed so far
- **AND** SHALL indicate the scan was interrupted in the log

#### Scenario: Empty treasure summary
- **GIVEN** the system has completed scanning
- **WHEN** no treasure essences were found
- **THEN** the system SHALL log "共找到 0 个宝藏基质"
- **AND** SHALL skip listing weapons with treasures

#### Scenario: Summary format structure
- **GIVEN** the system generates a summary report
- **THEN** the summary SHALL follow this format:
  ```
  ==================== 扫描总结 ====================
  共找到 <N> 个宝藏基质

  【已实装武器】
  - <武器名> (<rarity>★ <武器类型>): <x> 个
  - <武器名> (<rarity>★ <武器类型>): <x> 个
  =================================================
  ```

### Requirement: Group Treasures by Weapon
The system SHALL group treasure essences by the weapon they match to identify multiple essences suitable for the same weapon.

#### Scenario: Multiple essences match same weapon
- **GIVEN** the system scans multiple essences
- **WHEN** 2 or more essences match the same weapon
- **THEN** the system SHALL group them under one weapon entry
- **AND** SHALL display the total count (e.g., "3 个")

