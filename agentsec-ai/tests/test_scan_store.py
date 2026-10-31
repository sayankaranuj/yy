from backend.storage import ScanStore


def test_scan_store_persists_across_instances(tmp_path) -> None:
    store_path = tmp_path / "scans.json"

    first_store = ScanStore(store_path)
    first_store.create_record(name="Persisted scan", target="persisted.test")

    second_store = ScanStore(store_path)
    records = second_store.list_records()

    assert len(records) == 1
    assert records[0]["name"] == "Persisted scan"
    assert records[0]["target"] == "persisted.test"
