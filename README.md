# Oddball Task (MMN/P3)

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Oddball Task (MMN/P3) |
| Version | v0.2.0-dev |
| URL / Repository | https://github.com/TaskBeacon/T000018-oddball-mmn |
| Short Description | Three-stimulus visual oddball task for MMN/P3-style novelty and target detection ERP paradigms |
| Created By | TaskBeacon |
| Date Updated | 2026-02-24 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | EEG |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |

## 1. Task Overview

This task implements a three-stimulus oddball paradigm with `standard`, `deviant`, and `target` conditions. Participants respond only to `target` stimuli (space key) and withhold responses to `standard` and `deviant` stimuli. The task supports `human`, `qa`, and `sim` modes.

This repair removes an inherited MID-style state machine (`cue -> anticipation -> target -> feedback`) and replaces it with an oddball-appropriate trial flow (`fixation -> stimulus response window -> ITI`) aligned with the paradigm described in `references/task_logic_audit.md`.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Parse mode and load config | `main.py` loads one of `config/config*.yaml` and resolves `human`, `qa`, or `sim` runtime context. |
| 2. Initialize runtime | Build `TaskSettings`, window/keyboard, trigger runtime, and `StimBank`; preload all stimuli. |
| 3. Show instructions | Present config-defined Chinese instructions and wait for continue key (`space`). |
| 4. Generate conditions | `BlockUnit.generate_conditions(...)` creates weighted oddball condition labels from `condition_generation.weights`. |
| 5. Run trials | `run_trial(...)` executes fixation -> oddball stimulus response window -> ITI for each condition. |
| 6. Summarize block | Compute `overall_accuracy`, `target_hit_rate`, and non-target `false_alarm_rate`; display `block_break`. |
| 7. Finalize | Display `good_bye`, emit `exp_end`, save CSV, close triggers, quit PsychoPy. |

### Trial-Level Flow

| Step | Description |
|---|---|
| 1. Trial setup | Read condition (`standard`, `deviant`, `target`), assign `trial_id`, determine `expected_response`. |
| 2. `trial_fixation` | Show central fixation for `timing.fixation_duration`; emit `fixation_onset`. |
| 3. `oddball_response_window` | Present condition-specific symbol (`*_stimulus`) for `timing.stimulus_duration`; capture response; emit stimulus/response/timeout triggers. |
| 4. Outcome classification | Classify trial as `hit`, `miss`, `false_alarm`, or `correct_rejection`; set `accuracy` and `score_delta`. |
| 5. `inter_trial_interval` | Show fixation for `timing.iti_duration`; emit `iti_onset`. |

### Controller Logic

| Component | Description |
|---|---|
| Adaptive RT controller | Not used. This task does not require dynamic RT-window/staircase control. |
| Condition generation | PsyFlow `BlockUnit.generate_conditions(...)` built-in weighted generation is used. |
| Optional stabilization | `main.py` optionally moves a configured label (default `standard`) to the first trial to avoid starting a block with a rare event. |

### Other Logic

| Component | Description |
|---|---|
| Mode-aware output plumbing | QA/sim runs use `context_from_config(...)` and `runtime_context(...)` for reproducible output directories and session metadata. |
| Trigger runtime in QA/sim | QA and sim use mock triggers; human mode uses configured trigger driver. |
| Responder context | `set_trial_context(...)` is set for fixation, oddball response window, and ITI phases to support scripted/sampler responders. |
| Block metrics | Metrics are computed from trial outcome labels instead of feedback screens. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `trial_fixation` | Pre-stimulus fixation phase |
| `oddball_response_window` | Stimulus presentation and response capture phase |
| `inter_trial_interval` | Post-stimulus fixation ITI phase |

## 3. Configuration Summary

All settings are defined in `config/config.yaml` (human) and parallel QA/sim profiles.

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | Participant identifier (3-digit integer in GUI mode; fixed IDs in QA/sim). |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `bg_color` | `black` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Stimulus ID | Type | Description |
|---|---|---|
| `fixation` | text | Central fixation cross used in fixation and ITI phases |
| `instruction_text` | text | Chinese instructions (SimHei font) |
| `standard_stimulus` | text | Frequent non-target symbol |
| `deviant_stimulus` | text | Infrequent non-target deviant symbol |
| `target_stimulus` | text | Infrequent target symbol requiring `space` |
| `block_break` | text | Block summary screen with accuracy/hit/false-alarm metrics |
| `good_bye` | text | Final summary screen |

### d. Timing

| Parameter | Human | QA/Sim |
|---|---:|---:|
| `fixation_duration` | `0.3 s` | `0.2 s` |
| `stimulus_duration` | `0.5 s` | `0.4 s` |
| `iti_duration` | `0.5 s` | `0.2 s` |

### e. Triggers

| Event | Code |
|---|---:|
| `exp_onset` / `exp_end` | `1` / `2` |
| `block_onset` / `block_end` | `10` / `11` |
| `fixation_onset` | `20` |
| `standard_stimulus_onset` / `deviant_stimulus_onset` / `target_stimulus_onset` | `40` / `41` / `42` |
| `standard_key_press` / `deviant_key_press` / `target_key_press` | `50` / `51` / `52` |
| `standard_no_response` / `deviant_no_response` / `target_no_response` | `60` / `61` / `62` |
| `iti_onset` | `80` |

### f. Condition Generation

| Parameter | Human | QA/Sim |
|---|---|---|
| `weights.standard` | `0.70` | `0.65` |
| `weights.deviant` | `0.20` | `0.20` |
| `weights.target` | `0.10` | `0.15` |
| `order` | `random` | `random` |
| `first_trial_label` | `standard` | `standard` |

### g. Adaptive Controller (if present)

| Item | Status |
|---|---|
| Adaptive controller | Not used for this task |
| Rationale | Oddball task does not require dynamic RT threshold or staircase updates |

## 4. Methods (for academic publication)

Participants completed a three-stimulus visual oddball task designed for MMN/P3-style ERP analyses of novelty processing and target detection. Each trial belonged to one of three conditions: frequent `standard`, infrequent `deviant`, or infrequent `target`. Participants were instructed to press the space key only for `target` stimuli and to withhold responses to non-target stimuli.

Trials were implemented as a fixation period, followed by a stimulus presentation/response window, followed by an inter-trial interval (ITI). Condition identity determined the displayed visual symbol and the stimulus onset trigger code. Behavioral outcomes were classified as `hit`, `miss`, `false_alarm`, or `correct_rejection`, and summary metrics (overall accuracy, target hit rate, and non-target false alarm rate) were reported at block and task end.

Condition sequences were generated using PsyFlow's built-in weighted block condition generator from config-defined weights, with optional first-trial stabilization to a `standard` event for practical block starts. This design keeps the task implementation auditable and avoids paradigm-irrelevant template state machines.
