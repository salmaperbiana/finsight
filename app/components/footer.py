import streamlit as st


def render_footer():
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("""
<div style="text-align:center;color:#1565C0;font-size:0.82rem;padding:10px 0">
    💰 <b>Finsight</b> · Platform Literasi Keuangan · EDA Dashboard · Powered by Streamlit
</div>
""", unsafe_allow_html=True)
