    # -----------------------
    # Cookie Handling
    # -----------------------

    def setup_cookie_handling(self) -> None:
        """
        Set up cookie handling by connecting the QWebEngineProfile's cookie store and loading saved cookies.
        """
        self.cookie_store = self.web_profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.on_cookie_added)
        self.load_cookies()
        logging.debug("Cookie handling initialized")

    def load_cookies(self) -> None:
        """
        Load cookies from the 'cookies' table and inject them into the QWebEngineProfile.
        """
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, domain, path, value, expiration, secure, httponly FROM cookies")
                cookies = cursor.fetchall()

                for name, domain, path, value, expiration, secure, httponly in cookies:
                    cookie = QNetworkCookie(name.encode('utf-8'), value.encode('utf-8'))
                    cookie.setDomain(domain)
                    cookie.setPath(path)
                    cookie.setSecure(bool(secure))
                    cookie.setHttpOnly(bool(httponly))
                    if expiration:
                        try:
                            # Handle both string (ISO) and int (epoch) expiration formats
                            if isinstance(expiration, str):
                                cookie.setExpirationDate(QDateTime.fromString(expiration, Qt.ISODate))
                            elif isinstance(expiration, int):
                                cookie.setExpirationDate(QDateTime.fromSecsSinceEpoch(expiration))
                            else:
                                logging.warning(f"Invalid expiration type for cookie '{name}': {type(expiration)}")
                        except ValueError as e:
                            logging.warning(f"Failed to parse expiration '{expiration}' for cookie '{name}': {e}")
                    self.cookie_store.setCookie(cookie, QUrl(f"https://{domain}"))
                logging.debug(f"Loaded {len(cookies)} cookies from database")
        except sqlite3.Error as e:
            logging.error(f"Failed to load cookies: {e}")

    def on_cookie_added(self, cookie: QNetworkCookie) -> None:
        name = bytes(cookie.name()).decode()
        value = bytes(cookie.value()).decode()
        domain = cookie.domain().lstrip('.')  # Normalize domain

        # Only process quiz.ravenblack.net
        if domain != 'quiz.ravenblack.net':
            return

        # Skip high-churn cookies
        if name in ['ip', 'stamp']:
            return

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM cookies WHERE name = ? AND domain = ?", (name, domain))
                row = cursor.fetchone()

                if not row or row[0] != value:
                    cursor.execute(
                        "REPLACE INTO cookies (name, value, domain, path, secure, httponly) VALUES (?, ?, ?, ?, ?, ?)",
                        (name, value, domain, cookie.path(), int(cookie.isSecure()), int(cookie.isHttpOnly()))
                    )
                    conn.commit()
                    logging.debug(f"Cookie '{name}' updated for domain '{domain}'")
        except Exception as e:
                logging.error(f"Error updating cookie '{name}': {e}")
