# -----------------------
# AVITD Scraper Class
# -----------------------
class AVITDScraper:
    """
    A scraper class for 'A View in the Dark' to update guilds and shops data in the SQLite database.
    """

    def __init__(self):
        """
        Initialize the scraper with the required headers and database connection.
        """
        self.url = "https://aviewinthedark.net/"
        self.connection = sqlite3.connect(DB_PATH)  # SQLite connection
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        # Set up logging
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("AVITDScraper initialized.")

    def scrape_guilds_and_shops(self):
        """
        Scrape the guilds and shops data from the website and update the SQLite database.
        """
        logging.info("Starting to scrape guilds and shops.")
        response = requests.get(self.url, headers=self.headers)
        logging.debug(f"Received response: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        guilds = self.scrape_section(soup, "the guilds")
        shops = self.scrape_section(soup, "the shops")
        guilds_next_update = self.extract_next_update_time(soup, 'Guilds')
        shops_next_update = self.extract_next_update_time(soup, 'Shops')

        # Display results in the console (for debugging purposes)
        self.display_results(guilds, shops, guilds_next_update, shops_next_update)

        # Update the SQLite database with scraped data
        self.update_database(guilds, "guilds", guilds_next_update)
        self.update_database(shops, "shops", shops_next_update)
        logging.info("Finished scraping and updating the database.")

    def scrape_section(self, soup, section_image_alt):
        """
        Scrape a specific section (guilds or shops) from the website.

        Args:
            soup (BeautifulSoup): Parsed HTML content.
            section_image_alt (str): The alt text of the section image to locate the section.

        Returns:
            list: A list of tuples containing the name, column, and row of each entry.
        """
        logging.debug(f"Scraping section: {section_image_alt}")
        data = []
        section_image = soup.find('img', alt=section_image_alt)
        if not section_image:
            logging.warning(f"No data found for {section_image_alt}.")
            return data

        table = section_image.find_next('table')
        rows = table.find_all('tr', class_=['odd', 'even'])

        for row in rows:
            columns = row.find_all('td')
            if len(columns) < 2:
                logging.debug(f"Skipping row due to insufficient columns: {row}")
                continue

            name = columns[0].text.strip()
            location = columns[1].text.strip().replace("SE of ", "").strip()

            try:
                column, row = location.split(" and ")
                data.append((name, column, row))
                logging.debug(f"Extracted data - Name: {name}, Column: {column}, Row: {row}")
            except ValueError:
                logging.warning(f"Location format unexpected for {name}: {location}")

        logging.info(f"Scraped {len(data)} entries from {section_image_alt}.")
        return data

    def extract_next_update_time(self, soup, section_name):
        """
        Extract the next update time for a specific section (guilds or shops).

        Args:
            soup (BeautifulSoup): Parsed HTML content.
            section_name (str): The name of the section (e.g., 'Guilds', 'Shops').

        Returns:
            str: The next update time in 'YYYY-MM-DD HH:MM:SS' format or 'NA' if not found.
        """
        logging.debug(f"Extracting next update time for section: {section_name}")

        # Find all divs with the 'next_change' class
        section_divs = soup.find_all('div', class_='next_change')

        # Iterate through the divs to find the matching section
        for div in section_divs:
            if section_name in div.text:
                # Search for the time pattern
                match = re.search(r'(\d+)\s+days?,\s+(\d+)h\s+(\d+)m\s+(\d+)s', div.text)
                if match:
                    # Parse time components
                    days = int(match.group(1))
                    hours = int(match.group(2))
                    minutes = int(match.group(3))
                    seconds = int(match.group(4))

                    # Calculate the next update time
                    next_update = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
                    logging.debug(f"Next update time for {section_name}: {next_update}")

                    # Return the formatted date-time string
                    return next_update.strftime('%Y-%m-%d %H:%M:%S')

        # Return 'NA' if no match is found
        logging.warning(f"No next update time found for {section_name}.")
        return 'NA'

    def display_results(self, guilds, shops, guilds_next_update, shops_next_update):
        """
        Display the results of the scraping in the console for debugging purposes.

        Args:
            guilds (list): List of scraped guild data.
            shops (list): List of scraped shop data.
            guilds_next_update (str): The next update time for guilds.
            shops_next_update (str): The next update time for shops.
        """
        logging.info(f"Guilds Next Update: {guilds_next_update}")
        logging.info(f"Shops Next Update: {shops_next_update}")

        logging.info("Guilds Data:")
        for guild in guilds:
            logging.info(f"Name: {guild[0]}, Column: {guild[1]}, Row: {guild[2]}")

        logging.info("Shops Data:")
        for shop in shops:
            logging.info(f"Name: {shop[0]}, Column: {shop[1]}, Row: {shop[2]}")

    def update_database(self, data, table, next_update):
        """
        Update the SQLite database with the scraped data.

        Args:
            data (list): List of tuples containing the name, column, and row of each entry.
            table (str): The table name ('guilds' or 'shops') to update.
            next_update (str): The next update time to be stored in the database.
        """
        if not self.connection:
            logging.error("Failed to connect to the database.")
            return

        cursor = self.connection.cursor()

        # Step 1: Set all entries' Row and Column to 'NA', except Peacekeeper's Missions for guilds
        try:
            logging.debug(
                f"Setting all {table} entries' Row and Column to 'NA', except Peacekeeper's Missions for guilds.")
            if table == "guilds":
                cursor.execute(f"""
                    UPDATE {table}
                    SET `Column`='NA', `Row`='NA', `next_update`=?
                    WHERE Name NOT LIKE 'Peacekeepers Mission%'
                """, (next_update,))
            else:  # If updating 'shops', clear all without exception
                cursor.execute(f"""
                    UPDATE {table}
                    SET `Column`='NA', `Row`='NA', `next_update`=?
                """, (next_update,))
        except sqlite3.Error as e:
            logging.error(f"Failed to reset {table} entries to 'NA': {e}")
            return

        # Step 2: Insert or update entries, excluding Peacekeeper's Missions in shops
        for name, column, row in data:
            if table == "shops" and "Peacekeepers Mission" in name:
                logging.warning(f"Skipping {name} as it belongs in guilds, not shops.")
                continue  # Skip Peacekeeper's Missions when updating shops

            try:
                logging.debug(
                    f"Updating {table} entry: Name={name}, Column={column}, Row={row}, Next Update={next_update}")
                cursor.execute(f"""
                    INSERT INTO {table} (Name, `Column`, `Row`, `next_update`)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(Name) DO UPDATE SET
                        `Column`=excluded.`Column`,
                        `Row`=excluded.`Row`,
                        `next_update`=excluded.`next_update`
                """, (name, column, row, next_update))
            except sqlite3.Error as e:
                logging.error(f"Failed to update {table} entry '{name}': {e}")

        # Step 3: Ensure Peacekeeper’s Missions Always Remain in Guilds Table Only
        if table == "guilds":
            try:
                logging.debug("Ensuring Peacekeeper's Mission locations remain constant in guilds table.")
                cursor.executemany("""
                    INSERT INTO guilds (Name, `Column`, `Row`, `next_update`)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(Name) DO UPDATE SET
                        `Column`=excluded.`Column`,
                        `Row`=excluded.`Row`,
                        `next_update`=excluded.`next_update`
                """, [
                    ("Peacekeepers Mission 1", "Emerald", "67th", next_update),
                    ("Peacekeepers Mission 2", "Unicorn", "33rd", next_update),
                    ("Peacekeepers Mission 3", "Emerald", "33rd", next_update),
                ])
            except sqlite3.Error as e:
                logging.error(f"Failed to persist Peacekeeper's Missions in guilds: {e}")

        self.connection.commit()
        cursor.close()
        logging.info(f"Database updated for {table}.")

    def close_connection(self):
        """
        Close the SQLite database connection.
        """
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed.")
