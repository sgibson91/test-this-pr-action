"""
Helper functions
"""
import subprocess


def run_cmd(cmd: list) -> None:
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
