# TapFo Onboarding Implementation Plan

Version: 1.0  
Date: 2026-04-29  
Scope: Production onboarding rollout for `onboarding.html` + integration with `index.html`

---

## 1. Goal

Deliver a first-run onboarding system that:
- assigns user role correctly
- captures minimum profile/business/designer setup data
- supports resume/skip/reset
- routes users back into the main app with correct permissions

Target completion time for end users: under 3 minutes.

---

## 2. Current State (Verified)

- Runtime role/capability model exists in `scripts/PermissionsManager.js`.
- Mock account types exist in `index.html` (`browser`, `user`, `business-*`, `designer-*`, `staff`, `admin`).
- No active production onboarding flow UI is currently wired.
- No standalone `login.html` / `signup.html` in current repo snapshot.

---

## 3. Delivery Architecture

### 3.1 Files to Add

- `onboarding.html` (new standalone flow runner)
- `scripts/onboarding.js` (state machine + storage + routing)
- `scripts/onboarding-ui.js` (rendering + validation + transitions)
- `assets/onboarding/` (illustrations/icons if needed)

### 3.2 Integration Points

- `index.html` startup:
  - if onboarding incomplete -> redirect to `onboarding.html`
  - else continue normal app boot
- `PermissionsManager.js`:
  - keep existing capability checks
  - onboarding writes `tapfo_role_v2` + `tapfo_active_profile_v2`
- `PulseUpdater.js`:
  - emit onboarding start/step/complete events

---

## 4. Storage Contract

### 4.1 Keys

- `tapfo_onboarding_v2`
- `tapfo_onboarding_skipped`
- `tapfo_role_v2`
- `tapfo_active_profile_v2`

### 4.2 Session Shape

```js
{
  id: "uuid",
  startedAt: "ISO8601",
  completedAt: null,
  role: "consumer", // consumer | business | designer | staff | admin | browser
  stepsCompleted: [],
  profileData: {
    displayName: "",
    phone: "",
    avatar: null,
    location: null
  },
  businessData: {
    businessName: "",
    category: "",
    region: ""
  },
  designerData: {
    portfolio: null,
    specialty: "",
    commissionOptIn: false
  },
  featureTourCompleted: {
    search: false,
    notes: false,
    sums: false,
    trusted: false,
    location: false
  },
  skipped: false,
  version: "v2"
}
```

---

## 5. Role Flows

## 5.1 Browser / Guest

Steps:
1. Welcome
2. Intent selection -> "Browse only"
3. Location selection (city + area)
4. Quick tour (search + directory + promos)
5. Done -> role `browser`

Validation:
- city required
- area defaults to `All Areas`

---

## 5.2 Consumer

Steps:
1. Welcome
2. Role select -> Consumer
3. Profile basics (display name required, phone optional, region required)
4. Feature tour (search, location filters, trusted, notes)
5. Done -> role `consumer`

Validation:
- display name min length 2
- if phone present, normalize Botswana format
- region required

---

## 5.3 Business Owner

Steps:
1. Welcome
2. Role select -> Business Owner
3. Owner profile basics
4. Business setup (name, category, region)
5. Verification explanation (unvalidated -> validated path)
6. Dashboard intro + first CTA
7. Done -> role `business`

Validation:
- business name required
- category required
- region required

---

## 5.4 Designer

Steps:
1. Welcome
2. Role select -> Designer
3. Designer profile (name, specialty required)
4. Portfolio optional
5. Commission opt-in required
6. Creator tools intro
7. Done -> role `designer`

Validation:
- specialty required
- commission terms checkbox required

---

## 5.5 Staff

Entry: hidden route or secure staff invite link only.

Steps:
1. Staff identity check
2. Capability overview
3. Workflow tour (notifications, moderation, support paths)
4. Done -> role `staff`

---

## 5.6 Admin

Entry: secure admin route only.

Steps:
1. Admin identity check
2. Critical controls + audit warnings
3. Governance/permissions checklist
4. Done -> role `admin`

---

## 6. Screen Map (onboarding.html)

Base screens:
1. `ob-welcome`
2. `ob-role-select`
3. `ob-profile-basic`
4. `ob-location`
5. `ob-business-setup`
6. `ob-designer-setup`
7. `ob-tour`
8. `ob-staff-setup`
9. `ob-admin-setup`
10. `ob-complete`

Routing rule:
- flow controller shows only role-relevant screens.

---

## 7. Main App Routing Rules

On app load (`index.html` init):
1. Read `tapfo_onboarding_v2`.
2. If missing or incomplete -> redirect `onboarding.html`.
3. If complete:
   - load role from `tapfo_role_v2`
   - apply permissions
   - continue normal app boot.

Reset support:
- `onboarding.html?reset=onboarding` clears onboarding keys.

---

## 8. Validation Rules

- Required fields block Next.
- Inline error messages directly under field.
- Keep Next disabled until required fields valid.
- Preserve field values when navigating back.
- On close/reopen, resume from first incomplete step.

---

## 9. UX/Performance Rules

- Mobile-first, single-column.
- Step transitions <= 320ms.
- Keep DOM small: render one step at a time.
- No network dependency for step completion.
- Use local assets only (offline first).

---

## 10. Analytics Events

Emit events:
- `onboarding_start`
- `onboarding_step_view`
- `onboarding_step_complete`
- `onboarding_skip`
- `onboarding_complete`
- `onboarding_resume`

Event payload minimum:
- role
- stepId
- durationMs
- completionState

---

## 11. Implementation Sequence (Recommended)

1. Build core engine (`onboarding.js`):
   - storage read/write
   - role flow map
   - resume logic
2. Build UI shell (`onboarding.html` + `onboarding-ui.js`):
   - welcome + role + complete
3. Add consumer path
4. Add business path
5. Add designer path
6. Integrate with `index.html` boot guard
7. Add staff/admin gated flows
8. Add telemetry + reset
9. QA all role paths

---

## 12. QA Checklist

- First run opens onboarding.
- Skip works and sets temporary consumer/browser role.
- Resume works after browser close mid-flow.
- City/area selection persists to main app.
- Completed onboarding never reopens unless reset.
- Each role lands in app with correct permissions.
- Offline onboarding works end-to-end.

---

## 13. Decision: Separate HTML vs In-App Panel

Recommendation: use separate `onboarding.html`.

Reason:
- Keeps `index.html` complexity down.
- Avoids regressions in core navigation.
- Cleaner flow control for role branches + resume.
- Easier to test and iterate independently.

