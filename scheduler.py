import time
import datetime
# 导入我们在 Step 2 写好的抓取模块
import ingest 

# 设置运行间隔（秒）
# 注意：Alpha Vantage 免费版一天限制 25 次请求。
# 如果设置 300 秒（5分钟），2小时就会用完额度。
# 为了测试，我们可以先设为 300秒，但记得测试几次后就按 Ctrl+C 停止。
INTERVAL = 3600  

def start_scheduler():
    print(f"⏰ Scheduler initialized. Task: Fetch NVDA Price.")
    print(f"⏱️ Interval: Every {INTERVAL} seconds.")
    print("------------------------------------------------")

    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[Job Start] {now}")
        
        try:
            # 1. 执行抓取任务
            ingest.fetch_nvda_price()
            
            # 2. (可选) 可以在这里加个简单的验证，打印数据库最新的一条
            # ingest.database.fetch_recent_data(limit=1)
            
        except Exception as e:
            # 容错处理：万一断网了，不要让程序崩溃，而是打印错误并继续等待
            print(f"⚠️ Job Failed unexpectedly: {e}")

        print(f"[Job End] Waiting {INTERVAL} seconds for next run...")
        
        # 3. 睡眠（挂起程序，不占用 CPU）
        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        start_scheduler()
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user.")