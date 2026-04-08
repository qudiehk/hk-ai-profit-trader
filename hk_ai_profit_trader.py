import streamlit as st
import anthropic

st.set_page_config(page_title="HK AI Profit Trader", page_icon="📈", layout="wide")
st.title("🇭🇰 HK AI Profit Trader")
st.caption("全球經濟 500 日分析 · 未來 1 年升幅股票預測 | iOS 手機能版")

CLAUDE_API_KEY = st.secrets.get("CLAUDE_API_KEY")

if not CLAUDE_API_KEY:
    st.error("請先去 Manage app → Settings → Secrets 設定 CLAUDE_API_KEY")
    st.stop()

st.subheader("🌍 全球經濟近 500 日總結 + 未來 1 年 AI 選股")

if st.button("🚀 開始分析未來 1 年升幅股票", type="primary", use_container_width=True):
    with st.spinner("正在分析近 500 日全球經濟數據 + 預測未來 1 年升幅股票...（15-25 秒）"):
        prompt = """
You are a top global macro + stock analyst.
Summarize the most important global economic events, policies, geopolitics, interest rates, inflation, AI development etc. in the past 500 days (approx. Oct 2024 to now).
Based on this macro environment, predict which sectors / regions / individual stocks have the highest chance of significant rise in the next 12 months (Apr 2026 - Apr 2027).
Focus especially on Hong Kong stocks, US stocks, Technology, AI, New Energy, and Financial sectors.
Output format:
- Overall macro outlook (Bullish / Bearish / Sideways)
- Top 8 recommended stocks (code, company name, estimated 1-year upside %, main reasons)
- Risk warning

Reply in clear, professional English only. No Chinese characters.
"""

        try:
            client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            analysis = message.content[0].text
            st.success("✅ 分析完成！")
            st.markdown(analysis)
        except Exception as e:
            st.error(f"分析失敗：{str(e)}")
            st.info("請檢查 Claude API Key 是否正確，或稍後再試。")

st.caption("⚠️ 重要提醒：以上分析只供參考，AI 預測唔係保證。投資有風險，請自行做功課同分散風險。")
