# -----------------------
# RBC Community Map Main Class
# -----------------------

class RBCCommunityMap(QMainWindow):
    """
    Main application class for the RBC Community Map.
    """

    def __init__(self):
        """
        Initialize the RBCCommunityMap and its components efficiently.

        Sets up the main window, scraper, cookie handling, data loading, and UI components
        with proper error handling and asynchronous initialization where possible.
        """
        super().__init__()

        # Core state flags
        self.is_updating_minimap = False
        self.login_needed = True
        self.webview_loaded = False
        self.splash = None

        # Initialize character coordinates
        self.character_x = None
        self.character_y = None
        self.selected_character = None
        self.destination = None

        # Initialize essential components early
        self._init_data()
        self._init_scraper()
        self._init_window_properties()
        self._init_web_profile()

        # UI and character setup
        self._init_ui_state()
        self._init_characters()
        self._init_ui_components()

        # Final setup steps
        self._finalize_setup()

    @splash_message(None)
    def _init_scraper(self) -> None:
        """Initialize the AVITD scraper and start scraping in a separate thread."""
        self.AVITD_scraper = AVITDScraper()
        # Use QThread for non-blocking scraping (assuming AVITDScraper supports it)
        from PySide6.QtCore import QThreadPool
        QThreadPool.globalInstance().start(lambda: self.AVITD_scraper.scrape_guilds_and_shops())
        logging.debug("Started scraper in background thread")

    @splash_message(None)
    def _init_window_properties(self) -> None:
        """Set up main window properties."""
        try:
            self.setWindowIcon(QIcon('images/favicon.ico'))
            self.setWindowTitle('RBC Community Map')
            self.setGeometry(100, 100, 1200, 800)
            self.load_theme_settings()
            self.apply_theme()
        except Exception as e:
            logging.error(f"Failed to set window properties: {e}")
            # Fallback to default icon/title if needed
            self.setWindowTitle('RBC Community Map (Fallback)')

    @splash_message(None)
    def _init_web_profile(self) -> None:
        """Set up QWebEngineProfile for cookie handling."""
        self.web_profile = QWebEngineProfile.defaultProfile()
        cookie_storage_path = os.path.join(os.getcwd(), 'sessions')
        try:
            os.makedirs(cookie_storage_path, exist_ok=True)
            self.web_profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
            self.web_profile.setPersistentStoragePath(cookie_storage_path)
            self.setup_cookie_handling()
        except OSError as e:
            logging.error(f"Failed to set up cookie storage at {cookie_storage_path}: {e}")
            # Continue with in-memory cookies if storage fails

    @splash_message(None)
    def _init_data(self) -> None:
        """Load initial data from the database with fallback."""
        try:
            (
                self.columns, self.rows, self.banks_coordinates, self.taverns_coordinates,
                self.transits_coordinates, self.user_buildings_coordinates, self.color_mappings,
                self.shops_coordinates, self.guilds_coordinates, self.places_of_interest_coordinates,
                self.keybind_config, self.current_css_profile
            ) = load_data(DB_PATH)
        except sqlite3.Error as e:
            logging.critical(f"Failed to load initial data: {e}")
            # Use fallback data from load_data (already implemented)
            self.columns, self.rows, self.banks_coordinates, self.taverns_coordinates, \
            self.transits_coordinates, self.user_buildings_coordinates, self.color_mappings, \
            self.shops_coordinates, self.guilds_coordinates, self.places_of_interest_coordinates, \
            self.keybind_config = (
                {}, {}, [], {}, {}, {}, {'default': QColor('#000000')}, {}, {}, {}, 1
            )

    @splash_message(None)
    def _init_ui_state(self) -> None:
        """Initialize UI-related state variables."""
        self.zoom_level = 3
        self.load_zoom_level_from_database()  # May override zoom_level
        self.minimap_size = 280
        self.column_start = 0
        self.row_start = 0
        self.destination = None

    @splash_message(None)
    def _init_characters(self) -> None:
        """Initialize character-related data and widgets."""
        self.characters = []
        self.character_list = QListWidget()
        self.selected_character = None
        self.load_characters()
        if not self.characters:
            self.firstrun_character_creation()

    @splash_message(None)
    def _init_ui_components(self) -> None:
        """Set up UI components and console logging."""
        self.setup_ui_components()
        self.setup_console_logging()

    @splash_message(None)
    def _finalize_setup(self) -> None:
        """Complete initialization with UI display and final configurations."""
        self.show()
        self.update_minimap()
        self.load_last_active_character()
        self.setup_keybindings()
        self.setFocusPolicy(Qt.StrongFocus)
        if hasattr(self, 'website_frame'):
            self.website_frame.setFocusPolicy(Qt.StrongFocus)
        else:
            logging.warning("website_frame not initialized before focus setup")
        css = self.load_current_css()
        self.apply_custom_css(css)

    def load_current_css(self) -> str:
        """Load CSS for the current profile from the database."""
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT setting_value FROM settings WHERE setting_name = 'css_profile'")
                result = cursor.fetchone()
                profile = result[0] if result else "Default"
                cursor.execute("SELECT element, value FROM custom_css WHERE profile_name = ?", (profile,))
                return "\n".join(f"{elem} {{ {val} }}" for elem, val in cursor.fetchall())
        except sqlite3.Error as e:
            logging.error(f"Failed to load CSS: {e}")
            return ""
