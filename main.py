from fastapi import FastAPI, HTTPException
import sqlite3
import requests
import json

# 初始化 FastAPI 应用
app = FastAPI()

# 数据库文件路径
DB_NAME = "market_data.db"

def get_db_connection():
    """连接到 SQLite 数据库"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # 让返回结果像字典一样好读
    return conn

@app.get("/")
def read_root():
    """健康检查接口：确认服务器正在运行"""
    return {"status": "ok", "message": "NVDA Analytics API is running 🚀"}

@app.get("/price/latest")
def get_latest_price():
    """从数据库获取最新的 NVDA 价格"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL: 按 ID 倒序排列，取第1个（也就是最新的）
    cursor.execute("SELECT * FROM stock_prices ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="No data found in database")

    return {
        "symbol": row["symbol"],
        "price": row["price"],
        "timestamp": row["timestamp"]
    }

@app.get("/price/history")
def get_price_history(limit: int = 10):
    """获取历史价格数据（默认最近10条）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM stock_prices ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()

    # 将数据库行转换为 JSON 列表
    history = []
    for row in rows:
        history.append({
            "id": row["id"],
            "symbol": row["symbol"],
            "price": row["price"],
            "timestamp": row["timestamp"]
        })
    
    return {"history": history}
# --- 新增：AI 分析接口 ---
@app.get("/ai/summary")
def get_ai_summary():
    """调用本地 Ollama 生成市场分析"""
    
    # 1. 获取最近 10 天的数据
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock_prices ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"summary": "No data available for analysis."}

    # 2. 准备数据文本
    # 我们把数据变成这种格式： "2024-02-17: $136.5, 2024-02-16: $135.0..."
    data_text = "\n".join([f"{row['timestamp']}: ${row['price']}" for row in rows])

    # 3. 构造 Prompt (给 AI 的指令)
    prompt = f"""
    You are a financial analyst. 
    Analyze the following NVDA stock price history (most recent first):
    
    {data_text}
    
    Write a very concise (2 sentences max) summary of the price trend. 
    Do not use markdown formatting like bold or italic. Just plain text.
    """

    # 4. 发送给 Ollama (本地 API)
    try:
        # Ollama 默认监听 11434 端口
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3",  # 如果你下载的是 tinyllama，这里要改成 "tinyllama"
            "prompt": prompt,
            "stream": False     # False 表示我们要等它一次性说完，不是一个字一个字吐
        }
        
        print("🤖 Sending request to Ollama...")
        response = requests.post(url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return {"summary": result.get("response", "No response from AI.")}
        else:
            return {"summary": f"Error from Ollama: {response.text}"}

    except Exception as e:
        print(f"❌ AI Error: {e}")
        return {"summary": "Failed to connect to Local AI. Is Ollama running?"}