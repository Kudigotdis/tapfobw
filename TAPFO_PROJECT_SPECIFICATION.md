# TapFo.bw - Complete Project Specification

**Version:** 1.01.267  
**Last Updated:** April 2026  
**Type:** Progressive Web App (PWA) - Botswana Business Directory

---

## 1. PROJECT OVERVIEW

### 1.1 What is TapFo.bw?

**TapFo.bw** (pronounced "Tap-For") is Botswana's **offline-first business directory** PWA. The tagline is **"TapFo everything"** — a mobile-first platform for discovering local businesses, promotions, events, and services across Botswana.

### 1.2 Core Purpose

| Purpose | Description |
|---------|-------------|
| **Business Discovery** | Find local businesses by category, location, and services |
| **Promotions** | Browse weekly ads and promotional content from businesses |
| **Events** | Discover what's happening in Botswana (2026 calendar) |
| **Trust System** | Build personal list of trusted local businesses |
| **Offline Access** | Works without internet after initial caching |

### 1.3 Target Audience

- **Primary:** Botswana citizens seeking local services
- **Secondary:** Tourists and visitors to Botswana
- **Tertiary:** Business owners promoting their services
- **Platform:** Mobile-first (Android), Desktop browsers

### 1.4 Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vanilla HTML5, CSS3, JavaScript (ES6) |
| **Build System** | None (direct browser execution) |
| **Styling** | Custom CSS with CSS Variables |
| **Icons** | SVG (inline and file-based) |
| **Fonts** | PT Sans (locally hosted TTF) |
| **Storage** | localStorage (offline data, user preferences) |
| **PWA** | Service Worker API, Web App Manifest |

---

## 2. FILE STRUCTURE

```
TapFo/
│
├── index.html                    # MAIN APPLICATION (7206 lines)
│   ├── CSS (lines 24-4000)      # All styles
│   └── JavaScript (lines 4001-7206) # All logic
│
├── manifest.json                 # PWA configuration
├── sw.js                        # Service Worker (offline caching)
├── login.html                   # Standalone login page
├── signup.html                  # Standalone signup page
│
├── assets/
│   ├── fonts/
│   │   ├── PTSans-Regular.ttf
│   │   ├── PTSans-Bold.ttf
│   │   ├── PTSans-Italic.ttf
│   │   └── PTSans-BoldItalic.ttf
│   └── icons/                   # 70+ SVG/PNG icons
│       ├── TapFo_Logo.gif
│       ├── TapFo_Thumbnail.svg
│       ├── Directory_Icon.svg
│       ├── Promo_Icon.svg
│       ├── Add_Action.svg
│       ├── phone_icon_on.png
│       ├── facebook_icon_on.png
│       ├── whatsApp_icon_on.png
│       └── [60+ more icons]
│
├── scripts/                     # JavaScript modules
│   ├── PulseUpdater.js          # KPI tracking (Bothoflow Protocol)
│   ├── Commission_Engine.js     # Financial/economy logic
│   ├── PermissionsManager.js   # Role-based access control
│   ├── HistoryTracker.js       # Navigation history (88-item cap)
│   ├── extract_events.py       # Python: event data extraction
│   ├── generate_promo_manifest.py
│   ├── json_to_js.py           # JSON to JS conversion
│   ├── merge_events.py         # Event data merging
│   └── update_nav.py           # Navigation updates
│
├── data/                        # Static data files
│   ├── TapFo_Business_Database_V1.js    # 300 businesses
│   ├── TapFo_Business_Database_V2_enriched.json  # Enriched DB
│   ├── TapFo_Businesses_VB.py           # Python: business data
│   ├── Directory_Categories_V1.js       # 500+ categories
│   ├── Directory_Categories_V1.json
│   ├── botswana_events_2026.js           # 2026 events
│   ├── events_2026.js
│   ├── promos_manifest.js               # Promo paths (38 categories)
│   ├── mediums_manifest.js              # Media channels
│   ├── campaigns_manifest.json
│   ├── events_manifest.json
│   ├── businesses.json
│   ├── updates_changelog.json
│   └── TapFo_enrich_script.py           # DB enrichment script
│
├── PROMOS/                      # 38 categories of promotional images
│   ├── Accommodation_Property/
│   ├── Agriculture/
│   ├── Automotive/
│   ├── Beauty_Grooming/
│   ├── Clothing/
│   ├── Fast_Food/
│   ├── Finance/
│   ├── Groceries/
│   ├── Health_Medical/
│   ├── Restaurants/
│   └── [28 more categories]
│
├── MEDIUMS/                     # Media channel content
│   ├── DSTV/
│   ├── Gazettes/
│   ├── Magazines/
│   ├── Music/
│   ├── Newspapers/
│   ├── Podcasts/
│   ├── Press Releases/
│   ├── Radio/
│   └── Public Notices/
│
├── Gaborone/                    # Partitioned media by sector
│   ├── Accommodation & Property/
│   ├── Agriculture/
│   ├── Automotive/
│   ├── Beauty & Grooming/
│   ├── Construction/
│   ├── Education & Schools/
│   ├── Electronics/
│   ├── Fashion/
│   ├── Fast Food/
│   ├── Finance/
│   ├── Groceries/
│   ├── Health & Medical/
│   └── [20+ more categories]
│
├── scripts/                     # Python utility scripts
│   ├── audit_*.py              # CSS/HTML auditing
│   ├── fix_*.py                # Data fixing scripts
│   ├── generate_*.py           # Data generation scripts
│   ├── reorganize_promos.py
│   ├── recover.py
│   └── update_manifests.py
│
├── .idea/                       # IDE configuration
├── BACKUP INDEX/               # Backup of index.html
├── MAKE DATA FROM THIS/        # Source data reference
├── ORDER THESE/                # Organization reference
│
├── .gitignore
├── ai_builder_context.md        # AI development notes
├── project_context_listing.md   # Project context
├── TapFo About Us.txt
└── TAPFO1_BUSINESS_DIRECTORY_BW.md
```

---

## 3. APPLICATION PAGES

### 3.1 Pages in index.html

| Page ID | Purpose | Navigation |
|---------|---------|------------|
| `#page-home` | Main landing with search & quick links | Entry point |
| `#page-search` | Search results display | From home search |
| `#page-directory` | 3-level category browsing | Nav bar |
| `#page-business` | Individual business profile | From directory/search |
| `#page-promos` | Promotions hub (Weekly/Events/Mediums) | Nav bar |
| `#page-quicklinks` | Quick link category results | From home pills |
| `#page-profile` | User profile with tabs | From menu |
| `#page-notes` | Notes & items management | From menu |
| `#page-sums` | Aggregated calculations | From menu |
| `#page-trusted` | Trusted businesses list | From menu |
| `#page-history` | Navigation history | From menu |
| `#page-wonda` | Community pulse polls | From menu |
| `#page-accounts` | Account switcher (10 mock accounts) | From menu |
| `#page-howto` | How to use guide | From menu |
| `#page-changelog` | Version history | From menu |
| `#page-article` | News article reader | From business profile |

### 3.2 Page States

```javascript
state = {
  currentPage: 'home',        // Current active page
  pageStack: ['home'],        // Navigation stack for back button
  currentBusiness: null,      // Currently viewed business
  currentCity: 'Gaborone',    // Location filter
  currentArea: 'All Areas',  // Area filter
  searchQuery: '',           // Current search
  searchFilter: 'All',        // All/Companies/Consultants
  activeAccount: 'user1',     // Currently active mock account
  // ... plus 40+ more state properties
}
```

---

## 4. DATA SCHEMAS

### 4.1 Business Schema

```javascript
{
  id: "BUS_0328",
  name: "A Team Shopfitters (Pty) Ltd",
  category_main: "Construction",
  category_sub: ["Shop Fitting", "Interior", "Retail Fitout"],
  location: {
    city: "Gaborone",
    area: "Gaborone West Industrial",
    address: "Plot 22072, Gaborone West Ind"
  },
  phone: "+267 3973446",
  facebook: "https://facebook.com/...",
  whatsapp: "+267...",
  verified: false,
  established: null,
  description: "",
  type: "Company",  // or "Consultant"
  services: ["Service 1", "Service 2"],
  news: [{ title, date, preview, body }],
  contacts: { call: [], facebook: [], whatsapp: [] },
  media: [{ id, type, url, desc }]
}
```

### 4.2 Category Schema

```javascript
{
  key: "Retail_Pharmacy",      // Internal identifier
  display: "Pharmacy",         // Human-readable (may include emoji)
  mainCat: "Health & Medical"  // Parent category
}
```

### 4.3 Account Schema

```javascript
{
  id: "user1",
  type: "user",                // browser/user/business-*/designer/staff/admin
  typeBadge: "badge-user",
  typeLabel: "User",
  name: "Mau",
  surname: "Njeri",
  username: "Mojotorino:)",
  color: "#1a5276",
  desc: "3 months active. Gaborone West."
}
```

---

## 5. USER ROLES & PERMISSIONS

### 5.1 Role Hierarchy

| Role | Capabilities | Badge Color |
|------|--------------|-------------|
| **Browser** | View only | Grey |
| **User** | Player (engagement) | Blue |
| **Business-Unvalidated** | Limited features | Yellow |
| **Business-Validated** | Full business owner | Green |
| **Business-Validated-Senior** | +Creator | Teal |
| **Designer** | Ad design, commissions | Purple |
| **Designer-Senior** | +Admin | Dark Purple |
| **Staff** | Internal moderation | Red |
| **Admin** | Full system access | Dark Navy |

### 5.2 Capability Check

```javascript
PermissionsManager.check(account, 'Player');  // true for User+
PermissionsManager.check(account, 'BusinessOwner');  // true for Business-Validated+
PermissionsManager.check(account, 'Admin');  // true for Staff+
```

---

## 6. BOTH OFLOW PROTOCOL

### 6.1 Purpose
Internal economy and analytics system for tracking user engagement and calculating commissions.

### 6.2 Components

| Component | File | Purpose |
|-----------|------|---------|
| **PulseUpdater** | `PulseUpdater.js` | KPI tracking (visits, contacts, sentiment) |
| **CommissionEngine** | `Commission_Engine.js` | 0.5% base trigger, 20% designer cut |
| **HistoryTracker** | `HistoryTracker.js` | 88-item navigation history FIFO |
| **PermissionsManager** | `PermissionsManager.js` | Role-based capability checking |

### 6.3 Commission Rates

```javascript
BASE_RATE: 0.005      // 0.5% per interaction
DESIGNER_RATE: 0.20   // 20% goes to designer
```

---

## 7. LOCATION SUPPORT

### 7.1 Cities

| City | Status |
|------|--------|
| Gaborone | Primary |
| Francistown | Supported |
| Maun | Supported |
| Lobatse | Supported |
| Selebi-Phikwe | Supported |
| Jwaneng | Supported |
| Orapa | Supported |

### 7.2 Gaborone Areas

- CBD
- Gaborone West
- Gaborone North
- Gaborone South
- Phakalane
- Broadhurst
- Mogoditshane
- Tlokweng
- And 30+ more

---

## 8. PROMO CATEGORIES (38)

```
Accommodation & Property
Agriculture
Automotive
Babies & Kids
Beauty & Grooming
Beverages & Liquor
Books & Publishing
Building & Construction
Business & Office
Cargo, Courier & Delivery
Clothing
Clubs & Groups
Crafts
Cultural
Education & Schools
Electronics
Embassies & Consulates
Events
Fabrics & Textiles
Fashion
Fast Food
Film
Finance
Fuel & Transport
Gaming
Groceries
Health & Medical
Home & Decor
Jobs
Mobile Network
Music
Podcasts & TV
Restaurants
Security
Sports
Tourism
Transport
```

---

## 9. EVENTS CALENDAR (2026)

Full year calendar with events categorized by:
- Sports (soccer, athletics)
- Cultural
- Music
- Business
- Community
- Religious
- Government

---

## 10. KNOWN LIMITATIONS

| Limitation | Description |
|------------|-------------|
| **No Backend** | All data is static/localStorage |
| **No Real Auth** | Mock accounts only |
| **No Real Payments** | Commission system is conceptual |
| **No Database** | Data loaded from static JS/JSON |
| **No User Accounts** | Can only switch between mock profiles |

---

## 11. DEVELOPMENT WORKFLOW

See `TAPFO_WORKFLOW_GUIDELINES.md` for the complete debugging and development workflow.

---

## 12. COMPONENT CATALOG

See `TAPFO_COMPONENT_CATALOG.md` for all UI components and card specifications.

---

## 13. FEATURES INVENTORY

See `TAPFO_FEATURES_INVENTORY.md` for complete list of working and planned features.

---

**Document Version:** 1.0  
**Maintained By:** TapFo Development Team
