from pathlib import Path

# ── Project root & data paths ──────────────────────────────────────────────────
# ROOT is resolved relative to this file so the app works regardless of the
# working directory from which `streamlit run` is executed.
ROOT_DIR   = Path(__file__).resolve().parent.parent.parent   # project root (finsight/)
DATA_DIR   = ROOT_DIR / "data" / "processed"
IMAGES_DIR = DATA_DIR / "images"

PATH_TRANSAKSI = DATA_DIR / "dataset_transaksi_sintetik.csv"
PATH_KATEGORI  = DATA_DIR / "dataset_kategori.csv"

# ── Colour palette ─────────────────────────────────────────────────────────────
BLUE       = ["#1565C0", "#1E88E5", "#42A5F5", "#90CAF9", "#BBDEFB", "#E3F2FD"]
BG_COLOR   = "#FFFFFF"
CARD_COLOR = "#F0F6FF"
TEXT_COLOR = "#1A2E4A"
GRID_COLOR = "#BBDEFB"

# ── Budget thresholds (Rp) ─────────────────────────────────────────────────────
BUDGET_THRESHOLDS = {
    "tagihan": 2_500_000, "belanja": 2_000_000, "pendidikan": 1_800_000,
    "kesehatan dan perawatan diri": 1_500_000, "sosial": 1_200_000,
    "makanan": 1_000_000, "transportasi": 1_500_000, "hiburan": 1_200_000,
    "travel": 1_800_000, "lainnya": 800_000,
}
