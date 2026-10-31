"""A tiny state machine for scan workflows."""

from __future__ import annotations

from typing import Callable, Dict


class StateMachine:
    def __init__(self, initial: str) -> None:
        self.state = initial
        self._transitions: Dict[str, Dict[str, Callable[[], None]]] = {}

    def add_transition(self, from_state: str, to_state: str, action: Callable[[], None] | None = None) -> None:
        self._transitions.setdefault(from_state, {})[to_state] = action or (lambda: None)

    def trigger(self, to_state: str) -> None:
        actions = self._transitions.get(self.state, {})
        if to_state not in actions:
            raise RuntimeError(f"Invalid transition from {self.state} to {to_state}")
        action = actions[to_state]
        action()
        self.state = to_state


__all__ = ["StateMachine"]
