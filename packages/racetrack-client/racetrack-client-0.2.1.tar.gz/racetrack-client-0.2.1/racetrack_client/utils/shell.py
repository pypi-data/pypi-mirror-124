import io
import subprocess
import sys
from pathlib import Path
from typing import Optional
from racetrack_client.log.logs import get_logger

logger = get_logger(__name__)


def shell(cmd: str, workdir: Optional[Path] = None):
    """
    Run system shell command.
    Print live stdout as it comes (line by line) and capture entire output in case of errors.
    :raises:
        CommandError: in case of non-zero command exit code.
    """
    _run_shell_command(cmd, workdir)


def shell_output(cmd: str, workdir: Optional[Path] = None, print_stdout: bool = False) -> str:
    """
    Run system shell command and return its output.
    Print live stdout as it comes (line by line) and capture entire output in case of errors.
    """
    captured_stream = _run_shell_command(cmd, workdir, print_stdout)
    return captured_stream.getvalue()


def _run_shell_command(cmd: str, workdir: Optional[Path] = None, print_stdout: bool = True) -> io.StringIO:
    logger.debug(f'Command: {cmd}')
    if len(cmd) > 4096:  # see https://github.com/torvalds/linux/blob/v5.11/drivers/tty/n_tty.c#L1681
        raise RuntimeError('maximum tty line length has been exceeded')
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=workdir)
    try:
        # fork command output to stdout & captured buffer
        captured_stream = io.StringIO()
        for line in iter(process.stdout.readline, b''):
            line_str = line.decode()
            if print_stdout:
                sys.stdout.write(line_str)
                sys.stdout.flush()
            captured_stream.write(line_str)

        process.wait()
        if process.returncode != 0:
            stdout = captured_stream.getvalue()
            raise CommandError(cmd, stdout, process.returncode)
        return captured_stream
    except KeyboardInterrupt:
        logger.warning('killing subprocess')
        process.kill()
        raise


class CommandError(RuntimeError):
    def __init__(self, cmd: str, stdout: str, returncode: int):
        super().__init__()
        self.cmd = cmd
        self.stdout = stdout
        self.returncode = returncode

    def __str__(self):
        return f'command failed: {self.cmd}: {self.stdout}'
