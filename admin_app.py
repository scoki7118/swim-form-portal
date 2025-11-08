import streamlit as st
from auth import require_admin_password
import dashboard  # 既存の管理者UI（dashboard.py）

st.set_page_config(page_title="管理者ダッシュボード", page_icon="🛡️", layout="wide")
require_admin_password()   # st.secrets["ADMIN_PASSWORD"] と照合
dashboard.main()           # 以前お渡しの dashboard.py（main() 定義済み）
