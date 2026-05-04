# SNIS_08 — Drag & Drop

## 1. Overview

**Purpose:** Reorder Items within a Note, and reorder Notes within the sidebar/sum, using drag-and-drop gesture. Touch-optimized with clear visual feedback throughout the drag cycle.

**User Benefit:** Intuitive reordering without opening menus or using up/down buttons. Natural gesture for organizing personal lists.

**Dependencies:** Touch event handlers, `HistoryTracker.js` (reorder events), `localStorage`.

---

## 2. Data Model

```javascript
ReorderEvent {
  id: string,
  entityType: 'item' | 'note',
  parentId: string,              // noteId for items, null for notes
  itemId: string,
  fromIndex: number,
  toIndex: number,
  timestamp: ISO8601
}
```

---

## 3. Detection & Triggers

**Drag Start Trigger:**
- Long-press (400ms) on item/note row
- Visual: row lifts (shadow), haptic feedback (if available)
- Other items make space

**During Drag:**
- Finger move → item follows
- Drop zones highlight as item passes over
- Auto-scroll when near top/bottom edges

**Drop Trigger:**
- Release finger → item placed at new position
- List reflows with animation (300ms)
- `ReorderEvent` logged to history

**Cancel Trigger:**
- Drag outside list bounds
- Shake device
- Tap elsewhere

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Drag Reorder in Progress
```
┌────────────────────────────────────┐
│  📝 Morning Drinks (5 items)       │
├────────────────────────────────────┤
│                                    │
│  ┌──────────────────────────────┐  │  ← lifted item (shadow, elevated)
│  │ ☕ Latte          P35   [⋮⋮] │  │
│  └──────────────────────────────┘  │
│       ↑ drag handle (6 dots)        │
│                                    │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│  (drop zone highlighted)            │
│                                    │
│  ┌──────────────────────────────┐  │
│  │ ☕ Espresso         P25   [⋮⋮]│  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ ☕ Cappuccino       P38   [⋮⋮]│  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ 🥐 Croissant         P18  [⋮⋮]│  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ 🥛 Oat Milk Latte    P40  [⋮⋮]│  │
│  └──────────────────────────────┘  │
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Item Reorder Flow
1. User long-presses item row (400ms)
2. Item lifts with shadow + haptic
3. User drags to new position
4. Other items animate to make space
5. User releases
6. Item settles into new position
7. `ReorderEvent` saved
8. Toast: "Reordered" (auto-dismiss, 2s)

### Note Reorder Flow (Sidebar)
1. User long-presses note in sidebar
2. Note lifts
3. Drag to new position
4. Other notes shift
5. Release → note in new position

---

## 6. SnSIS Hierarchy Context

- Reordering items within a Note does NOT affect Sum comparisons (sums use any order)
- Reordering Notes changes personal display order only
- Sort order is per-user (not global)

---

## 7. Implementation Checklist

- [ ] Long- 400ms press to initiate drag
- [ ] Item lift animation (shadow, scale 1.02)
- [ ] Drag tracking (touch move events)
- [ ] Drop zone highlighting
- [ ] Auto-scroll near edges
- [ ] Drop and animate settle
- [ ] Reorder event logging
- [ ] Undo support (swap back)
- [ ] Haptic feedback
- [ ] Keyboard accessibility (arrow keys to reorder)
- [ ] Cancel on drag outside
