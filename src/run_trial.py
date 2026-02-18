from __future__ import annotations

from functools import partial

from psyflow import StimUnit, set_trial_context

# run_trial uses task-specific phase labels via set_trial_context(...).


def _next_trial_id(controller) -> int:
    histories = getattr(controller, "histories", {}) or {}
    done = 0
    for items in histories.values():
        try:
            done += len(items)
        except Exception:
            continue
    return int(done) + 1


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one oddball trial (standard / deviant / target)."""
    cond = str(condition)
    trial_id = _next_trial_id(controller)
    keys = list(getattr(settings, "key_list", ["space"]))
    expected_response = cond == "target"

    trial_data = {
        "condition": cond,
        "expected_response": expected_response,
    }
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # phase: pre_stim_fixation
    cue = make_unit(unit_label="cue").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="pre_stim_fixation",
        deadline_s=float(settings.cue_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=cond,
        task_factors={"condition": cond, "expected_response": expected_response, "stage": "pre_stim_fixation", "block_idx": block_idx},
        stim_id="fixation",
    )
    cue.show(
        duration=settings.cue_duration,
        onset_trigger=settings.triggers.get(f"{cond}_cue_onset"),
    ).to_dict(trial_data)

    # phase: pre_stim_jitter
    anticipation = make_unit(unit_label="anticipation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        anticipation,
        trial_id=trial_id,
        phase="pre_stim_jitter",
        deadline_s=float(settings.anticipation_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=cond,
        task_factors={"condition": cond, "stage": "pre_stim_jitter", "block_idx": block_idx},
        stim_id="fixation",
    )
    anticipation.show(
        duration=settings.anticipation_duration,
        onset_trigger=settings.triggers.get(f"{cond}_anticipation_onset"),
    ).to_dict(trial_data)

    # phase: oddball_response_window
    target = make_unit(unit_label="target").add_stim(stim_bank.get(f"{cond}_target"))
    set_trial_context(
        target,
        trial_id=trial_id,
        phase="oddball_response_window",
        deadline_s=float(settings.target_duration),
        valid_keys=keys,
        block_id=block_id,
        condition_id=cond,
        task_factors={
            "condition": cond,
            "expected_response": expected_response,
            "stage": "oddball_response_window",
            "block_idx": block_idx,
        },
        stim_id=f"{cond}_target",
    )
    target.capture_response(
        keys=keys,
        correct_keys=keys if expected_response else [],
        duration=settings.target_duration,
        onset_trigger=settings.triggers.get(f"{cond}_target_onset"),
        response_trigger=settings.triggers.get(f"{cond}_key_press"),
        timeout_trigger=settings.triggers.get(f"{cond}_no_response"),
    )

    response_key = target.get_state("response", None)
    response_made = response_key in keys
    hit = response_made if expected_response else (not response_made)
    delta = settings.delta if hit else 0

    target.set_state(
        expected_response=expected_response,
        response_made=response_made,
        response_key=response_key,
        hit=hit,
        delta=delta,
    ).to_dict(trial_data)

    # phase: post_stim_fixation
    prefeedback = make_unit(unit_label="prefeedback").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        prefeedback,
        trial_id=trial_id,
        phase="post_stim_fixation",
        deadline_s=float(settings.prefeedback_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=cond,
        task_factors={"condition": cond, "stage": "post_stim_fixation", "block_idx": block_idx},
        stim_id="fixation",
    )
    prefeedback.show(duration=settings.prefeedback_duration).to_dict(trial_data)

    # phase: outcome_feedback
    fb_state = "hit" if hit else "miss"
    feedback = make_unit(unit_label="feedback").add_stim(stim_bank.get(f"{cond}_{fb_state}_feedback"))
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="outcome_feedback",
        deadline_s=float(settings.feedback_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=cond,
        task_factors={
            "condition": cond,
            "expected_response": expected_response,
            "response_made": response_made,
            "hit": hit,
            "stage": "outcome_feedback",
            "block_idx": block_idx,
        },
        stim_id=f"{cond}_{fb_state}_feedback",
    )
    feedback.show(
        duration=settings.feedback_duration,
        onset_trigger=settings.triggers.get(f"{cond}_{fb_state}_fb_onset"),
    )
    feedback.set_state(hit=hit, delta=delta).to_dict(trial_data)

    # phase: inter_trial_interval
    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=float(settings.iti_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=cond,
        task_factors={"condition": cond, "stage": "inter_trial_interval", "block_idx": block_idx},
        stim_id="fixation",
    )
    iti.show(
        duration=settings.iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    controller.update(hit=hit, condition=cond)
    return trial_data
