def test_import_contracts() -> None:
    import contracts

    assert contracts.__name__ == "contracts"
