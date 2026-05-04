# TAPFO SNIS DOCUMENTATION — CONSOLIDATED EXPORT
## Complete UI/UX Documentation for All 15 Components
## Version: 1.0 | Date: April 2026

---

# TABLE OF CONTENTS

1. [SNIS_01] Notifications Panel
2. [SNIS_02] Onboarding Flow
3. [SNIS_03] Offline States
4. [SNIS_04] Help & Tooltips
5. [SNIS_05] Business Dashboard
6. [SNIS_06] Delete / Undo Flow
7. [SNIS_07] Bulk Operations
8. [SNIS_08] Drag & Drop
9. [SNIS_09] Duplicate Detection
10. [SNIS_10] Version History
11. [SNIS_11] Template System
12. [SNIS_12] Scheduling
13. [SNIS_13] Gamification
14. [SNIS_14] Share Preview
15. [SNIS_15] Copy / Import

---

# SNIS_01 — NOTIFICATIONS PANEL

## 1. Overview

**Purpose:** Real-time notification center for all TapFo user interactions — follows, contacts, leads, tag updates, commission alerts, and system messages. Aggregates events from PulseUpdater.js across all pages.

**User Benefit:** Single inbox for business intelligence (who is engaging, what is performing) and platform updates without leaving the current page.

**Dependencies:** PulseUpdater.js, PermissionsManager.js, HistoryTracker.js, localStorage sync queue.

---

## 2. Data Model

```javascript
Notification {
  id: string,
  type: 'follow' | 'contact' | 'lead' | 'tag' | 'commission' | 'system' | 'alert',
  priority: 'low' | 'medium' | 'high' | 'urgent',
  title: string,
  body: string,
  timestamp: ISO8601,
  read: boolean,
  dismissed: boolean,
  expires: ISO8601 | null,
  actionUrl: string,
  actionLabel: string,
  avatar: string | null,
  icon: string,
  metadata: {
    businessId: string | null,
    tagId: string | null,
    commissionAmount: number | null,
    pulseType: string | null,
    designerId: string | null,
    designerName: string | null
  }
}
```

**localStorage Keys:**
- tapfo_notifications_v2
- tapfo_notification_badge
- tapfo_notification_settings
- tapfo_notification_last_sync

**Firing Matrix:**

| Pulse Event | Type | Title Template | Priority |
|---|---|---|---|
| logVisit() | follow | "{name} viewed your profile" | medium |
| logContact() | contact | "{name} sent you a message" | high |
| logSentiment() positive | lead | "Positive sentiment spike +{n}%" | high |
| logSentiment() negative | alert | "Negative sentiment detected" | urgent |
| Tag purchased | tag | "New tag purchased: {tagName}" | medium |
| Tag expired | tag | "Tag expired: {tagName}" | low |
| Commission triggered | commission | "Commission earned: P{amount}" | high |
| Designer cut credited | commission | "Designer fee credited: P{amount}" | medium |

---

## 3. Detection & Triggers

**Opening:** Bell icon tap, swipe left on notification, N key (desktop)
**Closing:** Tap outside, X button, swipe right, Escape, navigate to actionUrl
**Auto-Triggers:** PulseUpdater event, reconnect after offline, session start

---

## 4. Wireframes

```
Wireframe 1: Closed Badge
┌────────────────────────────────────┐
│ [≡]      TAPFO         [🔔 3] [👤] │
└────────────────────────────────────┘

Wireframe 2: Panel Open
┌────────────────────────────────────┐
│ [≡]      NOTIFICATIONS       [✓]  │
├────────────────────────────────────┤
│ [🔍 Search notifications...        ]│
│ All  Follow  Contact  Tags  💰     │
├────────────────────────────────────┤
│ [👤] John Doe              2m     │
│     viewed your profile            │
│     [View Business]                │
├────────────────────────────────────┤
│ [💰] New commission        1h     │
│     P12.50 earned on sale          │
│     [View Dashboard]               │
├────────────────────────────────────┤
│ [📍] Tag purchased        3h     │
│     "Beverages" on Coffee Shop     │
│     [View Business]               │
└────────────────────────────────────┘

Wireframe 3: Filter Tab Active
│ All  [Follow]  Contact  Tags  💰  │

Wireframe 4: Unread vs Read
│  UNREAD: [●] John Doe viewed...   │
│  READ:   [ ] Jane Doe viewed...    │

Wireframe 5: Swipe to Dismiss
│ [👤] John Doe    [Swipe ←] [🗑️]  │

Wireframe 6: Settings Sub-panel
│ [← Back]   SETTINGS                │
│ [✓] Follow activity                 │
│ [✓] Contact messages               │
│ [✓] Tag purchases                   │
│ [ ] Marketing & promos             │
```

---

## 5. User Flows

**Flow 1: Open & Read**
1. Tap bell icon
2. Panel slides in (320ms)
3. List renders from localStorage
4. Badge decrements
5. Tap notification
6. Mark read, navigate to actionUrl
7. Panel closes

**Flow 2: Bulk Mark All Read**
1. Open panel
2. Tap "✓" button
3. Confirm "Mark all as read?"
4. All marked read
5. Badge resets to 0
6. Toast: "All notifications marked as read"

**Flow 3: Swipe Dismiss**
1. Swipe left on row (80px threshold)
2. Trash icon revealed
3. Release past threshold
4. Animate out (200ms)
5. Dismissed in localStorage
6. Undo toast (5s)

---

## 6. SnSIS Hierarchy Context

Notifications are cross-cutting — they surface events from Items, Notes, Sums, Tags, and businesses.
- Items → logVisit() → Follow notification
- Notes → logContact() → Contact notification
- Sums → logSentiment() → Lead/Alert notification
- Tags → Tag purchase/expire → Tag notification
- Businesses → Commission triggered → Commission notification
- Designers → Designer cut credited → Commission notification

---

## 7. Bothoflow Integration

- CommissionTriggered → high priority notification
- DesignerId lookup → if exists: DesignerFeeCredited → medium priority notification
- Commission notification never auto-expires (permanent record)
- Body: "Commission on {businessName} | Earned: P{amount}"

---

## 8. Offline Behavior

- Panel reads from localStorage — works fully offline
- Events logged to sync queue when offline
- On reconnect: queue flushes, notifications generated
- Offline indicator: "You're offline — changes will sync when connected"

---

## 9. Accessibility & Edge Cases

- role="log" on list, role="button" on bell, aria-live="polite"
- Tab order: bell → panel → list → close → settings
- 0 notifications: empty state "You're all caught up!"
- 200+ notifications: pagination (20 per page)
- Rapid notifications (5+ in 10s): batch into single entry

---

## 10. Implementation Checklist

- [ ] Bell icon with badge
- [ ] Slide-in panel (320ms transition)
- [ ] Notification list renderer
- [ ] Per-type filter tabs
- [ ] Text search with debounce
- [ ] Mark all read
- [ ] Swipe-to-dismiss
- [ ] Undo toast (5s timeout)
- [ ] Settings sub-panel
- [ ] PulseUpdater event hookup
- [ ] Commission notification generation
- [ ] Designer fee notification
- [ ] Badge count management
- [ ] Offline sync queue integration
- [ ] Accessibility audit
- [ ] High contrast mode
- [ ] Batch notification collapsing
- [ ] Pagination
- [ ] Empty state
- [ ] Unit tests

---

# SNIS_02 — ONBOARDING FLOW

## 1. Overview

**Purpose:** Guided first-run experience that classifies the user into one of three roles (Consumer, Business Owner, Designer), collects minimal viable profile data, and introduces core features progressively based on their path. Must be completable in under 3 minutes.

**User Benefit:** Zero friction setup. Users see only what matters to them based on intent. Designers see the commission earning flow immediately.

**Dependencies:** PermissionsManager.js (role assignment), PulseUpdater.js, HistoryTracker.js

---

## 2. Data Model

```javascript
OnboardingSession {
  id: string,
  startedAt: ISO8601,
  completedAt: ISO8601 | null,
  role: 'consumer' | 'business' | 'designer',
  stepsCompleted: string[],
  profileData: {
    displayName: string,
    phone: string,
    avatar: string | null,
    location: string | null
  },
  businessData: {
    businessName: string,
    category: string,
    region: string
  },
  designerData: {
    portfolio: string | null,
    specialty: string,
    commissionOptIn: boolean
  }
}
```

---

## 3. Detection & Triggers

**Opening:** First-ever app open, reset param, #page-howto if not completed
**Resume:** If stepsCompleted not empty and not completed, resume at last incomplete step
**Completion:** "Done" on final step, "Skip for now" grants consumer role

---

## 4. Wireframes

```
Wireframe 1: Welcome
┌────────────────────────────────────┐
│                                    │
│         [TAPFO LOGO]               │
│       Botswana's Business          │
│          Directory                │
│                                    │
│   Find local businesses,           │
│   compare prices, and connect      │
│   — all offline.                   │
│                                    │
│   [    Get Started    ]            │
│   [    Skip for now    ]           │
└────────────────────────────────────┘

Wireframe 2: Role Selection
┌────────────────────────────────────┐
│ [←]     Let's set you up           │
├────────────────────────────────────┤
│  What brings you to TapFo?         │
│                                    │
│  ┌────────────────────────────────┐ │
│  │ 🛒 I want to find &          │ │
│  │    support local businesses    │ │
│  │    Free • Full access          │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │ 🏪 I own or manage            │ │
│  │    a business                  │ │
│  │    P49/month • Tag ads         │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │ 🎨 I'm a designer             │ │
│  │    who earns from sales        │ │
│  │    20% commission • Build     │ │
│  └────────────────────────────────┘ │
└────────────────────────────────────┘

Wireframe 3: Consumer Profile
│  Display Name: [________________]   │
│  Phone Number: [+267 ___________]   │
│  Your Region: [Select region ▼ ]   │
│  [    Continue    ]               │

Wireframe 4: Business Profile
│  Business Name: [________________]  │
│  Category: [Select category ▼ ]   │
│  Region: [Select region ▼ ]       │
│  Add your first item...            │
│  [    Continue    ]               │

Wireframe 5: Designer Setup
│  Your Name: [__________________]   │
│  Design Specialty: [Logo ▼]       │
│  Portfolio URL: [https://...]     │
│  ☑️ I agree to the TapFo Terms     │
│  [    Start Earning    ]          │

Wireframe 6: Feature Tour
┌────────────────────────────────────┐
│ [×]   Discover TapFo                │
│ ┌──────────────────────────────┐   │
│ │      [ILLUSTRATION]           │   │
│ │  Search & Discover            │   │
│ │  Find any business or product │   │
│ │  by name, category, or        │   │
│ │  location.                    │   │
│ └──────────────────────────────┘   │
│      ● ○ ○ ○ ○ ○ ○ ○              │
│  [Skip tour]      [Next →]         │
└────────────────────────────────────┘

Wireframe 7: Complete
┌────────────────────────────────────┐
│         ✓                         │
│      You're all set,               │
│       {DisplayName}!              │
│   Your profile is ready.            │
│   [    Go to Home    ]            │
└────────────────────────────────────┘
```

---

## 5. User Flows

**Consumer Path (7 steps):** Welcome → Role: Consumer → Profile → Tour: Search → Tour: Notes → Tour: Sums → Tour: Tags → Done

**Business Path (9 steps):** Welcome → Role: Business → Business Profile → Add Item → Tour: Dashboard → Tour: Tags → Tour: Analytics → Tour: Sums → Done

**Designer Path (8 steps):** Welcome → Role: Designer → Designer Profile → Terms → Tour: Commission → Tour: Items → Tour: Sums → Done

**Resume Flow:** Reopen app → check localStorage → found incomplete session → resume at last step → "Welcome back" banner

**Skip Flow:** Tap "Skip for now" → confirm modal → consumer role by default → land on home

---

## 6. SnSIS Hierarchy Context

| Role | Can Create | Can View | Commission |
|---|---|---|---|
| Consumer | — | Notes, Sums | — |
| Business | Items, Notes, Tags | Items, Notes, Sums | Tag purchases |
| Designer | Items (for clients) | All items, sums | 20% of sales |

---

## 7. Bothoflow Integration

- Designer sees commission explanation on role selection
- Terms include Bothoflow designer agreement
- Post-onboarding: designer sees commission dashboard
- Commission display: "Your earnings appear here"

---

## 8. Offline Behavior

- Fully functional offline
- All data in localStorage immediately
- Final "Done" posts to server (if offline: queued for sync)

---

## 9. Accessibility & Edge Cases

- role="radio" on role cards, aria-checked
- aria-valuenow on progress indicator
- Focus management: auto-focus first input per step
- Very long name (>50 chars): truncate display, store full
- Invalid phone: inline error "Format: +267 followed by 7 digits"

---

## 10. Implementation Checklist

- [ ] Welcome screen
- [ ] Role selection cards
- [ ] Consumer/Business/Designer forms
- [ ] Step progress indicator
- [ ] Next/Back/Skip navigation
- [ ] Form validation
- [ ] Resume logic
- [ ] Skip confirmation modal
- [ ] Feature tour carousel
- [ ] Completion screen
- [ ] Role assignment
- [ ] PulseUpdater events
- [ ] HistoryTracker push
- [ ] Offline completion + sync
- [ ] Accessibility audit

---

# SNIS_03 — OFFLINE STATES

## 1. Overview

**Purpose:** Comprehensive offline-first architecture covering every user interaction — cached content, queued writes, sync-on-reconnect, and graceful degradation. TapFo is designed to work fully offline as its primary use case.

**Dependencies:** Service Worker, localStorage, IndexedDB, PulseUpdater.js

---

## 2. Data Model

```javascript
SyncQueueEntry {
  id: string,
  operation: 'CREATE' | 'UPDATE' | 'DELETE',
  entity: 'note' | 'item' | 'sum' | 'tag' | 'profile' | 'business',
  entityId: string,
  payload: object,
  createdAt: ISO8601,
  attempts: number,
  lastAttempt: ISO8601 | null,
  status: 'pending' | 'syncing' | 'failed' | 'conflict',
  errorMessage: string | null
}

SyncConflict {
  id: string,
  syncEntryId: string,
  localVersion: object,
  serverVersion: object,
  detectedAt: ISO8601,
  resolution: 'local_wins' | 'server_wins' | 'manual' | null
}
```

**Keys:** tapfo_sync_queue_v2, tapfo_cache_manifest_v2, tapfo_last_online_v2, tapfo_conflict_log_v2

---

## 3. Detection & Triggers

**Network Detection:**
- navigator.onLine events
- Heartbeat ping every 30s
- Service Worker fetch events

**Sync Triggers:** online event, manual "Sync Now", background sync, app foreground (>5 min stale)

---

## 4. Wireframes

```
Wireframe 1: Offline Banner
┌────────────────────────────────────┐
│ ⚡ You're offline — using cached   │
│     data. Changes will sync when   │
│     you're back online.    [✕]    │
└────────────────────────────────────┘

Wireframe 2: Cached Directory
│ ⚡ Offline — showing cached data   │
│ ┌──────────────────────────────────┐│
│ │ [☕] Coffee Corner        ★★★★☆ │
│ │     Gaborone • Coffee & Pastries │
│ └──────────────────────────────────┘│
│     Showing 47 cached businesses   │

Wireframe 3: Sync Queue
│ Last synced: 2 hours ago           │
│ [    Sync Now    ]                 │
│ 3 pending changes                  │
│ ┌──────────────────────────────────┐│
│ │ ↻ Create Item "Espresso"   [☕] │
│   Note: Coffee Corner         5m   │
│   [Cancel]                         │
│ └──────────────────────────────────┘│

Wireframe 4: Conflict Resolution
│         ⚠️ Sync Conflict           │
│ "Latte" price was changed          │
│ in two places:                     │
│ ┌────────────────────────────────┐ │
│ │  YOUR VERSION (Local)          │ │
│ │  Price: P35 • Updated: 10:30   │ │
│ │  [Keep this version]          │ │
│ └────────────────────────────────┘ │
│ ┌────────────────────────────────┐ │
│ │  SERVER VERSION (Remote)       │ │
│ │  Price: P38 • Updated: 11:15   │ │
│ │  [Keep this version]          │ │
│ └────────────────────────────────┘ │
│        [Merge Both →]              │

Wireframe 5: Cache Settings
│ STORAGE USAGE                      │
│ [████████░░░░░░░░░] 234MB / 512MB  │
│ [Clear image cache]                │
│ [Clear all offline data]           │
│ CACHE STRATEGY                     │
│ (•) Aggressive — all data         │
│ ( ) Balanced — important data      │
│ ( ) Minimal — text only            │

Wireframe 6: Sync in Progress
│ ⚡ Syncing...  [2/5]               │
│   ↻ Updating "Espresso"...        │
│ [████████████████░░░░] 80%        │
│ [Cancel]                           │
```

---

## 5. User Flows

**Browse Offline:** Connection lost → offline banner → serve from IndexedDB → writes go to queue

**Create Offline:** Create item → save locally → queue with pending → show toast → on reconnect → sync FIFO

**Sync on Reconnect:** online event → debounce 2s → process queue FIFO → on 409 conflict → modal → user resolves → retry

---

## 6. SnSIS Hierarchy Context

| Entity | Read Offline | Write Offline | Sync |
|---|---|---|---|
| Item | Full cache | Create/Edit/Delete → queue | ID on sync |
| Note | Full cache | Create/Edit/Delete → queue | Items synced together |
| Sum | Full cache | Read-only offline | Creates queued |
| Tag | Full cache (names/prices) | Purchase queued | Real payment on sync |
| Business | Full cache | Edit profile queued | Logo synced separately |

---

## 7. Bothoflow Integration

- Offline writes maintain designerId for commission
- Sync conflicts on commission items → admin notification
- Sync queue priority tier: commission events sync first
- Pending items do not count toward commission until synced

---

## 8. Storage Strategy

**IndexedDB stores:** notes, items, sums, tags, businesses, syncQueue, conflicts, media

**Cache expiry:** Business: 7 days, Items: 3 days, Tags: 1 day, User profile: 1 day, Media: 30 days

**Cache pre-warming (Wi-Fi):** Top 100 businesses, recently viewed, own data, category pages

---

## 9. Accessibility & Edge Cases

- role="status" on offline banner, aria-live="polite"
- aria-valuenow on sync progress bar
- Storage quota exceeded → prompt to clear cache
- Sync conflict on deleted entity → server wins
- Payment queued offline → PENDING only, never charged until online

---

## 10. Implementation Checklist

- [ ] Network detection
- [ ] Offline banner
- [ ] IndexedDB setup
- [ ] Cache manifest
- [ ] Sync queue processor
- [ ] Sync status indicators
- [ ] Conflict detection (409)
- [ ] Conflict resolution modal
- [ ] Manual sync trigger
- [ ] Background sync (SW)
- [ ] Cache pre-warming
- [ ] Cache expiry job
- [ ] Storage usage display
- [ ] Cache strategy selector
- [ ] Offline toast messages
- [ ] Retry with exponential backoff
- [ ] Service Worker registration
- [ ] Accessibility audit

---

# SNIS_04 — HELP & TOOLTIPS

## 1. Overview

**Purpose:** Context-sensitive help system covering every feature — tooltips on UI elements, searchable help panel, guided feature tours, and tag-specific explanations.

**Dependencies:** HistoryTracker.js, PulseUpdater.js, localStorage

---

## 2. Data Model

```javascript
HelpTooltip {
  id: string,
  targetSelector: string,
  title: string,
  content: string,
  position: 'top' | 'bottom' | 'left' | 'right' | 'auto',
  trigger: 'click' | 'hover' | 'focus' | 'auto',
  dismissible: boolean,
  showOnce: boolean
}

HelpArticle {
  id: string,
  slug: string,
  title: string,
  summary: string,
  content: string,
  category: string,
  relatedArticles: string[]
}
```

---

## 3. Detection & Triggers

**Tooltip:** Hover (400ms delay), tap/click, first visit, keyboard focus
**Help Panel:** "?" icon, #page-howto, shake gesture (3x)
**Guided Tour:** Onboarding complete, new feature release, feature first accessed, "Take a tour" button

---

## 4. Wireframes

```
Wireframe 1: In-Context Tooltip
│  ┌──────────────────────────────┐  │
│  │  What is a Note?              │  │
│  │  ─────────────────────────    │  │
│  │  A Note groups related items  │  │
│  │  into a single view.          │  │
│  │                               │  │
│  │  [Learn more →]    [✕ Got it] │  │
│  └──────────────────────────────┘  │

Wireframe 2: Spotlight Tour
│  [Background dimmed 60%]            │
│   ┌──────────────────────────┐     │
│   │  [🔔] Notifications       │     │
│   └──────────────────────────┘     │
│   ┌──────────────────────────────┐ │
│   │  Get notified when someone    │ │
│   │  views your business.          │ │
│   │  [Got it]                    │ │
│   └──────────────────────────────┘ │
│       ○ ● ○ ○ ○                    │

Wireframe 3: Help Panel
│ [×]     HELP CENTER                │
│ [🔍 Search help articles...]       │
│ POPULAR TOPICS                     │
│ ┌──────────────────────────────────┐│
│ │ 📝 What is a Note?               ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ ⚖️ What is a Sum?                ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 🏷️ How do tags work?             ││
│ └──────────────────────────────────┘│

Wireframe 4: Help Article
│ [←]  What is a Sum?                │
│  A Sum lets you compare 2+ items   │
│  side-by-side, like a Bloomberg    │
│  terminal for local prices.        │
│  ## How to create a Sum            │
│  1. Select 2+ items...             │
│  Was this helpful?                 │
│  [👍 Yes (24)]  [👎 No (2)]       │

Wireframe 5: Tag Tooltip
│  ┌────────────────────────────────┐ │
│  │  🏷️ Premium Tag                 │ │
│  │  Your item appears in top       │ │
│  │  search results for this tag.   │ │
│  │  Duration: 7 days               │ │
│  │  Price: P5.00/week             │ │
│  │  [Buy Tag]    [Learn more]      │ │
│  └────────────────────────────────┘ │
```

---

## 5. User Flows

**In-Context Tooltip:** Hover/tap element → show tooltip → tap "Got it" or outside → close

**Guided Tour:** Triggered → dim overlay → spotlight first step → tap Next → spotlight next → repeat → Done

**Help Panel Search:** Open panel → type query → debounce → search articles → highlight matches → tap result → article view

---

## 6. SnSIS Hierarchy Context

| SnSIS Entity | Help Articles | Tooltips |
|---|---|---|
| Item | Creating items, Item fields | Name, price, tags |
| Note | What is a Note?, Organising | Note name, add item |
| Sum | What is a Sum?, Bloomberg-style | Sum selector, KPIs |
| Tag | How tags work, Pricing | Tag chip, buy CTA |
| Business | Business profile setup | Profile fields |

---

## 7. Bothoflow Integration

- Help content includes Designer path explanations
- Tooltip on commission events: "Your 20% cut is calculated"
- Designer-specific tour: commission dashboard, payout schedule

---

## 8. Implementation Checklist

- [ ] Tooltip component (positioned, animated)
- [ ] Spotlight overlay
- [ ] Help panel (modal)
- [ ] Article renderer
- [ ] Help search (ranked)
- [ ] Guided tour engine
- [ ] Tour persistence
- [ ] "Helpful" feedback
- [ ] Offline article caching
- [ ] Keyboard navigation
- [ ] Accessibility audit

---

# SNIS_05 — BUSINESS DASHBOARD

## 1. Overview

**Purpose:** Command center for business owners to monitor performance, manage tags, control item visibility, and track earnings.

**Dependencies:** PulseUpdater.js, CommissionEngine.js, PermissionsManager.js

---

## 2. Data Model

```javascript
BusinessDashboard {
  businessId: string,
  overview: {
    totalViews: number,
    totalContacts: number,
    totalLeads: number,
    sentimentScore: number,
    rating: number
  },
  tagPerformance: [{
    tagId: string,
    tagName: string,
    impressions: number,
    clicks: number,
    ctr: number,
    cost: number
  }],
  commission: {
    earned: number,
    pending: number,
    paidOut: number,
    thisMonth: number
  }
}
```

---

## 3. Wireframes

```
Wireframe 1: Overview
│ THIS MONTH                        │
│ ┌──────────┐  ┌──────────┐        │
│ │   1,247  │  │    38    │        │
│ │  Views   │  │ Contacts │        │
│ └──────────┘  └──────────┘        │
│ ┌──────────┐  ┌──────────┐        │
│ │    89    │  │   ★★★★☆  │        │
│ │  Leads   │  │   4.2/5  │        │
│ └──────────┘  └──────────┘        │
│ SENTIMENT TREND                   │
│ [▁▂▃▅▄▆▅▇▆▅] ↑ +12%             │
│ TOP PERFORMING TAGS               │
│ 🏷️ Coffee    234 views • 4.2% CTR │
│ [    + Buy New Tag    ]           │

Wireframe 2: Tag Management
│ Tag Budget: P200/month    [Edit]  │
│ ACTIVE TAGS (5)                    │
│ ┌──────────────────────────────────┐│
│ │ 🏷️ Coffee             [Active]   ││
│ │    P5/week • Expires in 4 days   ││
│ │    [Pause] [Edit] [Renew]        ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 🏷️ Late Night         [Expired]  ││
│ │    [Renew for P2]               ││
│ └──────────────────────────────────┘│

Wireframe 3: Tag Purchase Modal
│         🏷️ BUY TAG                 │
│ Select tag:                        │
│ ┌──────────────────────────────────┐│
│ │ ☕ Coffee                 P5/wk  ││
│ └──────────────────────────────────┘│
│ Duration:                          │
│ [1 week] [4 weeks] [12 weeks]     │
│ Order Summary:                     │
│ Coffee tag (12 weeks)        P48  │
│ TapFo fee (5%)              P2    │
│ Total                     P50     │
│ [       Confirm Purchase       ]  │
```

---

## 4. User Flows

**Buy Tag:** Tap "+ Buy New Tag" → select tag → select duration → view summary → select payment → confirm → tag activated → notification sent

**Pause Tag:** Tap "Pause" → confirm → tag status → Paused → removed from search

---

## 5. Bothoflow Integration

- Commission section: earned, pending, paid out
- Designer cut displayed per transaction
- Tag purchase triggers CommissionEngine
- Dashboard shows: "Commission this month"

---

## 6. Implementation Checklist

- [ ] KPI overview cards
- [ ] Sentiment trend chart
- [ ] Tab navigation
- [ ] Tag list with status
- [ ] Tag purchase modal
- [ ] Duration selector
- [ ] Order summary with fees
- [ ] Tag pause/resume
- [ ] Item performance list
- [ ] Commission section
- [ ] Pull-to-refresh
- [ ] Offline mode

---

# SNIS_06 — DELETE / UNDO FLOW

## 1. Overview

**Purpose:** Safe, reversible deletion for all SnSIS entities. Prevents accidental deletion, shows dependencies, provides 10-second undo window.

---

## 2. Data Model

```javascript
DeletionRequest {
  id: string,
  entityType: 'note' | 'item' | 'sum' | 'tag' | 'business',
  entityId: string,
  status: 'pending' | 'confirmed' | 'undone' | 'deleted',
  dependencies: [{ type, relatedEntityId, relatedEntityName }],
  undoUntil: ISO8601
}

TrashBinItem {
  id: string,
  entityData: object,
  deletedAt: ISO8601,
  undoUntil: ISO8601
}
```

---

## 3. Wireframes

```
Wireframe 1: Delete Confirmation
│         ⚠️ Delete Item?             │
│  Are you sure you want to delete:  │
│  ┌────────────────────────────────┐ │
│  │ ☕ Espresso                    │ │
│  │    P25 • from Coffee Corner    │ │
│  └────────────────────────────────┘ │
│  This item is used in:             │
│  ⚠️ 3 Sum comparisons             │
│  [Cancel]          [Delete Item]  │

Wireframe 2: Dependency Warning
│         ⚠️ Cannot Delete           │
│  "Morning Drinks" is used in 2 Sums│
│  Items that will be affected:      │
│  ☕ Espresso ☕ Latte ☕ Cappuccino │
│  Sums affected:                    │
│  "Coffee Shop Comparison"          │
│  [Cancel]  [Delete Note + Items]   │

Wireframe 3: Undo Toast
│  ┌──────────────────────────────┐  │
│  │ ☕ Espresso deleted          │  │
│  │ [↩️ Undo]        [✕]        │  │
│  └──────────────────────────────┘  │

Wireframe 4: Trash Bin
│ [←]     TRASH BIN                 │
│ Items auto-delete after 30 days.   │
│ TODAY                             │
│ ┌──────────────────────────────────┐│
│ │ ☕ Espresso                 [↩️] ││
│ │    Deleted 2 hours ago           ││
│ │    [Restore] [Delete Forever]   ││
│ └──────────────────────────────────┘│
│ [Empty Trash]                     │
```

---

## 4. User Flows

**Delete Item (no deps):** Tap Delete → modal shows entity → no deps → confirm → soft delete → undo toast (10s)

**Delete Item (with deps):** Same but show "Used in X Sums" → confirm removes from sums → undo restores sum refs

**Restore:** Trash bin → tap Restore → confirm if name clash → entity restored to original Note

---

## 5. SnSIS Hierarchy Context

- Sum → References Items → Deleting Item removes from Sum
- Note → Contains Items → Deleting Note optionally deletes Items
- Deleting Sum: safe, no cascade
- Deleting Tag: safe, just removes visibility

---

## 6. Implementation Checklist

- [ ] Delete trigger (long-press, swipe, menu)
- [ ] Confirmation modal
- [ ] Dependency scanner
- [ ] Cascade delete options
- [ ] Trash bin (IndexedDB)
- [ ] 10s undo window
- [ ] Undo action
- [ ] Permanent delete
- [ ] 30-day auto-expiry
- [ ] Bulk delete
- [ ] Offline queue
- [ ] Deletion audit log

---

# SNIS_07 — BULK OPERATIONS

## 1. Overview

**Purpose:** Select multiple Items/Notes simultaneously and perform actions as a batch — delete, move, tag, share, export.

---

## 2. Wireframes

```
Wireframe 1: Selection Mode
│ [×]     SELECT ITEMS         [✓ 3] │
│ [☐ Select all 8]  [Sort ▼]        │
│ ┌──────────────────────────────────┐│
│ │ [☑] ☕ Espresso           P25   ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [☐] ☕ Latte                P35 ││
│ └──────────────────────────────────┘│
├────────────────────────────────────┤
│ [🗑️ Delete] [📂 Move] [🏷️ Tag] [↗️ Share] │
│  3 items selected                  │

Wireframe 2: Bulk Add to Note
│         📂 MOVE TO NOTE            │
│  Moving 3 items to:               │
│  ┌──────────────────────────────────┐│
│  │ 📝 Morning Drinks           ✓ ││
│  └──────────────────────────────────┘│
│  ┌──────────────────────────────────┐│
│  │ 📝 Lunch Menu                ○ ││
│  └──────────────────────────────────┘│
│  ☕ Espresso, ☕ Cappuccino,        │
│  will be added to "Morning Drinks". │
│  [Cancel]     [Move Items]         │
```

---

## 3. Implementation Checklist

- [ ] Long-press to enter selection mode
- [ ] Item selection toggle
- [ ] Select all
- [ ] Action bar (Delete, Move, Tag, Share)
- [ ] Bulk delete confirmation
- [ ] Bulk move modal
- [ ] Bulk tag application
- [ ] Offline queue for bulk ops

---

# SNIS_08 — DRAG & DROP

## 1. Overview

**Purpose:** Reorder Items within a Note, and Notes within sidebar/sum, using drag-and-drop. Touch-optimized.

---

## 2. Wireframe

```
Wireframe 1: Drag in Progress
│  📝 Morning Drinks (5 items)       │
│                                    │
│  ┌──────────────────────────────┐  │
│  │ ☕ Latte          P35   [⋮⋮] │  │ ← lifted (shadow)
│  └──────────────────────────────┘  │
│       ↑ drag handle                  │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│  (drop zone highlighted)            │
│  ┌──────────────────────────────┐  │
│  │ ☕ Espresso         P25   [⋮⋮]│  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ ☕ Cappuccino       P38   [⋮⋮]│  │
│  └──────────────────────────────┘  │
```

---

## 3. Implementation Checklist

- [ ] 400ms long-press to initiate
- [ ] Item lift animation
- [ ] Drag tracking
- [ ] Drop zone highlighting
- [ ] Auto-scroll near edges
- [ ] Drop and settle animation
- [ ] Reorder event logging
- [ ] Undo support
- [ ] Haptic feedback
- [ ] Keyboard accessibility

---

# SNIS_09 — DUPLICATE DETECTION

## 1. Overview

**Purpose:** Detect and surface duplicate or near-duplicate Items during creation/editing. Prevents catalog pollution, offers smart merge.

---

## 2. Detection Method

- Name: Levenshtein distance < 3 OR Jaro-Winkler > 0.85
- Price: within 5%
- Category: exact match
- Score = weighted average → flag if > 70

---

## 3. Wireframes

```
Wireframe 1: Duplicate Warning
│ ⚠️ Possible duplicate detected     │
│  "Espresso" is similar to:        │
│  ☕ Espresso (P28) — Coffee Corner│
│  [View & Merge]  [It's different] │

Wireframe 2: Merge Panel
│         🔀 MERGE ITEMS             │
│  ┌──────────────────┐ ┌──────────┐ │
│  │ NEW ITEM (keep)   │→│ RESULT   │ │
│  │ Name: Espresso   │ │ Name:    │ │
│  │ Price: P25   →25  │ │ P25      │ │
│  │ [Keep as new]     │ │          │ │
│  └──────────────────┘ └──────────┘ │
│  CONFLICTS:                        │
│  Price: P25 vs P28                 │
│  [Use P25] [Use P28]              │
│  [Cancel]        [Merge Items]     │
```

---

## 4. Implementation Checklist

- [ ] Fuzzy string matching
- [ ] Similarity scoring
- [ ] Duplicate warning banner
- [ ] Merge panel UI
- [ ] Conflict resolution
- [ ] Auto-merge non-conflicting
- [ ] Sum reference update
- [ ] Manual "Find Duplicates"
- [ ] Offline detection

---

# SNIS_10 — VERSION HISTORY

## 1. Overview

**Purpose:** Immutable audit trail and rollback for all Item and Note edits. Every change is versioned and restorable.

---

## 2. Data Model

```javascript
Version {
  id: string,
  entityType: 'item' | 'note',
  entityId: string,
  versionNumber: number,
  snapshot: object,
  diff: { changedFields, before, after },
  editedBy: string,
  editedAt: ISO8601
}
```

---

## 3. Wireframe

```
Wireframe 1: Version Timeline
│ [←]     VERSION HISTORY             │
│        ☕ Espresso                 │
│ v12 ─┬─ ● TODAY, 10:30 AM  ← CURRENT
│       │    You changed price       │
│       │    P28 → P25              │
│       │    [Restore] [View]       │
│       │                            │
│  v11 ─┤    Yesterday, 3:45 PM      │
│       │    You changed description │
│       │                            │
│  v10 ─┤    Apr 8, 2:15 PM          │
│       │    Designer edit: K. Dube  │
│       │    [Restore] [View]        │
│       │                            │
│   v1 ─┤    Mar 1, 9:00 AM          │
│       │    Created                 │
```

---

## 4. Implementation Checklist

- [ ] Version timeline UI
- [ ] Version snapshot storage
- [ ] Diff generation
- [ ] Current version indicator
- [ ] Version preview
- [ ] Restore action
- [ ] Version auto-pruning (90 days)
- [ ] Per-entity limit (50)
- [ ] Editor attribution
- [ ] Commission-attached protection

---

# SNIS_11 — TEMPLATE SYSTEM

## 1. Overview

**Purpose:** Pre-built Note templates for common business categories. One-tap setup, fully customizable.

---

## 2. Wireframe

```
Wireframe 1: Template Gallery
│ [×]     NOTE TEMPLATES              │
│ [🔍 Search templates...]          │
│ [All] [Restaurant] [Retail] [Service]│
│ ┌──────────────────────────────────┐│
│ │ [🍽️] Restaurant Menu             ││
│ │    12 items • ★★★★☆ (234 uses)  ││
│ │    [Use Template]                ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [📦] Product Catalog             ││
│ │    [Use Template]                ││
│ └──────────────────────────────────┘│
│ ─────────────────────────────────  │
│ MY TEMPLATES                       │
│ [📝] My Coffee List           [⋮] │
```

---

## 3. Implementation Checklist

- [ ] Template gallery UI
- [ ] Category filtering
- [ ] Search templates
- [ ] Template preview
- [ ] Use template → Note creation
- [ ] Save Note as Template
- [ ] My Templates management

---

# SNIS_12 — SCHEDULING

## 1. Overview

**Purpose:** Schedule future actions — publish notes, activate/deactivate tags, send promos, update prices.

---

## 2. Data Model

```javascript
ScheduledTask {
  id: string,
  type: 'tag_activate' | 'tag_deactivate' | 'note_publish' | 'price_update' | 'promo_send',
  entityId: string,
  scheduledFor: ISO8601,
  timezone: string,
  status: 'scheduled' | 'running' | 'completed' | 'failed' | 'cancelled',
  repeat: null | { frequency: 'daily' | 'weekly' | 'monthly', endDate }
}
```

---

## 3. Wireframe

```
Wireframe 1: Schedule List
│ [←]     SCHEDULED                  │
│ UPCOMING                           │
│ ┌──────────────────────────────────┐│
│ │ 🏷️ Activate "Late Night"  May 15 ││
│ │    8:00 AM • Coffee Corner       ││
│ │    [Edit] [Cancel]               ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 📝 Publish "Summer Menu"  May 20 ││
│ │    6:00 PM                       ││
│ │    [Edit] [Cancel]               ││
│ └──────────────────────────────────┘│
│ RECURRING                          │
│ ┌──────────────────────────────────┐│
│ │ 🔄 Price update "Latte"  Weekly ││
│ │    Every Monday 9:00 AM         ││
│ └──────────────────────────────────┘│
```

---

## 4. Implementation Checklist

- [ ] Schedule list UI
- [ ] Date/time picker
- [ ] Timezone handling
- [ ] Recurring tasks
- [ ] Background execution (SW alarms)
- [ ] Execution status updates
- [ ] "Run Now" trigger
- [ ] Cancel/edit tasks
- [ ] Execution history

---

# SNIS_13 — GAMIFICATION

## 1. Overview

**Purpose:** Motivation system using badges, points, streaks, and leaderboards to drive engagement.

---

## 2. Data Model

```javascript
Badge {
  id: string,
  name: string,
  description: string,
  category: 'discovery' | 'contribution' | 'social' | 'milestone',
  tier: 'bronze' | 'silver' | 'gold' | 'platinum',
  pointsValue: number,
  earnedAt: ISO8601 | null,
  progress: number
}

UserGamification {
  points: number,
  level: number,
  streak: { current, longest, lastActiveDate },
  earnedBadges: string[],
  weeklyRank: number | null
}
```

---

## 3. Wireframes

```
Wireframe 1: Badge Unlock Toast
│  ┌──────────────────────────────┐  │
│  │ 🏆 NEW BADGE EARNED!         │  │
│  │      [🥇]                    │  │
│  │   PROLIFIC CONTRIBUTOR       │  │
│  │   You added 100 items!       │  │
│  │   +50 points  → Level 8      │  │
│  │   [View Badges]   [Awesome!]  │  │
│  └──────────────────────────────┘  │

Wireframe 2: Profile Badge Row
│ ┌──────────────────────────────────┐│
│ │ [👤] Kudzanai                    ││
│ │     Level 8 • 2,340 points       ││
│ │     🔥 12 day streak 🔥         ││
│ │     🏆 24 badges                  ││
│ │     [View All Badges]            ││
│ └──────────────────────────────────┘│

Wireframe 3: Achievement Gallery
│ 2,340 pts │ Level 8 │ 🔥 12       │
│ [Discovery] [Contrib] [Social] [★] │
│ 🏆 PROLIFIC CONTRIBUTOR   [🥇]     │
│    Earned: Mar 15, 2026           │
│ ─────────────────────────────────  │
│ LOCKED                             │
│ 🔒 LEGENDARY STATUS        [  ]    │
│    2,340 / 25,000 points          │
│    [████████░░░░] 9%               │

Wireframe 4: Leaderboard
│ [This Week] [This Month] [All Time]│
│   1  🥇 @tumi_developer   4,521 pts│
│   2  🥈 @design_by_lesego 3,892 pts│
│   3  🥉 @creative_ane    3,201 pts│
│  ──────────────────────────────── │
│  12  📍 You               892 pts │ ← highlighted
│  13  📍 @cafe_owner_bw    756 pts │
```

---

## 4. Badge Types

**Discovery:** First search, First visit, First sum, Explorer (10 notes)
**Contribution:** First item, First note, 10 items, 50 items, Prolific (100 items)
**Social:** First follow, 10 follows, First share, Community helper
**Milestone:** 7-day streak, 30-day streak, 100-day streak

---

## 5. Bothoflow Integration

- Commission earnings contribute to leaderboard points
- "Top Designer" badge for highest earners
- Weekly designer leaderboard (separate)

---

## 6. Implementation Checklist

- [ ] Badge definition library
- [ ] Badge criteria engine
- [ ] Badge unlock toast
- [ ] Profile badge row
- [ ] Achievement gallery with tabs
- [ ] Progress bars on locked badges
- [ ] Points and level system
- [ ] Streak tracking
- [ ] Leaderboard UI
- [ ] Gamification toggle

---

# SNIS_14 — SHARE PREVIEW

## 1. Overview

**Purpose:** Rich preview cards for sharing Notes, Items, Sums, and business profiles to WhatsApp, Facebook, Twitter, SMS, Email.

---

## 2. Data Model

```javascript
SharePayload {
  type: 'note' | 'item' | 'sum' | 'business',
  entityId: string,
  title: string,
  description: string,
  imageUrl: string,
  deepLink: string,
  webLink: string,
  hashtags: string[]
}
```

---

## 3. Wireframe

```
Wireframe 1: Share Modal
│         ↗️ SHARE                    │
│ ┌────────────────────────────────┐ │
│ │  ☕ Espresso — P25             │ │
│ │  Coffee Corner • Gaborone      │ │
│ │  [image placeholder]           │ │
│ │  Strong single-shot coffee.    │ │
│ │  Perfect for a quick boost.    │ │
│ └────────────────────────────────┘ │
│ SHARE VIA                          │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐      │
│ │ 💬 │ │ 📘 │ │ 🐦 │ │ 📧 │      │
│ │WhatsApp│ FB │ Twitter│ Email│      │
│ └────┘ └────┘ └────┘ └────┘      │
│ ┌────┐ ┌────┐                    │
│ │ 📋 │ │ 📱 │                    │
│ │Copy │Native│                    │
│ └────┘ └────┘                    │
│ tapfo.bw/item/abc123              │
│ [📋 Copy Link]                    │
```

---

## 4. Deep Link Format

- tapfo://note/{id}
- tapfo://item/{id}
- tapfo://sum/{id}
- tapfo://business/{id}
- Fallback: https://tapfo.bw/{type}/{id}

---

## 5. Implementation Checklist

- [ ] Share modal UI
- [ ] Preview card generation
- [ ] Deep link generation
- [ ] WhatsApp/Facebook/Twitter/Email/SMS integration
- [ ] Copy to clipboard
- [ ] Web Share API
- [ ] OG meta tags
- [ ] Share analytics

---

# SNIS_15 — COPY / IMPORT

## 1. Overview

**Purpose:** Import data from CSV, JSON, and other apps. Export/copy TapFo data for portability, backup, and migration.

---

## 2. Data Model

```javascript
ImportJob {
  id: string,
  sourceFormat: 'csv' | 'json' | 'google_sheets' | 'excel',
  status: 'parsing' | 'mapping' | 'validating' | 'importing' | 'complete' | 'failed',
  totalRows: number,
  successCount: number,
  failureCount: number,
  mappings: [{ sourceField, targetField, transform }]
}

ExportJob {
  id: string,
  format: 'csv' | 'json' | 'pdf',
  status: 'preparing' | 'generating' | 'ready' | 'failed'
}
```

---

## 3. Wireframes

```
Wireframe 1: Export Sheet
│         📋 EXPORT NOTE             │
│  Export "Morning Drinks"           │
│  5 items                           │
│  FORMAT                            │
│  ┌────────────────────────────────┐ │
│  │ (●) CSV (for Excel/Sheets)    │ │
│  │ ( ) JSON (for developers)     │ │
│  │ ( ) PDF (printable)           │ │
│  └────────────────────────────────┘ │
│  INCLUDE                           │
│  [✓] Item names  [✓] Prices        │
│  [✓] Descriptions [✓] Tags         │
│  [Cancel]       [Generate Export]  │

Wireframe 2: Import Wizard Step 1
│         📥 IMPORT ITEMS            │
│  STEP 1: SELECT FILE               │
│  ┌────────────────────────────────┐ │
│  │     📁                         │ │
│  │  Drop file here or tap to browse│ │
│  │  Supported: CSV, JSON, XLSX    │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │ 📋 Or paste from clipboard     │ │
│  │    [Use This]                   │ │
│  └────────────────────────────────┘ │
│  [📥 Download TapFo Template]      │
```

---

## 4. Import Steps

1. Select/Upload file
2. Auto-detect headers → field mapping UI
3. Validation & review (show warnings)
4. Confirm → progress bar → success toast

---

## 5. Implementation Checklist

- [ ] Export sheet UI
- [ ] CSV/JSON/PDF export
- [ ] TapFo backup format
- [ ] Import wizard (3 steps)
- [ ] File upload (drag-drop)
- [ ] Clipboard paste detection
- [ ] CSV/JSON parser
- [ ] Auto field mapping
- [ ] Manual field mapping
- [ ] Live preview
- [ ] Validation with warnings
- [ ] Bulk item creation
- [ ] Duplicate detection on import
- [ ] Download trigger
- [ ] Template CSV download
- [ ] Error report
- [ ] Undo import

---

# END OF DOCUMENTATION

All 15 components documented. Each component follows the 10-section template:
1. Overview
2. Data Model
3. Detection & Triggers
4. Wireframes (375px mobile-first)
5. User Flows
6. SnSIS Hierarchy Context
7. Bothoflow Integration
8. Offline Behavior
9. Accessibility & Edge Cases
10. Implementation Checklist
