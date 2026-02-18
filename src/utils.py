from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from psychopy import logging


@dataclass
class Controller:
    """Oddball sequence planner and trial-level performance tracker."""

    standard_prob: float = 0.70
    deviant_prob: float = 0.20
    target_prob: float = 0.10
    randomize_order: bool = True
    force_first_standard: bool = True
    enable_logging: bool = True

    def __post_init__(self) -> None:
        probs = {
            "standard": float(self.standard_prob),
            "deviant": float(self.deviant_prob),
            "target": float(self.target_prob),
        }
        total = sum(max(0.0, v) for v in probs.values())
        if total <= 0.0:
            probs = {"standard": 0.7, "deviant": 0.2, "target": 0.1}
            total = 1.0
        self._probs = {k: max(0.0, v) / total for k, v in probs.items()}
        self._queues: dict[int, list[str]] = {}
        self.histories: dict[str, list[bool]] = {}

    @classmethod
    def from_dict(cls, config: dict[str, Any] | None = None) -> "Controller":
        config = config or {}
        allowed = {
            "standard_prob",
            "deviant_prob",
            "target_prob",
            "randomize_order",
            "force_first_standard",
            "enable_logging",
        }
        extra = set(config.keys()) - allowed
        if extra:
            raise ValueError(f"[OddballController] Unsupported config keys: {sorted(extra)}")
        return cls(**config)

    def _allocate_counts(self, n_trials: int) -> dict[str, int]:
        n = max(0, int(n_trials))
        expected = {k: self._probs[k] * n for k in self._probs}
        base = {k: int(expected[k]) for k in expected}
        remainder = n - sum(base.values())
        ranked = sorted(expected.keys(), key=lambda k: (expected[k] - base[k]), reverse=True)
        i = 0
        while remainder > 0 and ranked:
            key = ranked[i % len(ranked)]
            base[key] += 1
            remainder -= 1
            i += 1
        # Ensure rare classes still appear in practical oddball runs.
        if n >= 3:
            if base["deviant"] == 0:
                base["deviant"] = 1
                base["standard"] = max(0, base["standard"] - 1)
            if base["target"] == 0:
                base["target"] = 1
                base["standard"] = max(0, base["standard"] - 1)
        return base

    def prepare_block(self, *, block_idx: int, n_trials: int, seed: int | None) -> list[str]:
        counts = self._allocate_counts(n_trials)
        seq: list[str] = []
        for cond in ("standard", "deviant", "target"):
            seq.extend([cond] * counts.get(cond, 0))

        rng = random.Random(seed)
        if self.randomize_order:
            rng.shuffle(seq)

        if self.force_first_standard and seq:
            try:
                pos = seq.index("standard")
            except ValueError:
                pos = None
            if pos is not None and pos != 0:
                seq[0], seq[pos] = seq[pos], seq[0]

        self._queues[int(block_idx)] = list(seq)

        if self.enable_logging:
            dist = {k: seq.count(k) for k in ("standard", "deviant", "target")}
            logging.data(f"[OddballController] block={block_idx} n_trials={len(seq)} seed={seed} dist={dist}")

        return list(seq)

    def next_condition(self, *, block_idx: int) -> str:
        queue = self._queues.get(int(block_idx), [])
        if not queue:
            raise RuntimeError(f"[OddballController] Empty sequence for block_idx={block_idx}.")
        return str(queue.pop(0))

    def update(self, *, hit: bool, condition: str) -> None:
        cond = str(condition)
        self.histories.setdefault(cond, []).append(bool(hit))
        if not self.enable_logging:
            return
        hist = self.histories[cond]
        acc = sum(hist) / max(1, len(hist))
        logging.data(f"[OddballController] condition={cond} trials={len(hist)} accuracy={acc:.2%}")
