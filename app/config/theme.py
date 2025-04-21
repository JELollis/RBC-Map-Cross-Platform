    # -----------------------
    # Load and Apply Customized UI Theme
    # -----------------------
    def load_theme_settings(self) -> None:
        """
        Load theme settings from the SQLite database (settings table).

        Updates self.color_mappings using settings from the database,
        preserving any other existing color mappings.
        """
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT setting_name, setting_value FROM settings WHERE setting_name LIKE 'theme_%'")
                settings = dict(cursor.fetchall())

                # Update existing mappings only for theme-specific keys
                for key_with_prefix, value in settings.items():
                    key = key_with_prefix.replace("theme_", "", 1)
                    self.color_mappings[key] = QColor(value)

                logging.debug(f"Theme settings loaded from DB and applied. Keys updated: {list(settings.keys())}")
        except sqlite3.Error as e:
            logging.error(f"Failed to load theme settings: {e}")

    def save_theme_settings(self) -> bool:
        """
        Save each theme setting to the SQLite settings table.

        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                # Use executemany for bulk UPSERT
                cursor.executemany(
                    '''
                    INSERT INTO settings (setting_name, setting_value)
                    VALUES (?, ?)
                    ON CONFLICT(setting_name) DO UPDATE SET setting_value = excluded.setting_value
                    ''',
                    [(f"theme_{key}", color.name()) for key, color in self.color_mappings.items()]
                )
                conn.commit()
                logging.debug("Theme settings saved successfully")
                return True
        except sqlite3.Error as e:
            logging.error(f"Failed to save theme settings: {e}")
            return False

    def apply_theme(self) -> None:
        """Apply current theme settings to the application's stylesheet."""
        try:
            bg_color = self.color_mappings.get("background", QColor("#d4d4d4")).name()
            text_color = self.color_mappings.get("text_color", QColor("#000000")).name()
            btn_color = self.color_mappings.get("button_color", QColor("#b1b1b1")).name()

            stylesheet = (
                f"QWidget {{ background-color: {bg_color}; color: {text_color}; }}"
                f"QPushButton {{ background-color: {btn_color}; color: {text_color}; }}"
                f"QLabel {{ color: {text_color}; }}"
            )
            self.setStyleSheet(stylesheet)
            logging.debug("Theme applied successfully")
        except Exception as e:
            logging.error(f"Failed to apply theme: {e}")
            self.setStyleSheet("")  # Reset to default on failure

    def change_theme(self) -> None:
        """
        Open theme customization dialog and apply/save selected theme.

        Assumes ThemeCustomizationDialog is defined elsewhere with exec() and color_mappings.
        """
        dialog = ThemeCustomizationDialog(self, color_mappings=self.color_mappings)
        if dialog.exec():
            self.color_mappings = dialog.color_mappings
            self.apply_theme()
            if self.save_theme_settings():
                logging.info("Theme updated and saved")
            else:
                logging.warning("Theme applied but not saved due to database error")
