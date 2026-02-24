# Task Logic Audit

## 1. Paradigm Intent

- Task: Three-stimulus visual oddball task for MMN/P3-related novelty and target detection processing
- Primary construct: Frequent/infrequent event discrimination with target detection (active oddball)
- Manipulated factors: Trial condition (`standard`, `deviant`, `target`)
- Dependent measures: Hit rate on `target`, false alarm rate on non-targets, RT on target responses, trigger-locked event timing
- Key citations: `W2003906510` (selected reference bundle; active oddball structure inferred from MMN/P3 literature context)

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 3 in human profile; 1 in QA/sim smoke profiles
- Trials per block: 90 in human profile; 12 in QA/sim smoke profiles
- Randomization/counterbalancing:
  - PsyFlow `BlockUnit.generate_conditions(...)` built-in weighted random generation
  - Condition weights defined in config (`condition_generation.weights`)
  - Optional first-trial stabilization to `standard` via `condition_generation.first_trial_label`

### Trial State Machine

1. State name: `trial_fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown: `fixation`
   - Valid keys: none
   - Timeout behavior: auto-advance after `timing.fixation_duration`
   - Next state: `oddball_response_window`
2. State name: `oddball_response_window`
   - Onset trigger: `{condition}_stimulus_onset`
   - Stimuli shown: `{condition}_stimulus`
   - Valid keys: `task.key_list` (`space`)
   - Timeout behavior:
     - If no response before `timing.stimulus_duration`, emit `{condition}_no_response`
     - Classify as `miss` (target) or `correct_rejection` (non-target)
   - Next state: `inter_trial_interval`
3. State name: `inter_trial_interval`
   - Onset trigger: `iti_onset`
   - Stimuli shown: `fixation`
   - Valid keys: none
   - Timeout behavior: auto-advance after `timing.iti_duration`
   - Next state: next trial / block end

## 3. Condition Semantics

- Condition ID: `standard`
  - Participant-facing meaning: frequent non-target event
  - Concrete stimulus realization (visual/audio): white circle symbol (`standard_stimulus`)
  - Outcome rules: correct behavior is withhold response; response is `false_alarm`
- Condition ID: `deviant`
  - Participant-facing meaning: infrequent non-target deviant event
  - Concrete stimulus realization (visual/audio): yellow triangle symbol (`deviant_stimulus`)
  - Outcome rules: correct behavior is withhold response; response is `false_alarm`
- Condition ID: `target`
  - Participant-facing meaning: infrequent target requiring response
  - Concrete stimulus realization (visual/audio): red star symbol (`target_stimulus`)
  - Outcome rules: correct behavior is press `space`; no response is `miss`

## 4. Response and Scoring Rules

- Response mapping: `task.key_list` from config (single key `space`)
- Missing-response policy:
  - `target`: `miss`
  - `standard`/`deviant`: `correct_rejection`
- Correctness logic:
  - `target` + response -> `hit`
  - `target` + no response -> `miss`
  - non-target + response -> `false_alarm`
  - non-target + no response -> `correct_rejection`
- Reward/penalty updates:
  - `score_delta = task.delta` if correct (`hit` or `correct_rejection`), else `0`
  - Score is used only for optional summary display; no trial feedback screen is shown
- Running metrics:
  - block/final `overall_accuracy`
  - `target_hit_rate`
  - non-target `false_alarm_rate`

## 5. Stimulus Layout Plan

- Screen name: oddball trial displays (`trial_fixation`, `oddball_response_window`, `inter_trial_interval`)
  - Stimulus IDs shown together: one central stimulus at a time (`fixation` or one oddball symbol)
  - Layout anchors (`pos`): PsychoPy text default center (single-item screen; no overlap risk)
  - Size/spacing (`height`, width, wrap): symbol height `64`, fixation height `48`
  - Readability/overlap checks: single-stimulus screens avoid overlap; QA run used to confirm visibility
  - Rationale: simple central presentation supports ERP timing and minimizes eye movements
- Screen name: instruction / block break / goodbye
  - Stimulus IDs shown together: one formatted text stimulus
  - Layout anchors (`pos`): centered text
  - Size/spacing (`height`, width, wrap): `height` 24-28, `wrapWidth` 900-980
  - Readability/overlap checks: multiline text only; no concurrent text overlap
  - Rationale: config-defined Chinese participant-facing text for auditability and localization

## 6. Trigger Plan

- Experiment: `exp_onset`, `exp_end`
- Block boundaries: `block_onset`, `block_end`
- Trial phases:
  - `trial_fixation` -> `fixation_onset`
  - `oddball_response_window` -> `{condition}_stimulus_onset`, `{condition}_key_press`, `{condition}_no_response`
  - `inter_trial_interval` -> `iti_onset`

## 7. Inference Log

- Decision: Use visual symbol oddball (circle/triangle/star) rather than auditory tones
  - Why inference was required: Selected references are broad MMN/P3 literature and not a single exact stimulus set
  - Citation-supported rationale: MMN/P3 oddball structure (frequent standard, infrequent deviant/target) is preserved; stimulus modality/appearance is an implementation choice documented as inferred
- Decision: No cue/anticipation/feedback phases
  - Why inference was required: Previous scaffold inherited MID-style phases not supported by oddball paradigm
  - Citation-supported rationale: Oddball ERP analyses rely on event presentation and response timing, not incentive-delay cue/feedback state machines
- Decision: Use PsyFlow built-in weighted condition generation plus optional first-trial standard stabilization
  - Why inference was required: Sequence constraints are implementation-level and not fully specified in the selected references
  - Citation-supported rationale: Preserves oddball frequency structure while keeping code simple and auditable
