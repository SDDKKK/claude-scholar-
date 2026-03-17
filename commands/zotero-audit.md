---
name: zotero-audit
description: Audit a Zotero collection against the bound Obsidian paper-note corpus and report collection coverage, item-to-note mapping, schema drift, and missing notes
args:
  - name: collection
    description: Zotero collection name or keyword to audit
    required: true
tags: [Research, Zotero, Obsidian, Audit, Literature]
---

# /zotero-audit - Audit Zotero Collection Coverage

Audit a Zotero collection against the current Obsidian `Papers/` directory.

## Workflow

1. Resolve the bound project knowledge base. If the repo is not bound, bootstrap it first or clearly state that coverage cannot be audited against a project vault.
2. Use Zotero to locate the target collection and enumerate all item keys.
3. Run the deterministic verifier:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/zotero-obsidian-bridge/scripts/verify_paper_notes.py"      --papers-dir "/absolute/path/to/Papers"      --expected-zotero-keys "KEY1,KEY2,KEY3"
   ```
4. Report:
   - collection size
   - covered item count / total count
   - missing items
   - schema drift
   - item -> canonical note mapping
5. Ignore non-Zotero bridge notes in `Papers/` by default; use strict mode only when the user explicitly wants every paper note to have a `zotero_key`.
6. If the collection inventory note exists, update it with the latest coverage result.

## Final response

Include:
- coverage ratio such as `16 / 16`
- missing or drifted note paths if any
- the inventory note path when updated
- optional Obsidian open/URI shortcuts for the inventory note
