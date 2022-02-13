import subprocess

"""
    If shell is True, the specified command will be executed through the shell.
    If check is true, and the process exits with a non-zero exit code, a CalledProcessError exception will be raised.
    If capture_output is true, stdout and stderr will be captured.

    If returncode is non-zero, raise a CalledProcessError.
    """


def run_command(command, verbose=True):
    subprocess.run(command, shell=True, check=True, capture_output=not verbose)
