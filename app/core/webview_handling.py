    # -----------------------
    # Web View Handling
    # -----------------------

    def refresh_webview(self):
        """Refresh the webview content."""
        self.website_frame.reload()

    def apply_custom_css(self, css: str):
        cursor = sqlite3.connect(DB_PATH).cursor()
        cursor.execute("SELECT element, value FROM custom_css WHERE profile_name = ?", (self.current_css_profile,))
        css_rules = cursor.fetchall()

        if not css_rules:
            logging.warning(f"No CSS rules found for profile '{self.current_css_profile}'")
            return

        css = ""
        for element, value in css_rules:
            css += f"{element} {{{value}}}\n"

        script = f"""
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `{css}`;
            document.head.appendChild(style);
        """
        self.website_frame.page().runJavaScript(script)

    def on_webview_load_finished(self, success):
        if not success:
            logging.error("Failed to load the webpage.")
            QMessageBox.critical(self, "Error", "Failed to load the webpage. Check your network or try again.")
        else:
            logging.info("Webpage loaded successfully.")
            self.website_frame.page().toHtml(self.process_html)
            css = self.load_current_css()
            self.apply_custom_css(css)
            if self.login_needed:
                logging.debug("Logging in last active character.")
                self.login_selected_character()
                self.login_needed = False

    def process_html(self, html):
        """
        Process the HTML content of the webview to extract coordinates and coin information.

        Args:
            html (str): The HTML content of the page as a string.

        This method calls both the extract_coordinates_from_html and extract_coins_from_html methods.
        """
        try:
            # Extract coordinates for the minimap
            x_coord, y_coord = self.extract_coordinates_from_html(html)
            if x_coord is not None and y_coord is not None:
                # Set character coordinates directly
                self.character_x, self.character_y = x_coord, y_coord
                logging.debug(f"Set character coordinates to x={self.character_x}, y={self.character_y}")

                # Call recenter_minimap to update the minimap based on character's position
                self.recenter_minimap()

            # Call the method to extract bank coins and pocket changes from the HTML
            self.extract_coins_from_html(html)
            logging.debug("HTML processed successfully for coordinates and coin count.")
        except Exception as e:
            logging.error(f"Unexpected error in process_html: {e}")

    def extract_coordinates_from_html(self, html):

        soup = BeautifulSoup(html, 'html.parser')
        # logging.debug("Extracting coordinates from HTML...")

        # Try to extract the intersection label (like "Aardvark and 1st")
        intersect_span = soup.find('span', class_='intersect')
        text = intersect_span.text.strip() if intersect_span else ""
        # logging.debug(f"Intersection label found: {text}")

        # Check for city limits
        city_limit_cells = soup.find_all('td', class_='cityblock')

        # Extract coordinate inputs
        inputs = soup.find_all('input')
        x_vals = [int(inp['value']) for inp in inputs if
                  inp.get('name') == 'x' and inp.get('value') and inp['value'].isdigit()]
        y_vals = [int(inp['value']) for inp in inputs if
                  inp.get('name') == 'y' and inp.get('value') and inp['value'].isdigit()]
        last_x = max(x_vals) if x_vals else None
        last_y = max(y_vals) if y_vals else None

        # Get the first x/y (center of grid)
        first_x_input = soup.find('input', {'name': 'x'})
        first_y_input = soup.find('input', {'name': 'y'})
        first_x = int(first_x_input['value']) if first_x_input else None
        first_y = int(first_y_input['value']) if first_y_input else None

        logging.debug(f"First detected coordinate: x={first_x}, y={first_y}")
        logging.debug(f"Last detected coordinate: x={last_x}, y={last_y}")

        if city_limit_cells:
            logging.debug(f"Found {len(city_limit_cells)} city limit blocks.")

            # Check for first available coordinates
            first_x_input = soup.find('input', {'name': 'x'})
            first_y_input = soup.find('input', {'name': 'y'})

            first_x = int(first_x_input['value']) if first_x_input else None
            first_y = int(first_y_input['value']) if first_y_input else None

            logging.debug(f"First detected coordinate: x={first_x}, y={first_y}")

            if self.zoom_level == 3:
                if text == "Aardvark and 1st" and len(city_limit_cells) == 5:
                    logging.debug("Top-left corner detected with full border row: Aardvark and 1st")
                    return -1, -1

                if text == "Zestless and 1st" and len(city_limit_cells) == 5:
                    logging.debug("Top-right corner detected: Zestless and 1st")
                    return 198, -1

                if text == "Aardvark and 100th" and len(city_limit_cells) == 5:
                    logging.debug("Bottom-left corner detected: Aardvark and 100th")
                    return -1, 198

                if text == "Zestless and 100th" and len(city_limit_cells) == 5:
                    logging.debug("Bottom-right corner detected: Zestless and 100th")
                    return 198, 198

                # Adjust for Aardvark and NCL
                if len(city_limit_cells) == 3 and first_y == 0 and first_x == 0 and last_x == 2 and last_y == 1:
                    logging.debug(f"Detected Cell 0,1.")
                    return 0, -1

                # Adjust for WCL and 1st (0,1)
                if len(city_limit_cells) == 3 and first_y == 0 and first_x == 0:
                    logging.debug(f"Detected Cell 0,1.")
                    return -1, 0

                # Adjust for ON Zestless and 1st (198,1)
                if len(city_limit_cells) == 3 and first_x == 198 and first_y == 0:
                    logging.debug("Detected special case: on Zestless and 1st")
                    return first_x, first_y

                # Adjust for Northern Edge (Y=0)
                if len(city_limit_cells) == 3 and first_y == 0:
                    logging.debug(f"Detected Northern City Limit at y={first_y}")
                    return first_x, -1

                # Adjust for Western Edge (X=0)
                if len(city_limit_cells) == 3 and first_x == 0:
                    logging.debug(f"Detected Western City Limit at x={first_x}")
                    return -1, first_y

                # If no adjustments, return detected values
                return first_x, first_y

            if self.zoom_level == 5:
                if text == "Aardvark and 1st" and len(city_limit_cells) == 5:
                    logging.debug("Top-left corner detected with full border row: Aardvark and 1st")
                    return -2, -2

                if text == "Zestless and 1st" and len(city_limit_cells) == 5:
                    logging.debug("Top-right corner detected: Zestless and 1st")
                    return 197, -2

                if text == "Aardvark and 100th" and len(city_limit_cells) == 5:
                    logging.debug("Bottom-left corner detected: Aardvark and 100th")
                    return -2, 197

                if text == "Zestless and 100th" and len(city_limit_cells) == 5:
                    logging.debug("Bottom-right corner detected: Zestless and 100th")
                    return 197, 197

                # Adjust for Aardvark and NCL (1,0)
                if len(city_limit_cells) == 3 and first_y == 0 and first_x == 0 and last_x == 2 and last_y == 1:
                    logging.debug(f"Detected Cell 1,0.")
                    return -1, -2

                # Adjust for WCL and 1st (0,1)
                if len(city_limit_cells) == 3 and first_y == 0 and first_x == 0:
                    logging.debug(f"Detected Cell 0,1.")
                    return -2, -1

                # Adjust for ON Zestless and 1st (198,1)
                if len(city_limit_cells) == 3 and first_x == 198 and first_y == 0:
                    logging.debug("Detected special case: on Zestless and 1st")
                    return first_x - 1, first_y - 1

                # Adjust for Northern Edge (Y=0)
                if len(city_limit_cells) == 3 and first_y == 0:
                    logging.debug(f"Detected Northern City Limit at y={first_y}")
                    return first_x - 1, -2

                # Adjust for Western Edge (X=0)
                if len(city_limit_cells) == 3 and first_x == 0:
                    logging.debug(f"Detected Western City Limit at x={first_x}")
                    return -2, first_y - 1

                return first_x - 1, first_y - 1

            if self.zoom_level == 7:
                if text == "Aardvark and 1st" and len(city_limit_cells) == 5:
                    logging.debug("Top-left corner detected with full border row: Aardvark and 1st")
                    return -3, -3

                if text == "Zestless and 1st" and len(city_limit_cells) == 5:
                    logging.debug("Top-right corner detected: Zestless and 1st")
                    return 196, -3

                if text == "Aardvark and 100th" and len(city_limit_cells) == 5:
                    logging.debug("Bottom-left corner detected: Aardvark and 100th")
                    return -3, 196

                if text == "Zestless and 100th" and len(city_limit_cells) == 5:
                    logging.debug("Bottom-right corner detected: Zestless and 100th")
                    return 196, 196

                # Adjust for Aardvark and NCL (1,0)
                if len(city_limit_cells) == 3 and first_y == 0 and first_x == 0 and last_x == 2 and last_y == 1:
                    logging.debug(f"Detected Cell 1,0.")
                    return -2, -3

                # Adjust for WCL and 1st (0,1)
                if len(city_limit_cells) == 3 and first_y == 0 and first_x == 0:
                    logging.debug(f"Detected Cell 0,1.")
                    return -3, -2

                # Adjust for ON Zestless and 1st (198,1)
                if len(city_limit_cells) == 3 and first_x == 198 and first_y == 0:
                    logging.debug("Detected special case: on Zestless and 1st")
                    return first_x - 2, first_y - 2

                # Adjust for Northern Edge (Y=0)
                if len(city_limit_cells) == 3 and first_y == 0:
                    logging.debug(f"Detected Northern City Limit at y={first_y}")
                    return first_x - 2, -3

                # Adjust for Western Edge (X=0)
                if len(city_limit_cells) == 3 and first_x == 0:
                    logging.debug(f"Detected Western City Limit at x={first_x}")
                    return -3, first_y - 2

                return first_x - 2, first_y - 2

        logging.debug(f"Safe Fallback: x={first_x}, y={first_y}")
        return first_x, first_y

    def extract_coins_from_html(self, html):
        """
        Extract bank coins, pocket coins, and handle coin-related actions such as deposits,
        withdrawals, transit handling, and coins gained from hunting or stealing.

        Args:
            html (str): The HTML content as a string.

        This method searches for bank balance, deposits, withdrawals, hunting, robbing, receiving,
        and transit coin actions in the HTML content, updating both bank and pocket coins in the
        SQLite database based on character_id.
        """
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            character_id = self.selected_character['id']
            updates = []

            bank_match = re.search(r"Welcome to Omnibank. Your account has (\d+) coins in it.", html)
            if bank_match:
                bank_coins = int(bank_match.group(1))
                logging.info(f"Bank coins found: {bank_coins}")
                updates.append(("UPDATE coins SET bank = ? WHERE character_id = ?", (bank_coins, character_id)))

            pocket_match = re.search(r"You have (\d+) coins", html) or re.search(r"Money: (\d+) coins", html)
            if pocket_match:
                pocket_coins = int(pocket_match.group(1))
                logging.info(f"Pocket coins found: {pocket_coins}")
                updates.append(("UPDATE coins SET pocket = ? WHERE character_id = ?", (pocket_coins, character_id)))

            deposit_match = re.search(r"You deposit (\d+) coins.", html)
            if deposit_match:
                deposit_coins = int(deposit_match.group(1))
                logging.info(f"Deposit found: {deposit_coins} coins")
                updates.append(("UPDATE coins SET pocket = pocket - ? WHERE character_id = ?", (deposit_coins, character_id)))

            withdraw_match = re.search(r"You withdraw (\d+) coins.", html)
            if withdraw_match:
                withdraw_coins = int(withdraw_match.group(1))
                logging.info(f"Withdrawal found: {withdraw_coins} coins")
                updates.append(("UPDATE coins SET pocket = pocket + ? WHERE character_id = ?", (withdraw_coins, character_id)))

            transit_match = re.search(r"It costs 5 coins to ride. You have (\d+).", html)
            if transit_match:
                coins_in_pocket = int(transit_match.group(1))
                logging.info(f"Transit found: Pocket coins updated to {coins_in_pocket}")
                updates.append(("UPDATE coins SET pocket = ? WHERE character_id = ?", (coins_in_pocket, character_id)))

            actions = {
                'hunter': r'You drink the hunter\'s blood.*You also found (\d+) coins',
                'paladin': r'You drink the paladin\'s blood.*You also found (\d+) coins',
                'human': r'You drink the human\'s blood.*You also found (\d+) coins',
                'bag_of_coins': r'The bag contained (\d+) coins',
                'robbing': r'You stole (\d+) coins from (\w+)',
                'silver_suitcase': r'The suitcase contained (\d+) coins',
                'given_coins': r'(\w+) gave you (\d+) coins',
                'getting_robbed': r'(\w+) stole (\d+) coins from you'
            }

            for action, pattern in actions.items():
                match = re.search(pattern, html)
                if match:
                    coin_count = int(match.group(1 if action != 'given_coins' else 2))
                    if action == 'getting_robbed':
                        vamp_name = match.group(1)
                        updates.append(("UPDATE coins SET pocket = pocket - ? WHERE character_id = ?", (coin_count, character_id)))
                        logging.info(f"Lost {coin_count} coins to {vamp_name}.")
                    else:
                        updates.append(("UPDATE coins SET pocket = pocket + ? WHERE character_id = ?", (coin_count, character_id)))
                        logging.info(f"Gained {coin_count} coins from {action}.")
                    break

            for query, params in updates:
                cursor.execute(query, params)
            conn.commit()
            logging.info(f"Updated coins for character ID {character_id}.")

    def switch_css_profile(self, profile_name: str) -> None:
        self.current_css_profile = profile_name
        self.apply_custom_css()
        logging.info(f"Switched to profile: {profile_name} and applied CSS")
