import pytest
from worker.main import main


def test_worker_prints_readiness_line(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out == "mnemograph-worker: ready\n"
    assert captured.err == ""
