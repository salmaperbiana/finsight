import streamlit as st


def insight_card(title: str, body_html: str):
    import re
    clean = re.sub(r"<br\s*/?>", "\n", body_html, flags=re.IGNORECASE)
    clean = re.sub(r"<b>(.*?)</b>", r"**\1**", clean, flags=re.IGNORECASE | re.DOTALL)
    clean = re.sub(r"<[^>]+>", "", clean)
    lines = [ln.strip() for ln in clean.splitlines() if ln.strip()]
    items = [ln.lstrip("•").strip() for ln in lines if ln.lstrip("•").strip()]

    with st.expander(f"💡 {title}", expanded=True):
        for item in items:
            st.markdown(f"- {item}")


def medal_card(rank: int, kategori: str, total_nominal: float, persentase: float,
               jumlah_transaksi: int, rata_rata: float):
    medals = ["🥇", "🥈", "🥉"]
    medal  = medals[rank]
    st.markdown(f"""
    <div class="medal-card">
        <h4>{medal} #{rank+1} · {kategori.title()}</h4>
        <p class="medal-nominal">Rp {total_nominal/1_000_000:.2f}M</p>
        <p class="medal-sub">Kontribusi: <b>{persentase:.1f}%</b></p>
        <p class="medal-sub">{int(jumlah_transaksi)} transaksi · Avg Rp {rata_rata/1000:.0f}K</p>
    </div>
    """, unsafe_allow_html=True)


def budget_bar_row(kategori: str, status: str, total_pengeluaran: float,
                   budget: float, utilisasi: float):
    is_over  = status == "Over Budget"
    badge    = '<span class="badge-over">Over Budget</span>' if is_over else '<span class="badge-safe">Aman</span>'
    bar_cls  = "budget-bar-fill-over" if is_over else "budget-bar-fill-safe"
    util_pct = min(utilisasi, 100)
    st.markdown(f"""
    <div style="margin:12px 0">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
            <span style="color:#1565C0;font-weight:600;font-size:0.88rem">{kategori.title()}</span>
            {badge}
        </div>
        <div class="budget-bar-container">
            <div class="{bar_cls}" style="width:{util_pct}%"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.78rem;color:#1976D2;margin-top:2px">
            <span>Rp {total_pengeluaran/1000:.0f}K / Rp {budget/1000:.0f}K</span>
            <span><b>{utilisasi:.1f}%</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
