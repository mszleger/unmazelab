import subprocess

def call_command(command, stdin):
    command = command.split()
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.stdin.write(stdin.encode("utf8"))
    proc.stdin.flush()
    stdout, _ = proc.communicate()
    return stdout.decode("utf8").strip()