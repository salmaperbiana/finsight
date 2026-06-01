import streamlit as st
from pathlib import Path
from PIL import Image


@st.cache_data
def scan_images(folder: str | Path):
    folder = Path(folder)
    exts   = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}
    if not folder.exists():
        return []
    return sorted(
        [
            {
                "path": str(f),
                "name": f.name,
                "ext":  f.suffix.lower(),
                "size_kb": round(f.stat().st_size / 1024, 1),
            }
            for f in folder.iterdir()
            if f.suffix.lower() in exts
        ],
        key=lambda x: x["name"],
    )


@st.cache_data
def get_resolutions(path_name_pairs):
    res = []
    for path_str, name in path_name_pairs:
        try:
            with Image.open(path_str) as im:
                w, h = im.size
                res.append(
                    {
                        "name":      name,
                        "width":     w,
                        "height":    h,
                        "megapixel": round(w * h / 1_000_000, 2),
                        "mode":      im.mode,
                    }
                )
        except Exception:
            pass
    return res
