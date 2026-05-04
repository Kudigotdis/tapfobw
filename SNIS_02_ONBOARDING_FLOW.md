# SNIS_02 — Onboarding Flow

## 1. Overview

**Purpose:** Guided first-run experience that classifies the user into one of three roles (Consumer, Business Owner, Designer), collects minimal viable profile data, and introduces core features progressively based on their path. Must be completable in under 3 minutes.

**User Benefit:** Zero friction setup. Users see only what matters to them based on their intent. Designers see the commission earning flow immediately.

**Dependencies:** `PermissionsManager.js` (role assignment), `PulseUpdater.js` (onboarding completion event), `HistoryTracker.js`.

---

## 2. Data Model

```javascript
OnboardingSession {
  id: string,
  startedAt: ISO8601,
  completedAt: ISO8601 | null,
  role: 'consumer' | 'business' | 'designer',
  stepsCompleted: string[],      // ['welcome', 'role', 'profile', 'features', 'done']
  profileData: {
    displayName: string,
    phone: string,
    avatar: string | null,
    location: string | null       // Botswana region
  },
  businessData: {                 // only if role === 'business' | 'designer'
    businessName: string,
    category: string,
    region: string
  },
  designerData: {                 // only if role === 'designer'
    portfolio: string | null,
    specialty: string,
    commissionOptIn: boolean
  },
  featureTourCompleted: {
    search: boolean,
    notes: boolean,
    sums: boolean,
    tags: boolean,
    share: boolean
  }
}
```

**localStorage Keys:**
- `tapfo_onboarding_v2` — `OnboardingSession` object
- `tapfo_onboarding_skipped` — boolean, true if user skipped
- `tapfo_role_v2` — assigned role after completion

---

## 3. Detection & Triggers

**Opening Triggers:**
- First-ever app open (no `tapfo_onboarding_v2` key)
- First app open after manual reset (`?reset=onboarding` URL param)
- User navigates to `#page-howto` and hasn't completed onboarding

**Step Progression Triggers:**
- "Next" button tap (validate current step first)
- "Skip" link tap (optional steps only)
- "Back" button tap
- Feature tour "Got it" tap (per-feature)
- Progress indicator dot tap (jump to completed step)

**Completion Triggers:**
- "Done" on final step → `PermissionsManager.assignRole(role)` → `PulseUpdater.logSentiment('onboarding_complete')` → `HistoryTracker.push()`
- "Skip for now" on any step → sets `skipped: true`, grants consumer role temporarily
- Browser close mid-flow → session persists in `localStorage`, resume on next open

**Resume Logic:**
- If `stepsCompleted` length > 0 and < total steps → resume at last incomplete step
- If `completedAt` exists → never show onboarding again (unless reset)

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Welcome Screen
```
┌────────────────────────────────────┐
│                                    │
│                                    │
│         [TAPFO LOGO]               │
│       Botswana's Business          │
│          Directory                │
│                                    │
│   ─────────────────────────────    │
│                                    │
│   Find local businesses,           │
│   compare prices, and connect      │
│   — all offline.                   │
│                                    │
│   ─────────────────────────────    │
│                                    │
│   [    Get Started    ]            │  ← primary CTA, navy fill
│                                    │
│   [    Skip for now    ]           │  ← ghost button, small text
│                                    │
└────────────────────────────────────┘
```

### Wireframe 2: Role Selection
```
┌────────────────────────────────────┐
│ [←]     Let's set you up           │
├────────────────────────────────────┤
│                                    │
│  What brings you to TapFo?         │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  🛒  I want to find &          │ │  ← Consumer path
│  │       support local businesses │ │
│  │       ───────────────────      │ │
│  │       Free • Full access       │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  🏪  I own or manage          │ │  ← Business path
│  │       a business               │ │
│  │       ───────────────────      │ │
│  │       P49/month • Tag ads      │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  🎨  I'm a designer             │ │  ← Designer path
│  │       who earns from sales      │ │
│  │       ───────────────────      │ │
│  │       20% commission • Build    │ │
│  └────────────────────────────────┘ │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 3: Consumer Profile Setup
```
┌────────────────────────────────────┐
│ [←]     About you                  │
├────────────────────────────────────┤
│                                    │
│  Tell us a bit about yourself      │
│  so businesses can trust you.      │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Display Name                  │ │
│  │  [________________________]    │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Phone Number (optional)       │ │
│  │  [+267 ___________]            │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Your Region                   │ │
│  │  [Select region ▼         ]    │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  [    Continue    ]            │ │
│  └────────────────────────────────┘ │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 4: Business Profile Setup
```
┌────────────────────────────────────┐
│ [←]     Your Business               │
├────────────────────────────────────┤
│                                    │
│  Set up your business profile      │
│  to start earning with TapFo.      │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Business Name                 │ │
│  │  [________________________]    │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Category                      │ │
│  │  [Select category ▼       ]    │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Region                        │ │
│  │  [Select region ▼         ]    │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Add your first item           │ │  ← expandable section
│  │  ────────────────────────      │ │
│  │  Item Name: [______________]   │ │
│  │  Price: P[________]             │ │
│  │  + Add more items              │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  [    Continue    ]            │ │
│  └────────────────────────────────┘ │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 5: Designer Setup
```
┌────────────────────────────────────┐
│ [←]     Join as Designer            │
├────────────────────────────────────┤
│                                    │
│  Designers earn 20% commission     │
│  on every item they help create.   │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Your Name                     │ │
│  │  [________________________]    │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Design Specialty              │ │
│  │  [Logo  ▼]                     │ │
│  │  Options: Logo, Brand, UI/UX,  │ │
│  │  Print, Packaging, Other       │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  Portfolio URL (optional)      │ │
│  │  [https://...]                 │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  ☑️ I agree to the TapFo        │ │
│  │     Designer Terms              │ │
│  └────────────────────────────────┘ │
│                                    │
│  ┌────────────────────────────────┐ │
│  │  [    Start Earning    ]       │ │
│  └────────────────────────────────┘ │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 6: Feature Tour (Consumer)
```
┌────────────────────────────────────┐
│ [×]   Discover TapFo                │
├────────────────────────────────────┤
│                                    │
│  ┌──────────────────────────────┐   │
│  │                              │   │
│  │      [ILLUSTRATION]         │   │  ← feature image/illustration
│  │                              │   │
│  │  ─────────────────────────   │   │
│  │                              │   │
│  │  Search & Discover           │   │  ← feature name
│  │  Find any business or        │   │  ← 2-line description
│  │  product by name, category,  │   │
│  │  or location.                │   │
│  │                              │   │
│  └──────────────────────────────┘   │
│                                    │
│      ● ○ ○ ○ ○ ○ ○ ○              │  ← progress dots
│                                    │
│  [Skip tour]      [Next →]         │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 7: Onboarding Complete
```
┌────────────────────────────────────┐
│                                    │
│                                    │
│         ✓                         │  ← large checkmark, animated
│                                    │
│      You're all set,              │
│       {DisplayName}!              │
│                                    │
│   ────────────────────────────    │
│                                    │
│   Your profile is ready.           │
│   Explore TapFo to find the        │
│   best local deals.               │
│                                    │
│   ────────────────────────────    │
│                                    │
│   ┌──────────────────────────┐     │
│   │  [    Go to Home    ]    │     │
│   └──────────────────────────┘     │
│                                    │
│   [View tutorial video]            │
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Flow 1: Consumer Path (7 Steps)
```
Welcome → Role: Consumer → Profile (name/phone/location)
→ Feature Tour: Search → Feature Tour: Notes → Feature Tour: Sums
→ Feature Tour: Tags → Done
```
- Profile is optional (phone, location)
- Feature tour is skippable per step
- On complete: consumer role assigned, full read access granted

### Flow 2: Business Owner Path (9 Steps)
```
Welcome → Role: Business → Business Profile (name/category/region)
→ Add First Item → Feature Tour: Dashboard → Feature Tour: Tags
→ Feature Tour: Analytics → Feature Tour: Sums → Done
```
- All fields required for business profile
- Item creation is encouraged but skippable
- On complete: business role assigned, item management access granted

### Flow 3: Designer Path (8 Steps)
```
Welcome → Role: Designer → Designer Profile (name/specialty/portfolio)
→ Designer Terms → Feature Tour: Commission → Feature Tour: Items
→ Feature Tour: Sums → Done
```
- Terms agreement required
- Portfolio URL optional
- On complete: designer role assigned, commission tracking access granted

### Flow 4: Resume After Crash/Close
1. User reopens app
2. App checks `tapfo_onboarding_v2`
3. Finds `stepsCompleted` array, not empty, `completedAt` is null
4. Resumes at `stepsCompleted.length + 1`
5. "Welcome back" banner: "You were mid-setup — pick up where you left off?"
6. User taps banner or continues naturally

### Flow 5: Skip Onboarding
1. User taps "Skip for now" on welcome screen
2. Modal: "You can always personalize later. Skip for now?"
3. User confirms
4. `tapfo_onboarding_skipped: true`
5. Consumer role assigned by default
6. User lands on home page
7. Prompt appears periodically (not intrusive): "Finish setting up your profile?"

---

## 6. SnSIS Hierarchy Context

**Place in Hierarchy:** Onboarding is the entry point that sets up a user's initial relationship with the SnSIS system. The role assigned determines their starting point in the hierarchy.

**Role → SnSIS Access Mapping:**

| Role | Can Create | Can View | Can Edit | Commission |
|---|---|---|---|---|
| Consumer | — | Notes, Sums | Own profile | — |
| Business | Items, Notes, Tags | Items, Notes, Sums | Own items, notes | Tag purchases |
| Designer | Items (for clients) | All items, sums | Via client access | 20% of sales |

**Onboarding does not create SnSIS data** — it only assigns the role that determines access.

---

## 7. Bothoflow Integration

**Designer Path Specific Integration:**
- Designer sees commission explanation on role selection screen
- Terms include Bothoflow designer agreement
- Post-onboarding: designer sees commission dashboard as first feature tour
- Commission display: "Your earnings appear here as you help businesses grow"

**All Paths:**
- `PulseUpdater.logSentiment('onboarding_complete')` on final step
- `PulseUpdater.logSentiment('onboarding_skipped')` on skip
- Onboarding step names match `HistoryTracker` events for funnel analysis

---

## 8. Offline Behavior

- Onboarding is fully functional offline
- All data stored in `localStorage` immediately on each step
- No network calls required until final "Done" (which posts to server)
- If final submission fails offline:
  - Show "Saved — will sync when online" message
  - Queue submission in `tapfo_onboarding_pending_sync`
  - On reconnect: auto-submit and show "Onboarding synced!"

---

## 9. Accessibility & Edge Cases

**Accessibility:**
- All form inputs have `<label>` associations
- Role cards: `role="radio"` with `aria-checked`
- Progress indicator: `aria-valuenow`, `aria-valuemin`, `aria-valuemax`
- Feature tour images: `alt` text with feature description
- Skip buttons clearly labeled
- Focus management: auto-focus first input on each step

**Edge Cases:**
- Very long name (>50 chars): truncate input display, store full
- Invalid phone format: inline error "Format: +267 followed by 7 digits"
- No internet at end: offline completion, sync later
- Multiple rapid app opens: debounce onboarding trigger (100ms)
- User already completed onboarding but opens `#page-howto`: show condensed summary, not full flow
- Region not in dropdown: "Other" option with free text input
- Empty required field on Next: shake animation + red border + error message
- Back button on step 1: confirmation modal "Leave setup?"

---

## 10. Implementation Checklist

- [ ] Welcome screen (logo, tagline, CTAs)
- [ ] Role selection cards (3 paths)
- [ ] Consumer profile form (name/phone/location)
- [ ] Business profile form (name/category/region/item)
- [ ] Designer profile form (name/specialty/portfolio/terms)
- [ ] Step progress indicator (dots + labels)
- [ ] Next/Back/Skip navigation
- [ ] Form validation per step
- [ ] Resume logic (localStorage check on load)
- [ ] Skip confirmation modal
- [ ] Feature tour carousel (5 features)
- [ ] Feature tour skip per feature
- [ ] Completion screen (animated checkmark)
- [ ] Role assignment via `PermissionsManager`
- [ ] `PulseUpdater` event emission
- [ ] `HistoryTracker` push on complete
- [ ] Offline completion + sync queue
- [ ] Skip onboarding path (consumer default)
- [ ] Accessibility audit (ARIA, focus, labels)
- [ ] Input field error states
- [ ] "Welcome back" resume banner
- [ ] Unit tests for step validation
- [ ] Integration test for role assignment flow
