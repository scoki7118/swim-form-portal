# user_portal.py
import streamlit as st
from datetime import datetime
import importlib
from ui_settings import ui_settings_panel

# --- 登録フォームページ一覧 ---
PAGES = {
    "💤 お休み連絡": "user_pages.absent",
    "🔁 振替申込": "user_pages.transfer",
    # 必要に応じて以下を追加できます
    # "📞 お問い合わせ": "user_pages.contact",
    # "📚 コース変更": "user_pages.course_change",
}


def main():
    # ===== Streamlitの基本設定 =====
    st.set_page_config(
        page_title="各申込フォーム",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # ===== UI設定パネル（フォントサイズやデザイン調整） =====
    try:
        ui_settings_panel()
    except Exception as e:
        st.warning(f"⚠️ 表示設定パネルの読み込みに失敗しました: {e}")

    # ===== タイトル部分 =====
    st.title("📋 各申込フォーム")
    st.caption(f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    st.markdown("#### ご希望の申込内容を選んでください")

    # ===== 各申込ボタンを横並びで表示 =====
    cols = st.columns(len(PAGES))
    keys = list(PAGES.keys())
    for col, label in zip(cols, keys):
        with col:
            if st.button(label, use_container_width=True, type="primary"):
                st.session_state["user_page"] = label

    st.divider()

    # ===== 選択されたページを読み込み =====
    current = st.session_state.get("user_page", None)

    if current:
        module_name = PAGES[current]
        try:
            # モジュールを動的に読み込み
            mod = importlib.import_module(module_name)

            # render() 関数があれば呼び出す
            if hasattr(mod, "render"):
                mod.render()
            else:
                st.error(f"❌ {module_name} に render() 関数が定義されていません。")

        except ModuleNotFoundError:
            st.error(f"📦 ページモジュール '{module_name}' が見つかりません。")
        except Exception as e:
            st.error(f"⚠️ ページ読み込みエラー: {e}")

    else:
        st.info("⬆️ 上のボタンから申込内容を選択してください。")


# ===== メイン実行 =====
if __name__ == "__main__":
    main()
