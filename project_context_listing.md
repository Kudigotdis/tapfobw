# TapFo Project Context: File Listing

Below is a comprehensive list of the primary files and data sources that define the TapFo application's structure, logic, and content. These files provide the necessary context for implementing new features like the 7 proposed panels.

1.  **[index.html](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/index.html)**: The main application file containing the single-page architecture, CSS styles, routing logic, and core UI components.
2.  **[data/TapFo_Business_Database_V1.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/data/TapFo_Business_Database_V1.js)**: The primary database containing all business entities and their associated metadata (services, location, contacts).
3.  **[data/Directory_Categories_V1.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/data/Directory_Categories_V1.js)**: Definitions of the high-level categories and sub-categories used in the directory.
4.  **[data/promos_manifest.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/data/promos_manifest.js)**: Manifest of active promotions and their categorization.
5.  **[data/mediums_manifest.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/data/mediums_manifest.js)**: Data for different media channels (Radio, Newspapers, Podcasts, etc.).
6.  **[data/botswana_events_2026.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/data/botswana_events_2026.js)**: The events calendar for 2026.
7.  **[scripts/HistoryTracker.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/scripts/HistoryTracker.js)**: Logic for tracking user navigation and page history.
8.  **[scripts/PermissionsManager.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/scripts/PermissionsManager.js)**: Role-based access control and capability management.
9.  **[scripts/PulseUpdater.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/scripts/PulseUpdater.js)**: Real-time telemetry and user interaction logging.
10. **[scripts/Commission_Engine.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/scripts/Commission_Engine.js)**: Business logic related to financial transactions/commissions within the app.
11. **[Gaborone/](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/Gaborone)** (Directory): Contains partitioned data for various sectors (Health, Finance, Mobile Networks, Sports, etc.), providing localized context for the Gaborone region.
12. **[login.html](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/login.html)** & **[signup.html](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/signup.html)**: External templates for the authentication flow.

---

### Understanding the Data Context
- **Geography**: Categorized by Village, Town, and City (focused on Gaborone-specific neighbourhoods like Block 6, Phakalane, CBD).
- **Interests**: Lists of specific activities and sports (found in `Gaborone/Sports` and `Directory_Categories_V1.js`).
- **Infrastructure**: Mobile networks list (found in `Gaborone/Mobile Networks`).
