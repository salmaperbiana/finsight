import streamlit as st
import pandas as pd
import numpy as np

from components.metrics import (
    render_transaksi_metrics, render_budget_metrics,
    render_anomaly_metrics,
)
from components.charts import (
    chart_distribusi_nominal, chart_tren_harian,
    chart_top_kategori_frekuensi, chart_boxplot_nominal,
    chart_top_nominal, chart_pie_top3,
    chart_selisih_budget,
    chart_anomaly_scatter, chart_zscore_distribusi,
    chart_anomaly_per_kategori, chart_tren_mingguan,
)
from components.cards import insight_card, medal_card, budget_bar_row


def render(df_f, upper_bound, zscore_threshold, adj_budgets):
    st.markdown('<span class="dataset-badge">📂 Sumber: dataset_transaksi_sintetik.csv</span>', unsafe_allow_html=True)
    st.markdown("Dataset transaksi keuangan pengguna selama periode 90 hari, berisi nominal, kategori, dan tanggal pengeluaran.")

    total_transaksi, total_pengeluaran, rata_rata, total_anomali = render_transaksi_metrics(df_f)

    st.markdown("<br>", unsafe_allow_html=True)

    sub1, sub2, sub3, sub4 = st.tabs([
        "🔎 Overview EDA",
        "📊 Top Kategori",
        "🔔 Budget Alert",
        "🚨 Anomaly Detection",
    ])

    # ── Overview ──────────────────────────────────────────────────────────────
    with sub1:
        st.markdown("### Overview Distribusi & Pola Transaksi")
        col_a, col_b = st.columns(2)
        with col_a: chart_distribusi_nominal(df_f)
        with col_b: chart_tren_harian(df_f)

        col_c, col_d = st.columns(2)
        with col_c: chart_top_kategori_frekuensi(df_f)
        with col_d: chart_boxplot_nominal(df_f)

        st.markdown("### 📋 Statistik Deskriptif")
        desc = df_f["nominal"].describe().rename({
            "count": "Jumlah", "mean": "Mean", "std": "Std Dev",
            "min": "Min", "25%": "Q1 (25%)", "50%": "Median", "75%": "Q3 (75%)", "max": "Max"
        })
        st.dataframe(pd.DataFrame({"Nilai (Rp)": desc}).map(lambda x: f"Rp {x:,.0f}"), use_container_width=True)

        insight_card("Insight Overview", (
            "Distribusi nominal cenderung **right-skewed** — pengguna lebih sering bertransaksi kecil-menengah.\n"
            "Median mendekati mean → distribusi relatif simetris dengan beberapa outlier di sisi kanan.\n"
            "Tren harian stabil dengan fluktuasi normal, tidak ada lonjakan ekstrem.\n"
            "Kategori dengan frekuensi tertinggi belum tentu yang paling besar nominalnya."
        ))

    # ── BQ1 ───────────────────────────────────────────────────────────────────
    with sub2:
        st.markdown("### BQ1 · Distribusi Kontribusi & Top 3 Kategori")
        st.markdown("Mengidentifikasi 3 kategori pengeluaran terbesar berdasarkan total nominal dan persentase kontribusi.")

        cat_contrib = df_f.groupby("category_clean")["nominal"].agg(["sum", "count", "mean"]).round(0).reset_index()
        cat_contrib.columns = ["Kategori", "Total_Nominal", "Jumlah_Transaksi", "Rata_rata"]
        total_spend = cat_contrib["Total_Nominal"].sum()
        cat_contrib["Persentase"] = (cat_contrib["Total_Nominal"] / total_spend * 100).round(2)
        cat_contrib = cat_contrib.sort_values("Total_Nominal", ascending=False).reset_index(drop=True)
        top3 = cat_contrib.head(3)

        cc1, cc2, cc3 = st.columns(3)
        for i, (col, (_, row)) in enumerate(zip([cc1, cc2, cc3], top3.iterrows())):
            with col:
                medal_card(i, row["Kategori"], row["Total_Nominal"],
                           row["Persentase"], row["Jumlah_Transaksi"], row["Rata_rata"])

        st.markdown("<br>", unsafe_allow_html=True)
        col_e, col_f = st.columns(2)
        with col_e: chart_top_nominal(cat_contrib)
        with col_f: chart_pie_top3(top3, cat_contrib)

        st.markdown("### 📋 Detail Semua Kategori")
        disp = cat_contrib.copy()
        disp["Kategori"] = disp["Kategori"].str.title()
        disp.index = range(1, len(disp) + 1)
        disp.index.name = "No"
        st.dataframe(
            disp,
            use_container_width=True,
            column_config={
                "Kategori":          st.column_config.TextColumn("Kategori"),
                "Total_Nominal":     st.column_config.NumberColumn("Total Nominal",     format="Rp %,.0f"),
                "Jumlah_Transaksi":  st.column_config.NumberColumn("Jml Transaksi",     format="%d"),
                "Rata_rata":         st.column_config.NumberColumn("Rata-rata",          format="Rp %,.0f"),
                "Persentase":        st.column_config.NumberColumn("Persentase (%)",     format="%.2f%%"),
            },
        )

        pct_top3 = top3["Persentase"].sum()
        insight_card("Insight BQ1", (
            f"**{pct_top3:.1f}% pengeluaran** terkonsentrasi di Top 3 kategori.\n"
            "Keseimbangan Konsumsi–Investasi: Belanja (konsumtif) vs Pendidikan & Kesehatan (investasi diri).\n"
            "Frekuensi ketiga kategori hampir setara → pola pengeluaran yang terstruktur.\n"
            "Rekomendasi: Fokuskan monitoring dan budget alert pada Top 3 kategori ini."
        ))

    # ── BQ2 ───────────────────────────────────────────────────────────────────
    with sub3:
        st.markdown("### BQ2 · Simulasi Budget Alert System")
        st.markdown("Deteksi kategori yang melebihi batas anggaran bulanan dengan threshold yang dapat disesuaikan.")

        budget_df = df_f.groupby("category_clean")["nominal"].sum().reset_index()
        budget_df.columns = ["Kategori", "Total_Pengeluaran"]
        budget_df["Budget"]      = budget_df["Kategori"].map(adj_budgets)
        budget_df = budget_df.dropna(subset=["Budget"])
        budget_df["Selisih"]     = budget_df["Total_Pengeluaran"] - budget_df["Budget"]
        budget_df["Utilisasi_%"] = (budget_df["Total_Pengeluaran"] / budget_df["Budget"] * 100).round(1)
        budget_df["Status"]      = budget_df["Selisih"].apply(lambda x: "Over Budget" if x > 0 else "Aman")
        budget_df = budget_df.sort_values("Utilisasi_%", ascending=False).reset_index(drop=True)

        over_count, safe_count, effectiveness = render_budget_metrics(budget_df)

        st.markdown("<br>", unsafe_allow_html=True)
        col_g, col_h = st.columns([1, 1.2])

        with col_g:
            st.markdown("#### Status Budget per Kategori")
            for _, row in budget_df.iterrows():
                budget_bar_row(row["Kategori"], row["Status"],
                               row["Total_Pengeluaran"], row["Budget"], row["Utilisasi_%"])

        with col_h:
            chart_selisih_budget(budget_df)

        st.markdown("### 📋 Detail Analisis Budget")
        tbl = budget_df.copy()
        tbl["Total_Pengeluaran"] = tbl["Total_Pengeluaran"].apply(lambda x: f"Rp {x:,.0f}")
        tbl["Budget"]            = tbl["Budget"].apply(lambda x: f"Rp {x:,.0f}")
        tbl["Selisih"]           = tbl["Selisih"].apply(lambda x: f"Rp {x:,.0f}")
        tbl["Utilisasi_%"]       = tbl["Utilisasi_%"].apply(lambda x: f"{x:.1f}%")
        tbl.index = range(1, len(tbl) + 1)
        st.dataframe(tbl, use_container_width=True)

        insight_card("Insight BQ2", (
            f"Sistem Budget Alert menunjukkan efektivitas **{effectiveness:.1f}%**.\n"
            "Threshold adaptif berbasis Q75 historis memberikan estimasi yang realistis.\n"
            "**Proactive Alert Strategy:** Kirim notifikasi saat pengeluaran mencapai 80% threshold.\n"
            "Gunakan slider penyesuaian budget di sidebar untuk simulasi skenario berbeda."
        ))

    # ── BQ3 ───────────────────────────────────────────────────────────────────
    with sub4:
        st.markdown("### BQ3 · Anomaly Detection")
        st.markdown("Identifikasi transaksi anomali menggunakan **Z-Score per kategori** dan **IQR**.")

        anomaly_df   = df_f[df_f["is_anomaly"]]
        anomaly_rate = render_anomaly_metrics(df_f, anomaly_df, upper_bound, zscore_threshold)

        st.markdown("<br>", unsafe_allow_html=True)
        col_i, col_j = st.columns(2)
        with col_i: chart_anomaly_scatter(df_f, anomaly_df, zscore_threshold)
        with col_j: chart_zscore_distribusi(df_f, zscore_threshold)

        col_k, col_l = st.columns(2)
        with col_k:
            if len(anomaly_df) > 0:
                chart_anomaly_per_kategori(anomaly_df)
            else:
                st.info("Tidak ada anomali Z-Score dengan threshold saat ini.")
        with col_l:
            chart_tren_mingguan(df_f)

        if len(anomaly_df) > 0:
            st.markdown("### 🚨 Daftar Transaksi Anomali (Z-Score)")
            anom_display = anomaly_df[["tanggal", "category", "deskripsi", "nominal", "z_score"]].copy()
            anom_display["nominal"] = anom_display["nominal"].apply(lambda x: f"Rp {x:,.0f}")
            anom_display["z_score"] = anom_display["z_score"].apply(lambda x: f"{x:.3f}")
            anom_display = anom_display.sort_values("z_score", ascending=False)
            anom_display.index = range(1, len(anom_display) + 1)
            st.dataframe(anom_display, use_container_width=True)

        if len(anomaly_df) > 0:
            top_anom = anomaly_df["category_clean"].value_counts().head(3)
            rec_lines = "\n".join([f"Kategori **{c.title()}**: {n} anomali — monitoring direkomendasikan." for c, n in top_anom.items()])
        else:
            rec_lines = "Semua transaksi dalam batas normal. Pertahankan threshold saat ini."

        insight_card("Insight BQ3", (
            f"Z-Score ±{zscore_threshold} memberikan deteksi akurat tanpa false positives berlebihan.\n"
            f"Tingkat anomali **{anomaly_rate:.2f}%** — pola pengeluaran sehat dan konsisten.\n"
            f"{rec_lines}\n"
            "Update statistik kategori secara berkala (mingguan) untuk threshold yang adaptif."
        ))
