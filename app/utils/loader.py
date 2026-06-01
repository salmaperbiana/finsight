import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path


@st.cache_data
def load_transaksi(path: str | Path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    df = pd.read_csv(path)
    df = df.dropna()
    df = df[~df.duplicated()]
    df["tanggal"]            = pd.to_datetime(df["tanggal"])
    df["category_clean"]     = df["category"].str.lower().str.strip()
    df["tahun"]              = df["tanggal"].dt.year
    df["bulan"]              = df["tanggal"].dt.month
    df["hari"]               = df["tanggal"].dt.day
    df["hari_dalam_minggu"]  = df["tanggal"].dt.day_name()
    df["minggu"]             = df["tanggal"].dt.isocalendar().week.astype(int)
    df["year_month"]         = df["tanggal"].dt.to_period("M")
    stats = df.groupby("category_clean")["nominal"].agg(["mean", "std"]).reset_index()
    stats.columns = ["category_clean", "mean_nominal", "std_nominal"]
    df = df.merge(stats, on="category_clean", how="left")
    df["z_score"]    = np.where(df["std_nominal"] > 0, (df["nominal"] - df["mean_nominal"]) / df["std_nominal"], 0)
    df["is_anomaly"] = df["z_score"].abs() > 2.5
    Q1 = df["nominal"].quantile(0.25)
    Q3 = df["nominal"].quantile(0.75)
    upper_bound = Q3 + 1.5 * (Q3 - Q1)
    df["anomaly_status"] = df["nominal"].apply(lambda x: "Anomaly" if x > upper_bound else "Normal")
    return df, Q1, Q3, upper_bound


@st.cache_data
def load_kategori(path: str | Path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    dk = pd.read_csv(path, usecols=["deskripsi", "category"])
    dk = dk.dropna()
    dk = dk[~dk.duplicated()]
    dk["category_clean"]    = dk["category"].str.lower().str.strip()
    dk["deskripsi_clean"]   = dk["deskripsi"].str.strip()
    dk["panjang_deskripsi"] = dk["deskripsi_clean"].str.len()
    dk["jumlah_kata"]       = dk["deskripsi_clean"].str.split().str.len()
    return dk
