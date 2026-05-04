# SNIS_01 — Notifications Panel

## 1. Overview

**Purpose:** Real-time notification center for all TapFo user interactions — follows, contacts, leads, tag updates, commission alerts, and system messages. Aggregates events from `PulseUpdater.js` across all pages.

**User Benefit:** Single inbox for business intelligence (who's engaging, what's performing) and platform updates without leaving the current page.

**Dependencies:** `PulseUpdater.js`, `PermissionsManager.js`, `HistoryTracker.js`, `localStorage` sync queue.

---

## 2. Data Model

```javascript
Notification {
  id: string,                    // UUID
  type: 'follow' | 'contact' | 'lead' | 'tag' | 'commission' | 'system' | 'alert',
  priority: 'low' | 'medium' | 'high' | 'urgent',
  title: string,
  body: string,
  timestamp: ISO8601,
  read: boolean,
  dismissed: boolean,
  expires: ISO8601 | null,       // null = never expires
  actionUrl: string,            // '#page-business?id=xyz'
  actionLabel: string,           // 'View Business'
  avatar: string | null,         // Base64 or URL
  icon: string,                  // emoji or icon class
  metadata: {
    businessId: string | null,
    tagId: string | null,
    commissionAmount: number | null,
    pulseType: string | null,    // 'visit' | 'contact' | 'sentiment'
    designerId: string | null,
    designerName: string | null
  }
}
```

**localStorage Keys:**
- `tapfo_notifications_v2` — array of last 200 notifications
- `tapfo_notification_badge` — unread count (integer)
- `tapfo_notification_settings` — per-type toggles
- `tapfo_notification_last_sync` — ISO8601 of last server sync

**Firing Matrix (PulseUpdater → Notification):**

| Pulse Event | Notification Type | Title Template | Priority |
|---|---|---|---|
| `logVisit()` | `follow` | "{name} viewed your profile" | medium |
| `logContact()` | `contact` | "{name} sent you a message" | high |
| `logSentiment()` positive | `lead` | "Positive sentiment spike +{n}%" | high |
| `logSentiment()` negative | `alert` | "Negative sentiment detected" | urgent |
| Tag purchased on your business | `tag` | "New tag purchased: {tagName}" | medium |
| Tag expired on your business | `tag` | "Tag expired: {tagName}" | low |
| Commission triggered (0.5% base) | `commission` | "Commission earned: P{amount}" | high |
| Designer cut (20%) credited | `commission` | "Designer fee credited: P{amount}" | medium |
| System update | `system` | "TapFo update: {version}" | medium |
| Account alert | `alert` | "{message}" | urgent |

---

## 3. Detection & Triggers

**Opening Triggers:**
- Tap bell icon in nav bar (persistent across all pages)
- Swipe left on any notification in the list
- Keyboard shortcut: `N` key (desktop/tablet)

**Closing Triggers:**
- Tap outside the panel
- Tap X button
- Swipe right
- `Escape` key
- Navigate to a notification's `actionUrl`

**Auto-Triggers:**
- New `PulseUpdater` event → notification added → badge increments
- App comes online after offline → sync queue flushed → notifications updated
- Session start → unread count loaded from `localStorage` → badge rendered
- Notification expires → removed from list, not shown

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Closed State (Badge Only)
```
┌────────────────────────────────────┐
│ [≡]      TAPFO         [🔔 3] [👤] │  ← nav bar, badge shows 3 unread
└────────────────────────────────────┘
```

### Wireframe 2: Panel Open (Default)
```
┌────────────────────────────────────┐
│ [≡]      NOTIFICATIONS       [✓]  │  ← Mark all read button
├────────────────────────────────────┤
│ [🔍 Search notifications...        ]│  ← filter by text
│ All  Follow  Contact  Tags  💰     │  ← pill tabs, scrollable
├────────────────────────────────────┤
│ ┌──────────────────────────────────┐
│ │ [👤] John Doe              2m   │  ← avatar, name, time
│ │     viewed your profile          │  ← body text (1 line truncate)
│ │     [View Business]              │  ← action button
│ └──────────────────────────────────┘
│ ┌──────────────────────────────────┐
│ │ [💰] New commission        1h   │
│ │     P12.50 earned on sale        │
│ │     [View Dashboard]             │
│ └──────────────────────────────────┘
│ ┌──────────────────────────────────┐
│ │ [📍] Tag purchased        3h   │
│ │     "Beverages" on Coffee Shop   │
│ │     [View Business]              │
│ └──────────────────────────────────┘
│ ┌──────────────────────────────────┐
│ │ [⚠️] Negative sentiment   5h   │
│ │     -15% drop detected           │
│ │     [View Analytics]             │
│ └──────────────────────────────────┘
│           ▼ Load more              │
└────────────────────────────────────┘
```

### Wireframe 3: Filter Tab Active
```
│ All  [Follow]  Contact  Tags  💰  │  ← Follow tab active (filled)
├────────────────────────────────────┤
│ ┌──────────────────────────────────┐
│ │ [👤] John Doe              2m   │
│ │     viewed your profile          │
│ │     [View Business]              │
│ └──────────────────────────────────┘
│ ┌──────────────────────────────────┐
│ │ [👤] Mary Smith           1d   │
│ │     viewed your profile          │
│ │     [View Business]              │
│ └──────────────────────────────────┘
```

### Wireframe 4: Unread vs Read States
```
│  UNREAD (bold title, white bg)     │
│ ┌──────────────────────────────────┐
│ │ [●] John Doe viewed...    2m    │  ← dot indicator + bold
│ └──────────────────────────────────┘
│  READ (grey text, grey bg)         │
│ ┌──────────────────────────────────┐
│ │ [ ] Jane Doe viewed...    2d    │  ← no dot, lighter weight
│ └──────────────────────────────────┘
```

### Wireframe 5: Swipe to Dismiss
```
│ ┌──────────────────────────────────┐
│ │ [👤] John Doe              2m   │
│ │     viewed your profile     ←←←←│  ← swipe left reveals
│ │     [View Business]    [🗑️]     │  ← trash icon on right
│ └──────────────────────────────────┘
│        ← Swipe: 80px threshold     │
```

### Wireframe 6: Notification Settings Sub-panel
```
│ [← Back]   SETTINGS                │
├────────────────────────────────────┤
│ NOTIFICATION PREFERENCES            │
│                                    │
│ [✓] Follow activity                 │
│ [✓] Contact messages               │
│ [✓] Tag purchases on my business    │
│ [ ] Tag purchases on others        │
│ [✓] Commission earnings             │
│ [✓] Designer fee credits           │
│ [ ] System updates                  │
│ [ ] Marketing & promos             │
│                                    │
│ SOUND                               │
│ [🔊] Notification sound      [ON] │
│                                    │
│ FREQUENCY                           │
│ ( ) Real-time                       │
│ (•) Daily digest                    │
│ ( ) Weekly digest                   │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Flow 1: Open & Read a Notification
1. User taps bell icon
2. Panel slides in from right (320ms, ease-out)
3. Notifications list renders from `localStorage`
4. Unread count badge updates (decrements)
5. User taps a notification
6. `read: true` set on notification
7. User navigated to `actionUrl`
8. Panel closes automatically

### Flow 2: Bulk Mark All Read
1. User opens panel
2. User taps "✓" (Mark all read) button
3. Confirmation micro-modal: "Mark all as read?"
4. User confirms
5. All `read: false` → `read: true`
6. Badge count resets to 0
7. Toast: "All notifications marked as read"

### Flow 3: Dismiss Single Notification
1. User swipes left on notification row (80px threshold)
2. Trash icon revealed
3. User releases past threshold
4. Notification animates out (slide left + fade, 200ms)
5. `dismissed: true` set in localStorage
6. Unread count decremented if it was unread
7. Undo toast appears for 5 seconds

### Flow 4: Filter & Search
1. User taps filter tab (Follow/Contact/etc.)
2. List filters instantly (no loading state needed)
3. OR: User types in search field
4. Results filter as user types (debounced 200ms)
5. Empty state shown if no results: "No notifications match"

---

## 6. SnSIS Hierarchy Context

**Place in Hierarchy:** Notifications are cross-cutting — they surface events from Items, Notes, Sums, Tags, and business profiles. They are not part of the SNIS data model but provide the interaction layer on top of it.

**Connected Components:**
- **Items** → `logVisit()` on item detail → Follow notification
- **Notes** → `logContact()` on note → Contact notification
- **Sums** → `logSentiment()` on sum comparison → Lead/Alert notification
- **Tags** → Tag purchase/expire → Tag notification
- **Businesses** → Commission triggered → Commission notification
- **Designer accounts** → Designer cut credited → Commission notification

**No direct SnSIS hierarchy impact** — notifications are a UI overlay, not a data node.

---

## 7. Bothoflow Integration

**Commission Events that Generate Notifications:**

```
CommissionTriggered → Notification (commission, high priority)
  └─→ designerId lookup via PermissionsManager
  └─→ If designerId exists:
        └─→ DesignerFeeCredited → Notification (commission, medium priority)
```

**Notification body templates:**
- `Commission triggered (0.5% base):` "{entityName} | Base: P{baseAmount} | Your cut: P{designerAmount}"
- `Designer fee credited (20%):` "Commission on {businessName} | Earned: P{amount}"

**Commission notification never auto-expires** — designer needs permanent record.

---

## 8. Offline Behavior

- Panel always reads from `localStorage` — works fully offline
- New events logged to `PulseUpdater` sync queue when offline
- On reconnect: sync queue flushes → `PulseUpdater.sync()` called → new notifications generated
- Badge count persists across sessions
- "Syncing..." indicator shown during reconnection
- If sync fails: retry with exponential backoff (1s, 2s, 4s, max 30s)

**Offline-specific notifications:**
- "You're offline — changes will sync when connected" (system, low, transient)

---

## 9. Accessibility & Edge Cases

**Accessibility:**
- `role="log"` on notification list (`aria-label="Notifications"`)
- `role="button"` on bell icon with `aria-label="Notifications (n unread)"`
- `aria-live="polite"` on panel content area for new notifications
- All icons have `aria-hidden="true"`, text alternatives provided
- Tab order: bell → panel → list items → close → settings
- Focus trapped inside panel when open
- High contrast mode: notification borders + unread dot visible

**Edge Cases:**
- 0 notifications: Empty state "You're all caught up!" with illustration
- 200+ notifications: Pagination/load more (20 per page)
- Notification for deleted business: actionUrl shows "Business not found" page
- Notification for expired tag: shows tag re-purchase CTA
- Rapid notifications (5+ in 10s): batch into single "5 new notifications" entry
- Very long business name: truncate at 40 chars with ellipsis
- Offline badge: show cached unread count with "(cached)" label

---

## 10. Implementation Checklist

- [ ] Bell icon component with badge (nav bar)
- [ ] Slide-in panel (320ms transition, right edge)
- [ ] Notification list renderer (from localStorage)
- [ ] Per-type filter tabs
- [ ] Text search with debounce
- [ ] Mark all read functionality
- [ ] Individual swipe-to-dismiss
- [ ] Undo toast on dismiss (5s timeout)
- [ ] Notification settings sub-panel
- [ ] PulseUpdater event hookup (all 5 event types)
- [ ] Commission notification generation
- [ ] Designer fee notification generation
- [ ] Badge count management
- [ ] Offline sync queue integration
- [ ] Accessibility audit (ARIA roles, focus management)
- [ ] High contrast mode support
- [ ] Batch notification collapsing (5+ in 10s)
- [ ] Pagination (20 per page, load more)
- [ ] Empty state design
- [ ] Unit tests for notification generation logic
- [ ] Integration test for PulseUpdater → notification flow
