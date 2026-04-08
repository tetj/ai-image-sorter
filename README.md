# AI Image Sorter

Automatically organize your images into folders using a local AI vision model via [Ollama](https://ollama.com). 

No cloud, no API keys : runs entirely on your machine.

But requires a powerful machine (see recommend specs below)

## Scripts

| Script | Description |
|---|---|
| `suggest.py` | Analyzes a sample of your images and suggests folder categories |
| `sort.py` | Sorts images into folders based on your category list |

The intended workflow is to run `suggest.py` first, then paste the output into `sort.py`.

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


This step is optional. Indeed, instead, you can simply decide your categories by yourself, see Step #2.


Edit `SOURCE_DIR` in `suggest.py`, then run:
```bash
python suggest.py
```
It samples up to 50 images, describes each one, and outputs a ready-to-paste `CATEGORIES` list.

### 2. Sort images

a) Edit `sort.py` :

- Set your own `SOURCE_DIR`. 
- Edit the `CATEGORIES` to fit your needs.

Categories are **priority-ordered** : the first match wins.

For example, in the example below, a picture of a running shoe would be moved to shoes.

And a screenshot of a Strava run would be moved to Running.


```python
CATEGORIES = [
    "Shoes",  
    "Running",
    "Dog",  
    "Kids",
    ...
]
```

b) run the script :
```bash
python sort.py
```


## Recommended Specs

The bottleneck is almost entirely the vision model (`qwen2.5vl:7b`), not the script itself.

### Minimum (slow but functional)
- **GPU**: 8 GB VRAM (e.g. RTX 3070, RX 6700 XT) — fits the 7B model in VRAM at 4-bit quantization
- **RAM**: 16 GB
- **CPU**: Any modern quad-core (used only for image loading/moving)
- **Storage**: ~5 GB free for the model weights

Expect roughly **5–15 seconds per image** — 500 images would take 1–2 hours.

### Recommended (comfortable)
- **GPU**: 12 GB VRAM (e.g. RTX 4070) — fits the model comfortably with headroom
- **RAM**: 32 GB
- **Storage**: SSD recommended, the model loads faster

Roughly **2–5 seconds per image**.

### No GPU / CPU only
It will still run via Ollama, but expect **30–60 seconds per image** — only practical for very small batches.

### Tips to speed things up
- `qwen2.5vl:7b` in **Q4 quantization** (Ollama's default) — good balance of speed and accuracy
- Less VRAM? Try `moondream` or `llava:7b` — lighter models, slightly less accurate
- Large DSLR/RAW files slow things down significantly — add a resize step with Pillow before sorting

## Notes

- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`
- Re-running is safe — only files at the root of `SOURCE_DIR` are processed, already-sorted subfolders are ignored
- Images that don't match any category go into an `Uncategorized` folder
