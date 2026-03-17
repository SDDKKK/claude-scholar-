---
name: obsidian-project-bootstrap
description: Use this skill when starting a new research project, importing an existing code plus Markdown repository into Obsidian, or binding the current repository to a compact project knowledge base for future syncing.
---

# Obsidian Project Bootstrap

Bootstrap a project knowledge base for the current repository.

## Role in the workflow

This is a **supporting skill**.

Use `obsidian-project-memory` as the main workflow authority. Use this skill only when a repository still needs its initial binding or rebuild.

## When to use

- The user says “start a new research project”
- The user has an existing repo with code plus Markdown and wants an Obsidian knowledge base generated automatically
- `obsidian-project-memory` detects a research-project candidate but no existing binding

## Required input

Resolve the vault path from one of:
1. explicit user input
2. `OBSIDIAN_VAULT_PATH`

## Procedure

1. Identify the repository root.
2. Run the helper script:
   ```bash
   python3 ../obsidian-project-memory/scripts/project_kb.py bootstrap --cwd "$PWD" --vault-path "$OBSIDIAN_VAULT_PATH"
   ```
3. Verify that the bootstrap created at least:
   - `.claude/project-memory/registry.yaml`
   - `.claude/project-memory/<project_id>.md`
   - `Research/{project-slug}/00-Hub.md`
   - `Research/{project-slug}/01-Plan.md`
   - `Research/{project-slug}/Knowledge/Source-Inventory.md`
   - `Research/{project-slug}/Knowledge/Codebase-Overview.md`
4. If the imported project still lacks real background or experiment context, switch to an agent-first pass:
   - read the most informative repo docs and code entry points,
   - synthesize durable notes into `Knowledge/`, `Papers/`, `Experiments/`, `Results/`, or `Writing/`,
   - avoid placeholder notes.
5. Summarize the created knowledge base and the next recommended canonical notes to fill in.

## Notes

- The bootstrap process imports **structure and summaries**, not raw datasets, caches, checkpoints, or the whole code tree.
- Ignore `.git`, `.venv`, `node_modules`, caches, checkpoints, binaries, and other heavy artifacts.
- The default vault is compact: `00-Hub.md`, `01-Plan.md`, `Knowledge/`, `Papers/`, `Experiments/`, `Results/`, `Writing/`, `Daily/`, `Archive/`.
