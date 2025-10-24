# user_portal.py
import streamlit as st
from datetime import datetime
import importlib
from ui_settings import ui_settings_panel

# --- 登録フォームページ一覧 ---
PAGES = {
    "💤 お休み連絡": "user_pages.absent",
    "🔁 振替申込": "user_pages.transfer",
}

def main():
    st.set_page_config(page_title="各申込フォーム", layout="wide", initial_sidebar_state="collapsed")
    ui_settings_panel()  # 表示設定パネル（フォントサイズ・ボタン拡大など）
    
    # ==== タイトル部分 ====
    st.title("📋 各申込フォーム")
    st.caption(f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    st.markdown("#### ご希望の申込内容を選んでください")
    
    # ==== ボタンを横並びで表示 ====
    cols = st.columns(len(PAGES))
    keys = list(PAGES.keys())
    for col, label in zip(cols, keys):
        with col:
            if st.button(label, use_container_width=True, type="primary"):
                st.session_state["user_page"] = label

    st.divider()

    # ==== 選択されたページを読み込み ====
    current = st.session_state.get("user_page", None)
    if current:
        try:
            mod = importlib.import_module(PAGES[current])
            if hasattr(mod, "render"):
                mod.render()
            else:
                st.error("render() が定義されていません。")
        except Exception as e:
            st.error(f"ページ読み込みエラー: {e}")
    else:
        st.info("⬆️ 上のボタンから申込内容を選択してください。")

if __name__ == "__main__":
    main()
