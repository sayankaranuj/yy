from backend.storage import FindingsStore


def test_findings_store_persists_records(tmp_path) -> None:
    store_path = tmp_path / "findings.json"

    store = FindingsStore(store_path)
    store.create_record(title="Weak TLS policy", severity="high")

    reloaded = FindingsStore(store_path)
    records = reloaded.list_records()

    assert len(records) == 1
    assert records[-1]["title"] == "Weak TLS policy"
    assert records[-1]["severity"] == "high"
