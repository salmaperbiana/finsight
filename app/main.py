import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import warnings
import numpy as np
import streamlit as st

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Finsight Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.styles import inject_css, set_mpl_theme
from components.footer import render_footer
from utils.loader import load_transaksi, load_kategori
from utils.constants import PATH_TRANSAKSI, PATH_KATEGORI, BUDGET_THRESHOLDS
from utils.helpers import MONTH_NAMES
from pages import transaksi_page, kategori_page, ocr_page

inject_css()
set_mpl_theme()

# ── Load data ──────────────────────────────────────────────────────────────────
try:
    df, Q1, Q3, upper_bound = load_transaksi(PATH_TRANSAKSI)
except FileNotFoundError:
    st.error(f"❌ Dataset tidak ditemukan.\n\nPath yang dicari: `{PATH_TRANSAKSI}`")
    st.stop()

dk       = None
dk_error = None
try:
    dk = load_kategori(PATH_KATEGORI)
except FileNotFoundError:
    dk_error = f"❌ Dataset tidak ditemukan.\n\nPath yang dicari: `{PATH_KATEGORI}`"

if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

# ── Sidebar ───────────────────
with st.sidebar:
    st.markdown("## 💰 Finsight Dashboard")
    st.markdown("**Platform Literasi Keuangan**")
    st.markdown("---")

    if st.session_state.active_tab == 0:
        st.markdown("### 🔍 Filter Transaksi")

        all_cats = sorted(df["category"].unique())
        selected_cats = st.multiselect("Pilih Kategori", options=all_cats, default=all_cats, key="sel_cats")

        all_months = list(range(1, 13))
        selected_months = st.multiselect(
            "Pilih Bulan", options=all_months, default=all_months,
            format_func=lambda x: MONTH_NAMES.get(x, str(x)), key="sel_months"
        )

        zscore_threshold = st.slider("Z-Score Threshold (Anomaly)", 1.5, 3.5, 2.5, 0.1, key="zscore")

        st.markdown("---")
        st.markdown("### ⚙️ Budget Settings")
        budget_adjustment = st.slider(
            "Penyesuaian Budget (%)", 50, 200, 100, 5,
            help="Sesuaikan semua budget threshold secara proporsional", key="budget_adj"
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
    else:
        # Tab lain — sidebar bersih, hanya info singkat
        tab_names = ["Analisis Transaksi", "Dataset Kategori", "Dataset Gambar OCR"]
        st.markdown(f"**Tab aktif:** {tab_names[st.session_state.active_tab]}")
        st.markdown("<small style='color:#1565C0'>Filter transaksi tersedia di tab <b>Analisis Transaksi</b></small>", unsafe_allow_html=True)

# ── Ambil nilai filter dari session_state (aman meski widget tidak dirender) ──
selected_cats     = st.session_state.get("sel_cats",    sorted(df["category"].unique()))
selected_months   = st.session_state.get("sel_months",  list(range(1, 13)))
zscore_threshold  = st.session_state.get("zscore",      2.5)
budget_adjustment = st.session_state.get("budget_adj",  100)

adj_budgets = {k: int(v * budget_adjustment / 100) for k, v in BUDGET_THRESHOLDS.items()}

available_months_in_data = df["bulan"].unique()
months_to_filter = [m for m in selected_months if m in available_months_in_data]
if not months_to_filter:
    months_to_filter = list(available_months_in_data)

df_f = df[df["category"].isin(selected_cats) & df["bulan"].isin(months_to_filter)].copy()
df_f["is_anomaly"]     = df_f["z_score"].abs() > zscore_threshold
df_f["anomaly_status"] = df_f["nominal"].apply(lambda x: "Anomaly" if x > upper_bound else "Normal")

# ── Hero header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>📊 Finsight Dashboard</h1>
    <p>Exploratory Data Analysis · Platform Literasi Keuangan</p>
</div>
""", unsafe_allow_html=True)

# ── Main tabs ──────────────────────────────────────────────────────────────────
tab_labels = [
    "💳  Dataset Transaksi",
    "🏷️  Dataset Kategori",
    "🖼️  Dataset Gambar (OCR)",
]
main_tab1, main_tab2, main_tab3 = st.tabs(tab_labels)

with main_tab1:
    st.session_state.active_tab = 0
    transaksi_page.render(df_f, upper_bound, zscore_threshold, adj_budgets)

with main_tab2:
    st.session_state.active_tab = 1
    if dk_error:
        st.error(dk_error)
        st.stop()
    kategori_page.render(dk)

with main_tab3:
    st.session_state.active_tab = 2
    ocr_page.render()

render_footer()