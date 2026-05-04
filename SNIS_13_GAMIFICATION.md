# SNIS_13 — Gamification

## 1. Overview

**Purpose:** Motivation system using badges, points, streaks, and leaderboards to drive engagement and consistent app usage. Rewards discovery, contribution, and community participation.

**User Benefit:** Recognition for engagement. Visible achievements encourage more discovery and contribution. Leaderboards foster friendly competition.

**Dependencies:** `PulseUpdater.js` (event tracking), `HistoryTracker.js`, `localStorage`, `PermissionsManager.js`.

---

## 2. Data Model

```javascript
Badge {
  id: string,
  name: string,
  description: string,
  icon: string,
  category: 'discovery' | 'contribution' | 'social' | 'milestone',
  tier: 'bronze' | 'silver' | 'gold' | 'platinum',
  pointsValue: number,
  criteria: object,              // { type: 'count', entity: 'item', threshold: 10 }
  earnedAt: ISO8601 | null,
  progress: number,              // 0-100%
  isNew: boolean
}

UserGamification {
  userId: string,
  points: number,
  level: number,                 // 1-50
  streak: {
    current: number,            // consecutive days
    longest: number,
    lastActiveDate: ISO8601
  },
  earnedBadges: string[],       // badge IDs
  weeklyRank: number | null,
  monthlyRank: number | null,
  weeklyPoints: number,
  monthlyPoints: number
}
```

**Badge Types:**
- Discovery: First search, First visit, First sum, Explorer (10 notes)
- Contribution: First item, First note, 10 items, 50 items, Prolific (100 items)
- Social: First follow, 10 follows, First share, Community helper
- Milestone: 7-day streak, 30-day streak, 100-day streak, Top reviewer

---

## 3. Detection & Triggers

**Badge Unlock Trigger:**
- `PulseUpdater` event meets badge criteria
- Badge check runs after every `PulseUpdater` call
- If criteria met → badge unlocked

**Streak Update Trigger:**
- Daily app open (any page)
- Check `lastActiveDate`:
  - Same day: no change
  - Yesterday: increment streak
  - Earlier: reset streak to 1

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Badge Unlock Toast
```
┌────────────────────────────────────┐
│                                    │
│  ┌──────────────────────────────┐  │
│  │ 🏆 NEW BADGE EARNED!         │  │
│  │                               │  │
│  │      [🥇]                    │  │  ← badge icon, large
│  │                               │  │
│  │   PROLIFIC CONTRIBUTOR       │  │  ← badge name
│  │   You added 100 items!       │  │  ← description
│  │                               │  │
│  │   +50 points  → Level 8       │  │
│  │                               │  │
│  │   [View Badges]   [Awesome!]  │  │
│  └──────────────────────────────┘  │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 2: Profile Badge Row
```
│ ┌──────────────────────────────────┐│
│ │ [👤] Kudzanai                    ││
│ │     Level 8 • 2,340 points       ││
│ │     🔥 12 day streak 🔥          ││
│ │     🏆 24 badges                 ││
│ │     🥇 Prolific Contributor      ││
│ │                                   ││
│ │     [View All Badges]            ││
│ └──────────────────────────────────┘│
```

### Wireframe 3: Achievement Gallery
```
┌────────────────────────────────────┐
│ [←]     ACHIEVEMENTS               │
├────────────────────────────────────┤
│ 2,340 pts  │  Level 8  │  🔥 12   │
│ ─────────────────────────────────  │
│ [Discovery] [Contrib] [Social] [★] │
├────────────────────────────────────┤
│                                    │
│ 🏆 PROLIFIC CONTRIBUTOR   [🥇]    │
│    Add 100 items to TapFo          │
│    Earned: Mar 15, 2026            │
│    +50 points                      │
│                                    │
│ 🥈 FIRST NOTE            [🥈]     │
│    Create your first Note          │
│    Earned: Feb 28, 2026            │
│    +10 points                      │
│                                    │
│ ─────────────────────────────────  │
│ LOCKED                             │
│                                    │
│ 🔒 LEGENDARY STATUS      [  ]      │
│    Reach level 50                   │
│    2,340 / 25,000 points           │
│    [████████░░░░] 9%               │
│                                    │
│ 🔒 100-DAY STREAK        [  ]      │
│    Maintain a 100-day streak        │
│    Current: 12 days                │
│    [████████████░░░░] 12%          │
│                                    │
│ 🔒 MASTER REVIEWER       [  ]      │
│    Write 50 reviews                 │
│    Current: 8 / 50                  │
│    [███████░░░░░░░░░] 16%           │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 4: Leaderboard
```
┌────────────────────────────────────┐
│ [←]     LEADERBOARD                │
├────────────────────────────────────┤
│ [This Week] [This Month] [All Time]│
├────────────────────────────────────┤
│                                    │
│   1  🥇 @tumi_developer   4,521 pts │  ← gold highlight
│                                    │
│   2  🥈 @design_by_lesego 3,892 pts │  ← silver highlight
│                                    │
│   3  🥉 @creative_ane    3,201 pts │  ← bronze highlight
│                                    │
│   ──────────────────────────────── │
│                                    │
│  12  📍 You               892 pts │  ← user highlighted
│                                    │
│  13  📍 @cafe_owner_bw    756 pts │
│  14  📍 @retail_gaborone   634 pts │
│  15  📍 @tech_freelancer   521 pts │
│                                    │
│  ──────────────────────────────── │
│  Your rank: #12 this week          │
│  Need 300 more points for #11      │
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Badge Unlock Flow
1. User creates 100th item
2. `PulseUpdater` logs item creation
3. Badge criteria check runs
4. "Prolific Contributor" criteria met
5. Toast appears (full-screen celebration)
6. Badge saved to profile
7. Points added to total
8. Level recalculated

### Streak Flow
1. User opens app
2. Streak check runs
3. If yesterday was last active: streak +1
4. If new longest: "New streak record!" toast
5. Streak badge awarded at milestones (7, 30, 100 days)
6. If missed day: streak resets, "Start a new streak?" prompt

### Leaderboard View Flow
1. User navigates to leaderboard
2. Default: "This Week" tab
3. Can switch to Month / All Time
4. User's position highlighted
5. Tap any user → see their public profile
6. "Follow" button available

---

## 6. SnSIS Hierarchy Context

- Gamification applies to all SnSIS entities
- Badges track: Items created, Notes created, Sums created, Tags purchased
- Designer path: additional badges for commission earned, clients served
- Leaderboard aggregates all engagement types

---

## 7. Bothoflow Integration

- Designer commission earnings contribute to leaderboard points
- "Top Designer" badge for highest commission earners
- Designer earnings displayed in profile alongside gamification stats
- Weekly designer leaderboard (separate from general)

---

## 8. Implementation Checklist

- [ ] Badge definition library
- [ ] Badge criteria evaluation engine
- [ ] Badge unlock toast (celebration UI)
- [ ] Profile badge row
- [ ] Achievement gallery with tabs
- [ ] Progress bars on locked badges
- [ ] Points system
- [ ] Level calculation
- [ ] Streak tracking (daily check)
- [ ] Streak display in profile
- [ ] Leaderboard UI (3 tabs)
- [ ] Leaderboard API integration
- [ ] Rank display with next-rank gap
- [ ] Follow from leaderboard
- [ ] Gamification toggle (settings)
- [ ] Offline badge check
- [ ] Points/badges sync
