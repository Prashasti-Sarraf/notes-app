## Context

`app.py` is a single-file, interactive CLI notes manager backed by `notes.json`. Notes have `id`, `title`, `body`, `tags` (list of strings), and `created_at`. The menu loop in `main()` dispatches numeric choices to `add_note`, `list_notes`, and `delete_note`, all of which read via `load_notes()`. Search is purely additive and read-only; it must follow the same in-file, standard-library-only style with no new dependencies. See `proposal.md` for motivation and `specs/notes-search/spec.md` for requirements.

## Goals / Non-Goals

**Goals:**
- Find notes by keyword across title and body, and by tag.
- Rank results by relevance with title matches weighted above body matches; tags contribute too.
- Deterministic, repeatable ordering.
- Explicit, distinct handling of empty queries and no-result searches.
- Standard library only; consistent with the existing code style.

**Non-Goals:**
- Fuzzy matching, stemming, synonyms, or typo tolerance.
- Persisting search history or indexing for performance (the dataset is tiny).
- Boolean operators, phrase quoting, or field-scoped query syntax (e.g., `tag:foo`).
- Changing the `notes.json` schema or any existing command.

## Decisions

**Tokenization: split the query into whitespace-separated, lowercased terms.**
A query like `mumbai team` becomes `["mumbai", "team"]`; each term is matched independently and its contributions summed. Rationale: simple, predictable, and lets multi-word queries rank notes matching more terms higher. Alternative considered: treat the whole query as one substring — rejected because it can't reward partial multi-term matches and feels brittle for natural queries.

**Matching: always case-insensitive; substring (partial) match across title, body, AND tags.**
All comparisons lowercase both sides, so case never affects matching (no case-sensitive mode — chosen for simplicity). Title and body are free text, so substring (`term in title.lower()`) is the natural fit. Tags also match partially: a term matches a tag when it is a substring of that tag (e.g. `mum` matches tag `mumbai`), keeping matching behavior consistent across all fields. Alternative considered: exact tag equality — rejected so partial queries behave the same everywhere.

**Scoring: weighted sum with title > body, plus tags.** Weights:
- title term occurrence: **3** (`TITLE_WEIGHT`) per occurrence
- tag substring match: **2** (`TAG_WEIGHT`) per tag containing the term
- body term occurrence: **1** (`BODY_WEIGHT`) per occurrence

**Explicit ranking formula.** For a query tokenized into lowercased terms `T = {t1, …, tn}` (whitespace split), and a note `N` with lowercased `title`, `body`, and `tags`:

```
score(N) = Σ over t in T of [
      TITLE_WEIGHT * title.count(t)
    + BODY_WEIGHT  * body.count(t)
    + TAG_WEIGHT   * count(tag in tags where t in tag)
]
```

A note is a result iff `score(N) > 0`. Field contributions are **additive**: a note that matches a term in both its title and a tag earns `TITLE_WEIGHT + TAG_WEIGHT` for that term, so it outranks a note matching the term in only one field. This guarantees a title match outranks a body-only match and that more occurrences raise the score (satisfies the spec's ranking scenarios). Counting occurrences (via `str.count`) rather than a 0/1 flag rewards density. Alternative considered: binary field presence (title=2, body=1) — simpler but doesn't satisfy the "more matches score higher" scenario.

**Ordering: sort by score descending, then by `id` ascending for ties.**
Python's `sorted` is stable; using `key=lambda r: (-score, id)` makes ties deterministic and reproducible across runs, satisfying the deterministic-ordering scenario.

**Input handling: validate before searching.** Strip the raw input; if the result is empty, print an "empty query" message and return without scanning notes. After scoring, if no note has a score > 0, print a "no matches found" message. These are two distinct branches so the user always gets clear feedback. The no-notes-stored case naturally falls into the no-results branch (nothing scores).

**Structure: a pure `search_notes(notes, query)` helper plus a thin `search_notes_cli()` for I/O.**
Keeping ranking logic in a pure function (inputs → ranked list) makes the relevance rules directly testable and keeps `main()` dispatch consistent with the existing handlers. A new menu entry "Search notes" is inserted and the menu numbering / `main()` branches updated accordingly.

## Risks / Trade-offs

- **Substring matching produces incidental hits** (e.g., "art" matches "smart"; "mum" matches tag "mumbai") → Accept for v1; documented as a known limitation. Whole-word matching can be added later without changing the interface.
- **Weight values are somewhat arbitrary** → The exact numbers don't matter as long as title > body and occurrences accumulate; chosen so a single title match (3) always beats a single body match (1). Centralized as named constants so they're easy to tune.
- **No pagination for large result sets** → Dataset is tiny and CLI-bound; out of scope. Results print in ranked order regardless of count.
- **No case-sensitive option** → Search is always case-insensitive by design decision; a toggle can be added later if users need exact-case matching.
