import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image

from components.metrics import render_image_metrics
from components.charts import (
    chart_format_gambar, chart_ukuran_gambar,
    chart_resolusi_scatter, chart_megapixel,
)
from components.cards import insight_card
from utils.image_utils import scan_images, get_resolutions
from utils.constants import IMAGES_DIR


def render():
    st.markdown('<span class="dataset-badge-orange">📂 Sumber: folder /images (lokal)</span>', unsafe_allow_html=True)
    st.markdown("Dataset gambar struk/nota keuangan untuk pelatihan model **OCR (Optical Character Recognition)**. Gambar disimpan di folder `/images` — belum berlabel.")

    img_files  = scan_images(IMAGES_DIR)
    total_imgs = len(img_files)

    if total_imgs == 0:
        if not IMAGES_DIR.exists():
            st.error(
                f"❌ Folder `images` belum ada.\n\n"
                f"Path yang dicari: `{IMAGES_DIR}`\n\n"
                "Buat folder tersebut lalu masukkan gambar struk ke dalamnya."
            )
        else:
            st.warning("⚠️ Folder `images` ditemukan tapi kosong. Masukkan file gambar (JPG, PNG, dll) ke dalamnya.")
        return

    total_size = sum(f["size_kb"] for f in img_files)
    ext_count  = {}
    for f in img_files:
        ext_count[f["ext"]] = ext_count.get(f["ext"], 0) + 1

    render_image_metrics(total_imgs, total_size, ext_count)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Statistik Dataset Gambar")
    s1, s2 = st.columns(2)
    sizes = [f["size_kb"] for f in img_files]
    with s1: chart_format_gambar(ext_count)
    with s2: chart_ukuran_gambar(sizes)

    st.markdown("### 📐 Analisis Resolusi Gambar")
    with st.spinner("Membaca resolusi gambar..."):
        resolutions = get_resolutions([(f["path"], f["name"]) for f in img_files])

    if resolutions:
        res_df = pd.DataFrame(resolutions)
        r1, r2, r3 = st.columns(3)
        r1.metric("↔️ Rata-rata Lebar",  f"{res_df['width'].mean():.0f} px")
        r2.metric("↕️ Rata-rata Tinggi", f"{res_df['height'].mean():.0f} px")
        r3.metric("🔲 Rata-rata MP",     f"{res_df['megapixel'].mean():.2f} MP")

        res_c1, res_c2 = st.columns(2)
        with res_c1: chart_resolusi_scatter(res_df)
        with res_c2: chart_megapixel(res_df)

    st.markdown("### 🔍 Preview Sample Gambar")
    n_preview    = st.slider("Jumlah gambar yang ditampilkan", 4, min(24, total_imgs), min(8, total_imgs), 4)
    sample_files = img_files[:n_preview]
    for row_start in range(0, len(sample_files), 4):
        cols = st.columns(4)
        for col, img_info in zip(cols, sample_files[row_start:row_start + 4]):
            try:
                img = Image.open(img_info["path"])
                col.image(img, caption=f"{img_info['name']}\n{img_info['size_kb']} KB · {img.size[0]}×{img.size[1]}px", use_container_width=True)
            except Exception:
                col.warning(f"⚠️ {img_info['name']} — gagal dibuka")

    st.markdown("### 📋 Daftar Semua File Gambar")
    file_df = pd.DataFrame([{
        "No": i + 1, "Nama File": f["name"], "Format": f["ext"], "Ukuran": f"{f['size_kb']} KB",
    } for i, f in enumerate(img_files)]).set_index("No")
    st.dataframe(file_df, use_container_width=True)

    insight_card("Insight Dataset Gambar OCR", (
        f"Total **{total_imgs} gambar struk** tersimpan di folder `/images` dengan total ukuran **{total_size/1024:.2f} MB**.\n"
        f"Terdapat **{len(ext_count)} format file** — pastikan format yang digunakan konsisten untuk kemudahan preprocessing.\n"
        f"Variasi ukuran file (min {min(sizes):.0f} KB – maks {max(sizes):.0f} KB) menunjukkan perbedaan resolusi dan kualitas gambar antar struk.\n"
        "Seluruh gambar **belum berlabel** — proses anotasi perlu dilakukan sebelum dataset dapat digunakan untuk training model."
    ))
