"""Fallback handling for tool execution failures."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from backend.orchestrator.decision_engine import DecisionEngine

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ToolExecutionRecord:
    tool_name: str
    result_count: int
    output_quality_score: float = 0.0
    error: str | None = None


class FallbackManager:
    """Selects fallback tools when a primary tool fails or performs poorly."""

    def __init__(self) -> None:
        self.decision_engine = DecisionEngine()

    def evaluate_result_quality(self, tool_name: str, result: Any) -> float:
        if not result:
            return 0.0
        if isinstance(result, list):
            return min(1.0, len(result) / 5.0)
        return 0.5

    def should_fallback(self, record: ToolExecutionRecord) -> bool:
        if record.result_count == 0:
            logger.info("Fallback triggered for %s due to zero results", record.tool_name)
            return True
        if record.output_quality_score < 0.3:
            logger.info("Fallback triggered for %s due to low quality", record.tool_name)
            return True
        return False

    async def handle_failure(self, record: ToolExecutionRecord, scan_id: str, db: Any) -> str | None:
        fallback_tool = self.decision_engine.get_fallback_tool(record.tool_name)
        if fallback_tool:
            logger.info("Using fallback %s for %s on scan %s", fallback_tool, record.tool_name, scan_id)
            return fallback_tool
        return None

    def merge_results(self, primary_results: list[Any], fallback_results: list[Any], tool_category: str) -> list[Any]:
        merged = list(primary_results)
        merged.extend(fallback_results)
        seen: set[Any] = set()
        deduplicated: list[Any] = []
        for item in merged:
            key = (tool_category, item) if not isinstance(item, (str, int, float, bool)) else item
            if key in seen:
                continue
            seen.add(key)
            deduplicated.append(item)
        return deduplicated


__all__ = ["FallbackManager", "ToolExecutionRecord"]
