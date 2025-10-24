import streamlit as st
from utils import CLASSES, USERS, append_action

def render():
    st.header("💤 お休み連絡")
    who = st.selectbox("ご利用者名", USERS, index=None, placeholder="選択してください")
    klass = st.selectbox("クラスを選択", CLASSES, index=None)
    reason = st.radio("理由", ["体調不良","旅行","学校行事","その他"], horizontal=True)
    note = st.text_area("備考（任意）", placeholder="症状や詳細など（任意）")
    st.divider()
    colA, colB = st.columns([1,1])
    with colA:
        submit = st.button("✅ 確認して送信", use_container_width=True, type="primary")
    with colB:
        st.button("↩ キャンセル", use_container_width=True)

    if submit:
        if not (who and klass and reason):
            st.error("未入力の項目があります。")
            return
        ts = append_action(who, "お休み", klass, f"{reason}／{(note or '').strip()}".strip("／"))
        st.success(f"送信しました（{ts}）。ご連絡ありがとうございます。")
