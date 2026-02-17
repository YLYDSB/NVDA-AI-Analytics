import requests

API_KEY = "V2KADT3RUL46F59E"
SYMBOL = "NVDA"

url = "https://www.alphavantage.co/query"
params = {
    "function": "GLOBAL_QUOTE",
    "symbol": SYMBOL,
    "apikey": API_KEY
}

r = requests.get(url, params=params, timeout=20)
data = r.json()

print("Raw response:")
print(data)

quote = data.get("Global Quote", {})
price = quote.get("05. price")

if price is None:
    print("\n❌ Failed to fetch price.")
    print("Possible reasons:")
    print("- Wrong API key")
    print("- Rate limit reached")
    print("- API temporarily down")
else:
    print(f"\n✅ {SYMBOL} latest price: {price}")