"""
診斷 yfinance 連線問題
"""

import sys
import requests
from datetime import datetime, timedelta

print("=" * 60)
print("yfinance 連線診斷工具")
print("=" * 60)

# 1. 測試基本網路連線
print("\n[1] 測試基本網路連線...")
try:
    response = requests.get("https://www.google.com", timeout=5)
    print(f"    ✓ 基本網路連線正常 (狀態碼: {response.status_code})")
except Exception as e:
    print(f"    ✗ 基本網路連線失敗: {e}")

# 2. 測試 Yahoo Finance 網站連線
print("\n[2] 測試 Yahoo Finance 網站...")
try:
    response = requests.get("https://finance.yahoo.com", timeout=10)
    print(f"    ✓ Yahoo Finance 網站可存取 (狀態碼: {response.status_code})")
except Exception as e:
    print(f"    ✗ Yahoo Finance 網站無法存取: {e}")
    print("    提示: 可能需要 VPN 或代理")

# 3. 測試 Yahoo Finance API
print("\n[3] 測試 Yahoo Finance API...")
try:
    # 直接測試 API endpoint
    url = "https://query1.finance.yahoo.com/v8/finance/chart/2330.TW"
    params = {
        'period1': int((datetime.now() - timedelta(days=7)).timestamp()),
        'period2': int(datetime.now().timestamp()),
        'interval': '1d'
    }
    response = requests.get(url, params=params, timeout=10)
    print(f"    狀態碼: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if 'chart' in data and 'result' in data['chart']:
            print("    ✓ Yahoo Finance API 正常運作")
            print(f"    資料: {data['chart']['result'][0]['meta']['symbol']}")
        else:
            print("    ⚠️  API 有回應但資料格式異常")
    else:
        print(f"    ✗ API 回應異常")

except Exception as e:
    print(f"    ✗ Yahoo Finance API 無法存取: {e}")

# 4. 測試 yfinance 套件
print("\n[4] 測試 yfinance 套件...")
try:
    import yfinance as yf
    print(f"    ✓ yfinance 版本: {yf.__version__}")

    # 測試下載資料
    print("    測試下載台積電資料...")
    ticker = yf.Ticker("2330.TW")

    # 嘗試獲取資料
    hist = ticker.history(period="5d")

    if not hist.empty:
        print(f"    ✓ 成功獲取資料！")
        print(f"    資料筆數: {len(hist)}")
        print(f"    最新收盤價: {hist['Close'].iloc[-1]:.2f}")
    else:
        print("    ✗ 獲取的資料為空")

except Exception as e:
    print(f"    ✗ yfinance 測試失敗: {e}")
    import traceback
    traceback.print_exc()

# 5. 檢查代理設定
print("\n[5] 檢查代理設定...")
import os
http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')

if http_proxy or https_proxy:
    print(f"    HTTP_PROXY: {http_proxy or '未設定'}")
    print(f"    HTTPS_PROXY: {https_proxy or '未設定'}")
else:
    print("    ✓ 無代理設定")

# 6. 建議
print("\n" + "=" * 60)
print("診斷建議")
print("=" * 60)

print("""
如果 Yahoo Finance API 無法存取，可能的解決方案：

1. 使用 VPN
   - 安裝 VPN 軟體（例如: Surfshark, NordVPN, ProtonVPN）
   - 連線到美國、香港或新加坡伺服器
   - 重新執行程式

2. 設定代理伺服器
   - 如果您有代理伺服器，可以設定環境變數：
     set HTTP_PROXY=http://your-proxy:port
     set HTTPS_PROXY=http://your-proxy:port

3. 使用其他資料來源
   - twstock (台灣證交所，但目前有相容性問題)
   - FinMind API (需要註冊)
   - 券商 API (需要開戶)

4. 繼續使用參考資料模式
   - 系統已內建 2024-01 真實市場參考價格
   - 所有功能完整可用
   - 適合學習和測試
""")

print("=" * 60)
