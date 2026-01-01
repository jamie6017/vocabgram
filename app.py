# -*- coding: utf-8 -*-
"""
VocabGram Pro — 多了「頻次」與模式的加強版
作者：Jamie
說明：
1) 這個 App 會自動偵測你的 Excel 欄位並提供：
   - 關鍵字搜尋（跨欄位）
   - 欄位選擇顯示
   - 數值欄位（例如「頻次」「熟悉度」）的範圍滑桿
   - 專屬「頻次」強化（範圍、等級、排序、圖表）
   - 模式切換（學習／複習／挑戰）
2) 只要把 Excel 上傳，或將 data.xlsx 放在同資料夾即可使用。
3) 部署到 Streamlit Community Cloud 就能得到 Web App 連結。
"""

import os
import pandas as pd
import streamlit as st

# --- 頁面設定 ---
st.set_page_config(page_title="VocabGram Pro — 頻次加強版", page_icon="📚", layout="wide")

st.title("📚 VocabGram Pro — 頻次加強版")
st.caption("支援：上傳 Excel、篩選搜尋、頻次強化、模式切換、下載結果與圖表")

# --- 讀取 Excel 工具 ---
def read_excel_any(path_or_buffer) -> pd.DataFrame:
    try:
        return pd.read_excel(path_or_buffer, engine="openpyxl")
    except Exception as e:
        st.error(f"讀取 Excel 失敗：{e}")
        return pd.DataFrame()

# --- 偵測預設檔 ---
default_candidates = ["data.xlsx", "default.xlsx", "樣本.xlsx"]
existing_default = next((f for f in default_candidates if os.path.exists(f)), None)

# --- 側欄：資料來源與模式 ---
with st.sidebar:
    st.header("📁 資料來源")
    uploaded = st.file_uploader("上傳 Excel（.xlsx/.xls）", type=["xlsx", "xls"])
    use_default = st.checkbox("使用同資料夾中的預設檔", value=bool(existing_default))
    st.caption("可用預設檔名：" + (existing_default if existing_default else "（目前資料夾沒有）"))

    st.header("🎛️ 模式")
    mode = st.radio("選擇學習模式", options=["一般", "學習", "複習", "挑戰"], index=0, horizontal=True)

# --- 載入資料 ---
df = pd.DataFrame()
if uploaded is not None:
    df = read_excel_any(uploaded)
elif use_default and existing_default:
    df = read_excel_any(existing_default)

if df.empty:
    st.info("請上傳 Excel 或放置 data.xlsx 於同資料夾。建議欄位：單字／詞性／中文／頻次／熟悉度。")
    st.stop()

# --- 欄位資訊 ---
st.success("資料已載入！")
with st.expander("欄位資訊（Columns）", expanded=False):
    st.write(pd.DataFrame({"欄位": df.columns}))

# --- 介面：關鍵字、欄位選擇 ---
st.subheader("🔎 篩選與搜尋（跨欄位）")
all_cols = list(df.columns)
keyword = st.text_input("關鍵字（於所有欄位中比對，忽略大小寫）")
show_cols = st.multiselect("要顯示的欄位", options=all_cols, default=all_cols)

# --- 動態數值篩選（對所有數值欄位提供滑桿）---
st.markdown("**數值欄位篩選（自動偵測）**")
num_cols = [c for c in all_cols if pd.api.types.is_numeric_dtype(df[c])]
range_filters = {}
if num_cols:
    left, right = st.columns(2)
    with left:
        st.caption("選擇數值範圍（例如：頻次、熟悉度）")
        for c in num_cols:
            min_v = float(df[c].min()) if pd.notna(df[c].min()) else 0.0
            max_v = float(df[c].max()) if pd.notna(df[c].max()) else 0.0
            step = max(1.0, (max_v - min_v) / 100) if max_v > min_v else 1.0
            val = st.slider(f"範圍 → {c}", min_value=min_v, max_value=max_v, value=(min_v, max_v), step=step)
            range_filters[c] = val
    with right:
        st.caption("提示：若欄位看不到，請確認該欄位為數值型態（整數或小數）。")
else:
    st.info("目前沒有偵測到數值欄位。若要使用頻次或熟悉度篩選，請在 Excel 新增數值欄位。")

# --- 套用一般篩選 ---
filtered = df.copy()
if keyword:
    filtered = filtered[filtered.apply(lambda row: keyword.lower() in str(row.values).lower(), axis=1)]
for c, (min_v, max_v) in range_filters.items():
    filtered = filtered[(filtered[c] >= min_v) & (filtered[c] <= max_v)]

# --- 頻次強化（若存在）---
st.subheader("📈 頻次加強區")
if "頻次" in df.columns and pd.api.types.is_numeric_dtype(df["頻次"]):
    min_f = float(df["頻次"].min())
    max_f = float(df["頻次"].max())

    # 等級區間（可依需要調整門檻）
    st.caption("等級區間預設：A > 200、B 100–200、C < 100（可自行調整）")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        a_th = st.number_input("A 下限（>）", value=200.0, step=10.0)
    with col2:
        b_low = st.number_input("B 下限（≥）", value=100.0, step=10.0)
    with col3:
        b_high = st.number_input("B 上限（≤）", value=200.0, step=10.0)

    # 排序 & 顯示前 N 名
    sort_choice = st.radio("排序頻次", ["不排序", "由高到低", "由低到高"], index=0, horizontal=True)
    top_n = st.number_input("顯示前 N 名（若排序）", value=50, min_value=1, step=5)

    # 模式對頻次的預設篩選
    if mode == "學習":
        # 中頻（靠近 B 區間）
        filtered = filtered[(filtered["頻次"] >= b_low) & (filtered["頻次"] <= b_high)]
    elif mode == "複習":
        # 高頻（A 區間）
        filtered = filtered[filtered["頻次"] > a_th]
    elif mode == "挑戰":
        # 低頻（C 區間）
        filtered = filtered[filtered["頻次"] < b_low]

    # 依選擇排序
    if sort_choice == "由高到低":
        filtered = filtered.sort_values("頻次", ascending=False)
        filtered = filtered.head(top_n)
    elif sort_choice == "由低到高":
        filtered = filtered.sort_values("頻次", ascending=True)
        filtered = filtered.head(top_n)

    # 圖表區
    with st.expander("頻次圖表（分佈／Top N）", expanded=False):
        # 分佈（使用 value_counts，較直觀）
        st.caption("頻次分佈（依數值）")
        try:
            st.bar_chart(df["頻次"].value_counts().sort_index())
        except Exception:
            st.write("無法繪製分佈圖。")
else:
    st.info("未偵測到數值型『頻次』欄位。若要使用頻次加強功能，請在 Excel 加入『頻次』欄且為數值。")

# --- 顯示結果（套用欄位選擇）---
if show_cols:
    filtered_view = filtered[show_cols]
else:
    filtered_view = filtered

st.subheader("📄 表格結果")
st.dataframe(filtered_view, use_container_width=True)

# --- 下載 ---
st.subheader("⬇️ 下載")
csv_bytes = filtered_view.to_csv(index=False).encode("utf-8-sig")
st.download_button("下載目前篩選結果（CSV）", data=csv_bytes, file_name="filtered.csv", mime="text/csv")

# --- 統計摘要 ---
with st.expander("統計摘要（Numerical Summary）", expanded=False):
    try:
        st.write(filtered.describe(include="all"))
    except Exception:
        st.write("無法產生統計摘要。")

st.caption("© 2026 Jamie — VocabGram Pro 頻次加強版（Streamlit）")
