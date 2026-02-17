import requests
import time
# 导入database 模块
import database 

API_KEY = "V2KADT3RUL46F59E"  
SYMBOL = "NVDA"
URL = "https://www.alphavantage.co/query"

def fetch_nvda_price():
    """从 API 获取数据并存入数据库"""
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": SYMBOL,
        "apikey": API_KEY
    }

    try:
        print(f"🚀 Fetching data for {SYMBOL}...")
        response = requests.get(URL, params=params, timeout=10)
        data = response.json()

        # 错误检查
        if "Global Quote" not in data:
            print(f"❌ API Error: {data}")
            return

        quote = data["Global Quote"]
        price_str = quote.get("05. price")

        if price_str:
            price = float(price_str)
            
            # 调用 database 模块保存数据
            database.insert_price(SYMBOL, price)
        else:
            print("❌ Price not found in response.")

    except Exception as e:
        print(f"❌ Network or Script Error: {e}")

if __name__ == "__main__":
    # 1. 确保数据库已存在
    database.init_db()
    
    # 2. 抓取并保存
    fetch_nvda_price()
    
    # 3. 验证结果：打印数据库里的内容
    database.fetch_recent_data()