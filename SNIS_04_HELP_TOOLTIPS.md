# SNIS_04 — Help & Tooltips

## 1. Overview

**Purpose:** Context-sensitive help system covering every feature in TapFo — tooltips on individual UI elements, a searchable help panel, guided feature tours, and tag-specific explanations. Ensures zero training required for any feature.

**User Benefit:** Users never get stuck. Every icon, button, and term is explained inline without leaving the current context.

**Dependencies:** `HistoryTracker.js` (help usage analytics), `PulseUpdater.js` (help engagement tracking), `localStorage` (help dismissed state).

---

## 2. Data Model

```javascript
HelpTooltip {
  id: string,
  targetSelector: string,        // CSS selector for target element
  title: string,
  content: string,              // HTML allowed, max 200 chars
  position: 'top' | 'bottom' | 'left' | 'right' | 'auto',
  trigger: 'click' | 'hover' | 'focus' | 'auto',  // 'auto' = first visit only
  dismissible: boolean,
  showOnce: boolean,
  priority: 'high' | 'medium' | 'low',
  category: 'navigation' | 'snisis' | 'business' | 'tags' | 'general'
}

HelpArticle {
  id: string,
  slug: string,
  title: string,
  summary: string,               // 1-line preview
  content: string,               // Full markdown content
  category: string,
  tags: string[],
  relatedArticles: string[],     // article IDs
  lastUpdated: ISO8601,
  version: string,                // App version when last updated
  viewedCount: number,
  helpful: number,               // thumbs up count
  notHelpful: number
}

HelpTourStep {
  id: string,
  tourId: string,
  step: number,
  targetSelector: string,
  title: string,
  content: string,
  actionHint: string | null,     // "Tap the + button"
  spotlight: boolean,            // Highlight target element
  spotlightPadding: number
}

UserHelpState {
  viewedTooltips: string[],      // tooltip IDs shown
  completedTours: string[],      // tour IDs completed
  dismissedTooltips: string[],   // permanently dismissed
  lastHelpSearch: string,
  savedArticles: string[]        // bookmarked articles
}
```

**localStorage Keys:**
- `tapfo_help_state_v2` — `UserHelpState` object
- `tapfo_help_search_history_v2` — last 10 search queries
- `tapfo_tooltip_shown_v2` — tracking shown tooltips (for show-once)

---

## 3. Detection & Triggers

**Tooltip Triggers:**
- **Hover** (desktop/tablet): 400ms delay before showing
- **Tap/Click**: Toggle tooltip on tap
- **First visit**: Auto-show on `?showhelp=true` or fresh onboarding completion
- **Focus**: Show on keyboard focus (accessibility)
- **Context menu long-press**: Show extended help on long-press

**Help Panel Triggers:**
- "?" icon in nav bar → opens full help panel
- `#page-howto` URL navigation
- "Help" in profile/settings menu
- Shake gesture (3x) → help panel opens

**Guided Tour Triggers:**
- Completion of onboarding → prompts feature tour
- New feature release → "What's New" tour
- Feature first accessed → contextual tour prompt
- Manual: "Take a tour" button on any page

**Article Triggers:**
- Search in help panel
- Tapping related article link
- Tapping "Learn more" in tooltip
- Tag detail: "What are tags?" link

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: In-Context Tooltip
```
│  ┌──────────────────────────────┐  │
│  │  What is a Note?              │  │  ← title, 16px bold
│  │  ─────────────────────────    │  │
│  │  A Note groups related items  │  │  ← content, 14px regular
│  │  into a single view. Like a   │  │  ← max 3 lines
│  │  playlist for products.      │  │
│  │                               │  │
│  │  [Learn more →]    [✕ Got it] │  │  ← action + dismiss
│  └──────────────────────────────┘  │
│         ◄ 8px arrow pointing        │
│            to target element        │
│                                    │
│         [📝 Note name      ]        │  ← target element (spotlight)
```

### Wireframe 2: Hover Tooltip (Desktop)
```
│  ┌──────────────────────────────────┐│
│  │  Item    Sum    Tags    Business ││  ← nav items
│  └──────────────────────────────────┘│
│                                    │
│  ┌────────────────────────────────┐ │
│  │  🔍 Search                      │ │  ← input field
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │ [📋] My Notes                  │ │  ← list item
│  │    3 items • Updated today     │ │
│  └────────────────────────────────┘ │
│                                    │
│       ┌───────────────────────┐    │  ← tooltip appears on hover
│       │ ℹ️ My Notes            │    │     (200ms delay)
│       │ ─────────────────     │    │
│       │ Organise your items   │    │
│       │ into grouped notes.   │    │
│       └───────────────────────┘    │
│                        ◄           │
└────────────────────────────────────┘
```

### Wireframe 3: Spotlight Tour Highlight
```
┌────────────────────────────────────┐
│                                    │
│  [Background dimmed to 60% black]  │
│                                    │
│   ┌──────────────────────────┐     │  ← spotlit element (no dim)
│   │  [🔔] Notifications       │     │
│   └──────────────────────────┘     │
│                                    │
│   ┌──────────────────────────────┐ │
│   │  Get notified when someone    │ │
│   │  views your business or        │ │
│   │  sends you a message.         │ │
│   │  ──────────────────────────   │ │
│   │  [Got it]                     │ │
│   └──────────────────────────────┘ │
│                                    │
│       ◄ tooltip positioned         │
│         below spotlighted           │
│         element                     │
│                                    │
│   ○ ● ○ ○ ○                        │  ← step dots
│   [Skip tour]                      │
└────────────────────────────────────┘
```

### Wireframe 4: Help Panel (Full Screen)
```
┌────────────────────────────────────┐
│ [×]     HELP CENTER                │
├────────────────────────────────────┤
│ [🔍 Search help articles...]       │
├────────────────────────────────────┤
│ POPULAR TOPICS                     │
│ ┌──────────────────────────────────┐│
│ │ 📝 What is a Note?                ││
│ │    How to group your items       ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ ⚖️ What is a Sum?                 ││
│ │    Compare products side-by-side  ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 🏷️ How do tags work?              ││
│ │    Get visibility for your biz   ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 🎨 What is a Designer?           ││
│ │    Earn commission building apps  ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 📱 How does offline work?         ││
│ │    Access TapFo without internet  ││
│ └──────────────────────────────────┘│
├────────────────────────────────────┤
│ CATEGORIES                         │
│ [Getting Started] [Notes & Items]  │
│ [Sums & Comparisons] [Tags]         │
│ [Account & Profile] [Troubleshooting]│
└────────────────────────────────────┘
```

### Wireframe 5: Help Article View
```
┌────────────────────────────────────┐
│ [←]  What is a Sum?                │
├────────────────────────────────────┤
│                                    │
│  A Sum lets you compare 2 or more  │
│  items side-by-side, like a        │
│  Bloomberg terminal for local      │
│  prices.                           │
│                                    │
│  ──────────────────────────────    │
│                                    │
│  ## When to use a Sum              │
│                                    │
│  • Finding the best price          │
│  • Comparing features              │
│  • Tracking price changes          │
│                                    │
│  ## How to create a Sum            │
│                                    │
│  1. Select 2+ items from any Note  │
│  2. Tap "Compare"                   │
│  3. View your comparison            │
│                                    │
│  ──────────────────────────────    │
│                                    │
│  Was this helpful?                 │
│  [👍 Yes (24)]  [👎 No (2)]        │
│                                    │
│  Last updated: TapFo v2.1           │
│                                    │
│  RELATED                           │
│  • How to read a Sum chart         │
│  • Understanding tag analytics      │
│  • Pricing your items               │
└────────────────────────────────────┘
```

### Wireframe 6: Tag Context Tooltip
```
│  ┌────────────────────────────────┐ │
│  │ 🏷️ Premium Tag                  │ │  ← tag chip with tooltip
│  └────────────────────────────────┘ │
│         ▼ (tap/hover)               │
│  ┌────────────────────────────────┐ │
│  │  Premium Tag                    │ │
│  │  ────────────────────────       │ │
│  │  Your item appears in top       │ │
│  │  search results for this tag.   │ │
│  │                                 │ │
│  │  Duration: 7 days                │ │
│  │  Price: P5.00/week              │ │
│  │  Views: +127 this week          │ │
│  │                                 │ │
│  │  [Buy Tag]    [Learn more]      │ │
│  └────────────────────────────────┘ │
```

### Wireframe 7: Search Results (Help)
```
│  Search: "sum comparison"           │
├────────────────────────────────────┤
│  3 results found                   │
│                                    │
│  ┌────────────────────────────────┐ │
│  │ 📊 What is a Sum?               │ │
│  │    A Sum lets you compare...    │ │
│  │    [Matches: "sum", "comparison"]│ │
│  └────────────────────────────────┘ │
│ ┌────────────────────────────────┐  │
│ │ 📈 How to read Sum charts       │  │
│ │    Understanding the data...     │  │
│ │    [Matches: "sum"]              │  │
│ └────────────────────────────────┘  │
│ ┌────────────────────────────────┐  │
│ │ 🏷️ Tag vs Sum: When to use      │  │
│ │    Tags give visibility...      │  │
│ │    [Matches: "sum"]              │  │
│ └────────────────────────────────┘  │
│                                    │
│  Didn't find what you need?        │
│  [Contact Support]                  │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Flow 1: In-Context Tooltip
1. User hovers/taps on element with tooltip
2. Check `viewedTooltips` — if `showOnce` and already viewed, skip
3. Show tooltip with 200ms delay (hover) or instant (tap)
4. Spotlight pulses gently (2s animation loop)
5. User reads tooltip
6. Tap "Got it" → mark viewed, close
7. Tap "Learn more" → open help article
8. Tap outside → close (unless `dismissible: false`)
9. Store `viewedTooltips` in `localStorage`

### Flow 2: Guided Tour
1. Tour triggered (onboarding complete, new feature, manual)
2. Dim overlay applied to page
3. First step spotlighted
4. Tooltip positioned relative to spotlighted element
5. User reads instruction
6. Tap "Next" → move spotlight to next element
7. Repeat until final step
8. "Done" → mark tour complete, remove overlay
9. Store `completedTours` in `localStorage`
10. Never show same tour again (unless new feature)

### Flow 3: Help Panel Search
1. User taps "?" or navigates to `#page-howto`
2. Help panel opens (full screen or modal on mobile)
3. User types in search
4. Debounce 200ms → search across article titles, summaries, content
5. Results ranked: title match > summary match > content match
6. Highlight matching terms in results
7. Tap result → open article view
8. "Helpful?" feedback captured

### Flow 4: Tag Tooltip Flow
1. User taps or hovers tag chip
2. Tag tooltip shows: description, price, duration, performance stats
3. If tag not purchased: "Buy Tag" CTA prominent
4. If tag purchased: show performance metrics
5. "Learn more" → Tag help article
6. Business owner gets transparent pricing explanation

---

## 6. SnSIS Hierarchy Context

**Help topics mapped to SnSIS entities:**

| SnSIS Entity | Help Articles | Tooltips |
|---|---|---|
| Item | "Creating items", "Item fields explained", "Pricing your item" | Name, price, tags, photo |
| Note | "What is a Note?", "Organising with Notes", "Note templates" | Note name, add item, share note |
| Sum | "What is a Sum?", "Bloomberg-style comparison", "Reading charts" | Sum selector, KPI columns, trend chart |
| Tag | "How tags work", "Tag pricing", "Tag visibility" | Tag chip, buy CTA, performance |
| Business | "Business profile setup", "Verifying your business" | Profile fields, hours, contact |

**Tooltips follow the 80/20 rule:** 80% of users need only the tooltip; 20% need the full article.

---

## 7. Bothoflow Integration

- Help content includes "Designer" path explanations (what designers do, how commission works)
- Tooltip on commission events: "Your 20% cut is calculated on the sale price"
- Designer-specific tour: explains the commission dashboard, payout schedule, Bothoflow terms
- Help articles reference Bothoflow where relevant (tag purchases, designer fees)

---

## 8. Offline Behavior

- All help articles cached in `localStorage`/`IndexedDB` on first load
- Tooltip definitions stored locally (no server needed)
- Help panel works fully offline
- "New" badge on articles updated only when online
- Tour videos: not cached (too large), show placeholder image offline

---

## 9. Accessibility & Edge Cases

**Accessibility:**
- Tooltips: `role="tooltip"`, linked to trigger via `aria-describedby`
- Help panel: `role="dialog"`, focus trapped inside
- Tours: spotlight announced via `aria-live`, step count announced
- All images in articles have descriptive `alt` text
- Minimum touch target 44px for all help interactions
- Reduced motion: disable spotlight pulse animation

**Edge Cases:**
- No search results: "No articles found. Try different keywords" + contact support link
- Tooltip near screen edge: auto-reposition to stay within viewport
- Tour on element that navigates away: pause tour, resume on return
- Empty `viewedTooltips` on new session: show onboarding tooltips again
- Very long article: scrollable within panel, sticky header with back button
- User dismissed tooltip via ✕ but it's high priority: don't show again but log it
- Tour interrupted by incoming call: pause, resume on return
- Multiple tooltips triggered simultaneously: queue, show one at a time

---

## 10. Implementation Checklist

- [ ] Tooltip component (positioned, animated, dismissible)
- [ ] Spotlight overlay (dims non-relevant elements)
- [ ] Help panel (full-screen modal)
- [ ] Article renderer (markdown → styled HTML)
- [ ] Help search (full-text, ranked results)
- [ ] Search result highlighting
- [ ] Guided tour engine (step-based, spotlight management)
- [ ] Tour progress persistence
- [ ] "Helpful" feedback buttons
- [ ] Article bookmarking (save for later)
- [ ] Category filtering
- [ ] Popular topics section
- [ ] Related articles links
- [ ] Tag-specific tooltip component
- [ ] Contextual tour triggers
- [ ] Onboarding tour integration
- [ ] "What's New" tour for feature releases
- [ ] Help usage analytics
- [ ] Offline article caching
- [ ] Tooltip priority levels
- [ ] Auto-position on screen edge
- [ ] Keyboard navigation in help panel
- [ ] Focus management in tours
- [ ] Reduced motion support
- [ ] Accessibility audit
- [ ] Content management system for articles (admin)
