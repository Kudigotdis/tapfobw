# TapFo.bw - Development Workflow & Golden Rules

**Version:** 1.0  
**Last Updated:** April 2026

---

## PART 1: DEBUGGING WORKFLOW

### 1.1 Chrome DevTools → index.html → AI Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TAPFO DEBUGGING CYCLE                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 1: DISCOVER ISSUE IN CHROME                                       │
│                                                                         │
│ 1. Open TapFo.bw in Chrome (or local file)                            │
│ 2. Open DevTools (F12 or right-click → Inspect)                        │
│ 3. Navigate to Elements tab to inspect HTML                             │
│ 4. Check Console tab for errors/warnings                                │
│ 5. Use Application tab to inspect localStorage                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 2: ISOLATE THE CODE                                               │
│                                                                         │
│ In Chrome DevTools:                                                     │
│ 1. Find the element or function causing the issue                       │
│ 2. Note the LINE NUMBER in index.html (e.g., "line 4233")              │
│ 3. Check what function handles this (e.g., onclick handler)            │
│ 4. Determine what SHOULD happen vs what DOES happen                     │
│                                                                         │
│ Example:                                                               │
│   - Issue: "Engage button doesn't do anything"                         │
│   - Found: onclick="showToast('Engage feature coming soon!')"           │
│   - Line: 4233                                                         │
│   - Action Needed: Replace with actual engage functionality             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 3: DESCRIBE THE ISSUE                                             │
│                                                                         │
│ Copy this template and fill in:                                         │
│                                                                         │
│ ISSUE: [One sentence description]                                      │
│ LOCATION: [File:line number or component name]                          │
│ CURRENT BEHAVIOR: [What happens now]                                    │
│ EXPECTED BEHAVIOR: [What should happen]                                 │
│ RELATED CODE: [Any code snippets found]                                 │
│                                                                         │
│ Example:                                                               │
│   ISSUE: Engage button on directory page shows "coming soon" toast       │
│   LOCATION: index.html:4233                                            │
│   CURRENT: onclick="showToast('Engage feature coming soon!')"          │
│   EXPECTED: Should open engagement options (contact/share/save)         │
│   PRIORITY: HIGH                                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 4: FEED TO AI BUILDER                                              │
│                                                                         │
│ Send to AI:                                                             │
│ 1. The issue description template above                                 │
│ 2. The relevant code section (use "read index.html [offset] [limit]")    │
│ 3. Any context from related files                                       │
│ 4. Ask: "Implement [feature] following TapFo coding conventions"        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 5: AI IMPLEMENTS                                                   │
│                                                                         │
│ AI will:                                                               │
│ 1. Read the relevant section of index.html                              │
│ 2. Follow Golden Rules for TapFo development                            │
│ 3. Implement the fix following component patterns                        │
│ 4. Provide the exact code changes                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 6: VERIFY IN CHROME                                                │
│                                                                         │
│ 1. Copy the provided code changes                                       │
│ 2. Go to DevTools → Sources → index.html (or Elements for inline)       │
│ 3. Make temporary edits to test                                        │
│ 4. If it works, apply the change to the actual index.html file          │
│ 5. Test on actual device/PWA if possible                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 7: SAVE & DOCUMENT                                                │
│                                                                         │
│ 1. Update index.html with the verified fix                             │
│ 2. Document the change in updates_changelog.json                        │
│ 3. If new feature, update FEATURES_INVENTORY.md                        │
│ 4. Commit to git if version control is set up                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## PART 2: CHROME DEBUGGING TIPS

### 2.1 Finding Code in 7206-line index.html

```
Technique 1: Search in Elements
───────────────────────────────
1. Press Ctrl+F in Elements tab
2. Search for unique class names, IDs, or text
3. Example: Search "engage-btn" to find all engage buttons

Technique 2: Console Logging
────────────────────────────
1. Add console.log statements to functions
2. Check Console tab for output
3. Example: console.log('Current state:', state)

Technique 3: Breakpoints
────────────────────────
1. Go to Sources tab
2. Find index.html in the file tree
3. Click line number to set breakpoint
4. Trigger the function and inspect variables

Technique 4: localStorage Inspection
────────────────────────────────────
1. Go to Application tab → Local Storage
2. See tapfo_pulse, tapfo_history, etc.
3. Useful for tracking Bothoflow Protocol data
```

### 2.2 Common Issues & Quick Fixes

| Issue | Quick Debug | Fix Location |
|-------|-------------|--------------|
| Page not navigating | Check `showPage()` function | index.html:~4954 |
| Search not working | Check `performSearch()` function | index.html:~5290 |
| Business not opening | Check `openBusiness()` function | index.html:~5604 |
| Location filter broken | Check `filterByLocation()` | index.html:~5307 |
| Toast showing wrong message | Search for toast text | index.html |

### 2.3 Live Editing Workflow

```
1. Open Chrome DevTools (F12)
2. Go to Elements tab
3. Find the element to edit
4. Double-click to edit inline
5. Test the change
6. If successful, copy changes to index.html
7. If unsuccessful, revert and try different approach
```

---

## PART 3: GOLDEN RULES FOR AI BUILDERS

### 3.1 Code Structure Rules

```
RULE 1: NEVER MODIFY LINE NUMBERS DIRECTLY
──────────────────────────────────────────
✗ BAD:  "Change line 4233 to showToast('Done!')"
✓ GOOD: "Find the onclick handler for the engage button and update it"

Why: Line numbers change as file is edited. Always search for content.
```

```
RULE 2: PRESERVE EXISTING CSS VARIABLES
─────────────────────────────────────────
Always use existing CSS variables:
✗ BAD:  color: #1a5276;
✓ GOOD: color: var(--navy);

Existing variables in TapFo:
--navy: rgb(26, 82, 118)
--deep-navy: rgb(18, 52, 86)
--grey-light: rgb(230, 230, 230)
--grey-border: rgb(200, 200, 200)
--grey-text: rgb(180, 180, 180)
--white: #ffffff
--font: 'PTSans', sans-serif
--transition: 320ms cubic-bezier(0.4, 0, 0.2, 1)
```

```
RULE 3: USE EXISTING ICON PATHS
──────────────────────────────────
✗ BAD:  <img src="new_icon.png">
✓ GOOD: <img src="assets/icons/phone_icon_on.png">

Never introduce new icon paths without confirming with user.
```

```
RULE 4: FOLLOW STATE MANAGEMENT PATTERN
────────────────────────────────────────
✗ BAD:  Directly manipulating DOM without state update
✓ GOOD: Update state object, then re-render

Example:
state.trusted.add(bizId);  // Update state
renderDirectory();         // Re-render UI
```

```
RULE 5: USE EXISTING FUNCTIONS
──────────────────────────────
✗ BAD:  alert('Message');
✓ GOOD: showToast('Message');

Available global functions:
- showToast(message)
- showPage(pageId)
- navigateToPage(pageId)
- goBack()
- toggleTrust(bizId, element)
- renderDirectory()
- renderPromos()
- etc.
```

### 3.2 Naming Conventions

```
RULE 6: PAGE ID NAMING
───────────────────────
Format: #page-{pagename}
Examples:
  #page-home
  #page-directory
  #page-business
  #page-promos

Never use: page-home-page, homePage, HOME
```

```
RULE 7: FUNCTION NAMING
─────────────────────────
Format: {action}{Target}
Examples:
  openBusiness(bizId)
  renderDirectory()
  toggleTrust(bizId, element)
  switchAccount(accountId)
  setDirFilter(val, element)
  performSearch(query)

Never use: open_business, openBusiness(), OpenBusiness()
```

```
RULE 8: CSS CLASS NAMING
──────────────────────────
Format: .{component}-{variant}-{part}
Examples:
  .biz-row           (business list row)
  .biz-name          (business name text)
  .trust-bar         (trust indicator bar)
  .promo-advert-card (promo display card)
  .event-card        (event list item)

NEVER use: camelCase classes, BEM with double underscore
```

### 3.3 Feature Implementation Rules

```
RULE 9: "COMING SOON" FEATURES
────────────────────────────────
When implementing a "coming soon" feature:

1. Remove the showToast('...coming soon') call
2. Implement the actual functionality
3. If feature is complex, create a placeholder panel first
4. Track via Bothoflow Protocol (PulseUpdater)
5. Document in FEATURES_INVENTORY.md

Example transformation:
BEFORE: onclick="showToast('List Business coming soon!')"
AFTER:  onclick="openBusinessRegistrationForm()"
```

```
RULE 10: NEW CARD COMPONENTS
─────────────────────────────
Before creating a new card type:

1. Check TAPFO_COMPONENT_CATALOG.md for existing patterns
2. If similar card exists, adapt it
3. If new card needed, follow the card template
4. Document the new card in component catalog
5. Create SVG/PNG icon if needed

Required card properties:
- Container class: .card-name
- States: default, hover, active, disabled
- Touch target: minimum 44x44px
- Border radius: follows --radius-card
- Shadow: follows --shadow-card
```

```
RULE 11: ADDING NEW PAGES
───────────────────────────
1. Add page HTML in correct location (alphabetical or by flow)
2. Add CSS styles for the page
3. Add page state to state object
4. Add navigation function
5. Add to page routing in showPage()
6. Update SW.js cache list if needed
7. Document in PROJECT_SPECIFICATION.md
```

```
RULE 12: DATA PERSISTENCE
──────────────────────────
For new features that need data:

1. Use localStorage as primary storage
2. Key format: tapfo_{feature_name}
3. JSON.stringify/parse for objects
4. Check for null/undefined before use
5. Provide default values

Example:
localStorage.setItem('tapfo_notes', JSON.stringify(notes));
const notes = JSON.parse(localStorage.getItem('tapfo_notes')) || [];
```

### 3.4 Code Style Rules

```
RULE 13: NO COMMENTS (UNLESS REQUESTED)
────────────────────────────────────────
✗ BAD:  // This function handles search
        function performSearch(query) {
        
✓ GOOD: function performSearch(query) {
```

```
RULE 14: CONSISTENT INDENTATION
──────────────────────────────────
✓ Use 2 spaces for indentation
✓ Use single quotes for strings in JS
✓ Use double quotes for attributes in HTML
✗ No tabs, no mixed styles
```

```
RULE 15: FUNCTION LENGTH
──────────────────────────
✓ Maximum ~50 lines per function
✓ If longer, break into smaller functions
✓ Helper functions should be named descriptively

✗ BAD:  One 200-line function
✓ GOOD: mainFunction() calls step1(), step2(), step3()
```

```
RULE 16: AVOID DEEP NESTING
─────────────────────────────
✓ Maximum 3 levels of nesting
✓ Use early returns to reduce nesting
✓ Extract complex conditions to variables

✗ BAD:  if (a) { if (b) { if (c) { ... } } }
✓ GOOD: if (!a) return;
        if (!b) return;
        if (!c) return;
        // main logic
```

### 3.5 PWA & Offline Rules

```
RULE 17: SERVICE WORKER CACHING
────────────────────────────────
When adding new assets:

1. Add to ASSETS array in sw.js
2. Update CACHE_NAME version if needed
3. Test offline mode after changes

When adding new data files:
1. Add script tag to index.html head
2. OR add to sw.js ASSETS array for fetch caching
```

```
RULE 18: RESPONSIVE DESIGN
────────────────────────────
Mobile-first approach:
✓ Use dvh/vh for heights
✓ Touch targets minimum 44px
✓ Test on 375px width minimum
✓ Consider notch/pill camera areas

Media query breakpoints:
- Mobile: < 501px
- Desktop: >= 501px
```

---

## PART 4: IMPLEMENTATION CHECKLIST

### 4.1 Before Implementing Any Feature

- [ ] Read relevant section of index.html
- [ ] Check TAPFO_COMPONENT_CATALOG.md for patterns
- [ ] Check FEATURES_INVENTORY.md for similar features
- [ ] Understand the current state management
- [ ] Plan the changes following Golden Rules

### 4.2 During Implementation

- [ ] Use existing CSS variables
- [ ] Use existing icons/assets
- [ ] Follow naming conventions
- [ ] Update state BEFORE DOM manipulation
- [ ] Track engagement via PulseUpdater if applicable

### 4.3 After Implementation

- [ ] Test in Chrome DevTools
- [ ] Verify in mobile viewport
- [ ] Check for console errors
- [ ] Test offline mode if applicable
- [ ] Update documentation
- [ ] Update CHANGELOG

---

## PART 5: FILE REFERENCE PATTERNS

### 5.1 Reading Specific Sections

```javascript
// To read CSS section (lines 24-4000)
read index.html offset=24 limit=200

// To read JavaScript section (lines 4001-7206)
read index.html offset=4001 limit=200

// To find a specific function
grep pattern="function functionName" include=index.html

// To find all "coming soon" placeholders
grep pattern="coming soon" include=index.html
```

### 5.2 Common Search Patterns

```javascript
// Find all card CSS
grep pattern="\.card|\.row|\.item" include=index.html

// Find all onclick handlers
grep pattern="onclick=" include=index.html

// Find all state usage
grep pattern="state\." include=index.html

// Find all toast messages
grep pattern="showToast" include=index.html
```

---

**Document Version:** 1.0  
**For AI Builders:** Read this document before making ANY changes to TapFo code.
