import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Googleスプレッドシート認証設定
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=SCOPE
)

client = gspread.authorize(credentials)
sheet = client.open_by_key(st.secrets["spreadsheet"]["sheet_id"]).worksheet("シート1")

# タイトル
st.header("📋 管理者ダッシュボード")

# データ読込
data = sheet.get_all_records()
df = pd.DataFrame(data)

if df.empty:
    st.info("まだ申込データがありません。")
else:
    # データ表示
    st.dataframe(df, use_container_width=True)

    # フィルター
    st.subheader("🔍 絞り込み")
    selected_user = st.selectbox("利用者名で絞り込み", ["（全員）"] + sorted(df["ユーザー名"].unique().tolist()))
    if selected_user != "（全員）":
        df = df[df["ユーザー名"] == selected_user]

    selected_class = st.selectbox("クラスで絞り込み", ["（全て）"] + sorted(df["クラス名"].unique().tolist()))
    if selected_class != "（全て）":
        df = df[df["クラス名"] == selected_class]

    st.dataframe(df, use_container_width=True)

    # ダウンロード機能
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 CSVとしてダウンロード",
        data=csv,
        file_name="swim_portal_data.csv",
        mime="text/csv"
    )
