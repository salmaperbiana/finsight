import streamlit as st
import matplotlib.pyplot as plt
from utils.constants import BG_COLOR, CARD_COLOR, TEXT_COLOR, GRID_COLOR


def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: #F0F6FF; color: #1A2E4A; }

/* ── Hapus navigasi halaman bawaan Streamlit ── */
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebarNav"] { display: none !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #DAEEFF 0%, #C5E3FF 100%);
    border-right: 2px solid #90CAF9;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #1565C0 !important; }

[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1.5px solid #90CAF9;
    border-top: 4px solid #1E88E5;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(30,136,229,0.10);
}
[data-testid="metric-container"] label {
    color: #1565C0 !important; font-size: 0.78rem !important;
    font-weight: 700 !important; letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0D47A1 !important; font-size: 1.6rem !important; font-weight: 800 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #1976D2 !important; font-size: 0.8rem !important; font-weight: 600 !important;
}

h1 { color: #0D47A1 !important; font-weight: 800 !important; }
h2 { color: #1565C0 !important; font-weight: 700 !important; }
h3 { color: #1976D2 !important; font-weight: 600 !important; }
h4 { color: #1565C0 !important; font-weight: 700 !important; }
p  { color: #1A2E4A !important; }
hr { border-color: #BBDEFB !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #DAEEFF; border-radius: 12px; padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #1565C0 !important;
    border-radius: 8px; font-weight: 600; font-size: 0.88rem; padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1E88E5, #1565C0) !important;
    color: #FFFFFF !important; box-shadow: 0 2px 8px rgba(30,136,229,0.3);
}

[data-testid="stDataFrame"] {
    border: 1.5px solid #90CAF9; border-radius: 12px; overflow: hidden; background: #FFFFFF;
}
.stAlert { border-radius: 12px !important; }

/* ── Insight card via expander ── */
[data-testid="stExpander"] {
    background: linear-gradient(135deg, #E3F2FD 0%, #EEF6FF 100%) !important;
    border: 1.5px solid #90CAF9 !important;
    border-left: 5px solid #1E88E5 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 12px rgba(30,136,229,0.08) !important;
}
[data-testid="stExpander"] summary {
    color: #1565C0 !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stExpander"] p,
[data-testid="stExpander"] li { color: #1A2E4A !important; font-size: 0.92rem !important; line-height: 1.7 !important; }

/* ── Medal cards — tinggi seragam, tampilan bersih ── */
.medal-card {
    background: linear-gradient(135deg, #E3F2FD 0%, #EEF6FF 100%);
    border: 1.5px solid #90CAF9;
    border-radius: 16px;
    padding: 22px 24px;
    min-height: 180px;
    height: 100%;
    box-sizing: border-box;
    box-shadow: 0 4px 16px rgba(30,136,229,0.10);
}
.medal-card h4 {
    color: #1565C0 !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    margin: 0 0 12px 0 !important;
}
.medal-nominal {
    color: #0D47A1 !important;
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    margin: 0 0 8px 0 !important;
}
.medal-sub {
    color: #1A2E4A !important;
    font-size: 0.88rem !important;
    margin: 4px 0 !important;
}

.dataset-badge {
    display: inline-block; background: #E3F2FD; color: #1565C0;
    border: 1.5px solid #90CAF9; border-radius: 20px; padding: 4px 16px;
    font-size: 0.82rem; font-weight: 700; margin-bottom: 16px; letter-spacing: 0.04em;
}
.dataset-badge-green {
    display: inline-block; background: #E8F5E9; color: #2E7D32;
    border: 1.5px solid #66BB6A; border-radius: 20px; padding: 4px 16px;
    font-size: 0.82rem; font-weight: 700; margin-bottom: 16px; letter-spacing: 0.04em;
}
.dataset-badge-orange {
    display: inline-block; background: #FFF8E1; color: #F57F17;
    border: 1.5px solid #FFB300; border-radius: 20px; padding: 4px 16px;
    font-size: 0.82rem; font-weight: 700; margin-bottom: 16px; letter-spacing: 0.04em;
}

.badge-safe {
    background: #E8F5E9; color: #2E7D32; border: 1.5px solid #66BB6A;
    border-radius: 20px; padding: 3px 14px; font-size: 0.8rem; font-weight: 700;
}
.badge-over {
    background: #FFEBEE; color: #C62828; border: 1.5px solid #EF5350;
    border-radius: 20px; padding: 3px 14px; font-size: 0.8rem; font-weight: 700;
}

.hero-header {
    background: linear-gradient(135deg, #1565C0 0%, #1E88E5 55%, #42A5F5 100%);
    border-radius: 20px; padding: 36px 40px; margin-bottom: 30px;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 32px rgba(30,136,229,0.25);
}
.hero-header::before {
    content: ''; position: absolute; top: -40%; right: -10%;
    width: 380px; height: 380px; background: rgba(255,255,255,0.08); border-radius: 50%;
}
.hero-header::after {
    content: ''; position: absolute; bottom: -30%; left: 30%;
    width: 200px; height: 200px; background: rgba(255,255,255,0.05); border-radius: 50%;
}
.hero-header h1 { color: #FFFFFF !important; font-size: 2.2rem; margin: 0 0 8px 0; }
.hero-header p  { color: rgba(255,255,255,0.90) !important; font-size: 1rem; margin: 0; }

.budget-bar-container {
    background: #BBDEFB; border-radius: 8px; height: 12px; margin: 6px 0; overflow: hidden;
}
.budget-bar-fill-safe {
    height: 100%; border-radius: 8px; background: linear-gradient(90deg, #43A047, #66BB6A);
}
.budget-bar-fill-over {
    height: 100%; border-radius: 8px; background: linear-gradient(90deg, #E53935, #EF5350);
}
</style>
""", unsafe_allow_html=True)


def set_mpl_theme():
    plt.rcParams.update({
        "figure.facecolor": BG_COLOR,
        "axes.facecolor":   CARD_COLOR,
        "axes.edgecolor":   "#90CAF9",
        "axes.labelcolor":  TEXT_COLOR,
        "axes.titlecolor":  "#0D47A1",
        "axes.titlesize":   13,
        "axes.titleweight": "bold",
        "xtick.color":      TEXT_COLOR,
        "ytick.color":      TEXT_COLOR,
        "grid.color":       GRID_COLOR,
        "grid.alpha":       0.7,
        "text.color":       TEXT_COLOR,
        "font.family":      "DejaVu Sans",
        "legend.facecolor": "#FFFFFF",
        "legend.edgecolor": "#90CAF9",
        "legend.labelcolor": TEXT_COLOR,
    })
