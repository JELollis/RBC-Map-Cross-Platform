#!/usr/bin/env python3
# Filename: constants.py

"""
RBCMap Constants and Configuration

Defines application-wide constants and helper functions used for
environment setup, logging, theming defaults, and file path resolution.

See LICENSE for usage restrictions.
"""

import logging
import logging.handlers
# -----------------------
# Global Constants
# -----------------------
# Database Path
DB_PATH = 'sessions/rbc_map_data.db'

# Logging Configuration
LOG_DIR = 'logs'
DEFAULT_LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
def get_logging_level_from_db(default=logging.INFO) -> int:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT setting_value FROM settings WHERE setting_name = 'log_level'")
            row = cursor.fetchone()
            if row:
                return int(row[0])
    except Exception as e:
        print(f"Failed to load log level from DB: {e}", file=sys.stderr)
    return default

VERSION_NUMBER = "0.12.0"

# Keybinding Defaults
DEFAULT_KEYBINDS = {
    "move_up": "W",
    "move_down": "S",
    "move_left": "A",
    "move_right": "D",
    "zoom_in": "PageUp",
    "zoom_out": "PageDown",
}

# Required Directories
REQUIRED_DIRECTORIES = ['logs', 'sessions', 'images']



# -----------------------
# Imports Handling
# -----------------------

import math
import os
import subprocess
import sys

# List of required modules with pip package names (some differ from import names)
required_modules = {
    'requests': 'requests',
    're': 're',  # Built-in, no pip install needed
    'time': 'time',  # Built-in
    'sqlite3': 'sqlite3',  # Built-in
    'webbrowser': 'webbrowser',  # Built-in
    'datetime': 'datetime',  # Built-in
    'bs4': 'beautifulsoup4',
    'PySide6.QtWidgets': 'PySide6',
    'PySide6.QtGui': 'PySide6',
    'PySide6.QtCore': 'PySide6',
    'PySide6.QtWebEngineWidgets': 'PySide6',
    'PySide6.QtWebChannel': 'PySide6',
    'PySide6.QtNetwork': 'PySide6'
}

def check_and_install_modules(modules: dict[str, str]) -> bool:
    """
    Check if required modules are installed, prompt user to install missing ones, and attempt installation.

    Args:
        modules (dict): Dictionary mapping module names to their pip package names.

    Returns:
        bool: True if all modules are available after checking/installing, False otherwise.
    """
    missing_modules = []
    pip_installable = []

    # Check each module
    for module, pip_name in modules.items():
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
            if pip_name not in ('re', 'time', 'sqlite3', 'webbrowser', 'datetime'):  # Skip built-ins
                pip_installable.append(pip_name)

    if not missing_modules:
        return True

    # Inform user of missing modules
    print("The following modules are missing:")
    for mod in missing_modules:
        print(f"- {mod}")

    if not pip_installable:
        print("All missing modules are built-ins that should come with Python. Please check your Python installation.")
        return False

    # Prompt user for installation
    try:
        from PySide6.QtWidgets import QMessageBox  # Early import for GUI prompt
    except ImportError:
        # Fallback to console prompt if PySide6 isn't available yet
        response = input(f"\nWould you like to install missing modules ({', '.join(set(pip_installable))}) with pip? (y/n): ").strip().lower()
        if response != 'y':
            print("Please install the missing modules manually with:")
            print(f"pip install {' '.join(set(pip_installable))}")
            return False
    else:
        # Use GUI prompt if PySide6 is partially available
        app = QApplication(sys.argv)  # Minimal app for QMessageBox
        response = QMessageBox.question(None, "Missing Modules",f"Missing modules: {', '.join(missing_modules)}\n\nInstall with pip ({', '.join(set(pip_installable))})?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.No:
            print("Please install the missing modules manually with:")
            print(f"pip install {' '.join(set(pip_installable))}")
            return False

    # Attempt to install missing modules
    print(f"Installing missing modules: {', '.join(set(pip_installable))}...")
    try:
        # Use sys.executable to ensure the correct Python environment
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + list(set(pip_installable)))
        print("Installation successful! Please restart the application.")

        # Re-check modules after installation
        for module in missing_modules:
            try:
                __import__(module)
            except ImportError:
                print(f"Failed to import {module} even after installation. Please check your environment.")
                return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install modules: {e}")
        print("Please install them manually with:")
        print(f"pip install {' '.join(set(pip_installable))}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during installation: {e}")
        return False

# Check and attempt to install required modules
if not check_and_install_modules(required_modules):
    sys.exit("Missing required modules. Please resolve the issues and try again.")

# Proceed with the rest of the imports and program setup
import requests
import re
import webbrowser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QComboBox, \
    QLabel, QFrame, QSizePolicy, QLineEdit, QDialog, QFormLayout, QListWidget, QListWidgetItem, QFileDialog, \
    QColorDialog, QTabWidget, QScrollArea, QTableWidget, QTableWidgetItem, QInputDialog, QTextEdit, QSplashScreen, \
    QCompleter, QCheckBox, QGroupBox, QMenu
from PySide6.QtGui import QPixmap, QPainter, QColor, QFontMetrics, QPen, QIcon, QAction, QIntValidator, QMouseEvent, \
    QShortcut, QKeySequence, QDesktopServices
from PySide6.QtCore import QUrl, Qt, QRect, QEasingCurve, QPropertyAnimation, QSize, QTimer, QDateTime, QMimeData
from PySide6.QtCore import Slot as pyqtSlot
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
from PySide6.QtNetwork import QNetworkCookie
from typing import List, Tuple
from collections.abc import KeysView
import sqlite3

# -----------------------
# Define App Icon
# -----------------------

APP_ICON = None

# -----------------------
# Startup Splash
# -----------------------

class SplashScreen(QSplashScreen):
    def __init__(self, image_path, max_height=400):
        if not os.path.exists(image_path):
            logging.error(f"Image not found: {image_path}")
            pixmap = QPixmap(300, 200)
            pixmap.fill(Qt.black)
        else:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                logging.error(f"Failed to load image: {image_path}")
                pixmap = QPixmap(300, 200)
                pixmap.fill(Qt.black)
            else:
                # Scale pixmap to max_height, preserving aspect ratio
                if pixmap.height() > max_height:
                    pixmap = pixmap.scaledToHeight(max_height, Qt.SmoothTransformation)
        super().__init__(pixmap, Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def show_message(self, message):
        self.showMessage(f"Startup script: {message} loading...", Qt.AlignBottom | Qt.AlignHCenter, Qt.white)
        QApplication.processEvents()

# -----------------------
# Directory Setup
# -----------------------

# Constants defined at the top of the file (or in a constants section)
def ensure_directories_exist(directories: list[str] = REQUIRED_DIRECTORIES) -> bool:
    """
    Ensure that the required directories exist, creating them if necessary.

    This function verifies the presence of essential directories for the application's operation.
    If any are missing, they are created in the current working directory. The default directories are:
    - logs: Stores application log files.
    - sessions: Stores session-related data (e.g., user sessions, cookies).
    - images: Stores image files (e.g., icons, UI assets).

    Args:
        directories (list[str], optional): List of directory names to ensure. Defaults to REQUIRED_DIRECTORIES.

    Returns:
        bool: True if all directories exist or were created successfully, False if an error occurred.

    Raises:
        OSError: If a directory cannot be created due to permissions or other system issues (logged and handled).
    """
    success = True
    for directory in directories:
        try:
            # Check existence first to avoid unnecessary syscalls
            if not os.path.isdir(directory):
                os.makedirs(directory, exist_ok=True)
                logging.debug(f"Created directory: {directory}")
            else:
                logging.debug(f"Directory already exists: {directory}")
        except OSError as e:
            logging.error(f"Failed to create directory '{directory}': {e}")
            success = False
    return success

# Example usage at startup (optional, depending on your flow)
if not ensure_directories_exist():
    logging.warning("Some directories could not be created. Application may encounter issues.")

# -----------------------
# Logging Setup
# -----------------------
def setup_logging(log_dir: str = LOG_DIR, log_level: int = DEFAULT_LOG_LEVEL, log_format: str = LOG_FORMAT) -> bool:
    """
    Set up logging configuration to save logs in the specified directory with daily rotation.

    Configures the root logger to write logs to a file named 'rbc_YYYY-MM-DD.log' in the given directory.
    Logs are appended to the file for the current day, effectively rotating daily by filename.

    Args:
        log_dir (str, optional): Directory to store log files. Defaults to LOG_DIR ('logs').
        log_level (int, optional): Logging level (e.g., logging.debug). Defaults to LOG_LEVEL.
        log_format (str, optional): Log message format. Defaults to LOG_FORMAT.

    Returns:
        bool: True if logging was set up successfully, False if an error occurred.

    Raises:
        OSError: If the log file cannot be created or written to (logged to stderr if possible).
    """
    try:
        # Ensure log directory exists (assuming ensure_directories_exist is called earlier)
        log_filename = datetime.now().strftime(f'{log_dir}/rbc_%Y-%m-%d.log')

        # Clear any existing handlers to avoid duplication if called multiple times
        logger = logging.getLogger()
        if logger.handlers:
            logger.handlers.clear()

        # Set up file handler
        handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
        handler.setFormatter(logging.Formatter(log_format))
        handler.setLevel(log_level)

        # Configure root logger
        logger.setLevel(log_level)
        logger.addHandler(handler)

        logger.info(f"Logging initialized. Logs will be written to {log_filename}")
        return True
    except OSError as e:
        # Log to stderr as a fallback if file logging fails
        print(f"Failed to set up logging to {log_filename}: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error during logging setup: {e}", file=sys.stderr)
        return False

# Initialize logging at startup
if not setup_logging(log_level=get_logging_level_from_db()):
    print("Logging setup failed. Continuing without file logging.", file=sys.stderr)
    logging.basicConfig(level=DEFAULT_LOG_LEVEL, format=LOG_FORMAT, stream=sys.stderr)  # Fallback to console

# Log app version
logging.info(f"Launching app version {VERSION_NUMBER}")

def save_logging_level_to_db(level: int) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO settings (setting_name, setting_value)
                VALUES (?, ?)
                ON CONFLICT(setting_name) DO UPDATE SET setting_value=excluded.setting_value
            """, ('log_level', str(level)))
            conn.commit()
            logging.info(f"Log level updated to {logging.getLevelName(level)} in settings")
            return True
    except Exception as e:
        logging.error(f"Failed to save log level: {e}")
        return False


# -----------------------
# Webview Cookie Database
# -----------------------

def save_cookie_to_db(cookie: QNetworkCookie) -> bool:
    """
    Save or update a single cookie in the SQLite database, overwriting if it exists.

    Args:
        cookie (QNetworkCookie): The cookie to save or update.

    Returns:
        bool: True if the cookie was saved/updated successfully, False otherwise.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            name = cookie.name().data().decode('utf-8', errors='replace')
            domain = cookie.domain()
            path = cookie.path()
            value = cookie.value().data().decode('utf-8', errors='replace')
            expiration = cookie.expirationDate().toString(Qt.ISODate) if not cookie.isSessionCookie() else None
            secure = int(cookie.isSecure())
            httponly = int(cookie.isHttpOnly())

            # Use UPSERT (INSERT OR REPLACE) to overwrite existing cookies based on name, domain, and path
            cursor.execute('''
                INSERT OR REPLACE INTO cookies (name, value, domain, path, expiration, secure, httponly)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, value, domain, path, expiration, secure, httponly))

            conn.commit()
            logging.debug(f"Saved/updated cookie: {name} for domain {domain}")
            return True
    except sqlite3.Error as e:
        logging.error(f"Failed to save/update cookie {cookie.name().data()}: {e}")
        return False

def load_cookies_from_db() -> List[QNetworkCookie]:
    """
    Load all cookies from the SQLite database.

    Returns:
        list[QNetworkCookie]: List of QNetworkCookie objects from the database.
    """
    cookies = []
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, value, domain, path, expiration, secure, httponly FROM cookies')
            for name, value, domain, path, expiration, secure, httponly in cursor.fetchall():
                cookie = QNetworkCookie(
                    name.encode('utf-8'),
                    value.encode('utf-8')
                )
                cookie.setDomain(domain)
                cookie.setPath(path)
                if expiration:
                    cookie.setExpirationDate(QDateTime.fromString(expiration, Qt.ISODate))
                cookie.setSecure(bool(secure))
                cookie.setHttpOnly(bool(httponly))
                cookies.append(cookie)
            logging.debug(f"Loaded {len(cookies)} cookies from database")
    except sqlite3.Error as e:
        logging.error(f"Failed to load cookies: {e}")
    return cookies

def clear_cookie_db() -> bool:
    """
    Clear all cookies from the SQLite database.

    Returns:
        bool: True if cookies were cleared successfully, False otherwise.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cookies')
            conn.commit()
            logging.info("Cleared all cookies from database")
            return True
    except sqlite3.Error as e:
        logging.error(f"Failed to clear cookies: {e}")
        return False

# -----------------------
# Splash Messages Decorator
# -----------------------

def splash_message(splash):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if splash and not splash.isHidden():
                splash.show_message(func.__name__)  # Show the original method name
            return func(self, *args, **kwargs)
        wrapper.__name__ = func.__name__  # Preserve the original method name
        return wrapper
    return decorator
