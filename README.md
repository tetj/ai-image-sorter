# 🖼️ AI Image Sorter

Automatically organize your images into folders using a local AI vision model via [Ollama](https://ollama.com). No cloud, no API keys — runs entirely on your machine.

## Scripts

| Script | Description |
|---|---|
| `suggest_categories.py` | Analyzes a sample of your images and suggests folder categories |
| `sort_images.py` | Sorts images into folders based on your category list |

The intended workflow is to run `suggest_categories.py` first, then paste the output into `sort_images.py`.

## Requirements

```bash
pip install ollama tqdm
```

You also need [Ollama](https://ollama.com) installed with a vision-capable model pulled:

```bash
ollama pull qwen2.5vl:7b
```

## Usage

### 1. Suggest categories
Edit `SOURCE_DIR` in `suggest_categories.py`, then run:
```bash
python suggest_categories.py
```
It samples up to 50 images, describes each one, and outputs a ready-to-paste `CATEGORIES` list.

### 2. Sort images
Paste the suggested categories into `sort_images.py` and set your `SOURCE_DIR`. Categories are **priority-ordered** — the first match wins.

```python
CATEGORIES = [
    "Shoes",      # a running shoe → "Shoes", not "Running"
    "Running",
    "Dog",        # a dog with kids → "Dog", not "Kids"
    "Kids",
    ...
]
```

Do a dry run first (enabled by default) to preview results without moving anything:
```bash
python sort_images.py
```

Then set `DRY_RUN = False` and run again to move the files.

## Notes

- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`
- Re-running is safe — only files at the root of `SOURCE_DIR` are processed, already-sorted subfolders are ignored
- Images that don't match any category go into an `Uncategorized` folder
