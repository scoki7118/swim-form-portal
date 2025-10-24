import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime

# Google スプレッドシート連携設定
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Secrets から認証情報を読み込む
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=SCOPE
)

client = gspread.authorize(credentials)
sheet = client.open_by_key(st.secrets["spreadsheet"]["sheet_id"]).worksheet("シート1")

# 選択肢（必要に応じて編集可）
CLASSES = [
    "水曜17:00", "木曜17:00", "金曜17:00",
    "土曜11:00", "土曜15:00", "土曜16:00",
    "日曜10:00", "日曜11:00", "日曜15:00"
]

USERS = ["田中太郎", "佐藤花子", "鈴木次郎"]

def append_action(user: str, action_type: str, klass: str, content: str):
    """Googleスプレッドシートに1行追加"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [ts, user, action_type, klass, content]
    sheet.append_row(new_row)
    return ts
