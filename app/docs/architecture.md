# RBC Community Map - Application Architecture

## Overview

RBC Community Map is an interactive mapping tool for players of the text-based browser game **Vampires! The Dark Alleyway**, set in RavenBlack City. It includes minimap navigation, character and destination management, theme and CSS customization, and dynamic data scraping of in-game content.

> This document outlines the **current architecture** and lays a foundation for **modularization** in the upcoming `0.1.0` cross-platform fork.

---

## 1. Project Structure

```
app/
├── config/              # Constants, configuration values, and resource loaders
│   └── constants.py     # Core configuration settings (paths, defaults, settings)
├── database/            # Schema and initialization logic
│   └── schema.py        # SQLite schema, seed data, and data loading
├── ui/                  # GUI components and dialogs
│   ├── main_window.py   # Main application window and event logic
│   ├── dialogs/         # All custom PySide6 dialogs (character, powers, CSS, etc.)
│   └── themes/          # Theme-related UI helpers and color pickers
├── scraping/            # Web scraping engine for AVITD
│   └── avitd_scraper.py # Extracts guild and shop info from "A View in the Dark"
├── tools/               # Utility logic (damage calculator, shopping planner, etc.)
│   └── damage_calc.py   # In-game damage calculation tools
├── assets/              # Images, icons, and default stylesheets
├── logs/                # Application logs
└── main.py              # Entry point to the application
```

---

## 2. Core Components

### 🧠 `Main Application (RBCCommunityMap)`
- Manages the application window, event routing, map rendering, and database interaction.
- Coordinates input handling and calls out to dialogs and tools as needed.

### 🗺️ `Minimap Renderer`
- Extracts player coordinates using HTML parsing.
- Dynamically renders surrounding intersections and overlays banks, taverns, and transit icons.

### 📂 `SQLite Backend`
- Used for persistent storage of characters, destinations, settings, guild/shop locations, and customizations.
- Initialized and seeded with game data on first run.

### 🌐 `AVITDScraper`
- Periodically scrapes data from "A View in the Dark" to refresh in-game location info.
- Uses BeautifulSoup and `requests`.

### 🧰 Dialogs and Utilities
- Modular dialogs for managing characters, themes, CSS, damage calculator, and powers viewer.
- Tools like Shopping List and Damage Calculator use real game data for in-app planning.

---

## 3. Planned Modular Refactor (v0.1.0+)

Future architecture will separate concerns and enable platform-specific backends (e.g., desktop with PySide6 vs. mobile with Kivy):

```
core/                   # Core logic and platform-agnostic utilities
gui/                    # UI implementations (pyside6/, kivy/, etc.)
data/                   # SQLite abstraction layer
features/               # Modular tools (damage calculator, shopping list)
platform/               # Platform utilities (cookies, theming, etc.)
entrypoints/            # main_desktop.py, main_mobile.py, etc.
```

---

## 4. Dependencies

- `PySide6`: Qt-based GUI framework
- `PySide6-WebEngine`: For rendering web content and performing JS injections
- `sqlite3`: Embedded DB engine
- `requests`, `bs4`: For scraping guild/shop data
- `logging`: Log output for debugging and user support

---

## 5. Build and Deployment

The app currently builds into a Windows `.exe` using **NSIS**. Signed builds are managed through **SignPath**. For future cross-platform support, **PyInstaller**, **Buildozer (for Kivy)**, or **Briefcase** may be evaluated.

---

## 6. Developer Notes

- All settings and logs are written to local app data directories.
- Color themes are stored both in the DB and applied at runtime through stylesheets and QColor mappings.
- Map grid logic uses coordinate offsets (+1) to visually center based on player location.

---

_Last updated: April 2025_

