# 專案結構說明

## 檔案架構

```
stockIDE/
│
├── 📄 app.py                              # Streamlit 主應用程式（前端UI）
├── 📄 requirements.txt                     # Python 套件相依清單
├── 📄 test_backend.py                      # 後端功能測試腳本
│
├── 📜 README.md                            # 專案說明文件
├── 📜 QUICKSTART.md                        # 快速開始指南
├── 📜 PROJECT_STRUCTURE.md                 # 本檔案
│
├── 🚀 start.bat                            # Windows 啟動腳本
├── 🚀 start.sh                             # Linux/macOS 啟動腳本
│
├── ⚙️ .env.example                         # 環境變數範例
├── 📋 .gitignore                           # Git 忽略清單
│
└── 📁 backend/                             # 後端模組目錄
    ├── __init__.py
    │
    ├── 📁 modules/                         # 核心功能模組
    │   ├── __init__.py
    │   ├── 📊 data_fetcher.py             # 台灣股市資料串接
    │   ├── ⚠️ risk_predictor.py           # 風險預測與評估
    │   ├── 💡 strategy_analyzer.py        # 投資策略分析
    │   └── 🎯 warrant_analyzer.py         # 權證分析與推薦
    │
    ├── 📁 utils/                           # 工具函數（保留擴充）
    │   └── __init__.py
    │
    └── 📁 config/                          # 設定檔（保留擴充）
        └── __init__.py
```

## 核心檔案說明

### 前端

#### [app.py](app.py)
主應用程式，使用 Streamlit 框架建立 Web UI。

**主要功能：**
- 🏠 首頁：系統介紹和熱門股票
- 📊 股票分析：K線圖、價格統計
- ⚠️ 風險評估：波動率、VaR、Beta 等
- 💡 投資策略：技術指標、綜合分析、回測
- 🎯 權證分析：Black-Scholes、Greeks、篩選推薦

**程式碼行數：** ~600 行

### 後端模組

#### [backend/modules/data_fetcher.py](backend/modules/data_fetcher.py)
資料獲取模組

**類別：**
- `TaiwanStockDataFetcher`：台灣股票資料獲取
  - `get_stock_price()` - 獲取歷史價格
  - `get_realtime_price()` - 獲取即時股價
  - `get_stock_info()` - 獲取基本資訊
  - `get_top_stocks()` - 獲取熱門股票

- `WarrantDataFetcher`：權證資料獲取
  - `get_warrant_list()` - 獲取權證列表
  - `calculate_warrant_value()` - 計算權證價值

**資料來源：**
- twstock（台灣股市）
- yfinance（Yahoo Finance）

**程式碼行數：** ~260 行

#### [backend/modules/risk_predictor.py](backend/modules/risk_predictor.py)
風險預測模組

**類別：**
- `RiskPredictor`：風險評估器

**主要方法：**
- `calculate_volatility()` - 計算波動率
- `calculate_var()` - 計算 VaR 風險值
- `calculate_beta()` - 計算 Beta 係數
- `calculate_sharpe_ratio()` - 計算 Sharpe Ratio
- `calculate_max_drawdown()` - 計算最大回撤
- `assess_risk_level()` - 綜合風險評級
- `predict_risk()` - 完整風險分析

**使用技術：**
- 歷史模擬法（VaR）
- 統計分析（波動率、Beta）
- 財務指標（Sharpe Ratio）

**程式碼行數：** ~230 行

#### [backend/modules/strategy_analyzer.py](backend/modules/strategy_analyzer.py)
投資策略分析模組

**類別：**
- `StrategyAnalyzer`：策略分析器

**技術指標：**
- 移動平均線（MA5, MA10, MA20, MA60）
- RSI（相對強弱指標）
- MACD（指數平滑異同移動平均線）
- KDJ（隨機指標）
- 布林通道（Bollinger Bands）

**主要方法：**
- `calculate_*()` - 計算各項技術指標
- `generate_*_signals()` - 生成交易信號
- `comprehensive_analysis()` - 綜合技術分析
- `backtest_strategy()` - 策略回測

**程式碼行數：** ~400 行

#### [backend/modules/warrant_analyzer.py](backend/modules/warrant_analyzer.py)
權證分析模組

**類別：**
- `WarrantAnalyzer`：權證分析器

**主要功能：**
- Black-Scholes 定價模型
- Greeks 計算（Delta, Gamma, Theta, Vega, Rho）
- 槓桿分析（理論槓桿、實質槓桿）
- 內含價值與時間價值拆解
- 損益兩平點計算
- 權證評分與推薦

**主要方法：**
- `black_scholes_call()` - 認購權證定價
- `black_scholes_put()` - 認售權證定價
- `calculate_warrant_greeks()` - 計算 Greeks
- `analyze_warrant()` - 完整權證分析
- `screen_warrants()` - 權證篩選
- `recommend_warrants()` - 權證推薦

**使用技術：**
- Black-Scholes 模型
- scipy.stats（常態分佈）
- 財務工程計算

**程式碼行數：** ~400 行

### 測試與文件

#### [test_backend.py](test_backend.py)
後端功能測試腳本

**測試項目：**
- 資料獲取功能
- 風險預測功能
- 策略分析功能
- 權證分析功能

**使用方式：**
```bash
python test_backend.py
```

#### [README.md](README.md)
完整專案說明文件

**內容：**
- 功能特色
- 技術架構
- 安裝說明
- 使用指南
- 常見股票代碼
- 注意事項
- 未來擴充方向

#### [QUICKSTART.md](QUICKSTART.md)
5分鐘快速開始指南

**內容：**
- 快速安裝步驟
- 功能示範
- 常見問題解答
- 進階使用技巧

### 設定檔

#### [requirements.txt](requirements.txt)
Python 套件相依清單

**主要套件：**
- streamlit - Web UI 框架
- pandas - 資料處理
- numpy - 數值計算
- yfinance - Yahoo Finance API
- twstock - 台灣股市資料
- plotly - 互動式圖表
- scikit-learn - 機器學習工具
- ta - 技術分析指標
- scipy - 科學計算

#### [.gitignore](.gitignore)
Git 版本控制忽略清單

**忽略項目：**
- Python 快取檔
- 環境變數檔
- IDE 設定檔
- 資料檔案
- 日誌檔案

## 程式碼統計

| 檔案 | 行數 | 主要功能 |
|------|------|----------|
| app.py | ~600 | 前端 UI |
| data_fetcher.py | ~260 | 資料串接 |
| risk_predictor.py | ~230 | 風險評估 |
| strategy_analyzer.py | ~400 | 策略分析 |
| warrant_analyzer.py | ~400 | 權證分析 |
| test_backend.py | ~150 | 功能測試 |
| **總計** | **~2040** | **完整系統** |

## 技術棧

### 後端技術
- **語言**：Python 3.8+
- **資料處理**：pandas, numpy
- **統計分析**：scipy, scikit-learn
- **技術指標**：ta (Technical Analysis Library)
- **資料來源**：twstock, yfinance

### 前端技術
- **框架**：Streamlit
- **圖表**：Plotly
- **UI/UX**：自定義 CSS、響應式設計

### 開發工具
- **版本控制**：Git
- **套件管理**：pip
- **測試**：自建測試腳本

## 擴充方向

### 短期
1. 加入更多技術指標（威廉指標、CCI等）
2. 改善權證資料來源
3. 加入資料快取機制
4. 優化圖表呈現

### 中期
1. 機器學習預測模型
2. 投資組合管理
3. 自動化交易信號
4. 多股票比較功能

### 長期
1. 串接券商 API
2. 實時推送通知
3. 社群分享功能
4. 行動版應用程式

## 維護建議

1. **定期更新套件**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **測試功能**
   ```bash
   python test_backend.py
   ```

3. **檢查程式碼品質**
   - 遵循 PEP 8 規範
   - 添加適當的註解
   - 撰寫單元測試

4. **監控效能**
   - 資料獲取速度
   - 圖表渲染效能
   - 記憶體使用情況

## 貢獻指南

歡迎貢獻！請遵循以下步驟：

1. Fork 專案
2. 建立功能分支
3. 提交變更
4. 發送 Pull Request

## 授權

本專案僅供學習和研究使用。

---

**最後更新**：2024-01-10
**版本**：v1.0.0
