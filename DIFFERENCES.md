# Vibe Coding vs Spec-Driven Development — Observations

## Feature implemented
Search notes by keyword or tag with relevance ranking.

## TL;DR
The two approaches produced **functionally similar code**. The differences were
not in raw capability but in *what got surfaced to the human*, *what edge cases
were handled by default*, and *what artifacts were left behind in the repo*.

---

## Vibe Coding (branch: `vibe_coded_submission`)

**Prompt used:** A single vague instruction — "add a search feature... ranked by relevance. Make it work."

**What Claude did:**
- Implemented search with a clear relevance score and displayed it in output
- Made reasonable default choices (matching in title, body, tags)
- Wrote working code in one shot

**What was missing or implicit:**
- No record of *why* the scoring formula was chosen — it was decided silently
- Edge cases like empty queries, no matches, or partial matches were either
  unhandled or handled silently without me being asked
- No artifact in the repo explaining the design — only the code itself

**Pros**
- Fastest path to working code (one prompt, ~30 seconds)
- Surfaced the relevance score directly in the output, which was actually a nicer UX
- Zero overhead — no folders, no slash commands, no review step

**Cons**
- Decisions made invisibly; reviewing the code is the only way to know what was assumed
- A future session of Claude (or a teammate) would have to re-derive the logic from the code
- No room to push back on assumptions *before* code was written

---

## Spec-Driven Development (branch: `sdd_submission`)

**Workflow:** `/opsx:propose` → review proposal → `/opsx:apply` → `/opsx:archive`

**What Claude did:**
- Generated a proposal explicitly listing the search behavior, ranking rules, and edge cases
- Implemented case-insensitive matching by default
- Supported partial matches (substring search) without me asking
- Hid the raw relevance score from the user-facing output (cleaner but less transparent than the vibe-coded version)
- Left behind a permanent `openspec/specs/` folder documenting the feature

**What was different from vibe coding:**
- Case-insensitive search and partial matching were spec'd explicitly; vibe coding didn't surface this decision
- Output was more polished but *less informative* — the score was hidden
- The repo now has documentation of the feature that survives chat sessions

**Pros**
- The proposal step caught defaults I would otherwise not have known about
- `openspec/specs/` is a permanent record — next time someone touches search, they have context
- Forces a "review before build" moment, even if brief

**Cons**
- Slower (extra ~5 min for the propose + review cycle)
- For a feature this small, the extra ceremony didn't change the output meaningfully
- Some design choices (hiding the score) were *worse* than the vibe-coded version

---

## Honest Conclusion

For a **small, well-understood feature like this**, vibe coding and SDD produced
nearly identical results. The vibe-coded version was actually slightly better in
one respect — it showed the relevance score, which felt more useful. SDD made
different defaults (case-insensitive, partial match) that felt more polished but
also hid information.

Where SDD genuinely pulled ahead was **not in the code itself, but in the
artifacts left behind**:

- The proposal made silent assumptions explicit
- The archived spec means the next change to search has context
- The diff is reviewable at the *intent* level, not just the code level

**My takeaway:** SDD's value scales with project size and team size, not with
feature complexity. For a solo CLI tool, vibe coding is fine. For a codebase
where 10 people will touch the search logic over 2 years, the spec folder is
worth the overhead. The instructor's point about context being the bottleneck
matches what I observed — the value of OpenSpec isn't visible in this single
feature, it would compound across many features over time.
