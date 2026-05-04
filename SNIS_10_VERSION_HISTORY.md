# SNIS_10 — Version History

## 1. Overview

**Purpose:** Immutable audit trail and rollback capability for all Item and Note edits. Every change is versioned, timestamped, and restorable.

**User Benefit:** See exactly what changed, who changed it, and when. Restore any previous version in one tap.

**Dependencies:** `HistoryTracker.js` (extends it), `localStorage` (version snapshots), `HistoryTracker.js` FIFO 88-item cap with overflow to version history.

---

## 2. Data Model

```javascript
Version {
  id: string,
  entityType: 'item' | 'note',
  entityId: string,
  versionNumber: number,         // incrementing
  snapshot: object,              // full entity state
  diff: {
    changedFields: string[],
    before: object,
    after: object
  },
  editedBy: string,
  editedByName: string,
  editedAt: ISO8601,
  editType: 'create' | 'edit' | 'restore' | 'merge',
  note: string | null           // optional edit note from user
}
```

**Version retention:**
- Last 50 versions per entity
- Auto-prune older than 90 days (configurable)
- Never prune versions with commission attached

---

## 3. Detection & Triggers

**Opening Triggers:**
- "History" / "Version" button on item/note detail
- "..." menu → "View History"
- `?history=true` URL param

**Restore Trigger:**
- Tap version in timeline
- Tap "Restore this version"
- Confirmation modal
- Version restored as new current version

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Version Timeline
```
┌────────────────────────────────────┐
│ [←]     VERSION HISTORY             │
│        ☕ Espresso                 │
├────────────────────────────────────┤
│                                    │
│  v12 ─┬─ ● TODAY, 10:30 AM  ←── CURRENT
│       │    You changed price       │
│       │    P28 → P25              │
│       │    [Restore] [View]        │
│       │                            │
│  v11 ─┤    Yesterday, 3:45 PM      │
│       │    You changed description │
│       │    [Restore] [View]        │
│       │                            │
│  v10 ─┤    Apr 8, 2:15 PM          │
│       │    Designer edit: K. Dube  │
│       │    Price P25 → P28         │
│       │    [Restore] [View]        │
│       │                            │
│   ... ─┤    (scrollable)           │
│       │                            │
│   v1 ─┤    Mar 1, 9:00 AM          │
│       │    Created                │
│       │    [View]                  │
│       │                            │
└────────────────────────────────────┘
```

---

## 5. User Flows

### View History Flow
1. User taps History on item
2. Timeline loads (newest first)
3. Current version highlighted
4. User scrolls through versions
5. Tap "View" → shows that version's snapshot
6. Tap "Restore" → confirmation → restores

### Restore Flow
1. User taps "Restore" on v10
2. Confirmation: "Restore to v10? Current v12 will be saved as a new version."
3. User confirms
4. v12 saved, v10 becomes new current
5. Toast: "Restored to v10"
6. Item displays v10 data

---

## 6. SnSIS Hierarchy Context

- Version history tracks Items and Notes
- Sums are immutable (no version history needed)
- Restoring item updates Sum references
- Designer edits are marked with editor name

---

## 7. Implementation Checklist

- [ ] Version timeline UI
- [ ] Version snapshot storage (IndexedDB)
- [ ] Diff generation (changed fields)
- [ ] Current version indicator
- [ ] Version preview modal
- [ ] Restore action with confirmation
- [ ] Version auto-pruning (90 days)
- [ ] Per-entity version limit (50)
- [ ] Editor attribution (who changed)
- [ ] Commission-attached version protection
- [ ] Offline version history access
