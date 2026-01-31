# scan-abort Specification

## Purpose
TBD - created by archiving change 2026-01-31-add-scan-abort-on-failure. Update Purpose after archive.
## Requirements
### Requirement: Abort on Consecutive Button Recognition Failures
The system SHALL abort scanning when button state recognition (deprecated/locked) consistently fails, indicating the user may not be on the essence inventory screen.

#### Scenario: Three consecutive button recognition failures trigger abort
- **GIVEN** the system is scanning essences
- **WHEN** button state recognition returns None for both deprecated_str and locked_str
- **AND** this occurs for 3 consecutive essences
- **THEN** the system SHALL abort scanning immediately
- **AND** SHALL log a warning message: "连续 3 次无法识别按钮状态，可能未在基质界面。请按 'N' 键打开贵重品库后切换到武器基质页面。"
- **AND** SHALL still display the summary report

#### Scenario: Reset failure counter on successful recognition
- **GIVEN** the system has accumulated some button recognition failures
- **WHEN** the next essence recognition succeeds (both button states recognized)
- **THEN** the system SHALL reset the consecutive failure counter to 0
- **AND** SHALL continue scanning normally

#### Scenario: Intermittent failures do not trigger abort
- **GIVEN** the system is scanning essences
- **WHEN** button recognition fails, then succeeds, then fails again
- **THEN** the system SHALL NOT abort (failures are not consecutive)
- **AND** SHALL continue scanning

### Requirement: Abort on Consecutive Low Recognition Scores
The system SHALL abort scanning when attribute recognition scores are consistently very low, indicating recognition is not working properly.

#### Scenario: Five consecutive low-score recognitions trigger abort
- **GIVEN** the system is scanning essences
- **WHEN** all 3 attribute recognitions have scores below 0.6
- **AND** this occurs for 5 consecutive essences
- **THEN** the system SHALL abort scanning immediately
- **AND** SHALL log a warning message: "连续多次识别分数过低，可能不在正确页面或识别异常。请检查游戏界面。"
- **AND** SHALL still display the summary report

#### Scenario: Reset low-score counter on acceptable recognition
- **GIVEN** the system has accumulated some low-score recognitions
- **WHEN** the next essence has at least one attribute with score >= 0.6
- **THEN** the system SHALL reset the consecutive low-score counter to 0
- **AND** SHALL continue scanning normally

#### Scenario: Mixed scores do not trigger abort
- **GIVEN** the system is scanning essences
- **WHEN** an essence has 2 low scores but 1 acceptable score (>= 0.6)
- **THEN** the system SHALL NOT increment the low-score counter
- **AND** SHALL NOT abort

### Requirement: Return Recognition Scores for Abort Detection
The system SHALL return recognition scores along with recognition results to enable abort logic to detect low-quality matches.

#### Scenario: recognize_essence returns scores
- **GIVEN** the system needs to track recognition quality
- **WHEN** `recognize_essence()` is called
- **THEN** it SHALL return a tuple containing: (stats, deprecated_str, locked_str, attribute_scores)
- **WHERE** `attribute_scores` is a list of 3 floats representing recognition scores for each attribute

#### Scenario: Backward compatibility for existing callers
- **GIVEN** existing code calls `recognize_essence()`
- **WHEN** the function signature is extended to return scores
- **THEN** the function SHALL maintain backward compatibility
- **AND** callers that don't need scores can ignore the extra return value

### Requirement: Display Summary Report After Abort
The system SHALL display the summary report even when scanning is aborted early due to recognition failures.

#### Scenario: Summary after abort on button failures
- **GIVEN** scanning was aborted due to consecutive button recognition failures
- **WHEN** the scan loop exits (via break or abort condition)
- **THEN** the system SHALL still log the summary report
- **AND** SHALL show all treasures found before abort

#### Scenario: Summary after abort on low scores
- **GIVEN** scanning was aborted due to consecutive low recognition scores
- **WHEN** the scan loop exits (via break or abort condition)
- **THEN** the system SHALL still log the summary report
- **AND** SHALL show all treasures found before abort

#### Scenario: Summary after abort on duplicate results
- **GIVEN** scanning was aborted due to consecutive duplicate recognition results
- **WHEN** the scan loop exits (via break or abort condition)
- **THEN** the system SHALL still log the summary report
- **AND** SHALL show all treasures found before abort

