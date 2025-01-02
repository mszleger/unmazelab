from app import utilities

def test_call_command():
    '''Tests function call_command.

    Runs program returning everything sent to it's standard input
    on it's standard output.
    '''
    cmd = 'python tests/scripts/echo.py'
    test_str = 'abcd'
    assert utilities.call_command(cmd, test_str) == test_str
