# user_pages/course_change.py
import streamlit as st
from utils import USERS, append_action

def render():
    st.header("🔧 コース変更")
    who = st.selectbox("ご利用者名", USERS, index=None, placeholder="選択してください")
    current = st.selectbox("現在のコース", ["週1","週2"], index=None)
    new = st.selectbox("希望コース", ["週1","週2"], index=None)
    note = st.text_area("備考（任意）")
    st.divider()
    submit = st.button("✅ 変更を申請", type="primary", use_container_width=True)

    if submit:
        if not (who and current and new):
            st.error("未入力の項目があります。")
            return
        ts = append_action(who, "コース変更", current, f"→ {new}／{note}".strip("／"))
        st.success(f"コース変更申請を送信しました（{ts}）。")
