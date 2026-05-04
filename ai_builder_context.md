# AI Builder Context: Core Data & Logic

Provide the following files and information to the other AI assistant to ensure it has full context on the TapFo application's data structures, dropdowns, and performance indicators (KPIs).

### 1. Essential Context Files (The "Correct" Files)

1.  **[index.html](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/index.html)**: 
    - *Purpose*: Main UI orchestration, global `state` object (contains current user role, active page, and some hardcoded dropdown lists like Cities/Areas).
2.  **[data/Directory_Categories_V1.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/data/Directory_Categories_V1.js)**:
    - *Purpose*: The master list of categories and sub-categories. Critical for any "Category Selector" or "Dropdown" logic.
3.  **[data/TapFo_Business_Database_V1.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/data/TapFo_Business_Database_V1.js)**:
    - *Purpose*: The business data schema. Shows exactly what fields are stored (Name, Services, verified status, etc.).
4.  **[scripts/PulseUpdater.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/scripts/PulseUpdater.js)**:
    - *Purpose*: Tracking KPIs like Sentiment (Trust/Untrust) and user engagement metrics.
5.  **[scripts/Commission_Engine.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/scripts/Commission_Engine.js)**:
    - *Purpose*: Financial KPIs, earning logic, and commission structures.
6.  **[scripts/PermissionsManager.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/scripts/PermissionsManager.js)**:
    - *Purpose*: Defines roles (Admin, Staff, Business-Validated, Browser). Use this to determine which dropdown options are visible to which users.
7.  **[data/promos_manifest.js](file:///c:/Users/Kudzanai/Documents/2025/App%20Developments/TapFo/data/promos_manifest.js)**:
    - *Purpose*: Metadata for the promotions engine.

---

### 2. Business Information Collection Schema
When collecting information from new businesses (e.g., in the "+" Add Action flow), use the following standardized format (derived from `V1 Database`):

| Field | Format | Purpose |
| :--- | :--- | :--- |
| **id** | Integer | Unique identifier. |
| **name** | String | Official business name. |
| **category** | String | Must match top-level category in `Directory_Categories_V1.js`. |
| **subcategory** | Array (Strings) | Specific niche focus. |
| **type** | Enum | "Company" or "Consultant". |
| **location** | String | Village/Town/City + Area (e.g., "Gaborone, CBD"). |
| **services** | Array (Strings) | Detailed list of searchable services. |
| **verified** | Boolean | Status (handled by Admin/Staff roles). |
| **contacts** | Object | `{ call: [], facebook: [], whatsapp: [] }`. |
| **media** | Array (Objects) | `{ id, type, url, desc }` for images/videos. |

---

### 3. Application Components (Quick Reference)
- **Sign-up Panel**: In the main `index.html` file, this is identified by the ID `#page-accounts` (within the "Accounts Switcher" logic). However, the project also contains standalone templates `signup.html` and `login.html` for deep-link authentication.
- **Add Action Menu**: `#add-action-panel`.
- **Search View**: `#page-search`.
