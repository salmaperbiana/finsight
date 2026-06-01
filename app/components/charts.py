import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import streamlit as st
from utils.constants import BLUE, TEXT_COLOR


# ─── TAB 1: OVERVIEW ───────────────────────────────────────────────────────────

def chart_distribusi_nominal(df_f):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df_f["nominal"], bins=40, color="#1E88E5", alpha=0.80, edgecolor="#1565C0", lw=0.5)
    ax.axvline(df_f["nominal"].mean(),   color="#E53935", lw=2, ls="--", label=f"Mean: Rp {df_f['nominal'].mean():,.0f}")
    ax.axvline(df_f["nominal"].median(), color="#43A047", lw=2, ls=":",  label=f"Median: Rp {df_f['nominal'].median():,.0f}")
    ax.set_title("Distribusi Nominal Transaksi")
    ax.set_xlabel("Nominal (Rp)"); ax.set_ylabel("Frekuensi")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"Rp{x/1000:.0f}K"))
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_tren_harian(df_f):
    daily = df_f.groupby(df_f["tanggal"].dt.date).size().reset_index()
    daily.columns = ["tanggal","count"]
    import pandas as pd
    daily["tanggal"] = pd.to_datetime(daily["tanggal"])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(daily["tanggal"], daily["count"], color="#1E88E5", lw=2, marker="o", markersize=3)
    ax.fill_between(daily["tanggal"], daily["count"], alpha=0.15, color="#42A5F5")
    ax.set_title("Tren Jumlah Transaksi Harian")
    ax.set_xlabel("Tanggal"); ax.set_ylabel("Jumlah Transaksi")
    ax.tick_params(axis="x", rotation=30); ax.grid(True, alpha=0.4)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_top_kategori_frekuensi(df_f):
    top_cats = df_f["category_clean"].value_counts().head(10).reset_index()
    top_cats.columns = ["kategori","jumlah"]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(top_cats["kategori"][::-1], top_cats["jumlah"][::-1], color=BLUE[:len(top_cats)])
    for bar in bars:
        w = bar.get_width()
        ax.text(w+0.3, bar.get_y()+bar.get_height()/2, str(int(w)), va="center", fontsize=9)
    ax.set_title("Top 10 Kategori (Frekuensi)")
    ax.set_xlabel("Jumlah Transaksi"); ax.grid(True, alpha=0.4, axis="x")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_boxplot_nominal(df_f):
    top8    = df_f["category_clean"].value_counts().head(8).index
    df_top8 = df_f[df_f["category_clean"].isin(top8)]
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(data=df_top8, y="category_clean", x="nominal", palette=BLUE[:8], ax=ax,
                flierprops=dict(marker="o", color="#1E88E5", alpha=0.5, markersize=4))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"Rp{x/1000:.0f}K"))
    ax.set_title("Distribusi Nominal per Kategori (Top 8)")
    ax.set_xlabel("Nominal (Rp)"); ax.set_ylabel("Kategori"); ax.grid(True, alpha=0.4, axis="x")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


# ─── TAB 1: BQ1 ────────────────────────────────────────────────────────────────

def chart_top_nominal(cat_contrib):
    top10      = cat_contrib.head(10)
    colors_bar = BLUE[0:3] + ["#42A5F5"]*(len(top10)-3)
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.barh(top10["Kategori"][::-1], top10["Total_Nominal"][::-1]/1_000_000, color=colors_bar[::-1])
    for bar in bars:
        w = bar.get_width()
        ax.text(w+0.05, bar.get_y()+bar.get_height()/2, f"Rp{w:.1f}M", va="center", fontsize=9)
    ax.set_title("Top 10 Kategori · Total Nominal")
    ax.set_xlabel("Total Nominal (Rp Juta)"); ax.grid(True, alpha=0.4, axis="x")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_pie_top3(top3, cat_contrib):
    total_spend = cat_contrib["Total_Nominal"].sum()
    others_sum  = cat_contrib.iloc[3:]["Total_Nominal"].sum()
    pie_vals    = list(top3["Total_Nominal"]) + [others_sum]
    pie_labels  = [f"{r['Kategori'].title()}\n({r['Persentase']:.1f}%)" for _,r in top3.iterrows()] + [f"Lainnya\n({others_sum/total_spend*100:.1f}%)"]
    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts = ax.pie(pie_vals, labels=pie_labels, colors=BLUE[:4],
                           startangle=140, wedgeprops=dict(edgecolor="#FFFFFF", linewidth=2))
    for t in texts: t.set_fontsize(9); t.set_color(TEXT_COLOR)
    ax.set_title("Distribusi: Top 3 vs Lainnya")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


# ─── TAB 1: BQ2 ────────────────────────────────────────────────────────────────

def chart_selisih_budget(budget_df):
    colors_budget = ["#EF5350" if s>0 else "#43A047" for s in budget_df["Selisih"]]
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.barh(budget_df["Kategori"][::-1], budget_df["Selisih"][::-1]/1000, color=colors_budget[::-1])
    ax.axvline(0, color="#1A2E4A", lw=1.5, ls="--")
    ax.set_title("Selisih Budget per Kategori (Rp Ribu)")
    ax.set_xlabel("Selisih — Merah: Over, Hijau: Aman")
    ax.grid(True, alpha=0.4, axis="x")
    ax.legend(handles=[mpatches.Patch(color="#EF5350", label="Over Budget"),
                        mpatches.Patch(color="#43A047", label="Aman")], fontsize=9)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


# ─── TAB 1: BQ3 ────────────────────────────────────────────────────────────────

def chart_anomaly_scatter(df_f, anomaly_df, zscore_threshold):
    normal_d = df_f[~df_f["is_anomaly"]]
    anom_d   = df_f[df_f["is_anomaly"]]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(normal_d["tanggal"], normal_d["nominal"]/1000,
               color="#42A5F5", alpha=0.6, s=25, label="Normal")
    if len(anom_d) > 0:
        ax.scatter(anom_d["tanggal"], anom_d["nominal"]/1000,
                   color="#E53935", alpha=0.9, s=70, zorder=5,
                   label=f"Anomali (Z>{zscore_threshold})", marker="^")
    ax.set_title("Deteksi Anomali: Transaksi vs Waktu")
    ax.set_xlabel("Tanggal"); ax.set_ylabel("Nominal (Rp Ribu)")
    ax.tick_params(axis="x", rotation=30); ax.legend(fontsize=9); ax.grid(True, alpha=0.4)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_zscore_distribusi(df_f, zscore_threshold):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(df_f["z_score"], bins=40, color="#1E88E5", alpha=0.75, edgecolor="#1565C0", lw=0.4)
    ax.axvline( zscore_threshold, color="#E53935", lw=2, ls="--", label=f"+{zscore_threshold}")
    ax.axvline(-zscore_threshold, color="#E53935", lw=2, ls="--", label=f"-{zscore_threshold}")
    ax.set_title("Distribusi Z-Score Seluruh Transaksi")
    ax.set_xlabel("Z-Score"); ax.set_ylabel("Frekuensi")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.4)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_anomaly_per_kategori(anomaly_df):
    anom_cat = anomaly_df["category_clean"].value_counts().reset_index()
    anom_cat.columns = ["kategori","jumlah"]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(anom_cat["kategori"][::-1], anom_cat["jumlah"][::-1], color="#EF5350", alpha=0.85)
    ax.set_title("Jumlah Anomali Z-Score per Kategori")
    ax.set_xlabel("Jumlah Anomali"); ax.grid(True, alpha=0.4, axis="x")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_tren_mingguan(df_f):
    weekly = df_f.groupby("minggu")["nominal"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(weekly["minggu"], weekly["nominal"]/1_000_000, color="#1E88E5", lw=2.5, marker="o", markersize=6)
    ax.fill_between(weekly["minggu"], weekly["nominal"]/1_000_000, alpha=0.15, color="#42A5F5")
    ax.set_title("Tren Pengeluaran Mingguan (Rp Juta)")
    ax.set_xlabel("Nomor Minggu"); ax.set_ylabel("Total (Rp Juta)"); ax.grid(True, alpha=0.4)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


# ─── TAB 2: KATEGORI ───────────────────────────────────────────────────────────

def chart_bar_kategori(cat_count_dk):
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.barh(cat_count_dk["kategori"][::-1], cat_count_dk["jumlah"][::-1], color=BLUE[:len(cat_count_dk)][::-1])
    for bar in bars:
        w = bar.get_width()
        ax.text(w+0.5, bar.get_y()+bar.get_height()/2, str(int(w)), va="center", fontsize=9)
    ax.set_title("Jumlah Data per Kategori")
    ax.set_xlabel("Jumlah Data"); ax.grid(True, alpha=0.4, axis="x")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_pie_kategori(cat_count_dk):
    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts, autotexts = ax.pie(
        cat_count_dk["jumlah"], labels=cat_count_dk["kategori"],
        colors=BLUE[:len(cat_count_dk)], autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(edgecolor="#FFFFFF", linewidth=1.5),
    )
    for t in texts: t.set_fontsize(8); t.set_color(TEXT_COLOR)
    for at in autotexts: at.set_fontsize(8); at.set_color("#FFFFFF"); at.set_fontweight("bold")
    ax.set_title("Proporsi Data per Kategori")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_boxplot_kata(dk):
    import pandas as pd
    cats_ord = dk.groupby("category_clean")["jumlah_kata"].median().sort_values(ascending=False).index
    dk_ord   = dk.copy()
    dk_ord["category_clean"] = pd.Categorical(dk_ord["category_clean"], categories=cats_ord, ordered=True)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.boxplot(data=dk_ord.sort_values("category_clean"), y="category_clean", x="jumlah_kata",
                palette=BLUE[:len(cats_ord)], ax=ax,
                flierprops=dict(marker="o", color="#1E88E5", alpha=0.4, markersize=3))
    ax.set_title("Distribusi Jumlah Kata per Kategori")
    ax.set_xlabel("Jumlah Kata"); ax.set_ylabel("Kategori"); ax.grid(True, alpha=0.4, axis="x")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_hist_kata(dk):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(dk["jumlah_kata"], bins=30, color="#1E88E5", alpha=0.78, edgecolor="#1565C0", lw=0.5)
    ax.axvline(dk["jumlah_kata"].mean(),   color="#E53935", lw=2, ls="--", label=f"Mean: {dk['jumlah_kata'].mean():.1f} kata")
    ax.axvline(dk["jumlah_kata"].median(), color="#43A047", lw=2, ls=":",  label=f"Median: {dk['jumlah_kata'].median():.0f} kata")
    ax.set_title("Distribusi Jumlah Kata Deskripsi")
    ax.set_xlabel("Jumlah Kata"); ax.set_ylabel("Frekuensi")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.4)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_class_balance(cat_count_dk):
    avg_count  = cat_count_dk["jumlah"].mean()
    bar_colors = ["#EF5350" if v < avg_count*0.75 else "#43A047" if v >= avg_count else "#1E88E5"
                  for v in cat_count_dk["jumlah"]]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(cat_count_dk["kategori"], cat_count_dk["jumlah"], color=bar_colors, alpha=0.85)
    ax.axhline(avg_count, color="#E53935", lw=2, ls="--", label=f"Rata-rata: {avg_count:.0f}")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, h+0.5, str(int(h)), ha="center", va="bottom", fontsize=9)
    ax.set_title("Class Balance Check")
    ax.set_xlabel("Kategori"); ax.set_ylabel("Jumlah Data")
    ax.tick_params(axis="x", rotation=35); ax.legend(fontsize=9); ax.grid(True, alpha=0.4, axis="y")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_avg_kata(dk):
    avg_words = dk.groupby("category_clean")["jumlah_kata"].mean().sort_values(ascending=False).reset_index()
    avg_words.columns = ["kategori","rata_kata"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.barh(avg_words["kategori"][::-1], avg_words["rata_kata"][::-1], color=BLUE[:len(avg_words)][::-1])
    for bar in bars:
        w = bar.get_width()
        ax.text(w+0.05, bar.get_y()+bar.get_height()/2, f"{w:.1f}", va="center", fontsize=9)
    ax.set_title("Rata-rata Jumlah Kata per Kategori")
    ax.set_xlabel("Rata-rata Kata"); ax.grid(True, alpha=0.4, axis="x")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


# ─── TAB 3: GAMBAR ─────────────────────────────────────────────────────────────

def chart_format_gambar(ext_count):
    exts   = list(ext_count.keys())
    counts = list(ext_count.values())
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.bar(exts, counts, color=BLUE[:len(exts)], alpha=0.85)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, h+0.2, str(int(h)),
                ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.set_title("Distribusi Format File Gambar")
    ax.set_xlabel("Format"); ax.set_ylabel("Jumlah File")
    ax.grid(True, alpha=0.4, axis="y")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_ukuran_gambar(sizes):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.hist(sizes, bins=20, color="#1E88E5", alpha=0.8, edgecolor="#1565C0", lw=0.5)
    ax.axvline(np.mean(sizes),   color="#E53935", lw=2, ls="--", label=f"Mean: {np.mean(sizes):.0f} KB")
    ax.axvline(np.median(sizes), color="#43A047", lw=2, ls=":",  label=f"Median: {np.median(sizes):.0f} KB")
    ax.set_title("Distribusi Ukuran File (KB)")
    ax.set_xlabel("Ukuran (KB)"); ax.set_ylabel("Frekuensi")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.4)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_resolusi_scatter(res_df):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.scatter(res_df["width"], res_df["height"],
               color="#1E88E5", alpha=0.6, s=40, edgecolors="#1565C0", lw=0.5)
    ax.set_title("Scatter: Lebar vs Tinggi Gambar")
    ax.set_xlabel("Lebar (px)"); ax.set_ylabel("Tinggi (px)"); ax.grid(True, alpha=0.4)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)


def chart_megapixel(res_df):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.hist(res_df["megapixel"], bins=15, color="#42A5F5", alpha=0.8, edgecolor="#1565C0", lw=0.5)
    ax.set_title("Distribusi Megapixel")
    ax.set_xlabel("Megapixel"); ax.set_ylabel("Frekuensi"); ax.grid(True, alpha=0.4)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)
