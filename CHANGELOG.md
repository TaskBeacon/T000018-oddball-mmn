# CHANGELOG

All notable development changes for `T000018-oddball-mmn` are documented here.

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for Oddball Task (MMN/P3).
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
- Added generated cue/target image stimuli under `assets/generated/`.

### Changed
- Refactored oddball controller to sequence-driven planning with configurable probabilities (`standard/deviant/target`) and deterministic block seeding.
- Replaced MID-like trial path with oddball-appropriate flow: fixation cue -> target response window -> prefeedback -> feedback -> ITI.
- Added explicit anticipation stage (`cue -> anticipation -> target -> prefeedback -> feedback -> iti`) to satisfy responder-context contract validation.
- Updated `main.py` block flow to consume controller-planned condition sequences via `.add_condition(...)`.
- Reworked all config profiles to human-auditable format with Chinese participant text, `font: SimHei`, and clean section comments.
- Added oddball-specific sampler responder behavior with target hit and non-target false-alarm parameters.
- Rewrote `README.md` to full reproducibility structure (`Overview`, `Task Flow`, `Configuration Summary`, `Methods`).
- Extended `.gitignore` housekeeping rules (`.pytest_cache/`, `.mypy_cache/`, `.venv/`).

### Fixed
- Fixed responder-context contract failure by aligning explicit phase tokens and stage ordering in `src/run_trial.py`.

### Verified
- `python -m psyflow.validate <task_path>`
- `psyflow-qa <task_path> --config config/config_qa.yaml --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
