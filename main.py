from contextlib import nullcontext
from functools import partial
from pathlib import Path

import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    count_down,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import run_trial


MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def _resolve_generation_settings(settings: TaskSettings, condition_generation: dict | None) -> tuple[list[float] | None, str, str | None]:
    cfg = condition_generation or {}

    weights = None
    raw_weights = cfg.get("weights")
    if isinstance(raw_weights, dict):
        weights = [float(raw_weights.get(str(label), 1.0)) for label in settings.conditions]
    elif isinstance(raw_weights, list) and len(raw_weights) == len(settings.conditions):
        weights = [float(w) for w in raw_weights]

    order = str(cfg.get("order", "random")).lower()
    if order not in {"random", "sequential"}:
        order = "random"

    first_trial_label = cfg.get("first_trial_label")
    if first_trial_label is not None:
        first_trial_label = str(first_trial_label)

    return weights, order, first_trial_label


def _stabilize_first_trial_label(sequence: list[str], label: str | None) -> list[str]:
    if not sequence or not label:
        return sequence
    try:
        idx = sequence.index(label)
    except ValueError:
        return sequence
    if idx > 0:
        sequence[0], sequence[idx] = sequence[idx], sequence[0]
    return sequence


def _compute_block_metrics(block_trials: list[dict]) -> dict:
    if not block_trials:
        return {
            "overall_accuracy": 0.0,
            "target_hit_rate": 0.0,
            "false_alarm_rate": 0.0,
        }

    total_n = len(block_trials)
    overall_accuracy = sum(bool(t.get("accuracy", False)) for t in block_trials) / total_n

    target_trials = [t for t in block_trials if str(t.get("condition")) == "target"]
    non_target_trials = [t for t in block_trials if str(t.get("condition")) != "target"]

    target_hits = sum(str(t.get("outcome")) == "hit" for t in target_trials)
    non_target_false_alarms = sum(str(t.get("outcome")) == "false_alarm" for t in non_target_trials)

    target_hit_rate = target_hits / len(target_trials) if target_trials else 0.0
    false_alarm_rate = non_target_false_alarms / len(non_target_trials) if non_target_trials else 0.0

    return {
        "overall_accuracy": overall_accuracy,
        "target_hit_rate": target_hit_rate,
        "false_alarm_rate": false_alarm_rate,
    }


def run(options: TaskRunOptions):
    """Run oddball task in human/qa/sim mode with one auditable flow."""
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path), extra_keys=["condition_generation"])
    print(f"[Oddball MMN/P3] mode={options.mode} config={options.config_path}")

    output_dir: Path | None = None
    runtime_scope = nullcontext()
    runtime_ctx = None
    if options.mode in ("qa", "sim"):
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=options.mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)

    with runtime_scope:
        if options.mode == "human":
            subform = SubInfo(cfg["subform_config"])
            subject_data = subform.collect()
        elif options.mode == "qa":
            subject_data = {"subject_id": "qa"}
        else:
            participant_id = "sim"
            if runtime_ctx is not None and runtime_ctx.session is not None:
                participant_id = str(runtime_ctx.session.participant_id or "sim")
            subject_data = {"subject_id": participant_id}

        settings = TaskSettings.from_dict(cfg["task_config"])
        if options.mode in ("qa", "sim") and output_dir is not None:
            settings.save_path = str(output_dir)
        settings.add_subinfo(subject_data)

        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        settings.triggers = cfg["trigger_config"]
        settings.condition_generation = cfg.get("condition_generation_config", {})
        settings.save_to_json()

        trigger_runtime = (
            initialize_triggers(mock=True) if options.mode in ("qa", "sim") else initialize_triggers(cfg)
        )

        win, kb = initialize_exp(settings)

        if settings.voice_enabled and options.mode not in ("qa", "sim"):
            stim_bank = (
                StimBank(win, cfg["stim_config"])
                .convert_to_voice("instruction_text", voice=settings.voice_name)
                .preload_all()
            )
        else:
            stim_bank = StimBank(win, cfg["stim_config"]).preload_all()

        trigger_runtime.send(settings.triggers.get("exp_onset"))

        instruction = StimUnit("instruction_text", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get("instruction_text")
        )
        if settings.voice_enabled and options.mode not in ("qa", "sim"):
            instruction.add_stim(stim_bank.get("instruction_text_voice"))
        instruction.wait_and_continue()

        all_data: list[dict] = []
        weights, order, first_trial_label = _resolve_generation_settings(
            settings=settings,
            condition_generation=getattr(settings, "condition_generation", {}),
        )
        for block_i in range(settings.total_blocks):
            if options.mode not in ("qa", "sim"):
                count_down(win, 3, color="black")

            block = BlockUnit(
                block_id=f"block_{block_i}",
                block_idx=block_i,
                settings=settings,
                window=win,
                keyboard=kb,
            ).generate_conditions(
                condition_labels=list(settings.conditions),
                weights=weights,
                order=order,
            )
            _stabilize_first_trial_label(block.conditions, first_trial_label)

            block = (
                block.on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset")))
                .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end")))
                .run_trial(
                    partial(
                        run_trial,
                        stim_bank=stim_bank,
                        trigger_runtime=trigger_runtime,
                        block_id=f"block_{block_i}",
                        block_idx=block_i,
                    )
                )
                .to_dict(all_data)
            )

            metrics = _compute_block_metrics(block.get_all_data())
            StimUnit("block_break", win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get_and_format(
                    "block_break",
                    block_num=block_i + 1,
                    total_blocks=settings.total_blocks,
                    overall_accuracy=metrics["overall_accuracy"],
                    target_hit_rate=metrics["target_hit_rate"],
                    false_alarm_rate=metrics["false_alarm_rate"],
                )
            ).wait_and_continue()

        final_metrics = _compute_block_metrics(all_data)
        StimUnit("goodbye", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get_and_format(
                "good_bye",
                overall_accuracy=final_metrics["overall_accuracy"],
                target_hit_rate=final_metrics["target_hit_rate"],
                false_alarm_rate=final_metrics["false_alarm_rate"],
            )
        ).wait_and_continue(terminate=True)

        trigger_runtime.send(settings.triggers.get("exp_end"))

        pd.DataFrame(all_data).to_csv(settings.res_file, index=False)
        trigger_runtime.close()
        core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = parse_task_run_options(
        task_root=task_root,
        description="Run Oddball Task (MMN/P3) in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )
    run(options)


if __name__ == "__main__":
    main()
