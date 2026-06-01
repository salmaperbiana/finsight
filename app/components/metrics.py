import streamlit as st


def render_transaksi_metrics(df_f):
    total_transaksi   = len(df_f)
    total_pengeluaran = df_f["nominal"].sum()
    rata_rata         = df_f["nominal"].mean()
    total_anomali     = df_f["is_anomaly"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📦 Total Transaksi",       f"{total_transaksi:,}",                  f"{total_transaksi} records")
    c2.metric("💵 Total Pengeluaran",     f"Rp {total_pengeluaran/1_000_000:.1f}M","seluruh kategori")
    c3.metric("📈 Rata-rata / Transaksi", f"Rp {rata_rata:,.0f}",                  "per transaksi")
    c4.metric("⚠️ Anomali Terdeteksi",   f"{total_anomali}",                       f"{total_anomali/total_transaksi*100:.2f}%")
    c5.metric("🗂️ Kategori Aktif",       f"{df_f['category'].nunique()}",           "kategori unik")

    return total_transaksi, total_pengeluaran, rata_rata, total_anomali


def render_kategori_metrics(dk):
    dk1, dk2, dk3, dk4 = st.columns(4)
    dk1.metric("📦 Total Data",         f"{len(dk):,}",                     "baris unik")
    dk2.metric("🏷️ Jumlah Kategori",   f"{dk['category_clean'].nunique()}", "kategori unik")
    dk3.metric("✏️ Rata-rata Kata",     f"{dk['jumlah_kata'].mean():.1f}",  "kata/deskripsi")
    dk4.metric("📏 Rata-rata Karakter", f"{dk['panjang_deskripsi'].mean():.0f}", "karakter/deskripsi")


def render_budget_metrics(budget_df):
    over_count    = (budget_df["Status"]=="Over Budget").sum()
    safe_count    = (budget_df["Status"]=="Aman").sum()
    effectiveness = safe_count/len(budget_df)*100 if len(budget_df)>0 else 100

    k1, k2, k3 = st.columns(3)
    k1.metric("✅ Kategori Aman",     f"{safe_count}",         f"{safe_count}/{len(budget_df)} kategori")
    k2.metric("🚨 Over Budget",       f"{over_count}",         f"{over_count} kategori melebihi")
    k3.metric("🎯 Efektivitas Alert", f"{effectiveness:.1f}%", "compliance rate")

    return over_count, safe_count, effectiveness


def render_anomaly_metrics(df_f, anomaly_df, upper_bound, zscore_threshold):
    anomaly_rate = len(anomaly_df)/len(df_f)*100

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("🔍 Z-Score Threshold", f"±{zscore_threshold}", "sidebar")
    a2.metric("⚠️ Anomali Z-Score",   f"{len(anomaly_df)}",   f"{anomaly_rate:.2f}%")
    a3.metric("📏 IQR Upper Bound",   f"Rp {upper_bound:,.0f}", "batas atas")
    a4.metric("✅ Transaksi Normal",  f"{len(df_f)-len(anomaly_df)}", "dalam batas")

    return anomaly_rate


def render_image_metrics(total_imgs, total_size, ext_count):
    # Hapus "Format Unik" — ganti dengan 3 metric yang lebih informatif
    g1, g2, g3 = st.columns(3)
    g1.metric("🖼️ Total Gambar",    f"{total_imgs:,}",           "file gambar")
    g2.metric("💾 Total Ukuran",    f"{total_size/1024:.2f} MB", "di folder /images")
    g3.metric("🏷️ Status Label",   "Belum Berlabel",            "perlu anotasi")
