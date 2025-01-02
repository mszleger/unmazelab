'''A module containing any helper functions used by other modules.'''

import subprocess

def call_command(command: str, stdin: str) -> str:
    '''Calls command in shell.

    Calls given command in shell, sends on standard input of started program
    given string and returns data sent by started program to standard output.

    Args:
        command: Command to run in shell to start program.
        stdin: String to send on standard input of started program.

    Returns:
        String containing data sent by started program on it's standard output.
    '''
    command = command.split()
    proc = subprocess.Popen(command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    proc.stdin.write(stdin.encode('utf8'))
    proc.stdin.flush()
    stdout, _ = proc.communicate()
    return stdout.decode('utf8').strip()
