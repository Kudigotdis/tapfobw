# SNIS_15 — Copy / Import

## 1. Overview

**Purpose:** Import data from external sources (CSV, JSON, other apps) and export/copy TapFo data for portability, backup, and migration. Supports single items, entire notes, and full business profiles.

**User Benefit:** Migrate existing catalogs into TapFo in minutes, not hours. Export data for backup or use in other systems.

**Dependencies:** File API, localStorage, HistoryTracker.js, CSV/JSON parser.

---

## 2. Data Model

```javascript
ImportJob {
  id: string,
  sourceFormat: 'csv' | 'json' | 'google_sheets' | 'excel',
  sourceName: string,
  status: 'parsing' | 'mapping' | 'validating' | 'importing' | 'complete' | 'failed',
  totalRows: number,
  processedRows: number,
  successCount: number,
  failureCount: number,
  errors: ImportError[],
  mappings: FieldMapping[],
  createdAt: ISO8601,
  completedAt: ISO8601 | null
}

FieldMapping {
  sourceField: string,
  targetField: string,
  transform: 'none' | 'lowercase' | 'uppercase' | 'currency_strip' | 'date_parse'
}

ImportError {
  row: number,
  field: string,
  value: any,
  reason: string
}

ExportJob {
  id: string,
  entityType: 'item' | 'note' | 'full_business',
  entityIds: string[],
  format: 'csv' | 'json' | 'pdf',
  status: 'preparing' | 'generating' | 'ready' | 'failed',
  downloadUrl: string | null,
  expiresAt: ISO8601 | null
}
```

---

## 3. Detection & Triggers

**Import Trigger:**
- Note detail → "..." → "Import Items"
- Business profile → "Import Data"
- First-run if CSV detected in clipboard

**Export Trigger:**
- Note detail -> "..." -> "Export Note"
- Business profile -> "Export Data"
- Settings -> "Backup & Export"

---

## 4. Wireframes (375px Mobile-First)

### Wireframe 1: Copy/Export Sheet
```
┌────────────────────────────────────┐
│         📋 EXPORT NOTE             │
│ [×]                                │
├────────────────────────────────────┤
│                                    │
│  Export "Morning Drinks"            │
│  5 items • 2.3 MB estimated       │
│                                    │
│  FORMAT                           │
│  ┌──────────────────────────────────┐│
│  │ (●) CSV (for Excel/Sheets)     ││
│  │    Spreadsheet compatible        ││
│  └──────────────────────────────────┘│
│  ┌──────────────────────────────────┐│
│  │ ( ) JSON (for developers)       ││
│  │ ( ) PDF (printable)             ││
│  │ ( ) TapFo Backup (full)         ││
│  └──────────────────────────────────┘│
│                                    │
│  INCLUDE                           │
│  [✓] Item names                    │
│  [✓] Prices                        │
│  [✓] Descriptions                  │
│  [✓] Tags                          │
│  [ ] Photos (not available offline) │
│                                    │
│  [Cancel]       [Generate Export]  │
│                                    │
└────────────────────────────────────┘
```

### Wireframe 2: Import Wizard - Step 1 (Upload)
```
┌────────────────────────────────────┐
│         📥 IMPORT ITEMS            │
│ [×]                                │
├────────────────────────────────────┤
│                                    │
│  STEP 1: SELECT FILE               │
│                                    │
│  ┌──────────────────────────────────┐│
│  │                                   ││
│  │     📁                           ││
│  │                                   ││
│  │  Drop file here or tap to browse ││
│  │                                   ││
│  │  Supported: CSV, JSON, XLSX       ││
│  │                                   ││
│  └──────────────────────────────────┘│
│                                    │
│  ┌──────────────────────────────────┐│
│  │ 📋 Or paste from clipboard       ││
│  │    Detected: CSV (5 rows)         ││
│  │    [Use This]                    ││
│  └──────────────────────────────────┘│
│                                    │
│  ┌──────────────────────────────────┐│
│  │ [📥 Download TapFo Template]    ││
│  │    Get a pre-formatted CSV        ││
│  └──────────────────────────────────┘│
│                                    │
└────────────────────────────────────┘
```

---

## 5. User Flows

### CSV Import Flow
1. User taps "Import Items" on note
2. Step 1: Select/upload file
3. File parsed, headers detected
4. Step 2: Field mapping UI (auto-maps name, price)
5. User confirms/adjusts mappings
6. Step 3: Validation and review
7. Warnings shown for price format, missing fields
8. User taps "Import"
9. Progress bar shows import progress
10. Success toast: "42 items imported!"
11. Items appear in note

### Export Flow
1. User taps "Export" on note
2. Select format (CSV/JSON/PDF)
3. Select fields to include
4. Tap "Generate Export"
5. Processing indicator
6. File ready, download triggered

---

## 6. SnSIS Hierarchy Context

- Import creates Items within a Note
- Import into existing Note: items appended
- Import into new Note: Note created first
- Import validates against Item schema
- Duplicate detection runs on imported items

---

## 7. Implementation Checklist

- [ ] Export sheet UI (format picker, field selector)
- [ ] CSV export generation
- [ ] JSON export generation
- [ ] PDF export (basic)
- [ ] TapFo backup format (full JSON dump)
- [ ] Import wizard (3 steps)
- [ ] File upload (drag-drop + browse)
- [ ] Clipboard paste detection
- [ ] CSV/JSON parser
- [ ] Auto field mapping (name, price, description, tags)
- [ ] Manual field mapping UI
- [ ] Live preview during mapping
- [ ] Validation with warnings
- [ ] Warning resolution UI
- [ ] Import progress indicator
- [ ] Bulk item creation
- [ ] Duplicate detection on import
- [ ] Download trigger
- [ ] Share sheet for export
- [ ] Download TapFo template CSV
- [ ] Error report (failed rows)
- [ ] Undo import
