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
        print("3. Delete note")
        print("4. Quit")
        choice = input("> ").strip()
        if choice == "1":
            add_note()
        elif choice == "2":
            list_notes()
        elif choice == "3":
            delete_note()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()