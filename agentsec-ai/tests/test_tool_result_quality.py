from backend.plugins.base_plugin import PluginOutput
from backend.workflow_results import task_result_status


def test_tool_states_distinguish_empty_findings_and_findings() -> None:
    assert task_result_status("completed", {"finding_count": 0}) == "SUCCESS_NO_RESULTS"
    assert task_result_status("completed", {"findings": [{"id": "1"}]}) == "SUCCESS_WITH_FINDINGS"
    assert task_result_status("completed", {"timed_out": True}) == "TIMED_OUT"
    assert task_result_status("completed", {"unavailable": True}) == "UNAVAILABLE"


def test_plugin_output_exposes_execution_metadata() -> None:
    output = PluginOutput(
        scan_id="1",
        status="timed_out",
        timed_out=True,
        exit_code=None,
        execution_time=1.5,
    )
    assert output.status == "timed_out"
    assert output.timed_out is True
