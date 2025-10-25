import streamlit as st
import streamlit as st
from utils import CLASSES, USERS, append_action

def render():
    st.header("🔁 振替申込")
    who = st.selectbox("ご利用者名", USERS, index=None, placeholder="選択してください")
    current = st.selectbox("現在のクラス", CLASSES, index=None)
    hope = st.selectbox("希望クラス", CLASSES, index=None)
    note = st.text_area("備考（任意）", placeholder="希望理由など（任意）")
    st.divider()
    submit = st.button("✅ 申込する", type="primary", use_container_width=True)

    if submit:
        if not (who and current and hope):
            st.error("未入力の項目があります。")
            return
        ts = append_action(who, "振替申込", current, f"→ {hope}／{(note or '').strip()}".strip("／"))
        st.success(f"振替希望を送信しました（{ts}）。")
