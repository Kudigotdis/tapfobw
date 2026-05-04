# SNIS_06 — Delete / Undo Flow

## 1. Overview

**Purpose:** Safe, reversible deletion flow for all SnSIS entities (Notes, Items, Sums, Tags) and business profile data. Prevents accidental deletion, shows dependencies before deletion, and provides a 10-second undo window.

**User Benefit:** No permanent mistakes. Delete anything and undo within 10 seconds. See exactly what will break before committing.

**Dependencies:** `HistoryTracker.js` (deletion audit), `localStorage` (undo buffer), `PermissionsManager.js` (delete permission checks).

---

## 2. Data Model

```javascript
DeletionRequest {
  id: string,
  entityType: 'note' | 'item' | 'sum' | 'tag' | 'business',
  entityId: string,
  entityName: string,
  initiatedBy: string,           // user ID
  initiatedAt: ISO8601,
  status: 'pending' | 'confirmed' | 'undone' | 'deleted' | 'failed',
  dependencies: [
    {
      type: string,             // 'item_in_sum', 'note_has_items', etc.
      relatedEntityId: string,
      relatedEntityName: string
    }
  ],
  cascadeDelete: boolean,        // true = delete dependents too
  undoUntil: ISO8601,            // Date.now() + 10000
  deletedAt: ISO8601 | null
}

TrashBinItem {
  id: string,
  entityType: string,
  entityId: string,
  entityData: object,            // full snapshot before deletion
  deletedAt: ISO8601,
  deletedBy: string,
  undoUntil: ISO8601,
  status: 'trash' | 'restoring' | 'permanently_deleted'
}
```

**localStorage Keys:**
- `tapfo_trash_bin_v2` — array of `TrashBinItem` (max 50)
- `tapfo_deletion_pending_v2` — current pending deletion for undo
- `tapfo_deletion_audit_log_v2` — audit trail (last 200 deletions)

---

## 3. Detection & Triggers

**Delete Trigger:**
- Long-press on entity → context menu → "Delete"
- Swipe left on entity row → delete button revealed
- Entity detail view → "..." menu → "Delete"
- Keyboard: `Delete` key (desktop/tablet with entity selected)

**Undo Trigger:**
- Tap "Undo" button in toast (within 10 seconds)
- Swipe right on undo toast
- Keyboard: `Ctrl+Z` (desktop/tablet)

**Permanent Delete Trigger:**
- Trash bin → "Delete forever" action
- 30 days auto-expiry from trash
- Manual "Empty trash" action

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Delete Confirmation Modal
```
┌────────────────────────────────────┐
│         ⚠️ Delete Item?             │
├────────────────────────────────────┤
│                                    │
│  Are you sure you want to delete:  │
│                                    │
│  ┌────────────────────────────────┐ │
│  │ ☕ Espresso                    │ │
│  │    P25 • from Coffee Corner    │ │
│  └────────────────────────────────┘ │
│                                    │
│  This item is used in:             │
│  ┌────────────────────────────────┐ │
│  │ ⚠️ 3 Sum comparisons          │ │
│  │    It appears in 3 price        │ │
│  │    comparisons. Deleting it    │ │
│  │    will remove it from those.   │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │ ⚠️ 1 Note                      │ │
│  │    "Morning Drinks" Note        │ │
│  │    will have 1 fewer item.    │ │
│  └────────────────────────────────┘ │
│                                    │
│  [Cancel]          [Delete Item]   │
│                    (red button)    │
│                                    │
│  ↩️ Undo available for 10 seconds  │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 2: Dependency Warning (Multiple Dependencies)
```
┌────────────────────────────────────┐
│         ⚠️ Cannot Delete           │
├────────────────────────────────────┤
│                                    │
│  "Morning Drinks" Note contains    │
│  5 items and is used in 2 Sums.    │
│                                    │
│  ┌────────────────────────────────┐ │
│  │ Items that will be affected:    │ │
│  │ ────────────────────────────   │ │
│  │ ☕ Espresso                   │ │
│  │ ☕ Latte                      │ │
│  │ ☕ Cappuccino                 │ │
│  │ 🥛 Flat White                 │ │
│  │ 🍫 Mocha                      │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │ Sums that will be affected:    │ │
│  │ ────────────────────────────   │ │
│  │ "Coffee Shop Comparison"       │ │
│  │ "Morning Prices Gaborone"      │ │
│  └────────────────────────────────┘ │
│                                    │
│  [Cancel]  [Delete Note + Items]   │  ← cascade delete option
│                                    │
└────────────────────────────────────┘
```

### Wireframe 3: Undo Toast
```
┌────────────────────────────────────┐
│                                    │
│  ┌──────────────────────────────┐  │
│  │ ☕ Espresso deleted          │  │  ← toast, slides up from bottom
│  │                              │  │
│  │ [↩️ Undo]        [✕]         │  │  ← Undo button prominent
│  └──────────────────────────────┘  │
│                                    │
│  ────────────── 10s countdown ──── │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 4: Trash Bin View
```
┌────────────────────────────────────┐
│ [←]     TRASH BIN           [⚙️]  │
├────────────────────────────────────┤
│ Items in trash auto-delete after    │
│ 30 days.                           │
│                                    │
│ TODAY                             │
│ ┌──────────────────────────────────┐│
│ │ ☕ Espresso                 [↩️] ││
│ │    Deleted 2 hours ago          ││
│ │    Expires in 29 days            ││
│ │    [Restore] [Delete Forever]    ││
│ └──────────────────────────────────┘│
│                                    │
│ THIS WEEK                         │
│ ┌──────────────────────────────────┐│
│ │ 🍩 Muffin                   [↩️] ││
│ │    Deleted 3 days ago            ││
│ │    Expires in 27 days            ││
│ │    [Restore] [Delete Forever]    ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 📝 Breakfast Note          [↩️] ││
│ │    Deleted 5 days ago            ││
│ │    Note + 3 items                ││
│ │    Expires in 25 days            ││
│ │    [Restore] [Delete Forever]    ││
│ └──────────────────────────────────┘│
│                                    │
│ ┌──────────────────────────────────┐│
│ │ [Empty Trash]                    ││  ← destructive, requires confirm
│ └──────────────────────────────────┘│
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Flow 1: Delete Single Item (No Dependencies)
1. User taps "Delete" on item
2. Modal appears: entity name + icon
3. No dependencies shown (clean state)
4. "Delete Item" button (red)
5. User taps Delete
6. Entity moved to trash bin (soft delete)
7. Toast appears: "☕ Espresso deleted" + [Undo] button
8. 10-second countdown starts
9. If Undo tapped: entity restored from trash, toast "Restored"
10. If no Undo: entity permanently deleted after 10s

### Flow 2: Delete Item (With Dependencies)
1. User taps "Delete" on item
2. Modal appears with dependency warnings
3. Shows: "Used in 3 Sum comparisons" + affected Sum names
4. "Delete Item" button (red) still available
5. User confirms
6. Entity removed from all Sums
7. Entity moved to trash
8. Undo available for 10s
9. Undo restores entity AND re-adds to Sums

### Flow 3: Delete Note (Cascade)
1. User taps "Delete" on Note
2. Dependency check runs
3. Modal shows: Note has X items, used in Y Sums
4. Two options: "Delete Note Only" (items stay orphaned) or "Delete Note + Items"
5. User selects "Delete Note + Items"
6. All items also moved to trash
7. Sums updated to remove those items
8. Full cascade undo available for 10s
9. Undo restores Note + all items + Sum references

### Flow 4: Restore from Trash
1. User navigates to Trash Bin
2. Finds deleted entity
3. Taps "Restore"
4. Confirmation if entity name conflicts with existing: "Restore as 'Espresso (restored)'?"
5. Entity restored to original Note (or root if Note deleted)
6. If Sum references existed: re-added to Sums
7. Toast: "☕ Espresso restored"

### Flow 5: Permanent Delete
1. User taps "Delete Forever" in trash
2. Confirmation: "This cannot be undone. Delete permanently?"
3. User confirms
4. Entity permanently removed from all systems
5. Audit log entry created

---

## 6. SnSIS Hierarchy Context

**Deletion cascades through SnSIS:**
```
Sum → References Items → Deleting Item removes from Sum
Note → Contains Items → Deleting Note optionally deletes Items
Note → Referenced by Sums → Deleting Note removes from Sums
Business → Has Notes/Items → Deleting Business deletes all
```

**Deleting a Sum:** Safe — no cascade, no dependencies. Sums are read-only comparisons.

**Deleting a Tag:** Safe — just removes visibility, does not touch Items.

**Soft delete vs Hard delete:**
- Soft delete (10s window): Trash bin, reversible
- Hard delete (after 10s or manual): Permanent, audit logged

---

## 7. Bothoflow Integration

- Deletion of a tagged item triggers: "Item deleted — tag {tagName} freed for re-use"
- Commission on deleted item: if item had pending commission, that commission is cancelled
- `HistoryTracker` logs: who deleted what, when, for audit purposes
- Designer-deleted items: notify business owner

---

## 8. Accessibility & Edge Cases

**Accessibility:**
- Delete buttons: `aria-label="Delete {entityName}"`
- Undo toast: `role="status"`, `aria-live="polite"`
- Dependency warnings: `role="alert"` for urgent warnings
- All actions keyboard-accessible

**Edge Cases:**
- Delete during offline: queued for sync, undo available locally
- Bulk delete (10+ items): confirmation shows count, single undo button for all
- Delete item being edited: save edits first, then delete
- Delete item during Sum comparison: redirect to Sum, item removed with message
- Circular references: handled (Item in Note in Sum referencing Item)
- Empty trash: "Trash is empty" illustration
- 30-day expiry: background job removes expired items, notification shown

---

## 9. Implementation Checklist

- [ ] Delete trigger (long-press, swipe, menu)
- [ ] Confirmation modal with entity preview
- [ ] Dependency scanner (recursive)
- [ ] Dependency warning display
- [ ] Cascade delete options
- [ ] Trash bin storage (IndexedDB)
- [ ] Soft delete (10s window)
- [ ] Undo toast with countdown
- [ ] Undo action (restore from trash)
- [ ] Restore to original context
- [ ] Permanent delete action
- [ ] 30-day auto-expiry job
- [ ] Empty trash confirmation
- [ ] Bulk delete support
- [ ] Offline deletion queue
- [ ] Deletion audit log
- [ ] Keyboard shortcuts (Delete, Ctrl+Z)
- [ ] Swipe gestures (left=delete, right=undo)
- [ ] Conflict resolution on restore (name clash)
- [ ] Accessibility audit
- [ ] Unit tests for dependency detection
- [ ] Edge case tests (circular refs, offline)
