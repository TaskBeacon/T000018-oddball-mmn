# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `standard` | `oddball_response_window` | `standard_stimulus` | Frequent non-target visual symbol shown at center | W2003906510 | Frequent standard events in oddball/MMN paradigms | psychopy_builtin | config visual/text stimulus | No response expected |
| `deviant` | `oddball_response_window` | `deviant_stimulus` | Infrequent non-target deviant visual symbol | W2003906510 | Infrequent deviant events for novelty mismatch effects | psychopy_builtin | config visual/text stimulus | No response expected |
| `target` | `oddball_response_window` | `target_stimulus` | Infrequent target symbol requiring `space` response | W2003906510 | Active oddball variants include rare response target | psychopy_builtin | config visual/text stimulus | Response-evoking condition |
| `all` | `trial_fixation` | `fixation` | Center fixation before stimulus onset | W2003906510 | Prestimulus fixation for stable event timing | psychopy_builtin | config fixation stimulus | Shared across conditions |
| `all` | `inter_trial_interval` | `fixation` | Center fixation during ITI | W2003906510 | ITI separation between oddball events | psychopy_builtin | config fixation stimulus | Shared across conditions |
| `all` | `instruction/block_end/goodbye` | `instruction_text`, `block_break`, `good_bye` | Participant instruction, break, and completion text | W2003906510 | Runtime support screens for active oddball session control | psychopy_builtin | config text stimuli | Localization-ready config text |
