import pytest
import responses
from src.utils import post_request, run_cmd


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


@responses.activate
def test_post_request():
    test_url = "http://jsonplaceholder.typicode.com/"
    test_header = {"Authorization": "token ThIs_Is_A_ToKeN"}
    json = {"Payload": "Send this with the request"}

    responses.add(responses.POST, test_url, json={"Request": "Sent"}, status=200)

    post_request(test_url, headers=test_header, json=json)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_url
    assert responses.calls[0].response.text == '{"Request": "Sent"}'


@responses.activate
def test_post_request_exception():
    test_url = "http://josnplaceholder.typicode.com/"
    test_header = {"Authorization": "token ThIs_Is_A_ToKeN"}
    json = {"Payload": "Send this with the request"}

    responses.add(
        responses.POST,
        test_url,
        body="Could not reach provided URL",
        status=500,
    )

    with pytest.raises(RuntimeError):
        post_request(test_url, headers=test_header, json=json)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_url
