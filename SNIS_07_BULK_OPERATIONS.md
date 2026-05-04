# SNIS_07 — Bulk Operations

## 1. Overview

**Purpose:** Select multiple SnSIS entities (Items, Notes) simultaneously and perform actions on them as a batch — delete, move to Note, add tags, share, export.

**User Benefit:** Power users managing large catalogs (100+ items) can perform repetitive actions 10x faster by selecting in bulk rather than one-at-a-time.

**Dependencies:** `HistoryTracker.js`, `localStorage`, `PermissionsManager.js`.

---

## 2. Data Model

```javascript
BulkOperation {
  id: string,
  type: 'delete' | 'move' | 'tag' | 'share' | 'export' | 'sum_add',
  entityType: 'item' | 'note',
  entityIds: string[],
  initiatedBy: string,
  initiatedAt: ISO8601,
  status: 'selecting' | 'confirming' | 'processing' | 'complete' | 'failed',
  targetNoteId: string | null,    // for move/tag operations
  tagsToAdd: string[] | null,    // for tag operations
  result: {
    succeeded: number,
    failed: number,
    errors: string[]
  }
}
```

---

## 3. Detection & Triggers

**Selection Mode Entry:**
- Long-press on any item → enters selection mode
- "Select" link in note header → enters selection mode
- `?bulk=select` URL param

**Selection Actions:**
- Tap item → toggle selection
- "Select All" button → select all visible
- "Select by Tag" → opens tag filter, selects all matching

**Exit Selection Mode:**
- Tap X / Cancel
- Complete a bulk action
- Navigate away (with warning if items selected)

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Selection Mode (Item List)
```
┌────────────────────────────────────┐
│ [×]     SELECT ITEMS         [✓ 3] │  ← X=cancel, ✓=selected count
├────────────────────────────────────┤
│ [☐ Select all 8]  [Sort ▼]        │
│                                    │
│ ┌──────────────────────────────────┐│
│ │ [☑] ☕ Espresso           P25   ││  ← checked, highlighted
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [☐] ☕ Latte                P35 ││  ← unchecked
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [☑] ☕ Cappuccino          P38   ││  ← checked
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [☐] 🥐 Croissant           P18  ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [☑] 🥐 Chocolate Muffin     P22  ││  ← checked
│ └──────────────────────────────────┘│
│                                    │
├────────────────────────────────────┤
│ [🗑️ Delete] [📂 Move] [🏷️ Tag] [↗️ Share] │
│  ────────────────────────────────── │
│  3 items selected                  │
│  Est. P120 total value             │
└────────────────────────────────────┘
```

### Wireframe 2: Bulk Add to Note Modal
```
┌────────────────────────────────────┐
│         📂 MOVE TO NOTE            │
│ [×]                                │
├────────────────────────────────────┤
│                                    │
│  Moving 3 items to:               │
│                                    │
│  ┌──────────────────────────────────┐│
│  │ 📝 Morning Drinks           ✓ ││  ← selected (destination)
│  │    5 items • from Coffee Corner  ││
│  └──────────────────────────────────┘│
│  ┌──────────────────────────────────┐│
│  │ 📝 Lunch Menu                ○ ││  ← not selected
│  │    8 items                       ││
│  └──────────────────────────────────┘│
│  ┌──────────────────────────────────┐│
│  │ 📝 New Note...                ○ ││  ← create new option
│  │    + Create new note            ││
│  └──────────────────────────────────┘│
│                                    │
│  ─────────────────────────────────  │
│  ☕ Espresso, ☕ Cappuccino,        │
│  🥐 Chocolate Muffin will be       │
│  added to "Morning Drinks".        │
│                                    │
│  [Cancel]     [Move Items]         │
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Flow 1: Bulk Delete
1. Enter selection mode (long-press)
2. Tap items to select (visual feedback: checkmark, bg color)
3. Tap "Delete" in action bar
4. Confirmation modal: "Delete 3 items?" + list preview
5. Dependency warnings if applicable
6. Tap "Delete" → items moved to trash
7. Exit selection mode
8. Toast: "3 items deleted" + [Undo]

### Flow 2: Bulk Move to Note
1. Enter selection mode
2. Select items
3. Tap "Move" in action bar
4. Modal shows Note list
5. Select target Note (or create new)
6. Preview shows items that will be moved
7. Tap "Move Items"
8. Items moved, exit selection mode
9. Toast: "3 items moved to {NoteName}"

### Flow 3: Bulk Add Tags
1. Enter selection mode
2. Select items
3. Tap "Tag" in action bar
4. Tag selection modal (multi-select tags)
5. Preview: "Add 'Coffee' and 'Hot Drinks' to 3 items"
6. Tap "Add Tags"
7. Tags applied to all selected items
8. Toast: "Tags added to 3 items"

---

## 6. SnSIS Hierarchy Context

- Bulk operations work on Items and Notes
- Items can be moved between Notes (maintains Sum references if possible)
- Bulk delete respects dependency rules (same as single delete)
- Bulk tagging applies to all selected items at once

---

## 7. Implementation Checklist

- [ ] Long-press to enter selection mode
- [ ] Item selection toggle (checkbox + visual)
- [ ] Select all (all / filtered)
- [ ] Selection count display
- [ ] Action bar (Delete, Move, Tag, Share)
- [ ] Bulk delete with confirmation
- [ ] Bulk move to Note modal
- [ ] Bulk tag application
- [ ] Selection mode exit (X, complete, navigate away)
- [ ] Offline queue for bulk operations
- [ ] Progress indicator for large bulk ops
- [ ] Undo support for bulk delete
