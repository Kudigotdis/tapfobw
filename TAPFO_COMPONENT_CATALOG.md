# TapFo.bw - UI Component Catalog

**Version:** 1.0  
**Last Updated:** April 2026

---

## 1. CARD COMPONENT HIERARCHY

```
CARDS
├── BUSINESS CARDS
│   ├── .biz-row              (Directory search results)
│   ├── .biz-card             (Home featured businesses)
│   ├── .biz-profile-header   (Business profile top)
│   └── .biz-landing-card     (Business quick access)
│
├── LIST CARDS
│   ├── .dir-row              (Category list items)
│   ├── .dir-row-cat          (Category selector items)
│   ├── .item-row             (Generic list item)
│   └── .ql-drop-card         (Quick links results)
│
├── NOTE CARDS
│   ├── .note-card            (Note list item)
│   ├── .note-level-btn        (Note with two sections)
│   └── .note-add-btn         (Add note button)
│
├── EVENT CARDS
│   ├── .event-card           (Event list item)
│   ├── .event-card.featured  (Featured event)
│   └── .event-card.soccer    (Soccer event variant)
│
├── PROMO CARDS
│   ├── .promo-advert-card    (Single promo display)
│   ├── .promo-category-card  (Promo category tile)
│   └── .promo-media-card     (Media channel item)
│
├── PROFILE CARDS
│   ├── .profile-section-card (Profile section container)
│   ├── .interest-pill        (Profile interest tag)
│   └── .education-item       (Education entry)
│
├── ACCOUNT CARDS
│   ├── .account-row          (Account list item)
│   └── .account-row.active  (Currently selected)
│
├── CONTACT CARDS
│   ├── .contact-entry        (Contact list item)
│   ├── .contact-entry-icon   (Contact type icon)
│   └── .contact-pill        (Contact type filter)
│
├── MEDIA CARDS
│   ├── .media-note-item      (Media gallery item)
│   ├── .media-thumb          (Media thumbnail)
│   └── .online-item          (Online presence item)
│
├── WONDA CARDS
│   └── .wonda-card          (Poll question card)
│
└── UTILITY CARDS
    ├── .empty-state          (No data placeholder)
    └── .no-results           (Search no results)
```

---

## 2. BUSINESS CARDS

### 2.1 .biz-row (Directory Search Result)

**Purpose:** Single business entry in directory/search results  
**Location:** index.html:~5331-5349

```css
.biz-row {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--grey-border);
  cursor: pointer;
  transition: background var(--transition);
}
.biz-row:active {
  background: var(--grey-light);
}

/* Trust indicator bar (left edge) */
.trust-bar {
  width: 4px;
  height: 40px;
  background: transparent;
  border-radius: 2px;
  margin-right: 12px;
  flex-shrink: 0;
}
.trust-bar.trusted {
  background: #22c55e; /* Green */
}

/* Business name */
.biz-name {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
  color: var(--dark-text);
}

/* Contact icons */
.contact-icons {
  display: flex;
  gap: 8px;
}
.contact-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.contact-icon.phone-active { background: #f59e0b; }
.contact-icon.fb-active { background: #1877f2; }
.contact-icon.wa-active { background: #25d366; }
.contact-icon.inactive { background: var(--grey-light); opacity: 0.5; }
```

**HTML Structure:**
```html
<div class="biz-row" onclick="openBusiness('BUS_001')">
  <div class="trust-bar trusted" onclick="event.stopPropagation();toggleTrust('BUS_001',this)"></div>
  <div class="biz-name">Business Name Here</div>
  <div class="contact-icons">
    <button class="contact-icon phone-active" onclick="event.stopPropagation();handleContact('phone','BUS_001')">
      <img src="assets/icons/phone_icon_on.png">
    </button>
    <button class="contact-icon fb-active" onclick="event.stopPropagation();handleContact('facebook','BUS_001')">
      <img src="assets/icons/facebook_icon_on.png">
    </button>
    <button class="contact-icon wa-active" onclick="event.stopPropagation();handleContact('whatsapp','BUS_001')">
      <img src="assets/icons/whatsApp_icon_on.png">
    </button>
  </div>
</div>
```

---

### 2.2 .dir-row (Directory Category Row)

**Purpose:** Category or subcategory in directory browser  
**Location:** index.html:~5428-5479

```css
.dir-row {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  background: var(--white);
  border-bottom: 1px solid var(--grey-border);
  cursor: pointer;
  transition: background var(--transition);
}
.dir-row:active {
  background: var(--grey-light);
}

.dir-row-icon {
  width: 44px;
  height: 44px;
  background: var(--grey-light);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-right: 12px;
  flex-shrink: 0;
}

.dir-row-content {
  flex: 1;
}

.dir-row-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--dark-text);
}

.dir-row-subtitle {
  font-size: 13px;
  color: var(--grey-text);
  margin-top: 2px;
}

.dir-row-arrow {
  font-size: 24px;
  color: var(--grey-text);
  font-weight: 300;
}
```

---

### 2.3 .note-card (Note List Item)

**Purpose:** Individual note in notes list  
**Location:** index.html:~3277-3338

```css
.note-card {
  background: var(--white);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
  margin: 12px 16px;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow var(--transition);
}
.note-card:active {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.note-card-header {
  padding: 14px 16px;
  border-bottom: 1px solid var(--grey-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.note-card-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--dark-text);
}

.note-card-date {
  font-size: 12px;
  color: var(--grey-text);
  margin-top: 2px;
}

.note-card-count {
  font-size: 13px;
  color: var(--navy);
  font-weight: 600;
}
```

---

### 2.4 .note-level-btn (Two-Section Note Button)

**Purpose:** Note with expandable top/bottom sections  
**Location:** index.html:~3341-3367

```css
.note-level-btn {
  display: flex;
  align-items: stretch;
  margin: 0 16px 10px;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.note-level-top {
  padding: 14px 16px;
  font-size: 16px;
  font-weight: 700;
  color: white;
  flex: 1;
  background: var(--navy);
}

.note-level-bottom {
  padding: 10px 16px;
  font-size: 13px;
  color: rgb(80, 80, 80);
  background: rgb(239, 239, 239);
  flex: 1;
  display: flex;
  align-items: center;
}
```

---

### 2.5 .event-card (Event List Item)

**Purpose:** Individual event in events calendar  
**Location:** index.html:~6234-6249

```css
.event-card {
  background: var(--white);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
  margin: 10px 16px;
  padding: 14px 16px;
  cursor: pointer;
  transition: box-shadow var(--transition);
}
.event-card:active {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.event-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.event-status {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
  background: var(--grey-light);
  color: var(--grey-text);
}
.event-status.active { /* Ongoing */
  background: #22c55e;
  color: white;
}
.event-status.upcoming { /* Upcoming */
  background: var(--navy);
  color: white;
}

.event-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--dark-text);
  margin-bottom: 4px;
}

.event-meta {
  font-size: 13px;
  color: var(--body-text);
  display: flex;
  gap: 12px;
  margin-bottom: 4px;
}

.event-location {
  font-size: 12px;
  color: var(--grey-text);
}

/* Variants */
.event-card.featured {
  border-left: 4px solid var(--navy);
}
.event-card.soccer {
  background: linear-gradient(135deg, #1a5276 0%, #2e6893 100%);
}
.event-card.soccer .event-name,
.event-card.soccer .event-meta,
.event-card.soccer .event-location {
  color: white;
}
```

---

### 2.6 .promo-advert-card (Promotional Content)

**Purpose:** Display single promo image/video/audio  
**Location:** index.html:~6143-6147

```css
.promo-advert-card {
  background: var(--white);
  border-radius: var(--radius-card);
  overflow: hidden;
  margin-bottom: 12px;
}
.promo-advert-card img,
.promo-advert-card video {
  width: 100%;
  display: block;
}
.promo-advert-card audio {
  width: 100%;
  margin: 20px 0;
}
```

---

### 2.7 .empty-state (No Data Placeholder)

**Purpose:** Shown when a list has no items  
**Location:** index.html (shared component)

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
}

.empty-state-emoji {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.7;
}

.empty-state-text {
  font-size: 15px;
  color: var(--grey-text);
  max-width: 280px;
}
```

**Common Emojis:**
| Emoji | Used For |
|-------|----------|
| 🔍 | No search results |
| 📝 | No notes |
| 📭 | No contacts |
| 📰 | No news |
| 🎬 | No media |
| 🌐 | No online presence |
| 🖼️ | No promo images |
| 📅 | No events |

---

### 2.8 .contact-entry (Contact List Item)

**Purpose:** Individual contact entry (phone, FB, WhatsApp)  
**Location:** index.html:~5794-5806

```css
.contact-entry {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--grey-border);
  cursor: pointer;
  transition: background var(--transition);
}
.contact-entry:active {
  background: var(--grey-light);
}

.contact-entry-info {
  flex: 1;
}

.contact-entry-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--dark-text);
}

.contact-entry-desc {
  font-size: 13px;
  color: var(--body-text);
  margin-top: 2px;
}

.contact-entry-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-left: 10px;
}
.contact-entry-icon.phone { background: #f59e0b; }
.contact-entry-icon.fb { background: #1877f2; }
.contact-entry-icon.wa { background: #25d366; }

.contact-entry-icon svg {
  width: 16px;
  height: 16px;
  fill: white;
}
```

---

### 2.9 .account-row (Account Switcher Item)

**Purpose:** Individual account in account switcher  
**Location:** index.html:~7126-7143

```css
.account-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--grey-border);
  cursor: pointer;
  transition: background var(--transition);
}
.account-row:active {
  background: var(--grey-light);
}
.account-row.active-account {
  background: rgba(26, 82, 118, 0.08);
}

.account-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.account-info {
  flex: 1;
}

.account-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--dark-text);
}

.account-username {
  font-size: 13px;
  color: var(--grey-text);
  margin-top: 2px;
}

.account-type-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 12px;
  white-space: nowrap;
}
/* Badge colors defined elsewhere */

.active-account-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--navy);
}
```

---

### 2.10 .wonda-card (Poll Question)

**Purpose:** Community poll question card  
**Location:** index.html:~7031-7051

```css
.wonda-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 14px;
  cursor: pointer;
}
.wonda-card:active {
  opacity: 0.8;
}

.wonda-q {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 10px;
  line-height: 1.4;
}

.wonda-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.wonda-pill {
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  padding: 6px 14px;
  color: rgba(255, 255, 255, 0.7);
  font-family: var(--font);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}
.wonda-pill:active,
.wonda-pill.voted {
  background: rgba(26, 82, 118, 0.5);
  border-color: var(--navy);
  color: var(--white);
}
```

---

### 2.11 .interest-pill (Profile Interest Tag)

**Purpose:** Interest/category tag in profile  
**Location:** index.html:~3231-3245

```css
.interest-pill {
  background: var(--navy);
  color: var(--white);
  border-radius: 8px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 500;
  display: inline-block;
}

.interest-pills {
  padding: 12px 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
```

---

### 2.12 .news-item (Business News Article)

**Purpose:** News article preview in business profile  
**Location:** index.html:~2026-2054

```css
.news-item {
  padding: 16px;
  border-bottom: 1px solid var(--grey-border);
  cursor: pointer;
  transition: background var(--transition);
}
.news-item:active {
  background: var(--grey-light);
}

.news-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--dark-text);
  margin-bottom: 4px;
}

.news-date {
  font-size: 12px;
  color: var(--grey-text);
  margin-bottom: 6px;
}

.news-preview {
  font-size: 13px;
  color: var(--body-text);
  line-height: 1.45;
}
```

---

### 2.13 .online-item (Online Presence Link)

**Purpose:** Website/social link in business profile  
**Location:** index.html:~2134-2174

```css
.online-item {
  padding: 16px;
  border-bottom: 1px solid var(--grey-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.online-item-info {
  flex: 1;
}

.online-item-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--dark-text);
}

.online-item-url {
  font-size: 12px;
  color: var(--navy);
  margin-top: 2px;
}

.online-item-icon {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--grey-light);
  border: 1px solid var(--grey-border);
  display: flex;
  align-items: center;
  justify-content: center;
}

.online-item-icon svg {
  width: 18px;
  height: 18px;
  fill: var(--grey-text);
}
```

---

### 2.14 .service-cat-row (Business Service Item)

**Purpose:** Service category in business profile  
**Location:** index.html:~5683-5695

```css
.service-cat-row {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--grey-border);
  cursor: pointer;
  transition: background var(--transition);
}
.service-cat-row:active {
  background: var(--grey-light);
}

.service-dot {
  width: 8px;
  height: 8px;
  background: var(--navy);
  border-radius: 50%;
  margin-right: 12px;
  flex-shrink: 0;
}

.service-cat-name {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
  color: var(--dark-text);
}

.service-count {
  font-size: 13px;
  color: var(--grey-text);
}

.service-sub-list {
  display: none;
  padding: 8px 16px 16px 36px;
  background: var(--grey-light);
}
.service-sub-list.open {
  display: block;
}

.service-sub-item {
  padding: 10px 0;
  font-size: 14px;
  color: var(--body-text);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  cursor: pointer;
}
.service-sub-item:last-child {
  border-bottom: none;
}
```

---

## 3. NAVIGATION COMPONENTS

### 3.1 .bottom-nav (Bottom Navigation Bar)

**Location:** index.html:~276-374

```css
.bottom-nav {
  flex-shrink: 0;
  height: 56px;
  background: var(--deep-navy);
  display: flex;
  align-items: center;
  padding: 0 12px 0 16px;
  gap: 0;
  z-index: 20;
}

.nav-link {
  background: none;
  border: none;
  font-family: var(--font);
  font-size: 14px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  padding: 4px 0;
  white-space: nowrap;
  transition: color var(--transition);
}
.nav-link.nav-active {
  color: rgb(255, 255, 255);
  font-weight: 700;
}

.engage-btn {
  background: transparent;
  border: 2px solid #2e6893;
  color: var(--white);
  font-family: var(--font);
  font-size: 13px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
}
```

---

### 3.2 .ql-trap-pill (Quick Link Pill Button)

**Purpose:** Quick access category on home page  
**Location:** index.html:~4001-4025

```css
.ql-trap-pill {
  background: none;
  border: 2px solid var(--pc, var(--navy));
  border-radius: 20px;
  padding: 8px 16px;
  font-family: var(--font);
  font-size: 14px;
  font-weight: 600;
  color: var(--pc, var(--navy));
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
  --pc: #1a5276; /* Default color */
}
.ql-trap-pill:active {
  background: var(--pc, var(--navy));
  color: white;
}
```

---

### 3.3 .promo-pill (Filter Pill Button)

**Purpose:** Category/status filter pills  
**Location:** index.html:~2115-2131

```css
.promo-pill {
  background: var(--white);
  border: 1px solid rgba(26, 82, 118, 0.4);
  border-radius: 8px;
  padding: 6px 14px;
  font-family: var(--font);
  font-size: 13px;
  font-weight: 600;
  color: var(--navy);
  cursor: pointer;
  transition: all var(--transition);
  flex-shrink: 0;
}
.promo-pill.active {
  background: var(--navy);
  color: var(--white);
}
```

---

## 4. FORM COMPONENTS

### 4.1 .search-bar (Search Input)

**Location:** index.html:~442-468

```css
.search-bar {
  width: 100%;
  height: 60px;
  background: var(--white);
  border: 4px solid rgba(160, 160, 160, 0.5);
  border-radius: 8px;
  padding: 0 54px;
  font-family: var(--font);
  font-size: 16px;
  color: var(--dark-text);
  outline: none;
  transition: border-color var(--transition);
  text-align: center;
}
.search-bar:focus {
  border-color: var(--navy);
}
.search-bar::placeholder {
  color: rgb(180, 180, 180);
  font-size: 16px;
}
```

---

### 4.2 .note-add-btn (Add Button)

**Location:** index.html:~3317-3338

```css
.note-add-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px;
  margin: 12px 16px;
  background: var(--white);
  border-radius: var(--radius-card);
  border: 2px dashed var(--grey-border);
  cursor: pointer;
  font-family: var(--font);
  font-size: 15px;
  font-weight: 600;
  color: var(--grey-text);
  width: calc(100% - 32px);
  transition: border-color var(--transition), color var(--transition);
}
.note-add-btn:hover {
  border-color: var(--navy);
  color: var(--navy);
}
```

---

## 5. CSS VARIABLES REFERENCE

```css
:root {
  /* Colors */
  --navy: rgb(26, 82, 118);
  --deep-navy: rgb(18, 52, 86);
  --grey-light: rgb(230, 230, 230);
  --grey-border: rgb(200, 200, 200);
  --grey-text: rgb(180, 180, 180);
  --white: #ffffff;
  
  /* Typography */
  --font: 'PTSans', sans-serif;
  
  /* Animation */
  --transition: 320ms cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Z-Index */
  --z-bottom: 1;
  --z-foreground: 2;
  --z-top: 10;
  --z-overlay: 100;
  
  /* Radius */
  --radius-card: 12px;
  --radius-button: 8px;
  
  /* Shadows */
  --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.08);
}
```

---

## 6. CARD DESIGN GUIDELINES

### 6.1 Required Properties

| Property | Value |
|----------|-------|
| Border Radius | 12px (--radius-card) or 16px |
| Shadow | 0 2px 8px rgba(0,0,0,0.08) |
| Padding | 14-16px |
| Touch Target | Minimum 44px height |
| Font Size | 13-16px body, 16-20px titles |
| Color | Use CSS variables |

### 6.2 Card States

```
DEFAULT → HOVER/ACTIVE → DISABLED/INACTIVE
   ↓           ↓               ↓
 Normal    Darker bg        50% opacity
```

### 6.3 Empty State Pattern

```html
<div class="empty-state">
  <div class="empty-state-emoji">🔍</div>
  <div class="empty-state-text">Descriptive message here</div>
</div>
```

---

**Document Version:** 1.0  
**Maintainer:** TapFo Development Team
