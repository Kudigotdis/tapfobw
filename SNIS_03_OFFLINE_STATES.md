# SNIS_03 — Offline States

## 1. Overview

**Purpose:** Comprehensive offline-first architecture covering every user interaction — cached content, queued writes, sync-on-reconnect, and graceful degradation. TapFo is designed to work fully offline as its primary use case (Botswana's intermittent connectivity).

**User Benefit:** Users can browse the full directory, create notes/items, manage tags, and queue updates without internet. Everything syncs seamlessly when connectivity returns.

**Dependencies:** Service Worker, `localStorage`, `IndexedDB`, `PulseUpdater.js` (sync events), `HistoryTracker.js`.

---

## 2. Data Model

### Sync Queue Entry
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
```

### Conflict Record
```javascript
SyncConflict {
  id: string,
  syncEntryId: string,
  localVersion: object,
  serverVersion: object,
  detectedAt: ISO8601,
  resolution: 'local_wins' | 'server_wins' | 'manual' | null
}
```

### Cached Entity
```javascript
CachedEntity {
  entityId: string,
  entityType: string,
  data: object,
  cachedAt: ISO8601,
  expiresAt: ISO8601,
  version: number,
  isDirty: boolean
}
```

**localStorage / IndexedDB Keys:**
- `tapfo_sync_queue_v2` — array of `SyncQueueEntry` (IndexedDB for performance)
- `tapfo_cache_manifest_v2` — metadata for all cached entities
- `tapfo_last_online_v2` — ISO8601 of last successful sync
- `tapfo_conflict_log_v2` — array of `SyncConflict`
- `tapfo_network_status_v2` — 'online' | 'offline'
- `tapfo_cache_strategy_v2` — 'aggressive' | 'balanced' | 'minimal'

---

## 3. Detection & Triggers

### Network Detection
```javascript
// Primary: Navigator.onLine
window.addEventListener('online', onNetwork恢复);
window.addEventListener('offline', onNetworkLoss);

// Secondary: Heartbeat ping every 30s
fetch('/api/ping', {timeout: 5000})
  .then(() => status = 'online')
  .catch(() => status = 'offline');

// Tertiary: Service Worker lifecycle
self.addEventListener('online', ...);
self.addEventListener('offline', ...);
```

### Offline Mode Triggers
- `navigator.onLine === false`
- Heartbeat ping fails 3 consecutive times
- Service Worker `fetch` event catches a network failure

### Sync Triggers
- Network restored (`online` event)
- Manual "Sync Now" tap
- Background sync (Service Worker)
- App foreground after >5 minutes background
- Every 30 minutes if app is open

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Offline Banner (Top)
```
┌────────────────────────────────────┐
│ ⚡ You're offline — using cached   │  ← yellow/amber banner, 44px height
│     data. Changes will sync when   │  ← 2 lines max, dismissible
│     you're back online.    [✕]     │
└────────────────────────────────────┘
│                                    │
│ [Cached content displays normally   │
│  below the banner]                 │
└────────────────────────────────────┘
```

### Wireframe 2: Cached Directory (Business Listing)
```
┌────────────────────────────────────┐
│ [≡]   BUSINESS DIRECTORY    [🔍]  │
├────────────────────────────────────┤
│ ⚡ Offline — showing cached data   │  ← amber indicator
│ ┌──────────────────────────────────┐│
│ │ [☕] Coffee Corner        ★★★★☆ ││
│ │     Gaborone • Coffee & Pastries ││
│ │     P45 avg • 1.2km away        ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [🍔] Burger Joint        ★★★★☆  ││
│ │     Francistown • Burgers        ││
│ │     P85 avg • 3.5km away        ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [🥗] Fresh Salads         ★★★☆☆ ││
│ │     Gaborone • Healthy Food      ││
│ │     P60 avg • 4.1km away        ││
│ └──────────────────────────────────┘│
│     Showing 47 cached businesses   │
└────────────────────────────────────┘
```

### Wireframe 3: Sync Queue Panel
```
┌────────────────────────────────────┐
│ [≡]        SYNC QUEUE              │
├────────────────────────────────────┤
│ Last synced: 2 hours ago           │
│ [    Sync Now    ]                 │  ← manual trigger
│                                    │
│ 3 pending changes                  │
│                                    │
│ ┌──────────────────────────────────┐│
│ │ ↻ Create Item "Espresso"   [☕]  ││
│   Note: Coffee Corner         5m   │
│   Status: ⏳ Pending               ││
│   [Cancel]                         ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ ↻ Update Price "Latte"       [☕]││
│   Note: Coffee Corner         12m  │
│   Status: ⏳ Pending               ││
│   [Cancel]                         ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ ↻ Delete Item "Decaf"        [☕]││
│   Note: Coffee Corner         1h    │
│   Status: ⚠️ Failed — tap to retry ││
│   [Retry] [Cancel]                 ││
│ └──────────────────────────────────┘│
│                                    │
│ ⚠️ Sync failed: "Server unreachable"│
│    Will retry automatically         │
└────────────────────────────────────┘
```

### Wireframe 4: Conflict Resolution Modal
```
┌────────────────────────────────────┐
│         ⚠️ Sync Conflict           │
├────────────────────────────────────┤
│                                    │
│ "Latte" price was changed          │
│ in two places:                     │
│                                    │
│ ┌────────────────────────────────┐ │
│ │  YOUR VERSION (Local)          │ │
│ │  ────────────────────────      │ │
│ │  Price: P35                    │ │
│ │  Updated: 10:30 AM             │ │
│ │  [Keep this version]           │ │
│ └────────────────────────────────┘ │
│                                    │
│ ┌────────────────────────────────┐ │
│ │  SERVER VERSION (Remote)       │ │
│ │  ────────────────────────      │ │
│ │  Price: P38                    │ │
│ │  Updated: 11:15 AM by you      │ │
│ │  [Keep this version]           │ │
│ └────────────────────────────────┘ │
│                                    │
│        [Merge Both →]              │  ← smart merge option
│                                    │
└────────────────────────────────────┘
```

### Wireframe 5: Cache Settings
```
│ [← Back]   STORAGE & SYNC          │
├────────────────────────────────────┤
│ STORAGE USAGE                      │
│                                    │
│ [████████░░░░░░░░░] 234MB / 512MB  │
│                                    │
│ TapFo data: 180MB                  │
│ Images: 48MB                       │
│ Offline pages: 6MB                 │
│                                    │
│ [Clear image cache]                │
│ [Clear old pages]                 │
│ [Clear all offline data]           │
│                                    │
│ CACHE STRATEGY                     │
│ (•) Aggressive — all data         │  ← default for frequent users
│ ( ) Balanced — important data     │
│ ( ) Minimal — text only            │
│                                    │
│ SYNC SETTINGS                      │
│ [✓] Auto-sync on Wi-Fi             │
│ [✓] Background sync                │
│ [ ] Sync on mobile data            │
│                                    │
│ Last synced: Today at 10:30 AM     │
└────────────────────────────────────┘
```

### Wireframe 6: Sync in Progress Indicator
```
┌────────────────────────────────────┐
│ ⚡ Syncing...  [2/5]               │  ← progress bar + fraction
│   ↻ Updating "Espresso"...        │
│                                    │
│ [████████████████░░░░] 80%          │
│                                    │
│ [Cancel]                           │  ← cancel sync (leaves queued)
└────────────────────────────────────┘
```

---

## 5. User Flows

### Flow 1: Browse While Offline
1. User loses connection (or starts app offline)
2. Network detection fires → offline banner appears
3. App serves all data from IndexedDB cache
4. User can browse businesses, items, notes, sums
5. Any write operation goes to sync queue
6. Cached data shows "last updated X ago" timestamp
7. User can read all cached content normally

### Flow 2: Create Content While Offline
1. User creates an Item (or Note, or updates profile)
2. Operation immediately saved to local DB
3. Entry added to sync queue with `status: pending`
4. UI shows "Saved — will sync when online" toast
5. Item appears in local UI immediately
6. Sync icon shown next to item (indicating pending sync)
7. If user navigates away and back, item still visible (local)
8. On reconnect: sync queue processes in order (FIFO)
9. Server assigns final ID, propagates to other users

### Flow 3: Sync on Reconnect
1. `online` event fires
2. Wait 2 seconds (debounce flapping connections)
3. Show "Syncing..." banner
4. Process sync queue: FIFO order
5. For each entry: POST to server → wait for response
6. On success: remove from queue, update local with server response
7. On failure: increment `attempts`, set `status: failed`, retry later
8. After queue empty: show "Synced successfully" toast
9. Update `lastOnline` timestamp

### Flow 4: Conflict Resolution
1. Sync entry returns 409 Conflict
2. Fetch server version
3. Create `SyncConflict` record
4. Show conflict modal to user
5. User picks local/server/merge
6. Apply chosen resolution
7. Re-submit with version header
8. On success: resolve conflict, remove from queue
9. On merge: apply both changes, mark non-conflicting fields auto-resolved

### Flow 5: Background Sync
1. Service Worker registers for background sync
2. User makes offline change
3. Sync queued in Service Worker
4. When online, Service Worker processes queue
5. Main app receives message: "Sync complete"
6. UI updates to reflect synced state

---

## 6. SnSIS Hierarchy Context

**Offline Impact by Entity:**

| Entity | Read Offline | Write Offline | Sync Behavior |
|---|---|---|---|
| Item | Full cache | Create/Edit/Delete → queue | ID assigned on sync |
| Note | Full cache | Create/Edit/Delete → queue | Items in note synced together |
| Sum | Full cache | Read-only offline | Creates queued, compares cached data |
| Tag | Full cache (names/prices) | Purchase queued | Real payment on sync |
| Business | Full cache | Edit profile queued | Logo/images synced separately |
| User Profile | Full cache | Edit → queue | Profile pic uploaded on sync |

**Critical:** Tag purchases are queued but **never finalized until payment confirmed online**. Business owners must not assume tag visibility until sync confirmation received.

---

## 7. Bothoflow Integration

- All offline writes maintain `designerId` reference for commission tracking
- When queued items sync, `PulseUpdater.logSentiment()` fires on successful sync
- Sync conflicts on commission-bearing items trigger admin review notification
- Offline queue has a **priority tier**: commission events sync first
- `CommissionEngine` checks `isDirty` flag — pending items don't count toward commission until synced

---

## 8. Storage Strategy

**IndexedDB Stores:**
```
tapfo_db
├── notes        (cached entities, indexed by id + category)
├── items        (cached entities, indexed by noteId + updatedAt)
├── sums         (cached entities, indexed by id)
├── tags         (cached entities, indexed by businessId)
├── businesses   (cached entities, indexed by id)
├── syncQueue    (pending writes, indexed by status + createdAt)
├── conflicts    (conflict records, indexed by id)
└── media        (blobs for images, stored separately)
```

**Cache Expiry:**
- Business data: 7 days
- Item data: 3 days
- Tag data: 1 day (prices change frequently)
- User profile: 1 day
- Media: 30 days or manual clear

**Cache Pre-warming (on Wi-Fi):**
- Top 100 businesses by region
- User's recently viewed businesses
- User's own notes, items, businesses
- Category listing pages

---

## 9. Accessibility & Edge Cases

**Accessibility:**
- Offline banner: `role="status"`, `aria-live="polite"`
- Sync queue: `aria-label` on each item with operation type
- Conflict modal: full keyboard navigation between versions
- Progress indicator: `aria-valuenow` on sync progress bar

**Edge Cases:**
- App closed during sync: Service Worker completes, status in notification
- Very large sync queue (100+ items): batch in groups of 20, show overall progress
- Storage quota exceeded: prompt user to clear cache, prioritize own data over directory
- Sync conflict on deleted entity: server wins (entity deleted)
- Sync conflict on sum comparison: last-write-wins, sum auto-recalculates
- Offline for >30 days: show "Data may be outdated — sync to refresh" banner
- Simultaneous offline edits on multiple devices: merge on sync, no data loss
- Payment queued offline: PENDING status only, card never charged until online + confirmed

---

## 10. Implementation Checklist

- [ ] Network detection (Navigator.onLine + heartbeat + SW)
- [ ] Offline banner component
- [ ] IndexedDB setup (all stores + indexes)
- [ ] Cache manifest manager
- [ ] Sync queue processor (FIFO, with retry)
- [ ] Sync status indicators (per-entity and global)
- [ ] Conflict detection (409 handling)
- [ ] Conflict resolution modal (local/server/merge)
- [ ] Manual "Sync Now" trigger
- [ ] Background sync (Service Worker)
- [ ] Cache pre-warming on Wi-Fi
- [ ] Cache expiry/cleanup job
- [ ] Storage usage display
- [ ] Storage clear options
- [ ] Cache strategy selector (aggressive/balanced/minimal)
- [ ] Offline toast messages (saved, syncing, synced, failed)
- [ ] Progress bar for batch sync
- [ ] Retry logic with exponential backoff
- [ ] Conflict log viewer
- [ ] `PulseUpdater` sync events
- [ ] Service Worker registration
- [ ] SW cache-first strategy for static assets
- [ ] SW network-first for API calls (with offline fallback)
- [ ] Accessibility audit
- [ ] Large queue stress test (100+ items)
- [ ] Storage quota test
- [ ] Conflict resolution test cases
