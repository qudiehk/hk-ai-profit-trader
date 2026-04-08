import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import anthropic
import plotly.graph_objects as go

st.set_page_config(page_title="HK AI Profit Trader", page_icon="📈", layout="wide")
st.title("🇭🇰 HK AI Profit Trader")
st.caption("你專用港股 AI 必買工具 | iOS 手機版")

CLAUDE_API_KEY = st.secrets["CLAUDE_API_KEY"]

HK_SYMBOLS = ["0700.HK", "9988.HK", "0005.HK", "2318.HK", "0388.HK", "1299.HK", "0941.HK"]

with st.sidebar:
    st.header("設定")
    selected_symbols = st.multiselect("選擇股票", HK_SYMBOLS, default=HK_SYMBOLS)
    risk_level = st.select_slider("風險偏好", options=["保守", "平衡", "進取"], value="平衡")
    initial_capital = st.number_input("模擬資金 (HKD)", value=100000, step=1000)

@st.cache_data(ttl=60)
def get_stock_data(symbols):
    data = {}
    for sym in symbols:
        ticker = yf.Ticker(sym)
        info = ticker.info
        hist = ticker.history(period="5d")
        data[sym] = {
            "name": info.get("longName", sym),
            "price": info.get("regularMarketPrice", info.get("currentPrice", 0)),
            "change": info.get("regularMarketChange", 0),
            "changePercent": info.get("regularMarketChangePercent", 0),
            "volume": info.get("regularMarketVolume", 0),
            "history": hist
        }
    return data

stocks_data = get_stock_data(selected_symbols)

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("即時港股報價")
    df = pd.DataFrame([{
        "代碼": sym,
        "名稱": data["name"],
        "最新價": f"HK${data['price']:.2f}",
        "升跌": f"{data['change']:.2f}",
        "升跌%": f"{data['changePercent']:.2f}%",
        "成交量": f"{int(data['volume']):,}"
    } for sym, data in stocks_data.items()])
    st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("你的模擬持倉")
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = []
    if st.session_state.portfolio:
        st.dataframe(pd.DataFrame(st.session_state.portfolio), use_container_width=True)
    else:
        st.info("仲未有持倉，快啲買入試下！")

if st.button("🚀 叫 Claude 即時分析「必買訊號」", type="primary", use_container_width=True):
    with st.spinner("Claude 分析緊..."):
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        prompt = f"你係香港最強港股 AI 交易顧問。以下係即時數據（風險偏好：{risk_level}）：\n{chr(10).join([f'{sym} {data['name']}: HK${data['price']:.2f} ({data['changePercent']:.2f}%)' for sym, data in stocks_data.items()])}"
        message = client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=1000, messages=[{"role": "user", "content": prompt}])
        st.success("Claude 分析完成！")
        st.json(message.content[0].text)

st.subheader("模擬買賣")
col_buy, col_sell = st.columns(2)
with col_buy:
    buy_sym = st.selectbox("選擇要買嘅股票", selected_symbols, key="buy")
    if st.button("🟢 模擬買入 100 股", use_container_width=True):
        price = stocks_data[buy_sym]["price"]
        st.session_state.portfolio.append({"時間": datetime.now().strftime("%H:%M"), "代碼": buy_sym, "動作": "買入", "數量": 100, "買入價": round(price, 2), "現價": round(price, 2), "盈虧": 0})
        st.success(f"已模擬買入 100 股 {buy_sym}")
with col_sell:
    if st.session_state.portfolio:
        sell_sym = st.selectbox("選擇要賣嘅股票", [item["代碼"] for item in st.session_state.portfolio], key="sell")
        if st.button("🔴 模擬賣出", use_container_width=True):
            for i, item in enumerate(st.session_state.portfolio):
                if item["代碼"] == sell_sym:
                    st.session_state.portfolio.pop(i)
                    st.success(f"已模擬賣出 {sell_sym}")
                    break

st.subheader("K線圖")
selected_chart = st.selectbox("選擇股票睇 K線", selected_symbols)
if selected_chart in stocks_data:
    hist = stocks_data[selected_chart]["history"]
    fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
    fig.update_layout(title=f"{selected_chart} 5日 K線", height=500)
    st.plotly_chart(fig, use_container_width=True)

st.caption("⚠️ 模擬程式 · 市場有風險 · AI 只供參考")
