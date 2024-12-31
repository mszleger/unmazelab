from app.utilities import *

def test_call_command():
    assert call_command('python tests/scripts/echo.py', 'abcd') == 'abcd'
