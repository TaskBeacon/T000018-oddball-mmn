from __future__ import annotations

from dataclasses import dataclass
import random as _py_random
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Oddball sampler responder.

    - On `target` trials:
      - hit with probability `target_hit_rate` (respond)
      - miss otherwise (no response)
    - On non-target (`standard` / `deviant`) trials:
      - false alarm with probability `non_target_false_alarm_rate`
      - correct rejection otherwise (no response)
    """

    key: str | None = "space"
    target_hit_rate: float = 0.85
    non_target_false_alarm_rate: float = 0.05
    rt_mean_s: float = 0.35
    rt_sd_s: float = 0.06
    rt_min_s: float = 0.12

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.target_hit_rate = max(0.0, min(1.0, float(self.target_hit_rate)))
        self.non_target_false_alarm_rate = max(0.0, min(1.0, float(self.non_target_false_alarm_rate)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "oddball_sampler", "reason": "no_valid_keys"})

        chosen_key = self.key if self.key in valid_keys else valid_keys[0]
        rt_s = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))

        phase = str(obs.phase or "")
        factors = dict(obs.task_factors or {})
        condition = str(factors.get("condition", ""))

        if phase != "target":
            # Let scripted progression continue on non-target input screens if needed.
            return Action(
                key=chosen_key,
                rt_s=rt_s,
                meta={"source": "oddball_sampler", "phase": phase, "outcome": "continue"},
            )

        if condition == "target":
            hit = self._sample_random() < self.target_hit_rate
            if not hit:
                return Action(key=None, rt_s=None, meta={"source": "oddball_sampler", "condition": condition, "outcome": "miss"})
            return Action(key=chosen_key, rt_s=rt_s, meta={"source": "oddball_sampler", "condition": condition, "outcome": "hit"})

        false_alarm = self._sample_random() < self.non_target_false_alarm_rate
        if not false_alarm:
            return Action(
                key=None,
                rt_s=None,
                meta={"source": "oddball_sampler", "condition": condition, "outcome": "correct_rejection"},
            )
        return Action(
            key=chosen_key,
            rt_s=rt_s,
            meta={"source": "oddball_sampler", "condition": condition, "outcome": "false_alarm"},
        )
