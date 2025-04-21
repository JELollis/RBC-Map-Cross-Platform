# -----------------------
# Keybindings
# -----------------------

    def load_keybind_config(self) -> int:
        """
        Load keybind configuration from the database.

        Returns:
            int: Keybind mode (0=Off, 1=WASD, 2=Arrows), defaults to 1 (WASD) if not found.
        """
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT setting_value FROM settings WHERE setting_name = 'keybind_config'")
                result = cursor.fetchone()
                return int(result[0]) if result else 1  # Default to WASD
        except sqlite3.Error as e:
            logging.error(f"Failed to load keybind config: {e}")
            return 1  # Fallback to WASD on error

    def setup_keybindings(self) -> None:
        """Set up keybindings for character movement based on current config."""
        movement_configs = {
            1: {  # WASD Mode
                Qt.Key.Key_W: 1,  # Top-center
                Qt.Key.Key_A: 3,  # Middle-left
                Qt.Key.Key_S: 7,  # Bottom-center
                Qt.Key.Key_D: 5   # Middle-right
            },
            2: {  # Arrow Keys Mode
                Qt.Key.Key_Up: 1,
                Qt.Key.Key_Left: 3,
                Qt.Key.Key_Down: 7,
                Qt.Key.Key_Right: 5
            },
            0: {}  # Off mode (no keybindings)
        }

        self.movement_keys = movement_configs.get(self.keybind_config, movement_configs[1])
        logging.debug(f"Setting up keybindings: {self.movement_keys}")

        self.clear_existing_keybindings()

        if self.keybind_config == 0:
            logging.info("Keybindings disabled (mode 0)")
            return

        # Ensure website_frame exists before proceeding
        if not hasattr(self, 'website_frame'):
            logging.error("website_frame not initialized; skipping keybinding setup")
            return

        for key, move_index in self.movement_keys.items():
            shortcut = QShortcut(QKeySequence(key), self.website_frame, context=Qt.ShortcutContext.ApplicationShortcut)
            shortcut.activated.connect(lambda idx=move_index: self.move_character(idx))
            logging.debug(f"Bound key {key} to move index {move_index}")

    def move_character(self, move_index: int) -> None:
        """
        Move character to the specified grid position via JavaScript.

        Args:
            move_index (int): Index in the 3x3 movement grid (0-8).
        """
        if not hasattr(self, 'website_frame') or not self.website_frame.page():
            logging.warning("Cannot move character: website_frame or page not initialized")
            return

        logging.debug(f"Attempting move to grid index: {move_index}")
        js_code = """
            (function() {
                const table = document.querySelector('table table');
                if (!table) return 'No table';
                const spaces = Array.from(table.querySelectorAll('td'));
                if (spaces.length !== 9) return 'Invalid grid size: ' + spaces.length;
                const targetSpace = spaces[%d];
                if (!targetSpace) return 'No target space';
                const form = targetSpace.querySelector('form[action="/blood.pl"][method="POST"]');
                if (!form) return 'No form';
                const x = form.querySelector('input[name="x"]').value;
                const y = form.querySelector('input[name="y"]').value;
                form.submit();
                return 'Submitted to x=' + x + ', y=' + y;
            })();
        """ % move_index
        self.website_frame.page().runJavaScript(js_code, lambda result: logging.debug(f"Move result: {result}"))
        self.website_frame.setFocus()

    def toggle_keybind_config(self, mode: int) -> None:
        """
        Switch between keybinding modes (0=Off, 1=WASD, 2=Arrows) and update settings.

        Args:
            mode (int): Keybind mode to switch to.
        """
        if mode not in {0, 1, 2}:
            logging.warning(f"Invalid keybind mode: {mode}; ignoring")
            return

        self.keybind_config = mode
        mode_text = {0: "Off", 1: "WASD", 2: "Arrow Keys"}[mode]
        logging.info(f"Switching to keybind mode {mode} ({mode_text})")

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO settings (setting_name, setting_value) VALUES ('keybind_config', ?)",
                    (mode,)
                )
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Failed to save keybind config {mode}: {e}")
            return  # Don’t proceed if database fails

        self.setup_keybindings()
        self.update_keybind_menu()
        QMessageBox.information(self, "Keybind Config", f"Switched to {mode_text}")

    def update_keybind_menu(self) -> None:
        """Update keybinding menu checkmarks based on current config."""
        if not hasattr(self, 'keybind_wasd_action') or not hasattr(self, 'keybind_arrow_action') or \
           not hasattr(self, 'keybind_off_action'):
            logging.warning("Keybind menu actions not initialized; skipping update")
            return

        self.keybind_wasd_action.setChecked(self.keybind_config == 1)
        self.keybind_arrow_action.setChecked(self.keybind_config == 2)
        self.keybind_off_action.setChecked(self.keybind_config == 0)
        logging.debug(f"Updated keybind menu: WASD={self.keybind_config == 1}, Arrows={self.keybind_config == 2}, Off={self.keybind_config == 0}")

    def clear_existing_keybindings(self) -> None:
        """Remove existing shortcuts from website_frame to prevent duplicates."""
        if not hasattr(self, 'website_frame'):
            logging.debug("No website_frame to clear keybindings from")
            return

        shortcuts = self.website_frame.findChildren(QShortcut)
        for shortcut in shortcuts:
            shortcut.setParent(None)
            shortcut.deleteLater()  # Ensure cleanup
        logging.debug(f"Cleared {len(shortcuts)} existing keybindings")
