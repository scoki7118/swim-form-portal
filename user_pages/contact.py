# user_pages/contact.py
import streamlit as st
from utils import USERS, append_action

def render():
    st.header("💬 担当者へ連絡")
    who = st.selectbox("ご利用者名", USERS, index=None, placeholder="選択してください")
    msg = st.text_area("お問い合わせ内容", height=160, placeholder="質問や伝達事項をご入力ください")
    st.divider()
    submit = st.button("✅ 送信", type="primary", use_container_width=True)

    if submit:
        if not (who and msg):
            st.error("未入力の項目があります。")
            return
        ts = append_action(who, "メッセージ", "-", msg)
        st.success(f"メッセージを送信しました（{ts}）。")
