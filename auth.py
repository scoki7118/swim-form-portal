import streamlit as st

def require_admin_password(key: str = "ADMIN_PASSWORD"):
    if "admin_authed" not in st.session_state:
        st.session_state.admin_authed = False
    if st.session_state.admin_authed:
        return True

    st.title("🔐 管理者ログイン")
    pw = st.text_input("管理者パスワード", type="password")
    if st.button("ログイン", type="primary"):
        real = st.secrets.get(key)
        if real and pw == real:
            st.session_state.admin_authed = True
            st.rerun()
        else:
            st.error("パスワードが違います。")
    st.stop()
