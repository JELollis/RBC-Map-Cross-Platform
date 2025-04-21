    # -----------------------
    # Menu Control Items
    # -----------------------

    def get_default_screenshot_path(self, suffix: str) -> str:
        pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures", "RBC Map")
        os.makedirs(pictures_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_filename = f"{timestamp}_{suffix}.png"
        return os.path.join(pictures_dir, default_filename)

    def save_webpage_screenshot(self):
        """
        Save the current webpage as a screenshot to Pictures/RBC Map with a timestamped filename.
        """
        default_path = self.get_default_screenshot_path("webpage")
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Webpage Screenshot", default_path,
                                                   "PNG Files (*.png);;All Files (*)")
        if file_name:
            self.website_frame.grab().save(file_name)

    def save_app_screenshot(self):
        """
        Save the current application window as a screenshot to Pictures/RBC Map with a timestamped filename.
        """
        default_path = self.get_default_screenshot_path("app")
        file_name, _ = QFileDialog.getSaveFileName(self, "Save App Screenshot", default_path,
                                                   "PNG Files (*.png);;All Files (*)")
        if file_name:
            self.grab().save(file_name)

    def open_shopping_list_tool(self):
        """
        Opens the ShoppingListTool, using the currently selected character from character_list.
        If no character is selected, it displays an error message.
        """
        # Get the currently selected character from the QListWidget (character_list)
        current_item = self.character_list.currentItem()

        if current_item:
            character_name = current_item.text()
        else:
            # Show an error message if no character is selected
            QMessageBox.warning(self, "No Character Selected", "Please select a character from the list.")
            return

        # Open the ShoppingListTool with the selected character and unified database path
        self.shopping_list_tool = ShoppingListTool(character_name, DB_PATH)
        self.shopping_list_tool.show()

    def open_damage_calculator_tool(self):
        """
        Opens the Damage Calculator dialog within RBCCommunityMap.
        """
        # Initialize the DamageCalculator dialog with the SQLite database connection
        connection = sqlite3.connect(DB_PATH)
        damage_calculator = DamageCalculator(connection)

        # Set the default selection in the combobox to 'No Charisma'
        damage_calculator.charisma_dropdown.setCurrentIndex(0)  # Index 0 corresponds to 'No Charisma'

        # Show the DamageCalculator dialog as a modal
        damage_calculator.exec()

        # Close the database connection after use
        connection.close()

    def display_shopping_list(self, shopping_list):
        """
        Display the shopping list in a dialog.
        """
        shopping_list_text = "\n".join(
            f"{entry['shop']} - {entry['item']} - {entry['quantity']}x - {entry['total_cost']} coins"
            for entry in shopping_list
        )
        total_cost = sum(entry['total_cost'] for entry in shopping_list)
        shopping_list_text += f"\n\nTotal Coins - {total_cost}"

        QMessageBox.information(self, "Damage Calculator Shopping List", shopping_list_text)

    def open_powers_dialog(self):
        """
        Opens the Powers Dialog and ensures character coordinates are passed correctly.
        """
        powers_dialog = PowersDialog(self, self.character_x, self.character_y, DB_PATH)  # Ensure correct parameters
        powers_dialog.exec()

    def open_css_customization_dialog(self):
        """Open the CSS customization dialog."""
        dialog = CSSCustomizationDialog(self)
        dialog.exec()

    def update_log_level_menu(self) -> None:
        """
        Update the check state of log level actions based on current level from DB.
        """
        current_level = get_logging_level_from_db()
        for level, action in self.log_level_actions.items():
            action.setChecked(level == current_level)

    def set_log_level(self, level: int) -> None:
        """
        Set the log level and persist it in the database.
        """
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO settings (setting_name, setting_value)
                    VALUES ('log_level', ?)
                    ON CONFLICT(setting_name) DO UPDATE SET setting_value = excluded.setting_value
                """, (level,))
                conn.commit()

            logging.getLogger().setLevel(level)
            self.update_log_level_menu()
            logging.info(f"Log level set to {logging.getLevelName(level)}")

        except sqlite3.Error as e:
            logging.error(f"Failed to save log level to database: {e}")
