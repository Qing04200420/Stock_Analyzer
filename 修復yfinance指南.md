# 修復 yfinance 連線指南

## 🔍 診斷結果

**問題識別**: HTTP 429 - Rate Limit Exceeded

```
Yahoo Finance API 狀態碼: 429
含義: 請求速率超過限制
```

這表示：
- ✅ 網路連線正常
- ✅ Yahoo Finance 網站可存取
- ❌ API 請求被限制（太頻繁或地區限制）

---

## 💡 解決方案

### 方案 1: 使用 VPN（推薦）⭐

**最有效的解決方法**

1. **安裝 VPN 軟體**
   - 免費選項: ProtonVPN, Windscribe
   - 付費選項: NordVPN, Surfshark, ExpressVPN

2. **連線到適合的伺服器**
   - 🇺🇸 美國（推薦）
   - 🇭🇰 香港
   - 🇸🇬 新加坡
   - 🇯🇵 日本

3. **重新啟動程式**
   ```bash
   python -m streamlit run app.py
   ```

### 方案 2: 等待並重試

Yahoo Finance 的速率限制會在一段時間後重置：

1. **等待時間**: 30分鐘 - 1小時
2. **避免頻繁請求**: 不要快速重複查詢
3. **重新測試**:
   ```bash
   python test_yfinance_connection.py
   ```

### 方案 3: 修改 User-Agent 和請求標頭

更新 data_fetcher.py 來模擬瀏覽器請求：

```python
# 在 _try_online 方法中添加自定義 session
import requests
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

# 使用 session 來下載
import yfinance as yf
yf.download(..., session=session)
```

### 方案 4: 使用替代資料源

#### A. FinMind API (台灣金融資料)

**優點**: 專門提供台股資料，免費

```bash
pip install FinMind
```

```python
from FinMind.data import DataLoader
dl = DataLoader()
data = dl.taiwan_stock_daily(stock_id='2330', start_date='2024-01-01')
```

#### B. yfinance 搭配代理

如果您有代理伺服器：

```bash
# Windows
set HTTP_PROXY=http://proxy-server:port
set HTTPS_PROXY=http://proxy-server:port

# Linux/Mac
export HTTP_PROXY=http://proxy-server:port
export HTTPS_PROXY=http://proxy-server:port
```

### 方案 5: 降低請求頻率

修改程式碼添加延遲：

```python
import time

def _try_online(self, stock_id: str, days: int):
    time.sleep(2)  # 每次請求前等待2秒
    # ... 原有代碼
```

---

## 🛠️ 實作：整合 FinMind（推薦替代方案）

### 安裝 FinMind

```bash
pip install FinMind
```

### 修改 data_fetcher.py

我可以幫您整合 FinMind 作為備援資料來源，讓系統可以獲取真實的台股資料。

是否要我：
1. ✅ 整合 FinMind API
2. ✅ 保留 yfinance 作為主要來源
3. ✅ FinMind 作為第二備援
4. ✅ 參考價格作為最後備援

這樣可以建立**三層備援機制**：

```
yfinance → FinMind → 參考價格
(國際)    (台灣)     (本地)
```

---

## 📊 當前狀態

雖然 yfinance 暫時無法使用，但系統仍然：

✅ **完全可用**
- 使用 2024-01 真實市場參考價格
- 所有功能正常運作
- 價格範圍合理真實

✅ **適合用於**
- 學習技術分析
- 測試投資策略
- 回測系統驗證
- 教育培訓

⚠️ **限制**
- 非即時資料
- 無法反映最新市場變化

---

## 🎯 建議行動

### 立即可行

1. **使用 VPN** - 5分鐘解決
2. **等待重試** - 1小時後自動恢復
3. **繼續使用參考資料** - 功能完整

### 長期方案

1. **整合 FinMind** - 獲取真實台股資料
2. **設定代理** - 企業環境適用
3. **使用券商 API** - 最穩定但需開戶

---

## ❓ 常見問題

### Q: 為什麼會遇到 429 錯誤？

**A**: Yahoo Finance 對免費 API 有使用限制：
- 每小時/每天有請求次數上限
- 某些地區可能有額外限制
- 頻繁請求會觸發保護機制

### Q: VPN 會影響系統效能嗎？

**A**:
- ⚡ 延遲增加：10-50ms（通常無感）
- 💾 資料傳輸：正常使用無影響
- 🔒 安全性：提升隱私保護

### Q: FinMind 免費嗎？

**A**:
- ✅ 免費版：每日 500 次請求
- ✅ 包含：台股、期貨、選擇權資料
- ✅ 註冊：僅需 email，無需付費

### Q: 可以同時使用多個資料源嗎？

**A**: 可以！建議設定優先順序：
1. yfinance（國際資料、更新快）
2. FinMind（台股專門、穩定）
3. 參考資料（本地備援、永遠可用）

---

## 📝 下一步

請選擇您想要的解決方案：

### 選項 A: 我想整合 FinMind ⭐

**回覆**: "整合 FinMind"

我會幫您：
1. 安裝 FinMind
2. 修改 data_fetcher.py
3. 建立三層備援機制
4. 測試真實資料獲取

### 選項 B: 我會使用 VPN

**回覆**: "使用 VPN"

步驟：
1. 安裝並連線 VPN
2. 執行: `python test_yfinance_connection.py`
3. 確認狀態碼變成 200
4. 啟動系統: `python -m streamlit run app.py`

### 選項 C: 繼續使用當前系統

**回覆**: "保持現狀"

當前系統已經：
- ✅ 完全可用
- ✅ 價格真實合理
- ✅ 功能完整

隨時可以嘗試其他解決方案。

---

**請告訴我您想選擇哪個方案，我會立即協助您！** 🚀
