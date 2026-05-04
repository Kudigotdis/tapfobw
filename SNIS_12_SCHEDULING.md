# SNIS_12 — Scheduling

## 1. Overview

**Purpose:** Schedule future actions — publish notes, activate/deactivate tags, send promotional notifications, update item prices. Set-and-forget for time-sensitive operations.

**User Benefit:** Time-zone free automation. Schedule a tag to activate Monday 8am, a promo to send Friday 6pm, without being online.

**Dependencies:** Background scheduler, `localStorage` (scheduled tasks), Service Worker (background execution), `PulseUpdater.js`.

---

## 2. Data Model

```javascript
ScheduledTask {
  id: string,
  type: 'tag_activate' | 'tag_deactivate' | 'note_publish' | 'price_update' | 'promo_send' | 'item_hide' | 'item_show',
  entityId: string,
  entityName: string,
  action: object,               // { tagId, newPrice, newStatus, etc. }
  scheduledFor: ISO8601,
  timezone: string,              // 'Africa/Johannesburg'
  status: 'scheduled' | 'running' | 'completed' | 'failed' | 'cancelled',
  repeat: null | {               // recurring tasks
    frequency: 'daily' | 'weekly' | 'monthly',
    endDate: ISO8601 | null
  },
  createdBy: string,
  createdAt: ISO8601,
  lastRun: ISO8601 | null,
  runCount: number,
  failureReason: string | null
}
```

**localStorage Key:**
- `tapfo_scheduled_tasks_v2` — array of `ScheduledTask`

---

## 3. Detection & Triggers

**Schedule Creation Trigger:**
- "Schedule" button on tag/item/note detail
- "..." menu → "Schedule"
- Date/time picker modal

**Execution Triggers:**
- Scheduled time reached (checked on app open + background)
- Service Worker alarm/timer
- Manual "Run Now" on pending task

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Schedule List
```
┌────────────────────────────────────┐
│ [←]     SCHEDULED                  │
├────────────────────────────────────┤
│ UPCOMING                           │
│                                    │
│ ┌──────────────────────────────────┐│
│ │ 🏷️ Activate "Late Night"  May 15 ││
│ │    8:00 AM                       ││
│ │    Coffee Corner                 ││
│ │    [Edit] [Cancel]               ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 📝 Publish "Summer Menu"  May 20 ││
│ │    6:00 PM                       ││
│ │    Café Delight                  ││
│ │    [Edit] [Cancel]               ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 💰 Deactivate "WiFi"    May 18  ││
│ │    11:59 PM                      ││
│ │    Coffee Corner                 ││
│ │    [Edit] [Cancel]               ││
│ └──────────────────────────────────┘│
│                                    │
│ RECURRING                          │
│ ┌──────────────────────────────────┐│
│ │ 🔄 Price update "Latte"  Weekly ││
│ │    Every Monday 9:00 AM         ││
│ │    P35 → P37 (seasonal)          ││
│ │    [Edit] [Cancel]               ││
│ └──────────────────────────────────┘│
│                                    │
│ ─────────────────────────────────  │
│ HISTORY                            │
│ ┌──────────────────────────────────┐│
│ │ ✓ "Late Night" activated   May 1││
│ │    Ran at 8:00 AM                ││
│ └──────────────────────────────────┘│
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Schedule Tag Activation Flow
1. Business owner on tag management
2. Taps "Schedule" on a paused tag
3. Date/time picker opens (defaults to next available slot)
4. Selects date and time
5. "Schedule Activation" button
6. Confirmation: "Late Night tag will activate May 15 at 8:00 AM"
7. Task created, appears in Schedule list
8. Toast: "Tag activation scheduled"

### Recurring Schedule Flow
1. User taps "Schedule" on price update
2. Toggles "Repeat" on
3. Selects frequency (daily/weekly/monthly)
4. Sets end date or "Never"
5. Saves recurring task
6. Task runs automatically per schedule

---

## 6. SnSIS Hierarchy Context

- Scheduled tag activation/deactivation affects visibility immediately
- Scheduled note publish changes public/private status
- Scheduled price updates recalculate Sum comparisons
- Scheduling is per-business-owner (their own items/tags only)

---

## 7. Implementation Checklist

- [ ] Schedule list UI (upcoming, recurring, history)
- [ ] Date/time picker (mobile-optimized)
- [ ] Timezone handling (Africa/Johannesburg default)
- [ ] Recurring task options
- [ ] Schedule creation from entity detail
- [ ] Background execution (Service Worker alarms)
- [ ] Execution status updates
- [ ] Failure notifications
- [ ] "Run Now" manual trigger
- [ ] Cancel scheduled task
- [ ] Edit scheduled task
- [ ] Execution history log
- [ ] Offline scheduling (queued)
