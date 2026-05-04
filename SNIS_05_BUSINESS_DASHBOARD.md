# SNIS_05 — Business Dashboard

## 1. Overview

**Purpose:** Command center for business owners to monitor performance, manage tags, control item visibility, and track earnings. Aggregates all `PulseUpdater.js` KPI events into actionable insights.

**User Benefit:** At-a-glance business health — who's viewing, what's selling, which tags are performing, and real-time commission tracking.

**Dependencies:** `PulseUpdater.js`, `CommissionEngine.js`, `PermissionsManager.js`, `localStorage`.

---

## 2. Data Model

```javascript
BusinessDashboard {
  businessId: string,
  overview: {
    totalViews: number,
    totalContacts: number,
    totalLeads: number,
    sentimentScore: number,      // -100 to +100
    rating: number,                // 0-5 stars
    reviewCount: number
  },
  tagPerformance: [
    {
      tagId: string,
      tagName: string,
      impressions: number,
      clicks: number,
      ctr: number,                 // clicks / impressions
      cost: number,                // P spent
      roi: number                  // leads generated / cost
    }
  ],
  itemPerformance: [
    {
      itemId: string,
      itemName: string,
      views: number,
      inquiries: number,
      addedToSum: number
    }
  ],
  commission: {
    earned: number,                // P total earned
    pending: number,               // P pending payment
    paidOut: number,               // P paid out
    thisMonth: number,
    designerCut: number
  },
  recentActivity: [
    {
      type: 'view' | 'contact' | 'lead' | 'tag_purchase' | 'commission',
      timestamp: ISO8601,
      details: object
    }
  ]
}
```

**localStorage Keys:**
- `tapfo_business_dashboard_v2` — dashboard data cache
- `tapfo_dashboard_cache_time` — timestamp of last refresh
- `tapfo_tag_budget_v2` — active tag spend limits

---

## 3. Detection & Triggers

**Opening Triggers:**
- Tap dashboard icon in business profile nav
- Navigate to `#page-business?id=XYZ&view=dashboard`
- Tap "Dashboard" in business owner bottom nav

**Refresh Triggers:**
- Pull-to-refresh gesture
- Tab switch (views → dashboard → tags)
- Manual refresh button tap
- App foreground (auto-refresh if >5 min stale)

**Filter Triggers:**
- Date range picker (7 days / 30 days / 90 days / custom)
- Tab: Overview / Tags / Items / Commission

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Dashboard Overview
```
┌────────────────────────────────────┐
│ [←]     COFFEE CORNER              │
│        Gaborone • since 2019       │
├────────────────────────────────────┤
│ 📊 Dashboard          Tags  Items  │  ← tab strip
├────────────────────────────────────┤
│                                    │
│ THIS MONTH                        │
│ ┌──────────┐  ┌──────────┐        │
│ │   1,247  │  │    38    │        │
│ │  Views   │  │ Contacts │        │
│ └──────────┘  └──────────┘        │
│ ┌──────────┐  ┌──────────┐        │
│ │    89    │  │   ★★★★☆  │        │
│ │  Leads   │  │   4.2/5   │        │
│ └──────────┘  └──────────┘        │
│                                    │
│ SENTIMENT TREND                   │
│ [▁▂▃▅▄▆▅▇▆▅] ↑ +12%               │
│ ──────────────────────────────── │
│                                    │
│ ┌──────────────────────────────────┐│
│ │ [📈] View full analytics         ││
│ └──────────────────────────────────┘│
│                                    │
│ TOP PERFORMING TAGS               │
│ ┌──────────────────────────────────┐│
│ │ 🏷️ Coffee          234 views     ││
│ │    P5/week • 4.2% CTR            ││
│ │    [Manage]                       ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 🏷️ Breakfast       189 views     ││
│ │    P3/week • 3.8% CTR            ││
│ │    [Manage]                       ││
│ └──────────────────────────────────┘│
│                                    │
│ [    + Buy New Tag    ]            │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 2: Tag Management Tab
```
┌────────────────────────────────────┐
│ [←]     TAG MANAGEMENT             │
├────────────────────────────────────┤
│ Tag Budget: P200/month    [Edit]   │
│ Spent: P127 / P200                │
│ ──────────────────────────────── │
│                                    │
│ ACTIVE TAGS (5)                   │
│                                    │
│ ┌──────────────────────────────────┐│
│ │ 🏷️ Coffee             [Active]   ││
│ │    P5/week • Expires in 4 days   ││
│ │    [234 views] [18 clicks]       ││
│ │    [Pause] [Edit] [Renew]        ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 🏷️ Breakfast          [Active]   ││
│ │    P3/week • Expires in 2 days   ││
│ │    [189 views] [7 clicks]        ││
│ │    [Pause] [Edit] [Renew]        ││
│ └──────────────────────────────────┘│
│                                    │
│ ┌──────────────────────────────────┐│
│ │ 🏷️ WiFi Available    [Paused]    ││
│ │    P2/week • Paused 3 days ago   ││
│ │    [Resume] [Delete]             ││
│ └──────────────────────────────────┘│
│                                    │
│ ┌──────────────────────────────────┐│
│ │ 🏷️ Late Night         [Expired]  ││
│ │    P2/week • Expired yesterday   ││
│ │    [Renew for P2]                ││
│ └──────────────────────────────────┘│
│                                    │
│ AVAILABLE TAGS                     │
│ ┌──────────────────────────────────┐│
│ │ [🔍 Search tags...]              ││
│ │ ─────────────────────────────── ││
│ │ ☕ Coffee                        ││
│ │ 🍳 Breakfast                     ││
│ │ 🍔 Lunch                         ││
│ │ 🌙 Late Night                    ││
│ │ 📶 WiFi Available                ││
│ │ ...and 40+ more                  ││
│ └──────────────────────────────────┘│
│                                    │
│ [    + Buy New Tag    ]            │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 3: Item Performance Tab
```
┌────────────────────────────────────┐
│ [←]     ITEM PERFORMANCE            │
├────────────────────────────────────┤
│ Sort: [Views ▼] [Name] [Recent]    │
│                                    │
│ ┌──────────────────────────────────┐│
│ │ ☕ Espresso              ★★★★☆   ││
│ │    P25 • Views: 456              ││
│ │    Contacts: 23 • Sums: 12       ││
│ │    [Edit] [View Details]         ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ ☕ Latte                  ★★★★☆  ││
│ │    P35 • Views: 389              ││
│ │    Contacts: 31 • Sums: 8         ││
│ │    [Edit] [View Details]         ││
│ └──────────────────────────────────┘│
│ ┌──────────────────────────────────┐│
│ │ 🥐 Croissant              ★★★☆☆ ││
│ │    P18 • Views: 234              ││
│ │    Contacts: 12 • Sums: 3        ││
│ │    [Edit] [View Details]         ││
│ └──────────────────────────────────┘│
│                                    │
│ ┌──────────────────────────────────┐│
│ │ ☕ Cappuccino             ★★★★☆ ││
│ │    P38 • Views: 201              ││
│ │    Contacts: 8 • Sums: 5         ││
│ │    [Edit] [View Details]         ││
│ └──────────────────────────────────┘│
│                                    │
│ [    + Add New Item    ]           │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 4: Tag Purchase Modal
```
┌────────────────────────────────────┐
│         🏷️ BUY TAG                 │
│ [×]                                │
├────────────────────────────────────┤
│                                    │
│ Select tag:                        │
│ ┌──────────────────────────────────┐│
│ │ ☕ Coffee                 P5/wk  ││
│ │    Most popular for your type   ││
│ │    Estimated 200+ views/week     ││
│ └──────────────────────────────────┘│
│                                    │
│ Duration:                          │
│ [1 week - P5] [4 weeks - P18]      │
│ [12 weeks - P48] [52 weeks - P180] │
│                                    │
│ ┌──────────────────────────────────┐│
│ │ Order Summary                    ││
│ │ ────────────────────────────    ││
│ │ Coffee tag (12 weeks)      P48  ││
│ │ TapFo fee (5%)              P2  ││
│ │ ────────────────────────────    ││
│ │ Total                     P50  ││
│ │                                 ││
│ │ Your commission: 0.5% base       ││
│ │ Designer cut: 20% of base        ││
│ └──────────────────────────────────┘│
│                                    │
│ Payment: [💳 Visa ending 4242 ▼]   │
│                                    │
│ [       Confirm Purchase       ]  │
│                                    │
│ By purchasing, you agree to TapFo's│
│ Tag Terms and Bothoflow fees.      │
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Flow 1: View Dashboard
1. Business owner taps Dashboard tab
2. Load cached dashboard data (instant)
3. Background refresh from server
4. KPI cards animate in (staggered 100ms each)
5. Charts render with animation
6. Pull-to-refresh available

### Flow 2: Buy a Tag
1. Owner taps "+ Buy New Tag" or taps available tag
2. Modal opens with tag options
3. Owner selects tag (if from available list)
4. Owner selects duration (pricing auto-calculates)
5. Order summary shown with fees
6. Owner selects payment method
7. Owner taps "Confirm Purchase"
8. Payment processed → tag activated
9. Tag appears in Active Tags list
10. Notification sent: "Tag purchased: {tagName}"
11. Commission tracked via `CommissionEngine`

### Flow 3: Pause/Resume Tag
1. Owner taps "Pause" on active tag
2. Confirmation: "Pause {tagName}? It will stop appearing in searches."
3. Owner confirms
4. Tag status → Paused
5. Tag removed from search results (near-realtime)
6. Owner can tap "Resume" to reactivate

### Flow 4: Renew Expired Tag
1. Owner sees expired tag in list (red indicator)
2. Owner taps "Renew"
3. Tag purchase modal pre-filled
4. Owner confirms duration and payment
5. Tag reactivated

---

## 6. SnSIS Hierarchy Context

**Dashboard within SnSIS:**
- Items are the atomic unit of dashboard data
- Notes group items for dashboard filtering
- Sums show comparative performance across items
- Tags are the visibility mechanism — dashboard shows ROI per tag

**Dashboard connects:**
- Item performance → Sum creation (best performing item)
- Tag ROI → Next tag purchase recommendation
- Commission → Designer earnings breakdown

---

## 7. Bothoflow Integration

- Commission section shows: earned, pending, paid out
- Designer cut displayed per transaction
- "Commission breakdown" link → Bothoflow report
- Tag purchase triggers: `CommissionEngine.checkAndProcess(entityId, salePrice, designerId)`
- Dashboard KPI: "Commission this month" prominently displayed

---

## 8. Offline Behavior

- Dashboard loads from cache instantly
- Tag management (pause/resume) queued for sync
- Cannot purchase new tags offline (payment required)
- Commission data cached (last synced value)

---

## 9. Accessibility & Edge Cases

- KPI cards: `role="region"` with `aria-label`
- Charts: text alternatives for data
- Tag status indicators: color + text (not color alone)
- Empty performance data: "No data yet — share your business to get started"

---

## 10. Implementation Checklist

- [ ] KPI overview cards (views, contacts, leads, rating)
- [ ] Sentiment trend chart (sparkline)
- [ ] Tab navigation (Overview/Tags/Items/Commission)
- [ ] Tag list with status indicators
- [ ] Tag purchase modal with pricing calculator
- [ ] Duration selector (1/4/12/52 weeks)
- [ ] Order summary with fee breakdown
- [ ] Payment method selector
- [ ] Tag pause/resume functionality
- [ ] Tag renewal flow
- [ ] Item performance list
- [ ] Sort/filter for items
- [ ] Commission summary section
- [ ] Recent activity feed
- [ ] Pull-to-refresh
- [ ] Auto-refresh on foreground
- [ ] Cached data display
- [ ] Loading skeleton states
- [ ] Empty state designs
- [ ] Offline mode (queued actions)
- [ ] Accessibility audit
