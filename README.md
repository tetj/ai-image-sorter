# AI Image Sorter

Automatically organize your images into folders using a local AI vision model via [Ollama](https://ollama.com). 

No cloud, no API keys : runs entirely on your machine.

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

a) Edit the categories to fit your needs by editing the CATEGORIES in `sort.py`.
And set your own `SOURCE_DIR`. 
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


## Notes

- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`
- Re-running is safe — only files at the root of `SOURCE_DIR` are processed, already-sorted subfolders are ignored
- Images that don't match any category go into an `Uncategorized` folder
