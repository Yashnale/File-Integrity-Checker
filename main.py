import os
import hashlib
import json

HASH_FILE = "hashes.json"

def calculate_hash(file_path, algo="sha256"):
    """Calculate the hash of a file."""
    hash_func = hashlib.sha256() if algo == "sha256" else hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def scan_folder(folder_path, algo="sha256"):
    """Scan a folder and return a dict of file paths and their hashes."""
    file_hashes = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = calculate_hash(file_path, algo)
    return file_hashes

def save_hashes(file_hashes):
    """Save the hashes to a JSON file."""
    with open(HASH_FILE, "w") as f:
        json.dump(file_hashes, f, indent=4)

def load_hashes():
    """Load hashes from the JSON file."""
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, "r") as f:
        return json.load(f)

def check_integrity(new_hashes, old_hashes):
    """Compare old and new hashes to detect changes."""
    modified = []
    deleted = []
    added = []

    for path, hash_val in old_hashes.items():
        if path not in new_hashes:
            deleted.append(path)
        elif new_hashes[path] != hash_val:
            modified.append(path)

    for path in new_hashes:
        if path not in old_hashes:
            added.append(path)

    return modified, deleted, added

def main():
    folder_path = input("Enter the folder path: ")

    print("\n1. Scan and Save Hashes")
    print("2. Check Integrity")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        hashes = scan_folder(folder_path)
        save_hashes(hashes)
        print("\n✅ Hashes saved successfully!")
    elif choice == "2":
        old_hashes = load_hashes()
        if not old_hashes:
            print("⚠️ No hash records found! Please run option 1 first.")
            return
        new_hashes = scan_folder(folder_path)
        modified, deleted, added = check_integrity(new_hashes, old_hashes)

        print("\n🔍 Integrity Check Results:")
        print(f"Modified Files: {modified if modified else 'None'}")
        print(f"Deleted Files: {deleted if deleted else 'None'}")
        print(f"Added Files: {added if added else 'None'}")
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
