import sqlite3
from datetime import datetime

# 数据库文件名
DB_NAME = "market_data.db"

def get_db_connection():
    """创建并返回数据库连接"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # 让我们能像字典一样访问列名
    return conn

def init_db():
    """初始化数据库：如果表不存在，就创建它"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建 stock_prices 表
    # id: 自动递增的唯一标识符
    # symbol: 股票代码 (NVDA)
    # price: 价格
    # timestamp: 抓取时间
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database {DB_NAME} initialized and table 'stock_prices' is ready.")

def insert_price(symbol, price):
    """将价格数据插入数据库"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO stock_prices (symbol, price, timestamp)
        VALUES (?, ?, ?)
    ''', (symbol, price, current_time))
    
    conn.commit()
    conn.close()
    print(f"💾 Saved to DB: {symbol} at ${price} ({current_time})")

def fetch_recent_data(limit=5):
    """读取最近的几条数据（用于验证）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM stock_prices ORDER BY id DESC LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    print("\n--- Recent Database Records ---")
    for row in rows:
        print(f"ID: {row['id']} | {row['symbol']} | ${row['price']} | {row['timestamp']}")
    print("-------------------------------")

# 如果直接运行这个文件，就执行初始化
if __name__ == "__main__":
    init_db()