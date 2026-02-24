# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.conditions` | `['standard', 'deviant', 'target']` | `W2003906510` | `inferred` | Three-stimulus oddball condition set for MMN/P3-compatible active oddball implementation. |
| `task.key_list` | `['space']` | `W2003906510` | `inferred` | Single-button response for target detection is a common active oddball design choice. |
| `task.total_blocks` | `3` (human) / `1` (QA, sim) | `W2003906510` | `inferred` | Human run uses longer EEG-capable session; QA/sim profiles are shortened smoke tests. |
| `task.total_trials` | `270` (human) / `12` (QA, sim) | `W2003906510` | `inferred` | Human run preserves frequent/infrequent ratios at practical scale; QA/sim are mechanism-complete mini runs. |
| `timing.fixation_duration` | `0.3 s` human / `0.2 s` QA/sim | `W2003906510` | `inferred` | Neutral pre-stimulus fixation inserted for gaze stabilization in visual oddball runtime. |
| `timing.stimulus_duration` | `0.5 s` human / `0.4 s` QA/sim | `W2003906510` | `inferred` | Response window is coextensive with stimulus presentation in this implementation. |
| `timing.iti_duration` | `0.5 s` human / `0.2 s` QA/sim | `W2003906510` | `inferred` | ITI used to separate stimulus events and simplify event-locked analysis. |
| `condition_generation.weights` | `standard=.70, deviant=.20, target=.10` (human) | `W2003906510` | `inferred` | Frequent standard and infrequent deviant/target ratio is core oddball structure. |
| `condition_generation.order` | `random` | `W2003906510` | `inferred` | Randomized presentation within block is standard practice. |
| `condition_generation.first_trial_label` | `standard` | `W2003906510` | `inferred` | Practical stabilization choice to avoid starting a block with a rare event. |
| `triggers.map.fixation_onset` | `20` | `W2003906510` | `inferred` | Optional fixation event marker for timing verification. |
| `triggers.map.{standard,deviant,target}_stimulus_onset` | `40/41/42` | `W2003906510` | `inferred` | Condition-specific stimulus onset triggers for ERP averaging. |
| `triggers.map.{standard,deviant,target}_key_press` | `50/51/52` | `W2003906510` | `inferred` | Condition-tagged response events for behavioral QA and EEG alignment. |
| `triggers.map.{standard,deviant,target}_no_response` | `60/61/62` | `W2003906510` | `inferred` | Timeout/no-response events preserve explicit target-miss and non-target-correct-rejection logging. |
| `triggers.map.iti_onset` | `80` | `W2003906510` | `inferred` | ITI boundary trigger simplifies epoch segmentation diagnostics. |
