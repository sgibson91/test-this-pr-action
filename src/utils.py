"""
Helper functions
"""
import re
import functools
import subprocess
from loguru import logger
from copy import deepcopy


def logger_wraps(*, entry=True, exit=True, level="DEBUG"):

    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)

            # Prevent the logger from leaking ACCESS_TOKEN using regex to select
            # all characters between 'https://' and ':x-oauth-basic' in `git clone`
            # and `git remote set-url` commands
            clean_args = deepcopy(args)
            if ("clone" in clean_args[0]) or ("set-url" in clean_args[0]):
                clean_args[0][-1] = re.sub(r"(?<=\/\/)(.*?)(?=:)", "***", clean_args[0][-1])

            if entry:
                logger_.log(level, "Entering '{}' (args={}, kwargs{})", name, clean_args, kwargs)
            result = func(*args, **kwargs)

            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper


@logger_wraps()
def run_cmd(cmd: list) -> dict:
    """Use Popen to run a bash command in a sub-shell

    Args:
        cmd (list): The bash command to run

    Returns:
        dict: The output of the command, including status code and error
              messages
    """
    logger.info("Executing command...")

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    msgs = proc.communicate()

    result = {
        "returncode": proc.returncode,
        "output": msgs[0].decode(encoding=("utf-8")).strip("\n"),
        "err_msg": msgs[1].decode(encoding=("utf-8")).strip("\n"),
    }

    if result["returncode"] != 0:
        logger.error("Command execution failed!")
        raise RuntimeError(result["err_msg"])

    return result
