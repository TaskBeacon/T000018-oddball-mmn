# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| condition_set | `task.conditions` | `['standard','deviant','target']` | W2003906510 | Oddball paradigm uses frequent standard and infrequent deviant/target events | inferred | Active oddball variant |
| response_key | `task.key_list` | `['space']` | W2003906510 | Single-button response for target detection in active oddball tasks | inferred | Non-target requires withholding response |
| blocks_human | `task.total_blocks` | `3` | W2003906510 | Longer EEG-capable session for human acquisition | inferred | Runtime profile choice |
| blocks_smoke | `task.total_blocks` | `1` (qa/sim) | W2003906510 | Short smoke profile preserving stage mechanics | inferred | Gate-focused run duration |
| trials_human | `task.total_trials` | `270` | W2003906510 | Maintains oddball frequency structure at practical scale | inferred | Human run |
| trials_smoke | `task.total_trials` | `12` (qa/sim) | W2003906510 | Minimal mechanism-complete subset for QA/sim | inferred | Fast CI/local gate checks |
| fixation_duration | `timing.fixation_duration` | `0.3` human / `0.2` qa/sim | W2003906510 | Pre-stimulus fixation before oddball event | inferred | Gaze stabilization |
| stimulus_duration | `timing.stimulus_duration` | `0.5` human / `0.4` qa/sim | W2003906510 | Stimulus-aligned response window | inferred | Event timing parameter |
| iti_duration | `timing.iti_duration` | `0.5` human / `0.2` qa/sim | W2003906510 | Event separation for ERP epoching | inferred | ITI stage |
| weight_standard | `condition_generation.weights.standard` | `0.70` | W2003906510 | Standard should dominate oddball stream | inferred | Frequent baseline |
| weight_deviant | `condition_generation.weights.deviant` | `0.20` | W2003906510 | Deviant should be infrequent | inferred | Novel non-target |
| weight_target | `condition_generation.weights.target` | `0.10` | W2003906510 | Target should be rare response event | inferred | Response-evoking oddball |
| first_trial_label | `condition_generation.first_trial_label` | `standard` | W2003906510 | Initial stabilization with frequent condition | inferred | Prevent rare-event first trial |
| trig_fixation | `triggers.map.fixation_onset` | `20` | W2003906510 | Event marker by trial phase | inferred | Optional fixation trigger |
| trig_standard_onset | `triggers.map.standard_stimulus_onset` | `40` | W2003906510 | Condition-specific stimulus onset coding | inferred | ERP averaging key |
| trig_deviant_onset | `triggers.map.deviant_stimulus_onset` | `41` | W2003906510 | Condition-specific stimulus onset coding | inferred | ERP averaging key |
| trig_target_onset | `triggers.map.target_stimulus_onset` | `42` | W2003906510 | Condition-specific stimulus onset coding | inferred | ERP averaging key |
| trig_response_codes | `triggers.map.{standard,deviant,target}_key_press` | `50/51/52` | W2003906510 | Response event coding by condition | inferred | Behavioral-ERP alignment |
| trig_timeout_codes | `triggers.map.{standard,deviant,target}_no_response` | `60/61/62` | W2003906510 | Explicit omission coding | inferred | Miss/correct-rejection labeling |
| trig_iti | `triggers.map.iti_onset` | `80` | W2003906510 | ITI boundary marker | inferred | Epoch segmentation |
