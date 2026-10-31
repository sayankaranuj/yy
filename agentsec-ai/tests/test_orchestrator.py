from backend.orchestrator.decision_engine import DecisionEngine, ScanContext
from backend.orchestrator.fallback_manager import FallbackManager, ToolExecutionRecord
from backend.orchestrator.state_machine import InvalidStateTransitionError, StateMachine
from backend.models.domain import Domain, DomainState
from backend.orchestrator.event_bus import EventBus, ReconCompleteEvent


def test_decision_engine_wordpress() -> None:
    engine = DecisionEngine()
    context = ScanContext(scan_id="1", target="example.com", has_wordpress=True)
    decisions = engine.decide_vuln_tools(context)
    assert any(tool.tool_name == "wpscan" for tool in decisions)


def test_decision_engine_port_445() -> None:
    engine = DecisionEngine()
    context = ScanContext(scan_id="1", target="example.com", open_ports=[445])
    decisions = engine.decide_vuln_tools(context)
    assert any(tool.tool_name == "nmap_smb_scripts" for tool in decisions)


def test_fallback_quality_score() -> None:
    manager = FallbackManager()
    record = ToolExecutionRecord(tool_name="subfinder", result_count=0)
    assert manager.should_fallback(record) is True


def test_fallback_chain() -> None:
    engine = DecisionEngine()
    assert engine.get_fallback_tool("subfinder") == "amass"


def test_state_machine_valid_transition() -> None:
    machine = StateMachine()
    domain = Domain(state=DomainState.NEW)
    import asyncio
    asyncio.run(machine.transition(domain, DomainState.DISCOVERED, None))
    assert domain.state == DomainState.DISCOVERED


def test_state_machine_invalid_transition() -> None:
    machine = StateMachine()
    domain = Domain(state=DomainState.NEW)
    import asyncio
    try:
        asyncio.run(machine.transition(domain, DomainState.SCANNED, None))
    except InvalidStateTransitionError:
        return
    raise AssertionError("Expected InvalidStateTransitionError")


def test_event_bus_publish(monkeypatch) -> None:
    class FakeRedis:
        async def publish(self, channel, payload):
            self.channel = channel
            self.payload = payload
            return 1

    bus = EventBus()
    fake_client = FakeRedis()
    monkeypatch.setattr(bus, "_redis", fake_client)
    event = ReconCompleteEvent(scan_id="1", results=[])
    import asyncio
    asyncio.run(bus.publish(event))
    assert fake_client.channel == "agentsec:reconcompleteevent"
    assert fake_client.payload
