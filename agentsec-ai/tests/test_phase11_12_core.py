from backend.models.scan import ScanMode
from backend.plugins.registry import registry


def test_scan_mode_enum_exists() -> None:
    assert ScanMode.CLASSIC.value == "CLASSIC"
    assert ScanMode.HYBRID.value == "HYBRID"
    assert ScanMode.AUTONOMOUS.value == "AUTONOMOUS"


def test_removed_tools_are_not_discovered() -> None:
    registry.auto_discover()
    removed_tools = {
        "jwt_tool",
        "s3scanner",
        "gitleaks",
        "subjack",
        "scrapegraph_plugin",
        "strix_plugin",
    }
    assert removed_tools.isdisjoint(
        plugin["name"] for plugin in registry.list_all()
    )


def test_removed_tools_are_not_exposed_in_attack_catalog() -> None:
    from backend.api.schemas import ATTACK_CATALOG

    categories = {
        category
        for group in ATTACK_CATALOG.values()
        for category in group["items"]
    }
    assert "auth.jwt" not in categories
    assert "ai_agent.strix_validation" not in categories
