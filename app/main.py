import sys
from PySide6.QtWidgets import QApplication
from app.gui.mainwindow import RBCCommunityMap
from app.config.constants import APP_ICON
from app.config.theme import load_theme_settings
from app.config.constants import setup_logging, get_logging_level_from_db
from app.config.constants import SplashScreen


def main() -> None:
    """Run the RBC City Map Application."""
    app = QApplication(sys.argv)
    app.setWindowIcon(APP_ICON)

    splash = SplashScreen("images/loading.png")
    splash.show()
    splash.show_message("Starting up...")

    # Setup logging
    setup_logging(log_level=get_logging_level_from_db())
    splash.show_message("Logging ready")

    # Create main window
    main_window = RBCCommunityMap()

    # Load and apply theme
    main_window.color_mappings = load_theme_settings()
    main_window.apply_theme()
    splash.show_message("Theme applied")

    # Initialize with splash-decorated methods
    init_methods = [
        '_init_scraper',
        '_init_window_properties',
        '_init_web_profile',
        '_init_ui_state',
        '_init_characters',
        '_init_ui_components',
        '_finalize_setup'
    ]

    for name in init_methods:
        method = getattr(main_window, name)
        setattr(main_window, name, splash.show_message(name)(method))  # if splash_message is a decorator

    main_window.splash = splash
    main_window.show()
    splash.finish(main_window)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
