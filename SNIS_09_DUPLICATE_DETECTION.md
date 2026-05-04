# SNIS_09 — Duplicate Detection

## 1. Overview

**Purpose:** Detect and surface duplicate or near-duplicate Items during creation and editing. Prevents catalog pollution, maintains data quality, and offers smart merge for consolidation.

**User Benefit:** Never accidentally create the same item twice. Clean up duplicates with one tap.

**Dependencies:** Fuzzy string matching, `HistoryTracker.js`, `localStorage`.

---

## 2. Data Model

```javascript
DuplicateCandidate {
  sourceItemId: string,
  sourceItem: Item,
  duplicateItemId: string,
  duplicateItem: Item,
  matchScore: number,            // 0-100
  matchFields: string[],          // ['name', 'price', 'category']
  suggestion: 'merge' | 'ignore' | 'edit'
}

MergeResult {
  sourceItemId: string,
  targetItemId: string,
  mergedData: Item,
  conflicts: [
    { field: string, sourceValue: any, targetValue: any }
  ],
  resolvedBy: 'user' | 'auto'    // auto = same values or one empty
}
```

---

## 3. Detection & Triggers

**Detection Trigger:**
- On item create: check name similarity against existing items in same Note
- On item edit: check if changes create near-duplicate
- Manual: "Find Duplicates" button in note header

**Detection Method:**
- Name: Levenshtein distance < 3 OR Jaro-Winkler > 0.85
- Price: within 5%
- Category: exact match
- Score = weighted average → flag if > 70

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Duplicate Warning Banner
```
┌────────────────────────────────────┐
│ ⚠️ Possible duplicate detected     │  ← amber banner, dismissible
│                                    │
│  "Espresso" is similar to:        │
│  ☕ Espresso (P28) — Coffee Corner  │
│                                    │
│  [View & Merge]  [It's different]  │
└────────────────────────────────────┘
```

### Wireframe 2: Merge Panel
```
┌────────────────────────────────────┐
│         🔀 MERGE ITEMS             │
│ [×]                                │
├────────────────────────────────────┤
│                                    │
│  ┌──────────────────┐ ┌──────────┐ │
│  │ NEW ITEM (keep)  │→│ RESULT   │ │
│  │ ──────────────── │ │ ──────── │ │
│  │ Name: Espresso   │ │ Name:    │ │
│  │ Price: P25   →25 │ │ Espresso  │ │
│  │ Category: Coffee │ │ P25      │ │
│  │ Tags: ☕ Hot     │ │ Coffee   │ │
│  │                   │ │ ☕ Hot   │ │
│  │ [Keep as new]     │ │          │ │
│  └──────────────────┘ └──────────┘ │
│                                    │
│  CONFLICTS TO RESOLVE:             │
│  ┌──────────────────────────────────┐│
│  │ Price: P25 vs P28                ││
│  │ [Use P25] [Use P28] [Keep both] ││
│  └──────────────────────────────────┘│
│                                    │
│  MERGE INTO:                       │
│  ☕ Espresso (P25)                  │  ← selected
│                                    │
│  ─────────────────────────────────  │
│  Sum references will be updated:   │
│  "Coffee Prices Gaborone"           │
│                                    │
│  [Cancel]        [Merge Items]      │
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Flow 1: Create Duplicate Item
1. User creates item "Espresso" P25
2. System checks existing items in Note
3. Finds "Espresso" P28 (similar name)
4. Warning banner appears above save button
5. User taps "View & Merge" → merge panel opens
6. OR User taps "It's different" → saves anyway
7. If merge: items combined, duplicate removed

### Flow 2: Manual Duplicate Scan
1. User taps "⋮" menu on Note
2. Selects "Find Duplicates"
3. System scans all items in Note
4. Results shown in list: duplicates grouped
5. User taps group → merge panel
6. User resolves each duplicate

---

## 6. SnSIS Hierarchy Context

- Duplicate detection is per-Note scope (same Note = likely duplicate)
- Cross-Note duplicates suggested but not flagged (different owners possible)
- Merge updates all Sum references automatically

---

## 7. Implementation Checklist

- [ ] Fuzzy string matching (Levenshtein / Jaro-Winkler)
- [ ] Similarity scoring algorithm
- [ ] Duplicate warning banner
- [ ] Merge panel UI
- [ ] Conflict resolution per field
- [ ] Auto-merge for non-conflicting fields
- [ ] Sum reference update after merge
- [ ] Manual "Find Duplicates" trigger
- [ ] Scan results list
- [ ] Dismiss/skip duplicate
- [ ] Duplicate detection on edit
- [ ] Offline duplicate detection (local index)
