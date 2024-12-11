from app.app_state import AppState
from app.main_window import MainWindow

if __name__ == "__main__":
    app_state = AppState("config.xml")
    main_window = MainWindow(app_state)