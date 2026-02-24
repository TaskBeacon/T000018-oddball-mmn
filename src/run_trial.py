from __future__ import annotations

from functools import partial

from psyflow import StimUnit, set_trial_context, next_trial_id


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one three-stimulus oddball trial."""
    cond = str(condition)
    trial_id = next_trial_id()
    keys = list(getattr(settings, "key_list", ["space"]))
    expected_response = cond == "target"
    score_step = int(getattr(settings, "delta", 1))

    trial_data = {
        "condition": cond,
        "expected_response": expected_response,
    }
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # phase: trial_fixation
    fixation = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="trial_fixation",
        deadline_s=settings.fixation_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=cond,
        task_factors={
            "condition": cond,
            "expected_response": expected_response,
            "stage": "trial_fixation",
            "block_idx": block_idx,
        },
        stim_id="fixation",
    )
    fixation.show(
        duration=settings.fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    # phase: oddball_response_window
    stimulus = make_unit(unit_label="stimulus").add_stim(stim_bank.get(f"{cond}_stimulus"))
    set_trial_context(
        stimulus,
        trial_id=trial_id,
        phase="oddball_response_window",
        deadline_s=settings.stimulus_duration,
        valid_keys=keys,
        block_id=block_id,
        condition_id=cond,
        task_factors={
            "condition": cond,
            "expected_response": expected_response,
            "stage": "oddball_response_window",
            "block_idx": block_idx,
        },
        stim_id=f"{cond}_stimulus",
    )
    stimulus.capture_response(
        keys=keys,
        correct_keys=keys if expected_response else [],
        duration=settings.stimulus_duration,
        onset_trigger=settings.triggers.get(f"{cond}_stimulus_onset"),
        response_trigger=settings.triggers.get(f"{cond}_key_press"),
        timeout_trigger=settings.triggers.get(f"{cond}_no_response"),
    )

    response_key = stimulus.get_state("response", None)
    response_made = response_key in keys
    if expected_response and response_made:
        outcome = "hit"
    elif expected_response and not response_made:
        outcome = "miss"
    elif response_made:
        outcome = "false_alarm"
    else:
        outcome = "correct_rejection"

    accuracy = outcome in {"hit", "correct_rejection"}
    score_delta = score_step if accuracy else 0

    stimulus.set_state(
        expected_response=expected_response,
        response_made=response_made,
        response_key=response_key,
        outcome=outcome,
        accuracy=accuracy,
        score_delta=score_delta,
    ).to_dict(trial_data)

    trial_data.update(
        {
            "response_key": response_key,
            "response_made": response_made,
            "outcome": outcome,
            "accuracy": accuracy,
            "score_delta": score_delta,
        }
    )

    # phase: inter_trial_interval
    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=settings.iti_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=cond,
        task_factors={
            "condition": cond,
            "expected_response": expected_response,
            "stage": "inter_trial_interval",
            "block_idx": block_idx,
        },
        stim_id="fixation",
    )
    iti.show(
        duration=settings.iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    return trial_data
