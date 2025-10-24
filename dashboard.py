# dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import os, json

from ui_settings import ui_settings_panel  # ← 追加

# ============================================
# 設定
# ============================================
DATA_FILE = "data.xlsx"               # ユーザーアクションログ
WEEK_EVENTS_FILE = "week_events.xlsx" # 週次イベント管理
LAST_SEEN_FILE = "last_seen.json"     # 既読基準の保存

# クラス構成：曜日 → [(時間, クラスID)]（クラスIDは表示名用）
CLASS_MAP = {
    "水曜": [("17:00", "wed_17")],
    "木曜": [("17:00", "thu_17")],
    "金曜": [("17:00", "fri_17")],
    "土曜": [("11:00", "sat_11"), ("15:00", "sat_15"), ("16:00", "sat_16")],
    "日曜": [("10:00", "sun_10"), ("11:00", "sun_11"), ("15:00", "sun_15")],
}

LEDGER_COLUMNS = [
    "泳力級", "名前（ふりがな）", "学校・保育所名",
    "バス利用", "週２コース", "備考",
    "第1週", "第2週", "第3週", "第4週"
]

# ============================================
# 共通ユーティリティ
# ============================================
def get_week_of_month(target_date: date) -> int:
    first_day = target_date.replace(day=1)
    adjusted_dom = target_date.day + first_day.weekday()
    return int((adjusted_dom - 1) / 7) + 1

def jp_weekday_name(dt: date) -> str:
    en = dt.strftime("%A")
    jp_map = {
        "Wednesday": "水曜", "Thursday": "木曜", "Friday": "金曜",
        "Saturday": "土曜", "Sunday": "日曜",
        "Monday": "月曜", "Tuesday": "火曜",
    }
    return jp_map.get(en, "")

def load_last_seen():
    if os.path.exists(LAST_SEEN_FILE):
        try:
            with open(LAST_SEEN_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("last_seen_ts")
        except Exception:
            return None
    return None

def save_last_seen(ts_iso: str):
    with open(LAST_SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_seen_ts": ts_iso}, f, ensure_ascii=False, indent=2)

# ============================================
# 週次サマリー（Excel管理）
# ============================================
def load_week_event_from_excel(target: date) -> str:
    if not os.path.exists(WEEK_EVENTS_FILE):
        return "（イベント未登録）"
    try:
        df = pd.read_excel(WEEK_EVENTS_FILE)
        if not all(c in df.columns for c in ["年", "月", "週", "イベント"]):
            return "（events列不足：年・月・週・イベント）"
        wk = get_week_of_month(target)
        hit = df[(df["年"] == target.year) & (df["月"] == target.month) & (df["週"] == wk)]
        if len(hit) == 0:
            return "（該当週のイベントなし）"
        return str(hit.iloc[0]["イベント"])
    except Exception as e:
        return f"（イベント読込エラー：{e}）"

def render_week_summary():
    today = date.today()
    month_label = f"{today.month}月"
    week_no = get_week_of_month(today)
    event_text = load_week_event_from_excel(today)

    st.markdown(
        f"""
        <div class="card">
          <b>📅 {month_label} 第{week_no}週目</b>
          <small>（{today.strftime('%Y-%m-%d')} 現在）</small><br>
          🎉 <b>今週のイベント：</b>{event_text}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================
# 最新アクション・サマリー（縦リスト＋新着強調＋任意音）
# ============================================
def render_latest_actions():
    st.markdown("### 📊 最新のユーザーアクション")
    last_seen_ts = load_last_seen()
    last_seen_dt = pd.to_datetime(last_seen_ts) if last_seen_ts else None

    if not os.path.exists(DATA_FILE):
        st.info("📂 'data.xlsx' が存在しません。")
        return

    try:
        df = pd.read_excel(DATA_FILE)
        if not all(c in df.columns for c in ["日時", "ユーザー名", "種別", "内容"]):
            st.warning("必要な列（日時, ユーザー名, 種別, 内容）が不足しています。")
            return

        df["日時_dt"] = pd.to_datetime(df["日時"], errors="coerce")
        df = df.sort_values("日時_dt", ascending=False).head(20)
        df["新規"] = df["日時_dt"] > last_seen_dt if last_seen_dt is not None else True

        new_count = int(df["新規"].sum())

        # 新着音（任意）: 同フォルダに notify.mp3 がある場合のみ
        if new_count > 0 and os.path.exists("notify.mp3"):
            st.markdown(
                """
                <audio autoplay style="display:none;">
                  <source src="notify.mp3" type="audio/mpeg">
                </audio>
                """,
                unsafe_allow_html=True
            )
            st.success(f"🔔 新しいアクションが {new_count} 件あります！")

        for _, row in df.iterrows():
            bg = "#ffefef" if row["新規"] else "#f5f5f5"
            st.markdown(
                f"""
                <div style="background-color:{bg};padding:8px 10px;border-radius:10px;margin-bottom:6px;">
                    <b>{row['日時']}</b> ｜ <b>{row['ユーザー名']}</b> ｜ {row['種別']}<br>
                    <small>{row['内容']}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("✔ すべて既読にする"):
                newest = df["日時_dt"].max()
                if pd.notnull(newest):
                    save_last_seen(newest.isoformat())
                    st.rerun()
        with c2:
            st.caption("※ 新着（既読基準より後）のみ色で強調。")

    except Exception as e:
        st.error(f"データ読込エラー：{e}")

# ============================================
# クラス台帳（共通テンプレート：泳力級～第4週）
# ============================================
def render_class_ledger(title: str, capacity: int = 20, rows_to_show: int = 10):
    st.markdown(f"#### {title} 台帳（10月度）")
    st.caption(f"※ 定員{capacity}名（表示は{rows_to_show}名サンプル）")

    sample = [
        ["5級", "田中 太郎（たなか たろう）", "○○小学校", "有", "無", "", "○", "○", "", "○"],
        ["6級", "佐藤 花子（さとう はなこ）", "△△保育園", "無", "有", "", "○", "", "○", "○"],
    ]
    blanks = [[""] * len(LEDGER_COLUMNS) for _ in range(max(0, rows_to_show - len(sample)))]
    df = pd.DataFrame(sample + blanks, columns=LEDGER_COLUMNS)
    st.dataframe(df, width="stretch")

# ============================================
# 本日のスケジュール（該当曜日の全クラスを縦に表示）
# ============================================
def render_today_schedule():
    st.subheader("📅 本日のスケジュール")
    today = date.today()
    jp_day = jp_weekday_name(today)

    if jp_day in CLASS_MAP:
        for time_label, _module_id in CLASS_MAP[jp_day]:
            render_class_ledger(f"{jp_day} {time_label}")
            st.markdown("---")
    else:
        st.info("本日はクラススケジュールのない曜日です。")

# ============================================
# 曜日別クラス管理（タブ → 時間ボタン → クラス表示）
# ============================================
def render_class_tabs():
    st.subheader("🗓 曜日別クラス管理")
    tabs = st.tabs(list(CLASS_MAP.keys()))

    for (day_name, class_list), tab in zip(CLASS_MAP.items(), tabs):
        with tab:
            st.markdown(f"#### {day_name}クラス一覧")
            cols = st.columns(len(class_list))
            for col, (time_label, module_id) in zip(cols, class_list):
                with col:
                    if st.button(f"{time_label} を表示", key=f"{day_name}_{time_label}"):
                        st.session_state["selected_class"] = (day_name, time_label, module_id)

            if "selected_class" in st.session_state and st.session_state["selected_class"][0] == day_name:
                _, time_label, _module_id = st.session_state["selected_class"]
                render_class_ledger(f"{day_name} {time_label}")

# ============================================
# メイン
# ============================================
def main():
    st.set_page_config(page_title="教室ダッシュボード", layout="wide", initial_sidebar_state="collapsed")
    ui_settings_panel()  # ← サイドバーに表示設定 & CSS適用
    st.title("🏫 管理者ダッシュボード")
    st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d (%a)')}")

    # タイトル直下：週次サマリー（Excel管理）
    render_week_summary()

    # 最新アクション（縦リスト）
    render_latest_actions()
    st.markdown("---")

    # 本日の全クラス（縦並び）
    render_today_schedule()
    st.markdown("---")

    # 曜日→時間→クラス表示
    render_class_tabs()

    st.markdown("---")
    st.caption(f"🕒 最終更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
