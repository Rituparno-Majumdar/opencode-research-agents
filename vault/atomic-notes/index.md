---
title: Atomic Notes - Graph View
type: dashboard
tags: [atomic-notes, graph, navigation]
---

## 📊 Atomic Notes Graph

```dataviewjs
// Atomic Notes Graph - Only shows notes from vault/atomic-notes/

dv.list(dv.pages('"vault/atomic-notes"').file.name);
```

### Graph View Instructions

To see the actual **interactive graph**:

1. Open Obsidian
2. Navigate to `vault/atomic-notes/`
3. Right-click any note → **"Open local graph view"**

The graph will ONLY show notes from these folders:
- `vault/atomic-notes/concepts/`
- `vault/atomic-notes/people/`
- `vault/atomic-notes/texts/`
- `vault/atomic-notes/patterns/`
- `vault/atomic-notes/questions/`

### Quick Stats

```dataview
TABLE WITHOUT ID
  type,
  choice(length(rows) = 0, "⚠️ Empty", length(rows) + " notes") as "Count"
FROM "vault/atomic-notes"
GROUP BY type
```

### Recent Notes

```dataview
LIST
FROM "vault/atomic-notes"
WHERE file.ctime >= date("-7 days")
SORT file.ctime DESC
LIMIT 10
```

> 📌 **Note:** This vault excludes system files from graph view (agents, memory, research) via `.obsidian/.gitignore`