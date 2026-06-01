import streamlit as st
from utils.helpers import MONTH_NAMES
from utils.constants import BUDGET_THRESHOLDS


def render_sidebar(df):
    with st.sidebar:
        st.markdown("## 💰 Finsight EDA")
        st.markdown("**Platform Literasi Keuangan**")
        st.markdown("---")
        st.markdown("### 🔍 Filter Transaksi")

        all_cats = sorted(df["category"].unique())
        selected_cats = st.multiselect("Pilih Kategori", options=all_cats, default=all_cats)

        available_months = sorted(df["bulan"].unique())
        selected_months  = st.multiselect(
            "Pilih Bulan", options=available_months, default=available_months,
            format_func=lambda x: MONTH_NAMES.get(x, str(x)),
        )

        zscore_threshold = st.slider("Z-Score Threshold (Anomaly)", 1.5, 3.5, 2.5, 0.1)

        st.markdown("---")
        st.markdown("### ⚙️ Budget Settings")
        budget_adjustment = st.slider(
            "Penyesuaian Budget (%)", 50, 200, 100, 5,
            help="Sesuaikan semua budget threshold secara proporsional"
        )

        st.markdown("---")
        tgl_min = df["tanggal"].min().strftime("%d %b %Y")
        tgl_max = df["tanggal"].max().strftime("%d %b %Y")
        st.markdown(f"""
            <small style='color:#1565C0'>
            📊 Transaksi: {len(df):,} baris<br>
            📅 Periode: {tgl_min} – {tgl_max}<br>
            🏷️ {df['category'].nunique()} kategori
            </small>
        """, unsafe_allow_html=True)

    adj_budgets = {k: int(v * budget_adjustment / 100) for k, v in BUDGET_THRESHOLDS.items()}
    return selected_cats, selected_months, zscore_threshold, adj_budgets
