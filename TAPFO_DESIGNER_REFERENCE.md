# TapFo.bw - Designer Quick Reference Card

**For:** Graphic/UI Designers  
**Purpose:** Create consistent assets that work with the TapFo design system

---

## 1. CARD DIMENSIONS

### Standard Card Sizes

| Card Type | Width | Height | Notes |
|-----------|-------|--------|-------|
| Business Row | 100% | 60-70px | Flexible |
| Event Card | 100% - 32px | 100-140px | Margins 16px |
| Promo Card | 100% | Auto | Aspect ratio 3:4 or 1:1 |
| Note Card | 100% - 32px | Auto | Min 80px |
| Profile Card | 100% - 32px | Auto | Section-based |

### Touch Targets

| Element | Minimum Size |
|---------|--------------|
| Buttons | 44px × 44px |
| Icon buttons | 28px × 28px |
| List items | 48px height |
| Nav items | 56px height (bottom nav) |

---

## 2. BRAND COLORS

### Primary Colors

```
Navy (Primary):     #1A5276  →  rgb(26, 82, 118)
Deep Navy (Header): #123456  →  rgb(18, 52, 86)
```

### Contact Icon Colors

```
Phone (Call):       #F59E0B  (Amber/Yellow)
Facebook:           #1877F2  (Facebook Blue)
WhatsApp:           #25D366  (WhatsApp Green)
```

### Trust System Colors

```
Trusted:            #22C55E  (Green)
Favourited:         #F5C518  (Gold/Star Yellow)
```

### Neutral Colors

```
White:              #FFFFFF
Background:         #F3F3F3
Grey Light:         #E6E6E6
Grey Border:        #C8C8C8
Grey Text:          #B4B4B4
Body Text:          #333333
Dark Text:          #1A1A1A
```

---

## 3. TYPOGRAPHY

### Font Family

```
Primary Font:       PT Sans (Google Fonts)
Fallback:           Arial, sans-serif
```

### Font Sizes

| Element | Size | Weight |
|---------|------|--------|
| Page Title | 20px | Bold (700) |
| Card Title | 16px | Bold (700) |
| Body Text | 14-15px | Regular (400) |
| Subtitle | 13px | Regular (400) |
| Caption | 12px | Regular (400) |
| Small | 11px | Bold (700) |

### Line Heights

```
Titles:    1.2
Body:      1.4 - 1.5
Captions:  1.3
```

---

## 4. BORDER RADIUS

| Element | Radius |
|---------|--------|
| Cards | 12px |
| Buttons | 8px |
| Pills | 8px (full-round: 20px) |
| Avatars | 50% (circular) |
| Badges | 12px |
| Inputs | 8px |

---

## 5. SHADOWS

### Card Shadow

```
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
```

### Pressed State

```
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
```

### No shadows on:
- List items (dir-row, biz-row)
- Bottom navigation
- Modal overlays

---

## 6. ICON REQUIREMENTS

### Required Icon Sizes

| Context | Size |
|---------|------|
| Bottom nav | 24px × 24px |
| Contact icons | 16px × 16px |
| Action icons | 20-24px |
| Category icons | 44px × 44px (container) |
| Avatar icons | 16-24px |

### Icon Format

```
Preferred: SVG (scalable)
Fallback:  PNG @2x (@3x for retina)
```

### Icon States

Every interactive icon should have:
- Default state
- Hover/Active state (slightly darker)
- Disabled state (50% opacity)

---

## 7. PROMO IMAGE SPECS

### Aspect Ratios

| Promo Type | Ratio | Common Size |
|------------|-------|-------------|
| Square | 1:1 | 1080×1080 |
| Portrait | 3:4 | 1080×1440 |
| Landscape | 16:9 | 1920×1080 |

### File Formats

```
Images:  JPG (photos), PNG (graphics)
Video:   MP4 (H.264)
Audio:   MP3
```

### Naming Convention

```
TapFo_{Category}{Number}_{Week}.jpg
Examples:
  TapFo_Groceries1_DecWk1.jpg
  TapFo_BeautyGroom3_DecWk1.png
  TapFo_Fashion10_DecWk1.jpg
```

---

## 8. LOGO SPECS

### Main Logo

```
File:     TapFo_Logo.gif (animated) or .png (static)
Size:     280px × 280px (display)
Favicon:  32px × 32px, 192px × 192px
```

### Logo Colors

```
Navy:     #1A5276
White:    #FFFFFF
```

### Thumbnail (PWA)

```
File:     TapFo_Thumbnail.svg
Size:     192px × 192px (minimum)
          512px × 512px (recommended)
Format:   SVG (vector) or PNG
```

---

## 9. BADGE/TAG STYLES

### Status Badges

```
.font-size:  11px
.font-weight: 700
.padding:     4px 10px
.border-radius: 12px

Colors by type:
- User:      Blue background (#1A5276), white text
- Business:  Green background (#22C55E), white text
- Staff:     Red background (#DC2626), white text
- Admin:     Dark background (#0D1B2A), white text
```

### Pill Tags

```
.background:  var(--navy)
.color:       white
.border-radius: 8px
.padding:     6px 14px
.font-size:   13px
```

---

## 10. EMPTY STATE ILLUSTRATIONS

### Standard Empty States

| Context | Emoji | Message |
|---------|-------|---------|
| No search results | 🔍 | "No Results" |
| No notes | 📝 | "No notes yet" |
| No contacts | 📭 | "No contacts listed" |
| No news | 📰 | "No news articles yet" |
| No media | 🎬 | "No media notes yet" |
| No online presence | 🌐 | "No online presence listed" |
| No promos | 🖼️ | "No images found" |
| No events | 📅 | "No events found" |

### Design Guidelines for Empty States

- Center content vertically
- Large emoji (48px)
- Descriptive text below
- Max width 280px
- Grey text color

---

## 11. ANIMATION GUIDELINES

### Transition Timing

```css
/* Standard transitions */
transition: 320ms cubic-bezier(0.4, 0, 0.2, 1);

/* Quick feedback */
transition: 150ms ease;

/* Page transitions */
transform: translateY(100%);  /* Slide up to show */
transform: translateY(0);    /* Visible */
transform: translateY(-100%); /* Slide out top */
```

### Cursor Blink (Search)

```css
animation: cursorBlink 1.1s step-start infinite;
/* 1.1 second blink cycle */
```

---

## 12. RESPONSIVE BREAKPOINTS

### Mobile-First

```
Default:    < 501px (Mobile)
Desktop:    >= 501px (Full-bleed)
```

### Mobile Layout
- Full-width cards
- Bottom navigation (fixed)
- No sidebars

### Desktop Layout
- Full-bleed pages (no card container)
- Same bottom navigation
- Centered content max-width: 100%

---

## 13. QUICK EXPORT CHECKLIST

Before delivering assets:

- [ ] SVG files optimized (remove metadata)
- [ ] PNG files @2x or @3x resolution
- [ ] Colors in correct hex/RGB format
- [ ] Font embedded or outlined
- [ ] Named according to convention
- [ ] Tested on transparent background
- [ ] Consistent stroke widths (if applicable)

---

## 14. COMMON MISTAKES TO AVOID

| Mistake | Correction |
|---------|------------|
| Using non-brand colors | Always use CSS variables or brand hex |
| Wrong border radius | 12px for cards, 8px for buttons |
| Oversized shadows | Use box-shadow: 0 2px 8px rgba(0,0,0,0.08) |
| Missing touch target | Minimum 44px × 44px for buttons |
| Wrong icon size | 24px for nav, 16px for inline |
| Inconsistent padding | 14-16px standard for cards |
| Wrong text weight | Titles 700, body 400/500 |

---

## 15. CONTACT FOR QUESTIONS

For design clarification or new asset requests:
- Check COMPONENT_CATALOG.md for specs
- Check FEATURES_INVENTORY.md for context
- Reference specific card class names

---

**Document Version:** 1.0  
**For Designers:** These specs ensure your assets will integrate seamlessly with TapFo.bw
