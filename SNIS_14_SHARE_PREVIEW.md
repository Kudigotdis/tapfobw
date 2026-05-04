# SNIS_14 — Share Preview

## 1. Overview

**Purpose:** Rich preview cards for sharing Notes, Items, Sums, and business profiles to external platforms (WhatsApp, Facebook, Twitter, SMS, Email). OG meta tags + TapFo-native deep links.

**User Benefit:** Every shared link shows a beautiful, informative preview that drives engagement. Users know exactly what they're clicking.

**Dependencies:** Share API (Web Share API), deep link generation, OG meta tag generation, `HistoryTracker.js`.

---

## 2. Data Model

```javascript
SharePayload {
  type: 'note' | 'item' | 'sum' | 'business',
  entityId: string,
  title: string,
  description: string,
  imageUrl: string,
  deepLink: string,            // 'tapfo://item/xyz'
  webLink: string,              // 'https://tapfo.bw/item/xyz'
  via: 'TapFo',                 // for social attribution
  hashtags: string[]            // auto-generated from tags
}

ShareChannel {
  id: 'whatsapp' | 'facebook' | 'twitter' | 'sms' | 'email' | 'copy' | 'native',
  name: string,
  icon: string,
  color: string
}
```

**Deep Link Format:**
- `tapfo://note/{id}`
- `tapfo://item/{id}`
- `tapfo://sum/{id}`
- `tapfo://business/{id}`
- Fallback: `https://tapfo.bw/{type}/{id}`

---

## 3. Detection & Triggers

**Share Trigger:**
- "Share" button on any entity detail
- "..." menu → "Share"
- Swipe left on item row → share icon
- Long-press on entity → context menu
- `navigator.share()` API (native share sheet on mobile)

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Share Modal
```
┌────────────────────────────────────┐
│         ↗️ SHARE                    │
│ [×]                                │
├────────────────────────────────────┤
│                                    │
│  ┌────────────────────────────────┐ │
│  │  ☕ Espresso — P25             │ │  ← preview card (what will be shared)
│  │  Coffee Corner • Gaborone      │ │
│  │  ────────────────────────      │ │
│  │  [image placeholder]           │ │
│  │  ────────────────────────      │ │
│  │  Strong single-shot coffee.    │ │
│  │  Perfect for a quick boost.    │ │
│  └────────────────────────────────┘ │
│                                    │
│  SHARE VIA                         │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐      │
│  │ 💬 │ │ 📘 │ │ 🐦 │ │ 📧 │      │
│  │ WhatsApp│ FB │ Twitter│ Email│      │
│  └────┘ └────┘ └────┘ └────┘      │
│  ┌────┐ ┌────┐                    │
│  │ 📋 │ │ 📱 │                    │
│  │ Copy │ Native│                    │
│  └────┘ └────┘                    │
│                                    │
│  ─────────────────────────────────  │
│  tapfo.bw/item/abc123              │
│  [📋 Copy Link]                    │
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### Share to WhatsApp Flow
1. User taps Share on item
2. Modal opens with preview card
3. User taps WhatsApp icon
4. WhatsApp share sheet opens with:
   - Title + description
   - Image (if available)
   - Deep link URL
5. User sends message
6. `PulseUpdater.logSentiment('share_sent', {platform: 'whatsapp'})`

### Copy Link Flow
1. User taps "Copy Link"
2. Deep link copied to clipboard
3. Toast: "Link copied! Share it anywhere."
4. User pastes elsewhere

### Native Share (iOS/Android) Flow
1. User taps "Native" button
2. `navigator.share()` called
3. System share sheet appears
4. User selects app
5. Share proceeds via system

---

## 6. SnSIS Hierarchy Context

- Every SnSIS entity type is shareable
- Note shares show: note name, item count, first few items
- Item shares show: item name, price, business, photo, tags
- Sum shares show: comparison table preview, item names
- Business shares show: business name, rating, top items

---

## 7. Implementation Checklist

- [ ] Share modal UI
- [ ] Preview card generation
- [ ] Deep link generation (tapfo:// protocol)
- [ ] Web fallback links (https://tapfo.bw)
- [ ] WhatsApp share integration
- [ ] Facebook share integration
- [ ] Twitter share integration
- [ ] Email share (mailto: link)
- [ ] SMS share (sms: link)
- [ ] Copy to clipboard
- [ ] Web Share API (native share sheet)
- [ ] OG meta tags (server-side for web links)
- [ ] Share analytics tracking
- [ ] Share image generation (canvas or server)
- [ ] OG tag fallbacks (default image, title, description)
