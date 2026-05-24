## 1. Core search logic

- [x] 1.1 Add scoring weight constants to `app.py` (e.g. `TITLE_WEIGHT = 3`, `TAG_WEIGHT = 2`, `BODY_WEIGHT = 1`)
- [x] 1.2 Implement a pure `search_notes(notes, query)` helper that returns notes ranked by relevance (no I/O)
- [x] 1.3 Tokenize the query into lowercased, whitespace-separated terms; return an empty result for an empty/whitespace-only query
- [x] 1.4 Score each note (all comparisons lowercased / case-insensitive): title term occurrences × `TITLE_WEIGHT` + body term occurrences × `BODY_WEIGHT` + (tags containing the term as a substring) × `TAG_WEIGHT`; sum across all query terms and all fields (additive)
- [x] 1.5 Keep only notes with score > 0 and sort by score descending, then by `id` ascending for deterministic tie-breaking

## 2. CLI integration

- [x] 2.1 Implement `search_notes_cli()` that prompts for a query and reads notes via the existing `load_notes()`
- [x] 2.2 If the stripped query is empty, print an explicit "empty query" message and return without searching
- [x] 2.3 Call `search_notes()`; if it returns no matches, print an explicit "no matching notes found" message
- [x] 2.4 Print matched notes in ranked order using a readable summary (id, title, tags) consistent with `list_notes()`
- [x] 2.5 Add a "Search notes" entry to the menu in `main()` and wire the new choice to `search_notes_cli()`, renumbering the menu/branches

## 3. Verification

- [x] 3.1 Manually verify: a title-only match ranks above a body-only match for the same query (e.g., against `notes.json`)
- [x] 3.2 Manually verify: case-insensitive keyword match and partial tag match (e.g., "mum" → tag "mumbai") both return the expected note
- [x] 3.3 Manually verify: a note matching a term in both title and a tag outranks a note matching it in only one field (additive scoring)
- [x] 3.4 Manually verify: empty query and no-result query each show their distinct explicit message
- [x] 3.5 Confirm no new imports beyond the Python standard library were introduced
