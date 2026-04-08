import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import anthropic
import time

st.set_page_config(page_title="HK AI Profit Trader", page_icon="📈", layout="wide")
st.title("🇭🇰 HK AI Profit Trader")
st.caption("全球經濟 500 日分析 · 未來 1 年升幅股票預測 | iOS 手機能版")

CLAUDE_API_KEY = st.secrets.get("CLAUDE_API_KEY")

if not CLAUDE_API_KEY:
    st.error("請先去 Manage app → Settings → Secrets 設定 CLAUDE_API_KEY")
    st.stop()

# ====================== 新功能：全球經濟 500 日分析 ======================
st.subheader("🌍 全球經濟近 500 日總結 + 未來 1 年 AI 選股")

if st.button("🚀 開始分析未來 1 年升幅股票", type="primary", use_container_width=True):
    with st.spinner("正在拉取近 500 日全球經濟消息 + Claude 深度分析...（需 15-25 秒）"):
        # 這裡用 Claude 做真正長期分析
        prompt = """
你係全球頂級宏觀 + 股票分析師。
請根據以下要求分析：

1. 總結過去 500 日（約 2024 年 10 月至今）最重要全球經濟事件、政策、地緣政治、利率、通脹、AI 發展等。
2. 根據以上宏觀環境，預測未來 12 個月（2026 年 4 月至 2027 年 4 月）哪些板塊 / 地區 / 個股最有機會大升幅。
3. 特別 focus 港股 + 美股 + 科技 + AI + 新能源 + 金融板塊。
4. 輸出格式：
   - 整體宏觀展望（升 / 跌 / 震）
   - Top 8 推薦股票（每隻包括：代碼、公司名、預計 1 年升幅 %、主要理由）
   - 風險提醒

用專業、保守、數據驅動嘅語氣寫。
"""

        try:
            client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            analysis = message.content[0].text
            st.success("Claude 完成 500 日全球經濟 + 未來 1 年分析！")
            st.markdown(analysis)
        except Exception as e:
            st.error(f"分析失敗：{str(e)}")
            st.info("請檢查 Claude API Key 是否正確，或稍後再試。")

st.caption("⚠️ 重要提醒：以上分析只供參考，AI 預測唔係保證。投資有風險，市場可能大跌。請自行做功課同分散風險。")
