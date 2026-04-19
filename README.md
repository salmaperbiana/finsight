<div align="center">

# 📊 Finsight — Analytics Dashboard

**Data Analysis & Visualization untuk Platform Finsight**

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-latest-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-latest-3F4F75?logo=plotly)](https://plotly.com)

> Bagian dari Capstone Project **Coding Camp 2026 powered by DBS Foundation**
> Team ID: **CC26-PSU113**

</div>

---

## 📖 Tentang

Repo ini berisi **Analytics Dashboard** Finsight — aplikasi Streamlit untuk exploratory data analysis (EDA), visualisasi pola pengeluaran pengguna, dan pemantauan performa model ML.

Dashboard ini melayani dua kebutuhan:
1. **Internal (Tim DS)** — EDA, model evaluation, business insights
2. **User-facing** — Visualisasi spending summary yang embedded atau standalone

---

## 🗂️ Struktur Folder

```
finsight-analytics/
├── app/
│   ├── main.py                  # Entry point Streamlit
│   ├── pages/
│   │   ├── 1_Overview.py        # Ringkasan pengeluaran
│   │   ├── 2_Spending_Trend.py  # Tren pengeluaran per waktu
│   │   ├── 3_Category_Analysis.py # Analisis per kategori
│   │   ├── 4_Model_Performance.py # Akurasi & metrics model
│   │   └── 5_EDA.py             # Exploratory Data Analysis
│   ├── components/
│   │   ├── charts.py            # Plotly chart helpers
│   │   └── metrics.py           # KPI metric components
│   └── utils/
│       ├── db.py                # Koneksi ke PostgreSQL
│       └── data_loader.py       # Load & cache data
├── notebooks/
│   ├── 01_EDA.ipynb             # EDA awal dataset struk
│   ├── 02_Feature_Engineering.ipynb
│   └── 03_Model_Evaluation.ipynb
├── data/
│   ├── raw/                     # Dataset struk mentah (gitignored)
│   └── processed/               # Data bersih (gitignored)
├── requirements.txt
├── .env.example
└── .streamlit/
    └── config.toml              # Streamlit theme config
```

---

## ⚙️ Tech Stack

| Teknologi | Kegunaan |
|---|---|
| Streamlit | Dashboard framework |
| Pandas | Data manipulation |
| Plotly | Interactive charts |
| Scikit-learn | Model evaluation metrics |
| SQLAlchemy | Koneksi ke PostgreSQL |
| Matplotlib / Seaborn | Static charts (EDA) |

---

## 🚀 Cara Menjalankan

### Prasyarat
- Python >= 3.10
- PostgreSQL (`finsight_db`) sudah berjalan

### Langkah-langkah

```bash
# 1. Clone repo
git clone https://github.com/finsight-cc26/finsight-analytics.git
cd finsight-analytics

# 2. Buat virtual environment
python -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env

# 5. Jalankan dashboard
streamlit run app/main.py
```

Dashboard akan berjalan di **http://localhost:8501**

---

## 🌍 Environment Variables

```env
# Database (sama dengan backend)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=finsight_db
DB_USER=postgres
DB_PASSWORD=your_password_here

# Streamlit
STREAMLIT_SERVER_PORT=8501
```

---

## 📊 Halaman Dashboard

| Halaman | Konten |
|---|---|
| **Overview** | Total pengeluaran, jumlah transaksi, top kategori bulan ini |
| **Spending Trend** | Line chart pengeluaran harian/mingguan/bulanan |
| **Category Analysis** | Pie chart & bar chart per kategori pengeluaran |
| **Model Performance** | Akurasi classifier, confusion matrix, F1-score |
| **EDA** | Distribusi data, word cloud item, analisis merchant |

---

## 🔬 Business Questions

Dashboard menjawab research questions utama Finsight:

1. **Seberapa akurat pipeline OCR?** → Ditampilkan di halaman *Model Performance*
2. **Pola pengeluaran apa yang paling dominan?** → Ditampilkan di *Category Analysis*
3. **Apakah ada anomali pengeluaran?** → Ditampilkan di *Spending Trend*

---

## 📓 Notebooks

Untuk eksplorasi data secara mendalam, lihat folder `notebooks/`:

```bash
# Install Jupyter
pip install jupyter

# Jalankan
jupyter notebook notebooks/
```

---

## 🚢 Deployment

Analytics di-deploy ke **Streamlit Cloud**.

1. Push ke branch `main`
2. Connect repo di [share.streamlit.io](https://share.streamlit.io)
3. Set environment variables di Streamlit Cloud secrets
4. Deploy otomatis

---

## 👥 Maintainer

**Widya** & **Salma Perbiana** — Data Scientist
> Coding Camp 2026 | CC26-PSU113

