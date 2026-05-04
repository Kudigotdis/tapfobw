# TapFo.bw - Features Inventory

**Version:** 1.01.267  
**Last Updated:** April 2026

---

## 1. FEATURE STATUS LEGEND

| Status | Symbol | Description |
|--------|--------|-------------|
| **WORKING** | ✅ | Fully functional |
| **PARTIAL** | ⚠️ | Partially implemented, some issues |
| **PLANNED** | 📋 | Not implemented, placeholder only |
| **BROKEN** | ❌ | Implemented but not working |

---

## 2. CORE FEATURES

### 2.1 Home Page

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Animated logo | ✅ | ~3990 | Logo with online/offline status |
| Search bar | ✅ | ~3989 | With blinking cursor effect |
| Quick links | ✅ | ~4001 | 18 pill buttons |
| Location filter | ✅ | N/A | City + Area selector |
| Swipe navigation | ⚠️ | N/A | Swipe left/right |
| Online/offline indicator | ✅ | N/A | Visual status |

### 2.2 Search

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Real-time search | ✅ | ~5290 | `performSearch()` |
| Filter by type | ✅ | ~5266 | All/Companies/Consultants |
| Location filter | ✅ | ~5307 | `filterByLocation()` |
| Results display | ✅ | ~5316 | `renderResultsList()` |
| Empty state | ✅ | ~5320 | "No Results" message |

### 2.3 Business Directory

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| 3-level navigation | ✅ | ~5408 | Main→Sub→Businesses |
| Category icons | ✅ | ~5387 | `getCategoryIcon()` |
| Business count | ✅ | ~5463 | Shows per subcategory |
| All/Trusted filter | ✅ | ~5549 | `setDirFilter()` |
| Category selector | ⚠️ | ~4105 | Quick category dropdown |
| Breadcrumb/back | ✅ | ~5425 | Level-based navigation |

### 2.4 Business Profile

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Header with logo | ✅ | ~5626 | `renderBusinessProfile()` |
| Favourite button | ✅ | ~5659 | `toggleBizFav()` |
| Share button | ⚠️ | ~5643 | Shows toast only |
| Services tab | ✅ | ~5683 | Accordion list |
| News tab | ⚠️ | ~5699 | Shows articles |
| Online links tab | ⚠️ | ~5714 | Shows links |
| Contacts tab | ⚠️ | ~5734 | Call/FB/WA directory |
| Media tab | ⚠️ | ~5762 | Images/Videos/Audio |

### 2.5 Promotions

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Weekly promos tab | ✅ | N/A | 38 categories |
| Events tab | ✅ | ~6173 | Full 2026 calendar |
| Mediums tab | ✅ | N/A | 9 media channels |
| Image display | ✅ | ~6135 | Full promo viewer |
| Video support | ✅ | ~6135 | MP4 playback |
| Audio support | ✅ | ~6137 | MP3 playback |
| Category navigation | ✅ | ~5875 | Multi-level browse |
| Fullscreen view | ⚠️ | N/A | Overlay viewer |
| Scroll hide nav | ✅ | ~5878 | Hide on scroll down |

### 2.6 Events Calendar

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| 2026 calendar | ✅ | ~59757 bytes | Full year |
| Filter by category | ✅ | ~6179 | `renderEventFilters()` |
| Filter by month | ✅ | ~6189 | `renderEventMonthFilters()` |
| Status indicators | ✅ | ~6262 | Ongoing/Upcoming/Finished |
| Event cards | ✅ | ~6234 | With all metadata |
| Event details | 📋 | ~6235 | "coming soon" |

### 2.7 User Profile

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Avatar display | ✅ | ~6290 | From account data |
| Name/Location | ✅ | ~6297 | Dynamic rendering |
| Tabs navigation | ✅ | ~3166 | Profile sections |
| Interests display | ✅ | ~6328 | Static pills |
| Add interest | 📋 | ~6328 | "coming soon" |
| Education display | ✅ | ~6334 | Static list |
| Add education | 📋 | ~6334 | "coming soon" |
| Notes summary | ⚠️ | N/A | Shows note count |
| Wallet display | ⚠️ | ~6370 | Shows balance |
| Wallet withdrawal | 📋 | ~6380 | "coming soon" |
| Wallet history | 📋 | ~6381 | "coming soon" |

---

## 3. TRUST & FAVOURITES

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Trust bar toggle | ✅ | ~5587 | `toggleTrust()` |
| Trusted list view | ✅ | N/A | Filtered directory |
| Favourite toggle | ✅ | ~5659 | `toggleBizFav()` |
| Trust tracking | ✅ | N/A | Via PulseUpdater |
| State persistence | ⚠️ | N/A | In memory only |

---

## 4. NOTES & ITEMS SYSTEM

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Notes list view | ⚠️ | N/A | Mock data only |
| Create note | 📋 | ~6423 | "coming soon" |
| Edit note | 📋 | N/A | Not implemented |
| Delete note | 📋 | N/A | Not implemented |
| Note levels | ⚠️ | ~6444 | Visual only |
| Create item | 📋 | ~6444 | "coming soon" |
| View items | 📋 | ~6450 | "coming soon" |
| Link item to note | 📋 | ~6882 | "coming soon" |

---

## 5. SUMS (Calculations)

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Sums page | ⚠️ | N/A | Placeholder UI |
| Create sum | 📋 | ~4789 | "coming soon" |
| Calculate totals | 📋 | N/A | Not implemented |
| Sum-to-note link | 📋 | N/A | Not implemented |

---

## 6. ENGAGEMENT FEATURES

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Engage button | 📋 | ~4233 | 10 instances, all "coming soon" |
| List Business | 📋 | ~4167 | "coming soon" |
| Push Promo | 📋 | ~4170 | "coming soon" |
| Share business | ⚠️ | ~5643 | Toast only |
| Contact actions | ⚠️ | ~5351 | Logs to Bothoflow only |

---

## 7. BOTH OFLOW PROTOCOL

### 7.1 PulseUpdater

| Feature | Status | File | Notes |
|---------|--------|------|-------|
| Visit logging | ✅ | PulseUpdater.js | `logVisit()` |
| Contact logging | ✅ | PulseUpdater.js | `logContact()` |
| Sentiment tracking | ✅ | PulseUpdater.js | `logSentiment()` |
| localStorage sync | ✅ | PulseUpdater.js | `sync()` |
| Session stats | ✅ | PulseUpdater.js | `getPulseStats()` |

### 7.2 CommissionEngine

| Feature | Status | File | Notes |
|---------|--------|------|-------|
| Base rate (0.5%) | ✅ | Commission_Engine.js | `BASE_RATE` |
| Designer rate (20%) | ✅ | Commission_Engine.js | `DESIGNER_RATE` |
| Trigger calculation | ✅ | Commission_Engine.js | `calculateTrigger()` |
| Event processing | ✅ | Commission_Engine.js | `processEvent()` |
| Actual payout | 📋 | N/A | Not implemented |

### 7.3 HistoryTracker

| Feature | Status | File | Notes |
|---------|--------|------|-------|
| Interaction logging | ✅ | HistoryTracker.js | `log()` |
| FIFO 88-item cap | ✅ | HistoryTracker.js | `MAX_ITEMS` |
| History retrieval | ✅ | HistoryTracker.js | `get()` |
| History clear | ✅ | HistoryTracker.js | `clear()` |
| Insights generation | ✅ | HistoryTracker.js | `getInsights()` |

### 7.4 PermissionsManager

| Feature | Status | File | Notes |
|---------|--------|------|-------|
| Capability checking | ✅ | PermissionsManager.js | `check()` |
| 9 role types | ✅ | PermissionsManager.js | `DEFAULT_CAPS` |
| UI visibility | ✅ | PermissionsManager.js | `getVisibility()` |
| Real-time updates | ⚠️ | index.html:~7148 | `updatePermissions()` |

---

## 8. USER ACCOUNTS

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Account switcher | ✅ | ~7116 | 10 mock accounts |
| Role-based UI | ✅ | ~7148 | Via PermissionsManager |
| Active account display | ✅ | ~6290 | Profile page |
| Account types | ✅ | ~7063 | 9 role types |
| Guest/Browser mode | ✅ | ~7065 | Read-only access |

---

## 9. WONDA (Community Polls)

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Poll questions | ✅ | ~7031 | 5 questions |
| Vote selection | ✅ | ~7054 | `voteWonda()` |
| Vote persistence | ⚠️ | ~7055 | In memory only |
| Results display | ⚠️ | ~7050 | Shows "You voted" |

---

## 10. NAVIGATION & UX

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Page stack navigation | ✅ | ~4954 | `showPage()` |
| Back button | ✅ | N/A | `goBack()` |
| Bottom nav bar | ✅ | ~276 | Main navigation |
| Menu overlay | ✅ | ~4586 | Full menu |
| Location filter modal | ⚠️ | N/A | Partial implementation |
| Toast notifications | ✅ | N/A | `showToast()` |
| History panel | ⚠️ | N/A | View only |

---

## 11. PWA & OFFLINE

| Feature | Status | Line | Notes |
|---------|--------|------|-------|
| Service Worker | ✅ | sw.js | Full offline support |
| App manifest | ✅ | manifest.json | Installable |
| Offline indicator | ✅ | N/A | In logo area |
| Asset caching | ⚠️ | sw.js | Only 8 assets |
| Data caching | ⚠️ | sw.js | Limited |

---

## 12. "COMING SOON" FEATURES (PLANNED)

### Priority 1 (HIGH)

| Feature | Location | Impact |
|---------|----------|--------|
| Engage Button | 10 pages | User engagement |
| List Business | 2 pages | Revenue feature |
| Push Promo | Add Action | Monetization |
| Wallet Withdrawal | Profile | Economy system |

### Priority 2 (MEDIUM)

| Feature | Location | Impact |
|---------|----------|--------|
| Create Note | Notes page | Core feature |
| Create Item | Items page | Core feature |
| Create Sum | Sums page | Core feature |
| Add Note to Sum | Sums page | Integration |
| Event Details | Events page | UX |
| Wallet History | Profile | Economy system |

### Priority 3 (LOW)

| Feature | Location | Impact |
|---------|----------|--------|
| Add Interest | Profile | Personalization |
| Add Education | Profile | Personalization |
| Share Business | Business profile | Virality |
| Contact Actions | Business profile | Core feature |

---

## 13. FEATURE IMPLEMENTATION TRACKING

### Phase 1: Core User Flow

- [x] Home page with search
- [x] Directory browsing
- [x] Business profiles
- [ ] Engage button functionality
- [ ] Real contact actions

### Phase 2: Content

- [x] Promotions viewer
- [x] Events calendar
- [ ] Event details modal
- [x] Mediums viewer
- [ ] Full media upload

### Phase 3: User Data

- [ ] Create/Edit/Delete notes
- [ ] Create/Edit/Delete items
- [ ] Sums calculations
- [ ] Profile customization

### Phase 4: Business Features

- [ ] List Business form
- [ ] Push Promo system
- [ ] Business dashboard
- [ ] Admin validation queue

### Phase 5: Economy

- [ ] Wallet withdrawal
- [ ] Commission tracking
- [ ] Designer payouts
- [ ] Payment integration

---

## 14. KNOWN BUGS

| Bug | Severity | Status | Notes |
|-----|----------|--------|-------|
| Engage buttons non-functional | HIGH | 📋 | All show "coming soon" |
| Location filter limited | MEDIUM | ⚠️ | Only Gaborone working |
| Notes CRUD incomplete | MEDIUM | 📋 | Display only |
| No real authentication | HIGH | 📋 | Mock accounts only |
| Service worker cache incomplete | LOW | ⚠️ | Missing many assets |

---

## 15. SUGGESTED FEATURES

| Feature | Priority | Notes |
|---------|----------|-------|
| Dark mode | MEDIUM | Not currently supported |
| Multiple languages | LOW | Only English |
| Push notifications | MEDIUM | Not implemented |
| User registration | HIGH | Currently mock only |
| Business dashboard | HIGH | Admin features needed |
| Analytics dashboard | MEDIUM | Track app usage |
| Export data | LOW | Download notes/history |
| Import data | LOW | Restore from backup |

---

**Document Version:** 1.0  
**Last Updated:** April 2026
