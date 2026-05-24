## Why

The notes app can add, list, and delete notes, but offers no way to find a specific note once the list grows. Users must scan the entire list by eye. A keyword and tag search with relevance ranking lets users locate notes quickly.

## What Changes

- Add a **Search notes** option to the CLI menu.
- Accept a free-text query from the user and match it against each note's title, body, and tags.
- Rank matching notes by relevance, scoring **title matches higher than body matches**, with tag matches contributing as well.
- Display ranked results in a readable summary; show an explicit message when there are no matches.
- Handle an empty or whitespace-only query explicitly (prompt again / report the empty query) rather than returning every note or crashing.
- Implementation uses only the **Python standard library** — no new dependencies.

## Capabilities

### New Capabilities
- `notes-search`: Searching stored notes by keyword and tag, with relevance-ranked results and explicit handling of empty queries and no-result cases.

### Modified Capabilities
<!-- None. No existing specs define current behavior; search is purely additive. -->

## Impact

- **Code**: `app.py` — add a search function and a new menu entry wired into `main()`. Reuses the existing `load_notes()` data access.
- **Data**: Read-only over the existing `notes.json` schema (`id`, `title`, `body`, `tags`, `created_at`). No schema change.
- **Dependencies**: None added; standard library only (`re` / `str` operations).
- **APIs / systems**: None external. Interactive CLI only.
