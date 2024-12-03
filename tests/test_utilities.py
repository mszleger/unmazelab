from app.utilities import *

def test_call_command():
    assert call_command('ls tests/data/call_command', '') == 'file_1.txt\nfile_2.txt'
    assert call_command('cat', 'abcd') == 'abcd'