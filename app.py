import json
import os
from datetime import datetime

DATA_FILE = "notes.json"

# Relevance weights for search. Title matches outrank tag matches, which
# outrank body matches. Contributions across fields are additive.
TITLE_WEIGHT = 3
TAG_WEIGHT = 2
BODY_WEIGHT = 1


def load_notes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_notes(notes):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


def add_note():
    title = input("Title: ").strip()
    body = input("Body: ").strip()
    tags_raw = input("Tags (comma-separated): ").strip()
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    notes = load_notes()
    note = {
        "id": len(notes) + 1,
        "title": title,
        "body": body,
        "tags": tags,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    notes.append(note)
    save_notes(notes)
    print(f"✓ Note #{note['id']} saved.")


def list_notes():
    notes = load_notes()
    if not notes:
        print("No notes yet.")
        return
    for n in notes:
        tags = ", ".join(n["tags"]) if n["tags"] else "—"
        print(f"#{n['id']} | {n['title']}  [tags: {tags}]")


def delete_note():
    try:
        note_id = int(input("Note ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    notes = load_notes()
    new_notes = [n for n in notes if n["id"] != note_id]
    if len(new_notes) == len(notes):
        print("Note not found.")
        return
    save_notes(new_notes)
    print(f"✓ Note #{note_id} deleted.")


def search_notes(notes, query):
    """Return notes matching query, ranked by relevance (highest first).

    Matching is case-insensitive and uses partial (substring) matches across
    title, body, and tags. Score per note is the additive sum, over each
    whitespace-separated query term, of:
        TITLE_WEIGHT * occurrences in title
      + BODY_WEIGHT  * occurrences in body
      + TAG_WEIGHT   * number of tags containing the term
    Only notes with a score > 0 are returned. Ties break by ascending id so
    results are deterministic. An empty/whitespace-only query returns [].
    """
    terms = query.lower().split()
    if not terms:
        return []

    scored = []
    for n in notes:
        title = n.get("title", "").lower()
        body = n.get("body", "").lower()
        tags = [t.lower() for t in n.get("tags", [])]

        score = 0
        for term in terms:
            score += TITLE_WEIGHT * title.count(term)
            score += BODY_WEIGHT * body.count(term)
            score += TAG_WEIGHT * sum(1 for tag in tags if term in tag)

        if score > 0:
            scored.append((score, n))

    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [n for _, n in scored]


def search_notes_cli():
    query = input("Search: ").strip()
    if not query:
        print("Empty query — enter a keyword or tag to search.")
        return

    results = search_notes(load_notes(), query)
    if not results:
        print(f"No matching notes found for '{query}'.")
        return

    print(f"Found {len(results)} matching note(s):")
    for n in results:
        tags = ", ".join(n["tags"]) if n["tags"] else "—"
        print(f"#{n['id']} | {n['title']}  [tags: {tags}]")


def main():
    while True:
        print("\n--- Notes App ---")
        print("1. Add note")
        print("2. List notes")
        print("3. Search notes")
        print("4. Delete note")
        print("5. Quit")
        choice = input("> ").strip()
        if choice == "1":
            add_note()
        elif choice == "2":
            list_notes()
        elif choice == "3":
            search_notes_cli()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()