import streamlit as st

from components.metrics import render_kategori_metrics
from components.charts import (
    chart_bar_kategori, chart_pie_kategori,
    chart_boxplot_kata, chart_hist_kata,
    chart_class_balance, chart_avg_kata,
)
from components.cards import insight_card


def render(dk):
    st.markdown('<span class="dataset-badge-green">📂 Sumber: dataset_kategori.csv</span>', unsafe_allow_html=True)
    st.markdown("Dataset pelatihan model klasifikasi otomatis kategori transaksi berdasarkan teks deskripsi pengeluaran.")

    render_kategori_metrics(dk)

    cat_count_dk = dk["category_clean"].value_counts().reset_index()
    cat_count_dk.columns = ["kategori", "jumlah"]

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Distribusi Data per Kategori")
    r1a, r1b = st.columns(2)
    with r1a: chart_bar_kategori(cat_count_dk)
    with r1b: chart_pie_kategori(cat_count_dk)

    st.markdown("### 📐 Analisis Panjang Deskripsi Teks")
    r2a, r2b = st.columns(2)
    with r2a: chart_boxplot_kata(dk)
    with r2b: chart_hist_kata(dk)

    st.markdown("### ⚖️ Class Balance & Karakteristik Teks")
    r3a, r3b = st.columns(2)
    with r3a: chart_class_balance(cat_count_dk)
    with r3b: chart_avg_kata(dk)

    st.markdown("### 📋 Statistik Deskriptif Teks per Kategori")
    stat_teks = dk.groupby("category_clean").agg(
        Jumlah=("deskripsi", "count"), Rata_Kata=("jumlah_kata", "mean"),
        Min_Kata=("jumlah_kata", "min"), Max_Kata=("jumlah_kata", "max"),
        Rata_Karakter=("panjang_deskripsi", "mean"),
    ).round(1).reset_index()
    stat_teks.columns = ["Kategori", "Jumlah Data", "Rata-rata Kata", "Min Kata", "Max Kata", "Rata-rata Karakter"]
    stat_teks = stat_teks.sort_values("Jumlah Data", ascending=False).reset_index(drop=True)
    stat_teks.index = range(1, len(stat_teks) + 1)
    st.dataframe(stat_teks, use_container_width=True)

    st.markdown("### 🔍 Sample Deskripsi per Kategori")
    selected_cat_dk = st.selectbox(
        "Pilih kategori untuk lihat contoh deskripsi:",
        options=sorted(dk["category_clean"].unique()), key="cat_dk_select"
    )
    sample_dk = dk[dk["category_clean"] == selected_cat_dk][["deskripsi", "category"]].head(10).reset_index(drop=True)
    sample_dk.index = range(1, len(sample_dk) + 1)
    st.dataframe(sample_dk, use_container_width=True)

    imbalance = cat_count_dk["jumlah"].max() / cat_count_dk["jumlah"].min()
    most_cat  = cat_count_dk.iloc[0]["kategori"]
    least_cat = cat_count_dk.iloc[-1]["kategori"]
    imb_text  = (
        "⚠️ **Class imbalance terdeteksi** (>2x) — pertimbangkan teknik oversampling/undersampling sebelum pelatihan."
        if imbalance > 2 else
        "✅ **Distribusi kelas cukup seimbang** — dataset siap untuk pelatihan langsung."
    )

    insight_card("Insight Dataset Kategori", (
        f"Total **{len(dk):,} data** deskripsi transaksi untuk pelatihan model klasifikasi.\n"
        f"Kategori terbanyak: **{most_cat.title()}** · Tersedikit: **{least_cat.title()}** · Rasio imbalance: **{imbalance:.1f}x**.\n"
        f"{imb_text}\n"
        f"Rata-rata **{dk['jumlah_kata'].mean():.1f} kata/deskripsi** — panjang teks ideal untuk model NLP berbasis token pendek."
    ))
