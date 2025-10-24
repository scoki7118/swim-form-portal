import json, os
import streamlit as st

SETTINGS_FILE = "ui_settings.json"
DEFAULTS = {
    "base_font_px": 16,
    "heading_scale": 1.20,
    "table_density": "標準",
    "button_scale": 1.20,
    "high_contrast": False,
}

def load_ui_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return {**DEFAULTS, **json.load(f)}
        except Exception:
            return DEFAULTS.copy()
    return DEFAULTS.copy()

def save_ui_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)

def apply_ui_css(s):
    base = int(s["base_font_px"])
    h_scale = float(s["heading_scale"])
    btn_scale = float(s["button_scale"])
    density_map = {"ゆったり": "1.9", "標準": "1.6", "コンパクト": "1.35"}
    line_h = density_map.get(s["table_density"], "1.6")

    if s["high_contrast"]:
        fg = "#111"; bg = "#fff"; card = "#ffffff"; border = "#00000022"; link = "#0b63ff"
    else:
        fg = "#222"; bg = "#f7f7f9"; card = "#ffffff"; border = "#00000014"; link = "#1a73e8"

    css = f"""
    <style>
      html, body, [data-testid="stAppViewContainer"] {{
        font-size: {base}px !important; color: {fg}; background: {bg};
      }}
      h1 {{ font-size: {int(base*2.0*h_scale)}px !important; }}
      h2 {{ font-size: {int(base*1.6*h_scale)}px !important; }}
      h3 {{ font-size: {int(base*1.35*h_scale)}px !important; }}
      h4 {{ font-size: {int(base*1.20*h_scale)}px !important; }}

      [data-testid="stDataFrame"] table, [data-testid="stTable"] table {{
        line-height: {line_h};
        font-size: {int(base*0.95)}px;
      }}
      [data-testid="stDataFrame"] thead th {{
        position: sticky; top: 0; background: {card}; z-index: 1;
        border-bottom: 1px solid {border};
      }}
      [data-testid="stDataFrame"] tbody tr:nth-child(even) td {{
        background: rgba(0,0,0,0.015);
      }}

      .stButton>button, button[kind="primary"], button[kind="secondary"] {{
        transform: scale({btn_scale}); transform-origin: left center;
        padding: 0.6em 1.1em !important;
      }}

      .card {{
        background: {card}; border: 1px solid {border};
        border-radius: 12px; padding: 10px 12px; margin: 6px 0;
      }}
      a, a:visited {{ color: {link}; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def ui_settings_panel():
    s = load_ui_settings()
    st.sidebar.markdown("### ⚙ 表示設定")
    s["base_font_px"]  = st.sidebar.slider("文字サイズ（px）", 14, 22, s["base_font_px"])
    s["heading_scale"] = st.sidebar.slider("見出しの大きさ倍率", 1.0, 1.4, s["heading_scale"])
    s["table_density"] = st.sidebar.selectbox("表の行間", ["ゆったり","標準","コンパクト"],
                                              index=["ゆったり","標準","コンパクト"].index(s["table_density"]))
    s["button_scale"]  = st.sidebar.slider("ボタンの大きさ倍率", 1.0, 1.5, s["button_scale"])
    s["high_contrast"] = st.sidebar.toggle("ハイコントラスト（視認性優先）", s["high_contrast"])
    if st.sidebar.button("保存して適用"):
        save_ui_settings(s)
        st.sidebar.success("保存しました。画面に適用します。")
        st.rerun()
    apply_ui_css(s)
