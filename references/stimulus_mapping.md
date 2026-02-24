# Stimulus Mapping

Task: `Oddball Task (MMN/P3)`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `standard` | `standard_stimulus` | `W2003906510` | Three-stimulus oddball structure with frequent standard events is consistent with MMN/P3 paradigms described in the selected references. | `psychopy_builtin` | Frequent non-target visual symbol; no response required. |
| `deviant` | `deviant_stimulus` | `W2003906510` | Infrequent deviant/non-target events are used to elicit mismatch/novelty-related responses. | `psychopy_builtin` | Infrequent non-target visual symbol; no response required. |
| `target` | `target_stimulus` | `W2003906510` | Infrequent target events require an overt response in active oddball variants used for P3 measurement. | `psychopy_builtin` | Infrequent target visual symbol; press `space`. |
| `all` | `fixation` | `W2003906510` | Central fixation is an inferred implementation detail to stabilize gaze between stimuli. | `psychopy_builtin` | Used during `trial_fixation` and `inter_trial_interval`. |
| `all` | `instruction_text`, `block_break`, `good_bye` | `W2003906510` | Instruction and break screens are implementation support screens, not ERP event stimuli. | `psychopy_builtin` | Chinese participant-facing text in `config/*.yaml` (`font: SimHei`). |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
