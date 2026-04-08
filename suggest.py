import base64
import ollama
import json
from pathlib import Path
from tqdm import tqdm
from collections import Counter

# --- CONFIGURATION ---
SOURCE_DIR = Path(r"YOUR_PATH")  # 📁 Change this

MODEL = "qwen2.5vl:7b"  # Must be a vision-capable model

# How many images to sample (set to None to scan all)
SAMPLE_SIZE = 50

# How many category suggestions to return
NUM_SUGGESTIONS = 10

# Supported image extensions
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp')


def describe_image(image_path: Path) -> str:
    """Asks the AI for a short description of what's in the image."""
    prompt = (
        "Describe the main subject of this image in 3 to 5 words. "
        "Be concise and specific. Examples: 'golden retriever on grass', "
        "'child birthday party', 'trail running shoes', 'minecraft screenshot'. "
        "Reply with ONLY the short description, nothing else."
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
        return response['message']['content'].strip().strip('.')
    except Exception as e:
        tqdm.write(f"\n⚠️  Error on '{image_path.name}': {e}")
        return ""


def suggest_categories(descriptions: list[str], n: int) -> list[str]:
    """Asks a text model to cluster descriptions into suggested category names."""
    joined = "\n".join(f"- {d}" for d in descriptions if d)

    prompt = (
        f"Here are short descriptions of images from a personal photo collection:\n\n"
        f"{joined}\n\n"
        f"Based on these, suggest exactly {n} broad, useful folder categories "
        f"to organize these images (like 'Dogs', 'Kids', 'Running Shoes', 'Travel', etc.).\n"
        f"The categories should cover most of the images and be practical for sorting.\n"
        f"Return ONLY a JSON array of category name strings, no explanation. "
        f'Example: ["Dogs", "Kids", "Travel", "Sports"]'
    )

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{'role': 'user', 'content': prompt}]
        )
        raw = response['message']['content'].strip()

        # Extract JSON array from response
        start, end = raw.find('['), raw.rfind(']')
        if start != -1 and end != -1:
            return json.loads(raw[start:end + 1])

        # Fallback: split by newline/comma if JSON fails
        return [line.strip(' "-,') for line in raw.splitlines() if line.strip()]

    except Exception as e:
        print(f"\n⚠️  Error generating suggestions: {e}")
        return []


def main():
    if not SOURCE_DIR.exists():
        print(f"❌ Source directory not found: {SOURCE_DIR}")
        return

    # Collect image files at the top level only
    all_files = [
        f for f in SOURCE_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS
    ]

    if not all_files:
        print(f"🤷 No images found in {SOURCE_DIR}")
        return

    # Sample if needed
    import random
    files = all_files if SAMPLE_SIZE is None else random.sample(
        all_files, min(SAMPLE_SIZE, len(all_files))
    )

    print(f"📸 Found {len(all_files)} image(s) — analyzing {len(files)} sample(s)...\n")

    # Step 1: Describe each image
    descriptions = []
    for file_path in tqdm(files, desc="Describing images"):
        desc = describe_image(file_path)
        if desc:
            descriptions.append(desc)
            tqdm.write(f"  {file_path.name:<40} → {desc}")

    # Step 2: Suggest categories
    print(f"\n🤖 Asking AI to suggest {NUM_SUGGESTIONS} categories...\n")
    categories = suggest_categories(descriptions, NUM_SUGGESTIONS)

    # Step 3: Print results
    print("=" * 50)
    print(f"✅ Suggested categories for your images:\n")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    print("=" * 50)
    print("\n💡 Copy these into sort_images.py as your CATEGORIES list:")
    print(f"\nCATEGORIES = {json.dumps(categories, indent=4)}\n")


if __name__ == "__main__":
    main()
