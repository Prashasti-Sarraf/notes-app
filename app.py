import json
import os
from datetime import datetime

DATA_FILE = "notes.json"


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


def score_note(note, terms):
    """Return a relevance score for a note against the search terms.

    Matches are weighted by where they occur: an exact tag match counts
    most, then the title, then partial tag matches, then the body.
    """
    title = note["title"].lower()
    body = note["body"].lower()
    tags = [t.lower() for t in note["tags"]]

    score = 0
    for term in terms:
        if term in tags:
            score += 5
        else:
            score += sum(2 for tag in tags if term in tag)
        score += 3 * title.count(term)
        score += 1 * body.count(term)
    return score


def search_notes():
    query = input("Search (keywords or tags): ").strip().lower()
    terms = [t for t in query.split() if t]
    if not terms:
        print("Empty search.")
        return

    notes = load_notes()
    results = [(score_note(n, terms), n) for n in notes]
    results = [(score, n) for score, n in results if score > 0]
    results.sort(key=lambda pair: (-pair[0], pair[1]["id"]))

    if not results:
        print("No matching notes.")
        return

    print(f"Found {len(results)} matching note(s):")
    for score, n in results:
        tags = ", ".join(n["tags"]) if n["tags"] else "—"
        print(f"#{n['id']} | {n['title']}  [tags: {tags}]  (relevance: {score})")


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
            search_notes()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()