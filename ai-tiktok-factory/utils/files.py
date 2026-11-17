"""
File and path management utilities.
"""

import json
import re
import shutil
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional
import config

def remove_accents(text: str) -> str:
    """Remove Vietnamese tone marks and accents for slug generation."""
    # Custom replacement for Vietnamese characters like đ, Đ
    text = text.replace("đ", "d").replace("Đ", "D")
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")

def slugify(text: str) -> str:
    """Convert string to a clean URL/filename-safe slug."""
    text = remove_accents(text)
    text = text.lower()
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:60] if text else "video"

def get_output_dir(slug: str) -> Path:
    """Return and create the output folder for a specific video slug."""
    dir_path = config.OUTPUT_DIR / slug
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def get_temp_dir(slug: str) -> Path:
    """Return and create a temp folder for intermediate files."""
    dir_path = config.TEMP_DIR / slug
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def cleanup_temp(slug: Optional[str] = None):
    """Clean up temporary directory."""
    try:
        if slug:
            target = config.TEMP_DIR / slug
            if target.exists():
                shutil.rmtree(target, ignore_errors=True)
        else:
            if config.TEMP_DIR.exists():
                shutil.rmtree(config.TEMP_DIR, ignore_errors=True)
                config.TEMP_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[Warning] Failed to cleanup temp dir: {e}")

def save_json(file_path: Path, data: Any):
    """Save data as pretty-printed JSON with UTF-8 encoding."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(file_path: Path) -> Any:
    """Load JSON data from file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_text(file_path: Path, text: str):
    """Save plain text with UTF-8 encoding."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

def load_text(file_path: Path) -> str:
    """Load plain text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def get_available_assets(category: str) -> List[Path]:
    """
    Get list of files in assets folder (images, videos, music, fonts).
    """
    cat_dir = config.ASSETS_DIR / category
    if not cat_dir.exists():
        return []
    return [f for f in cat_dir.glob("*") if f.is_file()]
