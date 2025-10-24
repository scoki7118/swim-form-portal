import streamlit as st
from user_pages import transfer
from admin_pages import admin_dashboard

st.set_page_config(page_title="スイミング申込ポータル", layout="wide")

st.sidebar.title("🏠 メニュー")
page = st.sidebar.radio("ページを選択してください", ["各申込フォーム（ユーザー）", "管理者ダッシュボード"])

if page == "各申込フォーム（ユーザー）":
    transfer.render()
elif page == "管理者ダッシュボード":
    st.warning("⚠️ 管理者専用画面です")
    admin_dashboard
