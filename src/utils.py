"""
Helper functions
"""
import requests
import subprocess


def post_request(
    url: str, headers: dict = None, json: dict = None, return_json: bool = True
) -> None:
    """Send a POST request to an HTTP API endpoint
    Args:
        url (str): The URL to send the request to
        headers (dict, optional): A dictionary of any headers to send with the
            request. Defaults to None.
        json (dict, optional): A dictionary containing JSON payload to send with
            the request. Defaults to None.
        return_json (bool, optional): Return the JSON payload response.
            Defaults to False.
    """
    resp = requests.post(url, headers=headers, json=json)

    if not resp:
        raise RuntimeError(resp.text)

    if return_json:
        return resp.json()


def run_cmd(cmd: list) -> dict:
    """Use Popen to run a bash command in a sub-shell

    Args:
        cmd (list): The bash command to run

    Returns:
        dict: The output of the command, including status code and error
              messages
    """
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    msgs = proc.communicate()

    result = {
        "returncode": proc.returncode,
        "output": msgs[0].decode(encoding=("utf-8")).strip("\n"),
        "err_msg": msgs[1].decode(encoding=("utf-8")).strip("\n"),
    }

    if result["returncode"] != 0:
        raise RuntimeError(
            result["err_msg"]
        )

    return result
