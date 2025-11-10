# dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==== ページ設定 ====
st.set_page_config(
    page_title="管理者ダッシュボード",
    page_icon="🧭",
    layout="wide"
)

# ==== データファイル設定 ====
DATA_FILE = "data.xlsx"

# ==== データ読み込み関数 ====
def load_data(sheet_name):
    if not os.path.exists(DATA_FILE):
        st.warning(f"⚠️ データファイル {DATA_FILE} が存在しません。")
        return pd.DataFrame()
    try:
        df = pd.read_excel(DATA_FILE, sheet_name=sheet_name)
        if df.empty:
            st.info(f"🪶 {sheet_name} シートはまだ空です。")
        return df
    except Exception as e:
        st.error(f"データ読み込みエラー: {e}")
        return pd.DataFrame()

# ==== ページタイトル ====
st.title("🧭 管理者ダッシュボード")
st.caption(f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ==== メニュー ====
tab1, tab2 = st.tabs(["🏖 お休み連絡", "🔁 振替申込"])

# ==== お休み連絡 ====
with tab1:
    st.subheader("🏖 お休み連絡一覧")

    df_absent = load_data("お休み連絡")
    if not df_absent.empty:
        st.dataframe(df_absent, use_container_width=True)

        csv_abs = df_absent.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 お休みデータをCSVでダウンロード",
            data=csv_abs,
            file_name=f"absent_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ==== 振替申込 ====
with tab2:
    st.subheader("🔁 振替申込一覧")

    df_transfer = load_data("振替申込")
    if not df_transfer.empty:
        st.dataframe(df_transfer, use_container_width=True)

        csv_trans = df_transfer.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 振替データをCSVでダウンロード",
            data=csv_trans,
            file_name=f"transfer_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ==== フッター ====
st.divider()
st.caption("© 2025 Swim Form Portal | 管理者専用画面")
