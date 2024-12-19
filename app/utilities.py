import subprocess

def call_command(command, stdin):
    """
    Calls command in command line.

    :param stdin: String with standard input to send to runned command.
    :type stdin: str

    :return: Standard output returned by runned command.
    :rtype: str
    """
    command = command.split()
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.stdin.write(stdin.encode("utf8"))
    proc.stdin.flush()
    stdout, _ = proc.communicate()
    return stdout.decode("utf8").strip()