"""A tiny decision engine for routing and simple rules."""

from __future__ import annotations


from typing import Callable, List, Optional, Tuple, Union


class DecisionEngine:
    """A rule engine that maps predicates to an action (list of stages).

    Rules are evaluated in registration order; the first matching rule's
    action is returned. Actions may be a callable that receives the context
    and returns a list of stage task names, or a static list of stage names.
    """

    def __init__(self) -> None:
        self._rules: List[Tuple[Callable[[dict], bool], Union[Callable[[dict], list], list]]] = []

    def register_rule(self, predicate: Callable[[dict], bool], action: Union[Callable[[dict], list], list, None] = None) -> None:
        """Register a predicate -> action mapping.

        `action` can be a callable(context) -> list[str] or a static list.
        """
        # Allow registering predicate-only rules (useful for simple tests/guards)
        if action is None:
            # action default: return None (no action) — evaluate() still exposes predicates
            self._rules.append((predicate, []))
        else:
            self._rules.append((predicate, action))

    def evaluate(self, context: dict) -> List[Callable[[dict], bool]]:
        """Return predicates that match the context."""
        return [pred for pred, _ in self._rules if pred(context)]

    def decide(self, context: dict) -> Optional[list]:
        """Return the action (list of stages) for the first matching rule, if any."""
        for pred, action in self._rules:
            try:
                if pred(context):
                    if callable(action):
                        return action(context)
                    return list(action)
            except Exception:
                # swallow rule errors and continue
                continue
        return None


__all__ = ["DecisionEngine"]
