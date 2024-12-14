from app.utilities import *

def test_call_command_with_options():
    assert call_command('ls tests/data/call_command', '') == 'file_1.txt\nfile_2.txt'

def test_call_command_stdio_stdout_communication():
    assert call_command('cat', 'abcd') == 'abcd'