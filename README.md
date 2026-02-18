# Oddball Task (MMN/P3)

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field                | Value                                        |
|----------------------|----------------------------------------------|
| Name                 | Oddball Task (MMN/P3)                        |
| Version              | v0.1.0-dev                                   |
| URL / Repository     | https://github.com/TaskBeacon/T000018-oddball-mmn |
| Short Description    | Three-stimulus oddball paradigm for MMN/P3-related novelty and target detection processes |
| Created By           | TaskBeacon                                   |
| Date Updated         | 2026-02-17                                   |
| PsyFlow Version      | 0.1.9                                        |
| PsychoPy Version     | 2025.1.1                                     |
| Modality             | EEG                                          |
| Language             | Chinese                                      |
| Voice Name           | zh-CN-YunyangNeural                          |

## 1. Task Overview

This task implements a three-stimulus oddball paradigm with `standard`, `deviant`, and `target` trials. Participants are instructed to press `space` only when the target stimulus appears, while withholding responses to standard and deviant stimuli. The runtime supports `human`, `qa`, and `sim` modes and uses a controller to generate oddball trial sequences by probability, with block-level performance summaries and stage-wise trigger emission for EEG synchronization.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|------|-------------|
| 1. Parse mode and load config | `main.py` parses `human/qa/sim` options, then loads the selected YAML profile. |
| 2. Resolve participant context | Human mode collects subject info from GUI; QA uses fixed `subject_id=qa`; sim uses participant ID from simulation context. |
| 3. Initialize runtime | Build `TaskSettings`, initialize trigger runtime (mock in QA/sim), window, keyboard, and preload stimuli with `StimBank`. |
| 4. Initialize controller | `Controller.from_dict(...)` loads oddball sequence parameters (`standard_prob`, `deviant_prob`, `target_prob`, etc.). |
| 5. Start experiment | Emit `exp_onset`, then display instruction screen and wait for continue key. |
| 6. Enter block loop | For each block, optionally show countdown (human mode), then call `controller.prepare_block(...)` to generate planned oddball conditions. |
| 7. Run block trials | `BlockUnit` receives planned conditions via `.add_condition(...)`, emits `block_onset` and `block_end`, and executes `run_trial(...)` for each condition. |
| 8. Compute block feedback | After each block, compute accuracy from trial `target_hit` values and compute total score from `feedback_delta`. |
| 9. Show block break | Present `block_break` with block index, accuracy, and score; wait for continue key. |
| 10. Finalize and save | Show `good_bye` summary, emit `exp_end`, save all trial records to CSV, close trigger runtime, and quit PsychoPy. |

### Trial-Level Flow

| Step | Description |
|------|-------------|
| 1. Setup trial state | Determine condition (`standard/deviant/target`), assign trial ID, and set expected response (`target` requires response). |
| 2. Cue phase | Show fixation for `cue_duration` and emit condition-specific cue onset trigger (`standard_cue_onset`, `deviant_cue_onset`, or `target_cue_onset`). |
| 3. Anticipation phase | Show fixation for `anticipation_duration` and emit condition-specific anticipation onset trigger (`standard_anticipation_onset`, `deviant_anticipation_onset`, or `target_anticipation_onset`). |
| 4. Target phase | Present condition-specific target stimulus for `target_duration`, capture `space` response, emit condition-specific target onset/response/timeout triggers. |
| 5. Trial scoring | Compute `response_made`, `hit`, and `delta`: target trials are hit when responded; non-target trials are hit when no response. |
| 6. Pre-feedback phase | Show fixation for `prefeedback_duration`. |
| 7. Feedback phase | Show condition- and outcome-specific feedback stimulus (`{condition}_hit_feedback` or `{condition}_miss_feedback`) for `feedback_duration` with matching feedback trigger. |
| 8. ITI phase | Show fixation for `iti_duration` and emit `iti_onset`. |
| 9. Controller update | Update condition-specific performance history in controller and return trial dictionary. |

### Controller Logic

| Component | Description |
|-----------|-------------|
| Probability normalization | Controller normalizes `standard_prob`, `deviant_prob`, and `target_prob` so their sum equals 1.0. |
| Count allocation | For each block, expected condition counts are computed from probabilities and adjusted to exactly match `trial_per_block`. |
| Rare-condition guarantee | For practical oddball runs (`n_trials >= 3`), controller ensures at least one `deviant` and one `target` trial. |
| Sequence randomization | Planned conditions are shuffled when `randomize_order=true`. |
| First-trial stabilization | When `force_first_standard=true`, first trial is set to `standard` if available. |
| Performance logging | `update(hit, condition)` appends condition-specific hit history and logs running condition accuracy when enabled. |

### Other Logic

| Component | Description |
|-----------|-------------|
| Mode-specific output plumbing | QA and sim modes write outputs to mode-specific directories and use runtime context for reproducible session metadata. |
| Trigger safety in QA/sim | QA and sim use mock trigger runtime to preserve event logs without requiring hardware access. |
| Trial context for responders | Each stage uses `set_trial_context(...)` to expose condition, phase, deadlines, and factors for scripted/sampler responders. |

### Runtime Context Phases
| Phase Label | Meaning |
|---|---|
| `pre_stim_fixation` | pre stim fixation stage in `src/run_trial.py` responder context. |
| `pre_stim_jitter` | pre stim jitter stage in `src/run_trial.py` responder context. |
| `oddball_response_window` | oddball response window stage in `src/run_trial.py` responder context. |
| `post_stim_fixation` | post stim fixation stage in `src/run_trial.py` responder context. |
| `outcome_feedback` | outcome feedback stage in `src/run_trial.py` responder context. |
| `inter_trial_interval` | inter trial interval stage in `src/run_trial.py` responder context. |

## 3. Configuration Summary

All settings are defined in `config/config.yaml`.

### a. Subject Info

| Field | Meaning |
|-------|---------|
| subject_id | Required participant ID (3-digit integer, range 101-999). |

### b. Window Settings

| Parameter | Value |
|-----------|-------|
| size | `[1280, 720]` |
| units | `pix` |
| screen | `0` |
| bg_color | `black` |
| fullscreen | `false` |
| monitor_width_cm | `35.5` |
| monitor_distance_cm | `60` |

### c. Stimuli

| Name | Type | Description |
|------|------|-------------|
| fixation | text | Central fixation cross used for cue, pre-feedback, and ITI stages. |
| instruction_text | text | Chinese instruction: respond only to target stimulus (`★`) using `space`. |
| standard_target | text | Standard oddball stimulus (`○`). |
| deviant_target | text | Deviant oddball stimulus (`△`). |
| target_target | text | Target oddball stimulus (`★`) requiring key press. |
| standard_hit_feedback | text | Feedback when correctly withholding response on standard trial. |
| standard_miss_feedback | text | Feedback when false alarm occurs on standard trial. |
| deviant_hit_feedback | text | Feedback when correctly withholding response on deviant trial. |
| deviant_miss_feedback | text | Feedback when false alarm occurs on deviant trial. |
| target_hit_feedback | text | Feedback when target is correctly detected. |
| target_miss_feedback | text | Feedback when target is missed. |
| block_break | text | Inter-block summary (accuracy and score). |
| good_bye | text | End-of-task summary with total score. |

### d. Timing

| Phase | Duration |
|-------|----------|
| cue | `0.3 s` |
| anticipation | `0.2 s` |
| target | `0.5 s` |
| prefeedback | `0.2 s` |
| feedback | `0.4 s` |
| iti | `0.5 s` |

### e. Triggers

| Event | Code |
|-------|------|
| exp_onset | 1 |
| exp_end | 2 |
| block_onset | 10 |
| block_end | 11 |
| standard_cue_onset | 20 |
| deviant_cue_onset | 21 |
| target_cue_onset | 22 |
| standard_anticipation_onset | 30 |
| deviant_anticipation_onset | 31 |
| target_anticipation_onset | 32 |
| standard_target_onset | 40 |
| deviant_target_onset | 41 |
| target_target_onset | 42 |
| standard_key_press | 50 |
| deviant_key_press | 51 |
| target_key_press | 52 |
| standard_no_response | 60 |
| deviant_no_response | 61 |
| target_no_response | 62 |
| standard_hit_fb_onset | 70 |
| standard_miss_fb_onset | 71 |
| deviant_hit_fb_onset | 72 |
| deviant_miss_fb_onset | 73 |
| target_hit_fb_onset | 74 |
| target_miss_fb_onset | 75 |
| iti_onset | 80 |

### f. Adaptive Controller

| Parameter | Value |
|-----------|-------|
| standard_prob | `0.70` |
| deviant_prob | `0.20` |
| target_prob | `0.10` |
| randomize_order | `true` |
| force_first_standard | `true` |
| enable_logging | `true` |

## 4. Methods (for academic publication)

Participants completed a three-stimulus oddball task designed to probe novelty processing and target detection mechanisms relevant to MMN/P3 analysis. The paradigm contained standard, deviant, and target trials, and participants were instructed to respond only to the target stimulus (`★`) by pressing the space key while withholding responses to standard (`○`) and deviant (`△`) stimuli. The task was configured for three blocks with 90 trials per block (270 total trials), using probabilistic condition scheduling.

Each trial began with a brief fixation cue (0.3 s), followed by a short anticipation fixation period (0.2 s), then the oddball stimulus (0.5 s) during which responses were recorded. A pre-feedback fixation (0.2 s) preceded feedback (0.4 s), and each trial ended with an inter-trial fixation interval (0.5 s). Trial outcomes were scored as hits when behavior matched condition requirements (press on target; withhold on non-target), and condition-specific feedback was presented accordingly.

Condition order within each block was generated by a controller that normalized configured probabilities and converted them into trial counts per block, with randomization and first-trial standard stabilization enabled. Event triggers were emitted at experiment, block, stimulus, response, and feedback stages to support synchronization with EEG acquisition and reproducible event-level analysis.
