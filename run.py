#!/usr/bin/env python
import sys
sys.path.append('app')

from app import app_state
from app import ui

if __name__ == "__main__":
    app_state = app_state.AppState("config.xml")
    main_window = ui.MainWindow(app_state)