import shutil
import base64
import ollama
from pathlib import Path
from tqdm import tqdm
from collections import Counter

# --- CONFIGURATION ---
SOURCE_DIR = Path(r"C:\YOUR_PATH")  # 📁 Change this

# 🎯 ORDER MATTERS — first matching category wins.
CATEGORIES = [
    "Dog",
    "Kids",
    "Shoes",
    "Running",    
    "Cars", 
    "Video Games",    
    "Finances",
    "Shopping",
    "Jokes",
    "Home",
    "Work",
    "Programming",
    "AI",
    "Technology",    
]

MODEL = "qwen2.5vl:7b"  # Must be a vision-capable model

# Set to True to preview without moving anything
DRY_RUN = False

# Supported image extensions
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp')


def classify_image(image_path: Path) -> str:
    """Asks the local vision AI to categorize the image, respecting category priority."""

    # Build a numbered list so the AI understands the priority order
    numbered = "\n".join(f"  {i+1}. {cat}" for i, cat in enumerate(CATEGORIES))

    prompt = (
        "You are a file organization assistant.\n\n"
        "Below is a prioritized list of categories, from highest to lowest priority:\n"
        f"{numbered}\n\n"
        "Analyze the image and assign it to the FIRST category in the list that applies.\n"
        "If a higher-priority category partially matches, it wins over a lower-priority one.\n"
        "If none of the categories apply, reply 'Uncategorized'.\n"
        "Reply with ONLY the category name, nothing else."
    )

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_data],
            }]
        )
        ans = response['message']['content'].strip().strip('.')

        # Respect priority order when matching the response
        for cat in CATEGORIES:
            if cat.lower() in ans.lower():
                return cat

        return "Uncategorized"

    except Exception as e:
        tqdm.write(f"\n⚠️  Error on '{image_path.name}': {e}")
        return "Error"


def main():
    if not SOURCE_DIR.exists():
        print(f"❌ Source directory not found: {SOURCE_DIR}")
        return

    # Create category folders
    for cat in CATEGORIES + ["Uncategorized", "Error"]:
        (SOURCE_DIR / cat).mkdir(exist_ok=True)

    # Collect image files at top level only (skip already-sorted subfolders)
    files = [
        f for f in SOURCE_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS
    ]

    if not files:
        print(f"🤷 No images found in {SOURCE_DIR}")
        return

    print(f"📸 Found {len(files)} image(s) in {SOURCE_DIR}")
    if DRY_RUN:
        print("🔍 DRY RUN enabled — no files will be moved.\n")

    results = {}

    for file_path in tqdm(files, desc="Categorizing"):
        category = classify_image(file_path)
        results[file_path.name] = category

        dest = SOURCE_DIR / category / file_path.name

        if DRY_RUN:
            tqdm.write(f"  [{category:20s}] {file_path.name}")
        else:
            if dest.exists():
                tqdm.write(f"  ⚠️  Skipped (already exists): {dest}")
            else:
                shutil.move(str(file_path), str(dest))

    # --- Summary ---
    print("\n📊 Summary")
    print("=" * 40)
    counts = Counter(results.values())
    for cat, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:<25} {count} image(s)")
    print("=" * 40)
    print("✨ Done!" + (" (Dry run — nothing moved)" if DRY_RUN else ""))


if __name__ == "__main__":
    main()
