# SNIS_11 — Template System

## 1. Overview

**Purpose:** Pre-built Note templates for common business categories (Restaurant Menu, Product Catalog, Service List, Price Comparison). One-tap setup, fully customizable.

**User Benefit:** Create a professional Note in seconds. Start from proven templates rather than blank canvas.

**Dependencies:** Template library, `localStorage` (user templates), `HistoryTracker.js`.

---

## 2. Data Model

```javascript
NoteTemplate {
  id: string,
  name: string,
  description: string,
  category: string,             // 'restaurant' | 'retail' | 'service' | 'comparison'
  icon: string,
  itemCount: number,
  previewImage: string,
  items: Item[],                // template items with placeholder data
  tags: string[],
  isOfficial: boolean,
  usageCount: number,
  rating: number
}

UserTemplate {
  id: string,
  name: string,
  sourceNoteId: string,
  createdAt: ISO8601,
  usageCount: number
}
```

---

## 3. Detection & Triggers

**Template Gallery Trigger:**
- "Create Note" → shows "Blank" and "From Template"
- "From Template" opens template gallery
- "..." menu on Note → "Save as Template"

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Template Gallery
```
┌────────────────────────────────────┐
│ [×]     NOTE TEMPLATES              │
├────────────────────────────────────┤
│ [🔍 Search templates...]           │
│ [All] [Restaurant] [Retail] [Service]│
│                                    │
│ ┌──────────────────────────────────┐│
│ │ [🍽️] Restaurant Menu             ││
│ │    12 items • ★★★★☆ (234 uses)  ││
│ │    ──────────────────────────── ││
│ │    Appetizers, Mains, Desserts,  ││
│ │    Drinks — all pre-populated    ││
│ │    [Use Template]                ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [📦] Product Catalog             ││
│ │    8 items • ★★★★☆ (156 uses)   ││
│ │    [Use Template]                ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [⚙️] Service Price List         ││
│ │    6 items • ★★★★☆ (98 uses)    ││
│ │    [Use Template]                ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ [⚖️] Price Comparison            ││
│ │    4 items • ★★★☆☆ (67 uses)    ││
│ │    [Use Template]                ││
│ └──────────────────────────────────┘│
│                                    │
│ ─────────────────────────────────  │
│ MY TEMPLATES                       │
│ ┌──────────────────────────────────┐│
│ │ [📝] My Coffee List        [⋮] ││
│ │    Saved from "Espresso Bar"     ││
│ │    [Use] [Edit] [Delete]          ││
│ └──────────────────────────────────┘│
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Use Template Flow
1. User taps "From Template"
2. Gallery opens with categories
3. User browses or searches
4. Taps "Use Template"
5. Preview shown: full item list
6. "Use Template" → Note created with items
7. User redirected to Note editor
8. User customizes names/prices
9. Template source noted for analytics

### Save as Template Flow
1. User has completed Note with items
2. Taps "..." → "Save as Template"
3. Names template, adds description
4. Sets category and tags
5. "Save Template" → added to My Templates
6. Toast: "Template saved"

---

## 6. SnSIS Hierarchy Context

- Templates create Notes with pre-populated Items
- Items in templates use placeholder names/prices
- User replaces placeholders with real data
- Template categories map to directory categories

---

## 7. Implementation Checklist

- [ ] Template gallery UI
- [ ] Category filtering
- [ ] Search templates
- [ ] Template preview
- [ ] "Use Template" → Note creation
- [ ] Item placeholder replacement
- [ ] Save Note as Template
- [ ] My Templates management
- [ ] Template usage analytics
- [ ] Official vs user template distinction
- [ ] Template ratings (from usage)
