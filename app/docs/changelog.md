### Changelog for RBC City Map Application

### Version 0.11.3

#### Final Polishing & Full System Debug:
- **Coordinate Extraction Overhaul**:
  - Fixed edge cases for **map corners and borders** using full rule-based logic.
  - Added dynamic rules for **zoom-level offsets**, using `first_x`, `first_y`, `last_x`, `last_y`.
- **Coin Scraper Improvements**:
  - Recognizes `Money: X coins` pattern as a valid coin readout.
  - Improved logging of **coin loss/gain events** and updated match rules.
- **Powers Dialog Bug Fixes**:
  - Fixed integer conversion error from non-coordinate strings (e.g., "Tapir").
  - Power info loads properly, and **Set Destination** now triggers cleanly for all entries.
- **Guild/Shop Scraper Working**:
  - `AVITDScraper` now correctly updates rows for all known guild/shop entries.
  - Peacekeeper entries persist regardless of updates.
- **Bug Fixes**:
  - Fixed persistent crash on startup related to cookies table handling.
  - Improved fallback behavior for invalid grid scrapes.
- **Release Ready**:
  - This version is stable and marks a **milestone toward a future public release.**

---

### Version 0.11.2

#### Internal Changes:
- **Refactor Scraper Logic** *(Partial)*:
  - Introduced structural changes to `AVITDScraper` for handling verbose and quiet modes.
  - Implemented early groundwork for **split-mode updates**.
- **Testing & Preparation for 0.11.3**:
  - Updated coin and guild test entries.
  - Logged verbose output for corner-case coordinate scraping.


---

### Version 0.11.1

#### Feature Enhancements:
- **Peacekeeper’s Mission Handling**:
  - Added custom handling of **Peacekeeper’s Missions** in guild logic.
  - Ensured these locations are **preserved and not overwritten** by scraper updates.
- **Power Button Smart Routing**:
  - Introduced logic to always route **Battle Cloak** to the **nearest Peacekeeper’s Mission**.
- **Bug Fixes**:
  - Resolved race condition where **Set Destination button** failed for guilds with partial data.
  - Improved fallback logic for missing street coordinates.

---

### Version 0.11.0

#### Major Enhancements:
- **Complete Powers System**:
  - Added a fully functional **Powers dialog** with power info, quest hints, and Set Destination integration.
- **Set Destination Dialog Refactor**:
  - Improved **destination-setting workflow** with validation and feedback.
- **Expanded Coin Detection**:
  - Upgraded coin extractor to recognize **deposits, withdrawals, stealing**, and **bags of coins**.
- **Database Schema Updates**:
  - Refined structure of `powers`, `guilds`, and `cookies` tables for stability.
- **Bug Fixes & UI Polish**:
  - Fixed broken guild destination routing.
  - Improved Powers dialog alignment and accessibility.

---

### Version 0.10.3

#### Feature Additions:
- **Settings Dialog**:
  - Introduced a dedicated **settings menu** with toggles for startup scraper and verbose logging.
- **Improved Database Handling**:
  - Added logic to **initialize new databases** with default tables on first run.
- **Bug Fixes**:
  - Fixed **duplicate log file entries** on app restart.
  - Improved detection for **first-time setup scenarios**.

---


### Version 0.10.2

#### Feature Enhancements:
- **WASD Movement Support**:
  - Added support for navigating the map using **W, A, S, D** keys for improved movement control.
  - Ensured **keyboard input handling** is consistent across different UI elements.
- **Bug Fixes & Refinements**:
  - Addressed **key input recognition issues** to ensure smoother movement interaction.
  - Fixed **minor UI inconsistencies** with character selection.

---

### Version 0.10.1

#### UI & Performance Improvements:
- **Optimized User Interface**:
  - Adjusted **layout structure** for better usability.
  - Improved **character list management**.
- **Performance Enhancements**:
  - Refined **database query execution** for faster load times.
  - Improved **memory handling** in web scraping operations.
- **Bug Fixes**:
  - Resolved an issue with **incorrect coordinate tracking**.
  - Fixed a **rare crash** related to **destination setting**.

---

### Version 0.10.0 (Public Beta Release)

#### Major System Upgrades:
- **Minimap System Overhaul**:
  - Fully redesigned **zooming and scaling** functionality for better user control.
  - **Nearest POI indicators** now highlight the closest banks, taverns, and transit stations.
- **Character Management Enhancements**:
  - Introduced **multi-character support**, allowing users to manage multiple game accounts.
  - Implemented **secure login handling** with encrypted credentials.
- **Database System Migration**:
  - Moved to a **fully integrated SQLite database** for managing map data, destinations, and user settings.
- **Web Scraping & Integration**:
  - Improved **guild and shop tracking** with automated updates from "A View in the Dark."
  - Enhanced **coordinate extraction accuracy** for in-game location tracking.
- **UI & Theming**:
  - Introduced **customizable themes** for the application UI.
  - Improved **label positioning** and **grid rendering** for better readability.
- **Bug Fixes & Refinements**:
  - Addressed **inconsistent street labeling issues**.
  - Fixed **map rendering artifacts** when zooming or resizing the window.

---

### Version 0.9.1

#### Feature Enhancements:
- **Refactored Database Management**:
  - Improved **SQLite database schema** for faster queries and better data integrity.
  - Optimized **data fetching** for in-game points of interest.
- **Advanced Web Scraping Integration**:
  - Improved **guild/shop tracking** by fetching updates from "A View in the Dark".
  - Implemented **background update scheduler** for periodic data refreshing.
- **Minimap Rendering Updates**:
  - **Better alignment** of street labels for readability.
  - Fixed **overlapping UI elements** on smaller screen resolutions.

---

### Version 0.9.0

#### Major System Upgrades:
- **Encryption & Security Enhancements**:
  - Integrated **cryptography module** for secure **password and cookie storage**.
  - Cookies are now **encrypted** before being stored in the database.
- **Expanded Web Engine Capabilities**:
  - Added **JavaScript injection** to capture web events from the game.
  - Improved **coordinate extraction accuracy** when parsing game data.
- **User Account Management Improvements**:
  - Implemented **persistent login handling** using secure cookies.
  - Enhanced **character switching system** for seamless account changes.
- **Database Transition Enhancements**:
  - Improved **MySQL performance** by restructuring how guild and shop data is stored.
  - Introduced **automatic database migrations** to maintain data consistency.

---

### Version 0.8.1

#### Feature Enhancements:
- **Improved Character Management**:
  - Users can now **store and manage multiple characters**.
  - Auto-login feature implemented for **last active character**.
- **Persistent Web Sessions**:
  - Cookies are now **stored in an SQLite database**, ensuring persistent login across sessions.
  - Implemented **cookie injection** to maintain web session states.
- **Database Optimizations**:
  - Streamlined **MySQL and SQLite interactions** for improved performance.
  - Added new **indexes** to speed up frequent queries.

---

### Version 0.8.0

#### Major System Upgrades:
- **Full Integration of MySQL Database**:
  - Transitioned **map data storage** from SQLite to **MySQL**.
  - Data for **banks, taverns, transit stations, guilds, and shops** is dynamically fetched.
- **Web Scraping Enhancements**:
  - Improved **guild and shop tracking** using "A View in the Dark".
  - Added a **scheduler** for automatic periodic updates.
- **Expanded Minimap Features**:
  - Implemented **Action Point (AP) cost calculation** for movement.
  - Nearest **banks, pubs, and transit stations** now display AP cost.
- **User Interface Enhancements**:
  - Added **theme customization support**, allowing users to modify UI colors.
  - Improved **label positioning** on the minimap for better readability.
- **Enhanced Security & Encryption**:
  - Integrated **cryptography** module for **secure password storage**.
  - Web session cookies are now **securely stored and managed**.

---

### Version 0.7.3

#### Feature Enhancements:
- **Database Improvements**:
  - **Optimized MySQL queries** for fetching city map data.
  - **Improved caching mechanism** to reduce redundant database calls.
- **Web Scraping Enhancements**:
  - Implemented a **scheduler** for automatic guild/shop data updates.
  - Improved **error handling** in the `AVITDScraper` class to handle unexpected webpage changes.

---

### Version 0.7.2

#### UI & Functionality Improvements:
- **Map UI Enhancements**:
  - **Dynamic minimap updates** based on live coordinate extraction.
  - Improved **text rendering on the minimap** for better visibility.
- **Bug Fixes**:
  - Fixed an issue where **some destinations failed to save** properly.
  - Resolved a **web scraping timeout issue** with `requests`.

---

### Version 0.7.1

#### Core System Updates:
- **Cookie Management System**:
  - Added **persistent cookies storage** using SQLite.
  - Improved **web session handling** for a seamless login experience.
- **Performance Enhancements**:
  - Reduced **memory usage** by optimizing loaded data objects.
  - Improved **logging system** for better debugging.

---

### Version 0.7.0

#### Major System Overhaul:
- **Migration to PySide6**:
  - Fully transitioned the UI framework from **PyQt5 to PySide6**.
  - Improved **QtWebEngineView integration** for a smoother browsing experience.
- **Expanded Character Management**:
  - Added **character list storage** with an improved selection interface.
  - Implemented **auto-login** for last active character.
- **Web Integration Upgrades**:
  - Introduced **JavaScript console logging** to capture web events.
  - Improved **coordinate extraction accuracy** from the game’s webpage.

---

### Version 0.6.3

#### Feature Enhancements:
- **Logging System Introduced**:
  - Implemented **file-based logging** to track application activity.
  - Logs stored in the `logs/` directory with daily rotation.
- **Improved Character Management**:
  - Introduced **character selection list** with persistent storage.
  - Players can now **log in and out** of characters directly from the UI.
- **Web Integration Enhancements**:
  - Improved **login handling** using JavaScript injection.
  - Implemented a **"Website Coming Soon"** popup for future website integration.

---

### Version 0.6.2

#### UI & Performance Improvements:
- **Optimized Database Queries**:
  - Improved **MySQL connection handling** for better efficiency.
  - Reduced **redundant database calls** on startup.
- **Bug Fixes**:
  - Fixed an issue where **map labels overlapped incorrectly**.
  - Corrected **coordinate extraction logic** from the game’s HTML.

---

### Version 0.6.1

#### Core Enhancements:
- **Database Stability Fixes**:
  - Improved **error handling for failed MySQL connections**.
  - Enhanced **logging of database interactions** for debugging.
- **UI Adjustments**:
  - Modified **layout structure** for better scalability.
  - Adjusted **button sizing and alignment**.

---

### Version 0.6.0

#### Major System Upgrades:
- **New Data Management System**:
  - Added **session management** for tracking login states.
  - Expanded **database structure** to support **places of interest**.
- **MySQL Performance Improvements**:
  - Optimized **query efficiency** for location lookups.
  - Improved **data storage for guilds and shops**.
- **Web Scraping Enhancements**:
  - Implemented **scheduled scraping** for guild/shop updates.
  - Extracted **next update timestamps** from "A View in the Dark".

---

### Version 0.5.4

#### Feature Enhancements:
- **Shop & Guild Data Updates**:
  - Integrated **data scraping** from "A View in the Dark" for guilds and shops.
  - Added **automatic next update timestamps** for guild/shop tracking.
- **Database Enhancements**:
  - Improved **MySQL integration** to store shop and guild locations.
  - Optimized **query performance** for location lookups.

---

### Version 0.5.3

#### Performance & UI Fixes:
- **Improved Web Scraping Efficiency**:
  - Optimized **HTML parsing logic** for extracting player coordinates.
  - Reduced **redundant requests** to "A View in the Dark" to avoid unnecessary loads.
- **Map Labeling Fixes**:
  - Addressed **overlapping street name rendering issues**.
  - Improved **text alignment** for street intersections.

---

### Version 0.5.2

#### Core Improvements:
- **Enhanced Webview Integration**:
  - Improved coordinate extraction from the game’s **HTML structure**.
  - Enhanced support for **auto-updating minimap positions**.
- **New MySQL Data Handling**:
  - Extended database to **track next update timestamps** for guilds and shops.
  - Improved **error handling for failed MySQL connections**.

---

### Version 0.5.1

#### Bug Fixes & Refinements:
- **Database Stability Fixes**:
  - Fixed **intermittent connection failures** with MySQL.
  - Improved **data retrieval logic** for user locations.
- **UI Enhancements**:
  - Minor improvements to **minimap rendering**.

---

### Version 0.5.0

#### Major Enhancements:
- **MySQL Database Integration**:
  - Fully transitioned from **SQLite to MySQL**.
  - Now retrieves **banks, taverns, transit stations, and user buildings** dynamically.
- **Improved Character Management System**:
  - Placeholder UI for **adding, modifying, and deleting** saved characters.
- **Optimized Map Rendering**:
  - **QPainter rendering updates** for smoother UI performance.
- **Updated Web Browser**:
  - Replaced older implementation with **QWebEngineView** for better in-game site support.

---

### Version 0.4.3

#### Feature Enhancements:
- **Destination Tracking**:
  - Users can now **set a destination** on the minimap.
  - A **green line** is drawn from the player's location to the destination.
  - The destination is **saved** between sessions using `pickle`.

- **Improved Nearest Location Tracking**:
  - Identifies and displays **the closest bank, pub, and transit station**.
  - **Color-coded paths**:
    - **Blue**: Path to the nearest bank.
    - **Orange**: Path to the nearest pub.
    - **Red**: Path to the nearest transit station.

- **Web Integration Improvements**:
  - Coordinates now **auto-extract from the game's webpage**.
  - The **minimap updates dynamically** based on extracted coordinates.

---

### Version 0.4.2

#### Bug Fixes & Refinements:
- **Fixed pathfinding logic**:
  - Addressed inconsistencies in nearest-location tracking.
  - Improved **minimap rendering** when zooming.

- **Performance Enhancements**:
  - Reduced unnecessary **web view refreshes**.
  - Optimized **HTML parsing** for extracting coordinates.

---

### Version 0.4.1

#### Critical Bug Fixes:
- **Fixed Stack Overflow Bug**:
  - Selecting **1st, 2nd, or 3rd closest locations** previously caused a **stack buffer overflow**.
  - Temporarily disabled these buttons while reworking the logic.

- **Minimap Navigation Updates**:
  - Clicking the minimap **centers the view more accurately**.
  - **Street labels** now display more consistently.

---

### Version 0.4.0

#### Major Enhancements:
- **Improved Minimap UI**:
  - Increased **scalability** for different zoom levels.
  - Implemented **QPainter-based rendering**.

- **Integrated Web Browser**:
  - Embedded the **game’s website** inside the application using `QWebEngineView`.
  - The game page **loads automatically** when launching the application.

- **Character Management System**:
  - Placeholder for **adding, modifying, and deleting** saved characters.
  - **Character list panel** added to the UI.

- **New Buttons & Controls**:
  - **Refresh Button**: Reloads the game’s web page.
  - **Discord & Website Buttons**: Quick links to community resources.

---

### Version 0.3.4

#### UI & Feature Enhancements:
- **PyQt5 Migration Completed**:
  - Fully transitioned from **Tkinter** to **PyQt5** for a more modern UI.
  - Improved **layout structure** with frames, buttons, and widgets.
- **Minimap Overhaul**:
  - **QPainter-based rendering** for a smoother and scalable minimap.
  - **Street names** dynamically displayed at intersections.
  - New **color-mapped locations**:
    - **Banks** (Blue)
    - **Pubs** (Orange)
    - **Transit Stations** (Red)
    - **Alleyways** (Dark Grey)
    - **User Buildings** (Purple)
- **Improved Web Integration**:
  - **QtWebEngineView** implemented to embed the **game’s webpage** within the app.
  - **Auto-coordinate extraction** from the game’s HTML for real-time positioning.

---

### Version 0.3.3

#### Map & UI Refinements:
- **More accurate coordinate tracking** for streets.
- **QFontMetrics integration** for better text alignment in the minimap.
- **Character list feature added**:
  - Placeholder for storing multiple characters.
  - Basic UI buttons for adding/removing characters.

---

### Version 0.3.2

#### Core Improvements:
- **Introduced Closest Locations Feature**:
  - Added buttons for **1st, 2nd, and 3rd closest** locations.
  - Displayed **nearest banks, pubs, and transit stations**.
- **Enhanced Zoom & Destination Features**:
  - **Set Destination Button** (placeholder added).
  - Improved **zoom handling** for minimap navigation.
- **Data Management**:
  - Implemented **pickle-based storage** for credentials and settings.

---

### Version 0.3.1

#### UI & Structural Improvements:
- **Minimap Rendering Update**:
  - Improved rendering logic for street names.
  - **Dropdown-based navigation system** introduced.
- **Refactored Map Class**:
  - Separated map logic into a dedicated **Map class**.
  - Improved **data structure management** for streets and locations.

---

### Version 0.3.0

#### Major Transition:
- **PyQt5 Initial Implementation**:
  - Began migrating from **Tkinter to PyQt5**.
  - Basic **QWidget-based UI framework** introduced.
- **Enhanced Grid System**:
  - **Dynamic minimap scaling** based on zoom levels.
  - **Improved street navigation** with dropdown selection.
- **Web Integration Begun**:
  - **Planned implementation of web scraping** for real-time game data retrieval.

---

### Version 0.2.0

#### Feature Enhancements:
- **Expanded Minimap Functionality**:
  - Introduced **color-coded locations**:
    - **Blue**: Banks
    - **Orange**: Pubs
    - **Red**: Transit stations
    - **Black**: Alleys
  - Improved **labeling system** to display street intersections.

- **Street System Improvements**:
  - Refined logic for **street name generation**.
  - Enhanced the way **E-W and N-S streets** are referenced.

- **Interactivity Updates**:
  - Clicking on the **minimap** now updates movement with improved calculations.
  - Improved **dropdown-based location selection**.

#### UI & Code Improvements:
- **Variables Modularization**:
  - Introduced `variables.py` to manage streets, locations, and other constants separately.

- **Optimization**:
  - Updated **grid logic** for faster rendering.
  - **Improved visual representation** of key locations.

#### Placeholder Features:
- **Set Destination** (still a placeholder).
- **Open Webpage & Discord Buttons** (no functionality yet).

---

### Version 0.1.0

#### Initial Release:
- **Basic Minimap Functionality**:
  - Displayed a **3x3 grid** representing the player’s location.
  - Allowed **manual centering** by selecting locations from dropdowns.
  - **Click-based recentering** on the minimap.

#### Core Features:
- **Street System**:
  - Implemented a **grid-based street layout** with named E-W and N-S streets.
  - Dynamic **street name generation** for E-W coordinates (e.g., "1st", "2nd", etc.).

- **Zoom Controls**:
  - **Zoom In/Out** functionality with adjustable grid sizes.

- **Navigation & Destination**:
  - Users could **select a street intersection** and **navigate to it**.
  - Implemented a **"Set Destination"** button (placeholder).

- **UI Elements**:
  - **Tkinter-based interface** with dropdowns, buttons, and a canvas.
  - Initial **top bar controls** for zoom, refreshing, and setting destinations.

- **Basic Interactivity**:
  - Clicking on the **minimap grid** updated the position.
  - **Dropdown selections** allowed navigation to chosen locations.

#### Placeholder Features:
- **Set Destination** (not yet functional).
- **Open Webpage & Discord Buttons** (not yet implemented).

