# -----------------------
# Character Management
# -----------------------

    def load_characters(self):
        """
        Load characters from the SQLite database, including IDs for reference.
        Only populate the list, do not auto-select.
        """
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()

            # Fetch characters from the database including id
            cursor.execute("SELECT id, name, password FROM characters")
            character_data = cursor.fetchall()
            self.characters = [
                {'id': char_id, 'name': name, 'password': password}
                for char_id, name, password in character_data
            ]

            # Populate characters list without selecting
            self.character_list.clear()
            for character in self.characters:
                self.character_list.addItem(QListWidgetItem(character['name']))
            logging.debug(f"Loaded {len(self.characters)} characters from the database.")

            # Do not set self.selected_character here; let load_last_active_character handle it
            if not self.characters:
                logging.warning("No characters found in the database.")
                self.selected_character = None

        except sqlite3.Error as e:
            logging.error(f"Failed to load characters from database: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load characters: {e}")
            self.characters = []
            self.selected_character = None
        finally:
            connection.close()

    def save_characters(self):
        """
        Save characters to the SQLite database in plaintext.
        """
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            # Insert or update each character without encrypting the password
            for character in self.characters:
                cursor.execute('''
                    INSERT OR REPLACE INTO characters (id, name, password) VALUES (?, ?, ?)
                ''', (character.get('id'), character['name'], character['password']))
            connection.commit()
            logging.debug("Characters saved successfully to the database in plaintext.")
        except sqlite3.Error as e:
            logging.error(f"Failed to save characters to database: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save characters: {e}")
        finally:
            connection.close()

    def on_character_selected(self, item):
        """
        Handle character selection from the list.

        Args:
            item (QListWidgetItem): The selected item in the list.

        Logs the selected character, saves the last active character,
        logs out the current character, and then logs in the selected one.
        """
        character_name = item.text()
        selected_character = next((char for char in self.characters if char['name'] == character_name), None)

        if selected_character:
            logging.debug(f"Selected character: {character_name}")
            self.selected_character = selected_character

            # Fetch character ID if missing
            if 'id' not in self.selected_character:
                connection = sqlite3.connect(DB_PATH)
                cursor = connection.cursor()
                try:
                    cursor.execute("SELECT id FROM characters WHERE name = ?", (character_name,))
                    character_row = cursor.fetchone()
                    if character_row:
                        self.selected_character['id'] = character_row[0]
                        logging.debug(f"Character '{character_name}' ID set to {self.selected_character['id']}.")
                    else:
                        logging.error(f"Character '{character_name}' not found in characters table.")
                except sqlite3.Error as e:
                    logging.error(f"Failed to retrieve character_id for '{character_name}': {e}")
                finally:
                    connection.close()

            # Save last active character
            if 'id' in self.selected_character:
                self.save_last_active_character(self.selected_character['id'])
            else:
                logging.error(f"Cannot save last active character: ID missing for '{character_name}'.")

            # Logout current character and login the selected one
            self.logout_current_character()
            QTimer.singleShot(1000, self.login_selected_character)
        else:
            logging.error(f"Character '{character_name}' selection failed.")

    def logout_current_character(self):
        """
        Logout the current character by navigating to the logout URL.
        """
        logging.debug("Logging out current character.")
        self.website_frame.setUrl(QUrl('https://quiz.ravenblack.net/blood.pl?action=logout'))
        QTimer.singleShot(1000, self.login_selected_character)

    def login_selected_character(self):
        """Log in the selected character using JavaScript."""
        if not self.selected_character:
            logging.warning("No character selected for login.")
            return
        logging.debug(f"Logging in character: {self.selected_character['name']} with ID: {self.selected_character.get('id')}")
        name = self.selected_character['name']
        password = self.selected_character['password']
        login_script = f"""
            var loginForm = document.querySelector('form');
            if (loginForm) {{
                loginForm.iam.value = '{name}';
                loginForm.passwd.value = '{password}';
                loginForm.submit();
            }} else {{
                console.error('Login form not found.');
            }}
        """
        self.website_frame.page().runJavaScript(login_script)

    def firstrun_character_creation(self):
        """
        Handles the first-run character creation, saving the character in plaintext,
        initializing default coin values in the coins table, and setting this character as the last active.
        """
        logging.debug("First-run character creation.")
        dialog = CharacterDialog(self)

        if dialog.exec():
            name = dialog.name_edit.text()
            password = dialog.password_edit.text()
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('INSERT INTO characters (name, password) VALUES (?, ?)', (name, password))
                    character_id = cursor.lastrowid
                    cursor.execute('INSERT INTO coins (character_id, pocket, bank) VALUES (?, 0, 0)', (character_id,))
                    conn.commit()
                    self.save_last_active_character(character_id)
                    self.characters.append({'name': name, 'password': password, 'id': character_id})
                    self.character_list.addItem(QListWidgetItem(name))
                    logging.debug(f"Character '{name}' created with initial coin values and set as last active.")
                except sqlite3.Error as e:
                    logging.error(f"Failed to create character '{name}': {e}")
                    QMessageBox.critical(self, "Error", f"Failed to create character: {e}")
        else:
            sys.exit("No characters added. Exiting the application.")

    def add_new_character(self):
        """
        Add a new character to the list, saving the password in plaintext,
        initializing default coin values in the coins table, and setting this character as the last active.
        """
        logging.debug("Adding a new character.")
        dialog = CharacterDialog(self)

        if dialog.exec():
            name = dialog.name_edit.text()
            password = dialog.password_edit.text()
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('INSERT INTO characters (name, password) VALUES (?, ?)', (name, password))
                    character_id = cursor.lastrowid
                    cursor.execute('INSERT INTO coins (character_id, pocket, bank) VALUES (?, 0, 0)', (character_id,))
                    conn.commit()
                    self.save_last_active_character(character_id)
                    self.characters.append({'name': name, 'password': password, 'id': character_id})
                    self.character_list.addItem(QListWidgetItem(name))
                    logging.debug(f"Character '{name}' added with initial coin values and set as last active.")
                except sqlite3.Error as e:
                    logging.error(f"Failed to add character '{name}': {e}")
                    QMessageBox.critical(self, "Error", f"Failed to add character: {e}")

    def modify_character(self):
        """
        Modify the selected character's details, saving the new password in plaintext.
        """
        current_item = self.character_list.currentItem()
        if current_item is None:
            logging.warning("No character selected for modification.")
            return

        name = current_item.text()
        character = next((char for char in self.characters if char['name'] == name), None)
        if character:
            logging.debug(f"Modifying character: {name}")
            dialog = CharacterDialog(self, character)
            if dialog.exec():
                character['name'] = dialog.name_edit.text()
                character['password'] = dialog.password_edit.text()
                self.selected_character = character  # Sync selected_character with modified data
                self.save_characters()
                current_item.setText(character['name'])
                logging.debug(f"Character {name} modified.")

    def delete_character(self):
        """Delete the selected character from the list."""
        current_item = self.character_list.currentItem()
        if current_item is None:
            logging.warning("No character selected for deletion.")
            return

        name = current_item.text()
        self.characters = [char for char in self.characters if char['name'] != name]
        self.save_characters()
        self.character_list.takeItem(self.character_list.row(current_item))
        logging.debug(f"Character {name} deleted.")

    def save_last_active_character(self, character_id):
        """
        Save the last active character's ID to the last_active_character table.
        Ensures that only one entry exists, replacing any previous entry.
        """
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM last_active_character")
                cursor.execute('INSERT INTO last_active_character (character_id) VALUES (?)', (character_id,))
                conn.commit()
                logging.debug(f"Last active character set to character_id: {character_id}")
            except sqlite3.Error as e:
                logging.error(f"Failed to save last active character: {e}")

    def load_last_active_character(self):
        """
        Load the last active character from the database by character_id, set the selected character,
        and update the UI for auto-login.
        """
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT character_id FROM last_active_character")
                result = cursor.fetchone()
                if result:
                    character_id = result[0]
                    self.selected_character = next((char for char in self.characters if char.get('id') == character_id), None)
                    if self.selected_character:
                        # Sync UI with last active character
                        for i in range(self.character_list.count()):
                            if self.character_list.item(i).text() == self.selected_character['name']:
                                self.character_list.setCurrentRow(i)
                                break
                        logging.debug(f"Last active character loaded and selected: {self.selected_character['name']}")
                        if len(self.characters) > 1:  # Trigger login only if multiple characters exist
                            self.login_needed = True
                            self.website_frame.setUrl(QUrl('https://quiz.ravenblack.net/blood.pl'))
                    else:
                        logging.warning(f"Last active character ID '{character_id}' not found in character list.")
                        self.set_default_character()
                else:
                    logging.warning("No last active character found in the database.")
                    self.set_default_character()
        except sqlite3.Error as e:
            logging.error(f"Failed to load last active character from database: {e}")
            self.set_default_character()

    def set_default_character(self):
        """
        Set the first character in the database as the default selected character,
        update the UI, and save it as the last active character.
        """
        if self.characters:
            self.selected_character = self.characters[0]
            self.character_list.setCurrentRow(0)
            logging.debug(f"No valid last active character; defaulting to: {self.selected_character['name']}")
            self.save_last_active_character(self.selected_character['id'])
            self.login_needed = True
            self.website_frame.setUrl(QUrl('https://quiz.ravenblack.net/blood.pl'))
        else:
            self.selected_character = None
            logging.warning("No characters available to set as default.")
