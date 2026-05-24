# notes-search Specification

## Purpose

Provide a search capability over stored notes so users can find notes by free-text keyword or tag, with results ranked by relevance and explicit handling of empty queries and no-result searches.

## Requirements

### Requirement: Search notes by keyword and tag

The system SHALL provide a search action that accepts a free-text query and returns notes whose title, body, or tags match the query. Matching SHALL always be case-insensitive. A note SHALL be considered a match when the query (or any of its whitespace-separated terms) appears as a substring of the note's title, body, or any of the note's tags (partial matching across all three fields).

#### Scenario: Keyword matches note title

- **WHEN** a user searches for a term that appears in a note's title
- **THEN** that note SHALL be included in the results

#### Scenario: Keyword matches note body

- **WHEN** a user searches for a term that appears only in a note's body
- **THEN** that note SHALL be included in the results

#### Scenario: Query partially matches a tag

- **WHEN** a user searches for a term that appears as a substring of one of a note's tags (e.g., "mum" against the tag "mumbai")
- **THEN** that note SHALL be included in the results

#### Scenario: Search is case-insensitive

- **WHEN** a user searches using a different letter case than the stored text (e.g., "MUMBAI" against a note containing "mumbai")
- **THEN** the note SHALL still be matched

### Requirement: Rank results by relevance with title weighted above body

The system SHALL rank matching notes by a relevance score and present them in descending score order. A match in the title SHALL contribute more to the score than a match in the body. Tag matches SHALL also contribute to the score. Contributions from different fields SHALL be additive: when a query matches a note in more than one field (for example both its title and a tag), each matching field SHALL add to that note's score. When two notes have equal scores, the system SHALL fall back to a stable, deterministic order (e.g., by note id).

#### Scenario: Title match outranks body match

- **WHEN** one note matches the query in its title and another note matches the same query only in its body
- **THEN** the note with the title match SHALL be ranked above the note with the body-only match

#### Scenario: More matches score higher

- **WHEN** the query term appears multiple times across a note's title, body, and tags
- **THEN** that note SHALL receive a higher score than a note where the term appears fewer times in lower-weighted fields

#### Scenario: Match in both title and tags scores additively

- **WHEN** a query term appears in both a note's title and one of its tags
- **THEN** that note's score SHALL include both the title contribution and the tag contribution
- **AND** that note SHALL be ranked above a note where the same term appears in only one of those fields

#### Scenario: Deterministic ordering for ties

- **WHEN** two matching notes have identical relevance scores
- **THEN** the system SHALL order them deterministically (by ascending note id) so repeated identical searches return the same order

### Requirement: Handle empty queries explicitly

The system SHALL treat a query that is empty or contains only whitespace as invalid input. It SHALL NOT return all notes or perform a search for an empty query, and SHALL inform the user that the query was empty.

#### Scenario: Empty query entered

- **WHEN** a user submits a search with an empty or whitespace-only query
- **THEN** the system SHALL display a message indicating the query was empty
- **AND** SHALL NOT list any notes as results

### Requirement: Handle no-result searches explicitly

When a valid query matches no notes, the system SHALL display an explicit "no results" message rather than silent output or an empty listing.

#### Scenario: Valid query with no matches

- **WHEN** a user searches for a non-empty query that matches no note's title, body, or tags
- **THEN** the system SHALL display a message indicating that no matching notes were found

#### Scenario: Searching with no notes stored

- **WHEN** a user performs a search while no notes exist
- **THEN** the system SHALL display a message indicating that no matching notes were found
