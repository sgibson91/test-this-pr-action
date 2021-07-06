import pytest
from src.utils import run_cmd


def test_run_cmd():
    test_cmd = ["echo", "hello"]
    result = run_cmd(test_cmd)

    assert result["returncode"] == 0
    assert result["output"] == "hello"
    assert result["err_msg"] == ""


def test_run_cmd_exception():
    test_cmd = ["ehco", "hello"]

    with pytest.raises(FileNotFoundError):
        run_cmd(test_cmd)
