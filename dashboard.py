import streamlit as st
import pandas as pd
import requests
import os
# 如果环境变量里有 API_URL 就用环境变量，否则默认用 localhost
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="NVDA AI Analytics", layout="wide")

st.title("📈 NVIDIA (NVDA) AI Analytics Dashboard")
st.markdown("Real-time market data powered by **FastAPI** & **Alpha Vantage**")

# --- 1. 获取数据 ---
def fetch_data():
    try:
        response = requests.get(f"{API_URL}/price/history?limit=20")
        if response.status_code == 200:
            data = response.json()["history"]
            return data
        else:
            st.error("Failed to fetch data from API")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        st.warning("👉 Hint: Make sure 'uvicorn main:app' is running in another terminal!")
        return []

# --- 2. 处理数据 ---
data = fetch_data()

if data:
    # 把 JSON 数据转换成 Pandas DataFrame (表格)
    df = pd.DataFrame(data)
    
    # 把时间字符串转换成真正的时间格式，方便画图
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # 按照时间排序
    df = df.sort_values("timestamp")

    # --- 3. 显示核心指标 (Metrics) ---
    latest_price = df.iloc[-1]["price"]
    previous_price = df.iloc[-2]["price"] if len(df) > 1 else latest_price
    price_change = latest_price - previous_price
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="NVDA Latest Price", 
            value=f"${latest_price:.2f}", 
            delta=f"${price_change:.2f}"
        )
    
    with col2:
        st.metric(label="Data Points", value=len(df))

    # --- 4. 画图 (Line Chart) ---
    st.subheader("Price Trend (Last 20 Data Points)")
    
    # Streamlit 自带的简单折线图
    st.line_chart(df, x="timestamp", y="price")

    # --- 5. 原始数据表格 (可选) ---
    with st.expander("View Raw Data"):
        st.dataframe(df)

else:
    st.info("Waiting for data... (Is the backend running?)")

# --- 6. AI 区域 ---
st.divider()
st.subheader("🤖 AI Market Analysis (Local LLM)")

# 创建一个按钮
if st.button("Generate AI Summary"):
    with st.spinner("Thinking... (This runs locally on your GPU/CPU)"):
        try:
            # 请求后端的新接口
            response = requests.get(f"{API_URL}/ai/summary", timeout=60)
            
            if response.status_code == 200:
                summary = response.json().get("summary", "No summary returned.")
                st.success("Analysis Complete!")
                
                # 用一个漂亮的框框显示结果
                st.info(f"**Market Insight:** {summary}")
            else:
                st.error("Failed to get summary from backend.")
                
        except Exception as e:
            st.error(f"Connection Error: {e}")