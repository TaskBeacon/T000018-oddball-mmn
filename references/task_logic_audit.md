# Task Logic Audit

## 1. Paradigm Intent

- Task: three-stimulus oddball for MMN/P3-style novelty and target detection processing.
- Primary construct: discrimination of frequent/infrequent events plus target detection.
- Manipulated factor: trial condition (`standard`, `deviant`, `target`).
- Dependent measures: target hit rate, non-target false alarms, response RT, trigger-timing integrity.

## 2. Block/Trial Workflow

### Block Structure

- Human profile: 3 blocks; QA/sim: 1 block.
- Condition generation uses weighted random sampling with first-trial stabilization to `standard`.

### Trial State Machine

1. `trial_fixation`: fixation-only pre-stimulus phase.
2. `oddball_response_window`: present condition stimulus and capture response/timeout.
3. `inter_trial_interval`: fixation-only ITI phase.

## 3. Condition Semantics

- `standard`: frequent non-target, withhold response.
- `deviant`: infrequent non-target deviant, withhold response.
- `target`: infrequent target, press `space`.

## 4. Response and Scoring Rules

- Valid key: `space`.
- Outcome rules:
  - target + response -> hit.
  - target + no response -> miss.
  - non-target + response -> false alarm.
  - non-target + no response -> correct rejection.
- Score delta: `task.delta` for correct outcomes, otherwise `0`.

## 5. Stimulus Layout Plan

- Single central stimulus per phase to minimize overlap and saccades.
- Fixation and oddball symbols are centered.
- Instruction/break/goodbye use centered multiline text.

## 6. Trigger Plan

- Experiment: `exp_onset`, `exp_end`
- Block: `block_onset`, `block_end`
- Fixation: `fixation_onset`
- Stimulus onset: `{standard,deviant,target}_stimulus_onset`
- Responses: `{standard,deviant,target}_key_press`
- Timeouts: `{standard,deviant,target}_no_response`
- ITI: `iti_onset`

## 7. Architecture Decisions (Auditability)

- Condition scheduling stays in PsyFlow built-in block generation (weighted config fields).
- Runtime flow keeps explicit phase labels aligned to oddball state machine.
- Participant-facing text/symbol definitions remain config-driven for localization and reproducibility.

## 8. Inference Log

- Stimulus modality is implemented as visual symbols while preserving canonical oddball frequency logic.
- Timing constants and exact trigger integers are implementation-level and therefore documented as inferred.
- First-trial `standard` stabilization is an inferred operational guard to avoid rare-event starts.
