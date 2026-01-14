"""
Test yfinance connection
"""

import sys
import requests
from datetime import datetime, timedelta

print("=" * 60)
print("yfinance Connection Test")
print("=" * 60)

# 1. Test basic internet
print("\n[1] Testing basic internet connection...")
try:
    response = requests.get("https://www.google.com", timeout=5)
    print(f"    OK - Basic internet works (Status: {response.status_code})")
except Exception as e:
    print(f"    FAIL - Basic internet failed: {e}")

# 2. Test Yahoo Finance website
print("\n[2] Testing Yahoo Finance website...")
try:
    response = requests.get("https://finance.yahoo.com", timeout=10)
    print(f"    OK - Yahoo Finance accessible (Status: {response.status_code})")
except Exception as e:
    print(f"    FAIL - Yahoo Finance not accessible: {e}")
    print("    TIP: You may need VPN or proxy")

# 3. Test Yahoo Finance API directly
print("\n[3] Testing Yahoo Finance API...")
try:
    url = "https://query1.finance.yahoo.com/v8/finance/chart/2330.TW"
    params = {
        'period1': int((datetime.now() - timedelta(days=7)).timestamp()),
        'period2': int(datetime.now().timestamp()),
        'interval': '1d'
    }
    response = requests.get(url, params=params, timeout=10)
    print(f"    Status code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            print("    OK - Yahoo Finance API working!")
            symbol = data['chart']['result'][0]['meta']['symbol']
            print(f"    Symbol: {symbol}")
        else:
            print("    WARN - API responds but data format unusual")
    else:
        print(f"    FAIL - API response abnormal")

except Exception as e:
    print(f"    FAIL - Yahoo Finance API not accessible: {e}")

# 4. Test yfinance package
print("\n[4] Testing yfinance package...")
try:
    import yfinance as yf
    print(f"    yfinance version: {yf.__version__}")

    print("    Downloading TSMC (2330.TW) data...")
    ticker = yf.Ticker("2330.TW")
    hist = ticker.history(period="5d")

    if not hist.empty:
        print(f"    OK - Data retrieved successfully!")
        print(f"    Rows: {len(hist)}")
        print(f"    Latest close: {hist['Close'].iloc[-1]:.2f}")
    else:
        print("    FAIL - Data is empty")

except Exception as e:
    print(f"    FAIL - yfinance test failed: {e}")

# 5. Check proxy settings
print("\n[5] Checking proxy settings...")
import os
http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')

if http_proxy or https_proxy:
    print(f"    HTTP_PROXY: {http_proxy or 'Not set'}")
    print(f"    HTTPS_PROXY: {https_proxy or 'Not set'}")
else:
    print("    No proxy configured")

print("\n" + "=" * 60)
print("SOLUTIONS if Yahoo Finance API is blocked:")
print("=" * 60)
print("""
1. Use VPN
   - Install VPN software (e.g., Surfshark, NordVPN, ProtonVPN)
   - Connect to US, HK, or SG server
   - Restart the program

2. Set up proxy
   - If you have a proxy server:
     set HTTP_PROXY=http://your-proxy:port
     set HTTPS_PROXY=http://your-proxy:port

3. Use alternative data sources
   - FinMind API (requires registration)
   - Broker APIs (requires account)

4. Continue with reference data mode
   - System has built-in 2024-01 real market prices
   - All features fully functional
   - Perfect for learning and testing
""")
print("=" * 60)
