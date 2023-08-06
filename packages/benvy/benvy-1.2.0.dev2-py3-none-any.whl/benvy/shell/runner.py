import os
import sys
import io
import subprocess
from typing import Union


def run_and_read_output(command: Union[str, list], cwd: str = os.getcwd(), shell=True):
    proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, shell=shell)
    output = io.TextIOWrapper(proc.stdout, encoding="utf-8").read().rstrip()

    if not output:
        raise Exception(f"No output returned to stdout for: {command}")

    return output


def run_shell_command(command: Union[str, list], cwd: str = os.getcwd(), shell=True):
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell)

    for line in iter(process.stdout.readline, b""):
        sys.stdout.write(line)
