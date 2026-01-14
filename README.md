# 📈 台灣股市投資分析系統 v2.0

> 專業級台灣股市投資分析系統，整合技術分析、投資組合管理、市場情緒分析等多項進階功能

**版本**: v2.0 Professional | **更新日期**: 2026-01-10

---

## ✨ 系統特色

### 🎯 v2.0 重大更新

- ✅ **完整技術指標系統** - 7種主流技術指標（MA、MACD、RSI、KDJ、布林通道、ATR、OBV）
- ✅ **智能交易訊號** - 多指標綜合判斷，生成買賣建議
- ✅ **投資組合管理** - 完整持倉追蹤、績效分析、風險評估
- ✅ **市場情緒分析** - 恐懼貪婪指數、市場廣度、產業輪動
- ✅ **多股橫向比較** - 同時分析多支股票，找出強勢標的
- ✅ **2500+ 行新代碼** - 四個全新專業級分析模組

### 📊 核心功能模組

| 圖示 | 功能 | 說明 | 適合對象 |
|------|------|------|----------|
| 📊 | 股票分析 | K線圖、歷史走勢、即時報價 | 初學者 |
| 📈 | 技術分析 | MA/MACD/RSI/KDJ等技術指標 | 中高級 |
| 📊 | 多股比較 | 橫向比較多支股票表現 | 中級 |
| 💼 | 投資組合 | 持倉管理與績效追蹤 | 中高級 |
| 🎭 | 市場情緒 | 恐懼貪婪指數、市場廣度 | 高級 |
| ⚠️ | 風險評估 | 波動率、VaR、Beta係數 | 中級 |
| 💡 | 投資策略 | 策略回測與績效評估 | 高級 |
| 🎯 | 權證分析 | Black-Scholes、Greeks | 進階 |

---

## 🚀 快速開始

### 1. 環境需求

```bash
Python 3.11+
```

### 2. 安裝

```bash
# 安裝套件
pip install -r requirements.txt

# (可選) 安裝 FinMind 解決 Yahoo Finance 429 錯誤
pip install FinMind
```

### 3. 啟動系統

```bash
streamlit run app.py
```

系統會自動開啟瀏覽器：`http://localhost:8501`

### 4. 5分鐘快速體驗

查看 **[快速入門指南.md](快速入門指南.md)** 進行實際操作！

---

## 📚 完整文件

### 📖 使用指南

- **[快速入門指南.md](快速入門指南.md)** - 5分鐘快速上手，包含實際操作範例
- **[進階分析功能說明.md](進階分析功能說明.md)** - 完整功能介紹與使用技巧（8000+ 字）
- **[權證查詢功能說明.md](權證查詢功能說明.md)** - 權證分析詳細教學
- **[權證查詢功能演示.md](權證查詢功能演示.md)** - 實際案例演示

### 📝 技術文件

- **[v2.0更新總結.md](v2.0更新總結.md)** - 版本更新詳情

---

## 🔥 v2.0 新增模組

### 1. 📈 技術分析模組

**檔案**: `backend/modules/technical_analyzer.py` (700+ 行)

**支援指標**:
- MA (移動平均線) - 5/20/60日
- EMA (指數移動平均)
- MACD (指數平滑異同移動平均線)
- RSI (相對強弱指標)
- KDJ (隨機指標)
- Bollinger Bands (布林通道)
- ATR (真實波動幅度均值)
- OBV (能量潮指標)

**特色功能**:
- ✅ 自動計算所有技術指標
- ✅ K線圖與成交量視覺化
- ✅ 智能交易訊號生成（買入/持有/賣出）
- ✅ 詳細訊號說明與建議

### 2. 📊 多股比較模組

**檔案**: `backend/modules/stock_comparator.py` (400+ 行)

**核心功能**:
- 同時分析 2-10 支股票
- 價格走勢標準化比較
- 報酬率、波動率、夏普比率計算
- 視覺化對比圖表

**應用場景**:
- ✅ 選股：從候選股中挑選最優標的
- ✅ 配置：決定各股票投資比重
- ✅ 產業研究：比較同產業不同公司
- ✅ 對沖策略：找出負相關股票

### 3. 💼 投資組合管理模組

**檔案**: `backend/modules/portfolio_manager.py` (500+ 行)

**核心功能**:
- 持倉管理（新增/修改/刪除）
- 組合價值即時計算
- 績效分析（報酬率、夏普比率）
- 風險指標（波動率、最大回撤、VaR）
- 持倉分布視覺化
- 交易記錄追蹤

**實際應用**:
```
範例組合:
- 台積電 (2330): 1000股 @ 600元
- 鴻海 (2317): 2000股 @ 110元
- 聯發科 (2454): 500股 @ 850元

組合分析結果:
總成本: $1,245,000
當前市值: $1,370,000
總損益: +$125,000 (+10.0%)
夏普比率: 0.87
```

### 4. 🎭 市場情緒分析模組

**檔案**: `backend/modules/market_sentiment.py` (500+ 行)

**核心指標**:

1. **市場廣度**
   - 上漲/下跌家數統計
   - 漲跌比與成交量比
   - 市場情緒判斷（極度樂觀→極度悲觀）

2. **恐懼貪婪指數** (0-100)
   - 價格動能 (30%)
   - 市場廣度 (25%)
   - 波動率 (20%)
   - 成交量 (15%)
   - 新高新低 (10%)

3. **產業輪動**
   - 各產業表現排名
   - 領漲/落後產業識別
   - 資金流向分析

**指數解讀**:
- 0-25: 極度恐懼 😱 → 可能是買入機會
- 25-45: 恐懼 😨 → 可考慮分批進場
- 45-55: 中性 😐 → 保持觀望
- 55-75: 貪婪 😊 → 考慮獲利了結
- 75-100: 極度貪婪 🔥 → 注意風險

---

## 💡 使用範例

### 範例 1: 技術分析

```python
from backend.modules.technical_analyzer import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()

# 計算技術指標
df = analyzer.calculate_ma(df, periods=[5, 20, 60])
df = analyzer.calculate_rsi(df, period=14)
df = analyzer.calculate_macd(df)

# 生成交易訊號
signals = analyzer.generate_signals(df)
print(f"綜合訊號: {signals['綜合訊號']}")
# 輸出: 綜合訊號: 買入
```

### 範例 2: 多股比較

```python
from backend.modules.stock_comparator import StockComparator

comparator = StockComparator(data_fetcher)
result = comparator.compare_stocks(['2330', '2317', '2454'], days=90)

print(result['comparison_table'])
# 顯示比較表格：漲跌幅、波動率、夏普比率
```

### 範例 3: 投資組合

```python
from backend.modules.portfolio_manager import PortfolioManager

manager = PortfolioManager(data_fetcher)
manager.add_position('2330', shares=1000, cost_price=600)
manager.add_position('2317', shares=2000, cost_price=110)

portfolio_value = manager.get_portfolio_value()
print(f"報酬率: {portfolio_value['total_return']:.2f}%")
# 輸出: 報酬率: 10.00%
```

### 範例 4: 市場情緒

```python
from backend.modules.market_sentiment import MarketSentimentAnalyzer

analyzer = MarketSentimentAnalyzer(data_fetcher)
stock_ids = ['2330', '2317', '2454', '2881', '2882']

fear_greed = analyzer.calculate_fear_greed_index(stock_ids, days=30)
print(f"恐懼貪婪指數: {fear_greed['恐懼貪婪指數']}")
print(f"市場情緒: {fear_greed['情緒']}")
# 輸出: 恐懼貪婪指數: 68
#       市場情緒: 貪婪 😊
```

---

## 🏗️ 系統架構

```
stockIDE/
├── app.py                              # 主程式（Streamlit UI）
├── backend/
│   ├── modules/
│   │   ├── technical_analyzer.py       # ✨ 技術分析引擎 (NEW)
│   │   ├── stock_comparator.py         # ✨ 多股比較引擎 (NEW)
│   │   ├── portfolio_manager.py        # ✨ 投資組合管理 (NEW)
│   │   ├── market_sentiment.py         # ✨ 市場情緒分析 (NEW)
│   │   ├── data_fetcher.py             # 資料獲取
│   │   ├── warrant_analyzer.py         # 權證分析
│   │   ├── risk_predictor.py           # 風險預測
│   │   └── strategy_analyzer.py        # 策略分析
│   ├── utils/
│   │   ├── cache_manager.py            # 快取管理
│   │   └── logger.py                   # 日誌系統
│   └── config/
│       └── settings.py                 # 系統設定
├── 快速入門指南.md                      # ✨ 使用指南 (NEW)
├── 進階分析功能說明.md                  # ✨ 完整文檔 (NEW)
├── v2.0更新總結.md                      # ✨ 更新說明 (NEW)
├── requirements.txt
└── README.md
```

---

## 🔧 技術棧

### 後端
- **Python 3.11+** - 主要程式語言
- **Pandas** - 資料處理
- **NumPy** - 數值計算
- **SciPy** - 科學計算（統計分佈）

### 前端
- **Streamlit** - Web 應用框架
- **Plotly** - 互動式圖表

### 資料來源
- **Yahoo Finance** - 股價資料
- **FinMind** - 備用資料源（解決429錯誤）

---

## 🎯 使用場景

### 場景 1: 日內交易者
- 使用 **技術分析** 觀察 RSI、MACD
- 參考 **交易訊號** 進場出場

### 場景 2: 波段交易者
- 查看 **市場情緒** 判斷大環境
- 使用 **技術分析** 找出進場點
- MA 黃金交叉進場，死亡交叉出場

### 場景 3: 價值投資者
- 使用 **多股比較** 選股
- 建立 **投資組合** 追蹤績效
- 定期檢視並再平衡

### 場景 4: 市場研究者
- **市場情緒** 分析整體環境
- **產業輪動** 觀察資金流向
- **風險評估** 控管風險

---

## 📊 v2.0 統計數據

### 程式碼統計

| 模組 | 行數 | 類別數 | 函數數 |
|------|------|--------|--------|
| 技術分析 | 700+ | 1 | 15+ |
| 多股比較 | 400+ | 2 | 10+ |
| 投資組合 | 500+ | 2 | 12+ |
| 市場情緒 | 500+ | 1 | 12+ |
| 前端整合 | 420+ | 0 | 4 |
| **總計** | **2520+** | **6** | **53+** |

### 文件統計

| 文件名稱 | 字數 |
|---------|------|
| 進階分析功能說明.md | 8000+ |
| 快速入門指南.md | 4500+ |
| v2.0更新總結.md | 3500+ |
| **總計** | **16000+** |

---

## ⚠️ 免責聲明

**重要提示**:

1. **教育用途**: 本系統僅供教育和研究使用
2. **非投資建議**: 所有分析結果不構成投資建議
3. **風險自負**: 投資有風險，決策請謹慎
4. **專業諮詢**: 重大投資前請諮詢專業財務顧問
5. **示範資料**: 部分功能使用示範資料，實際投資前請查證
6. **資料延遲**: Yahoo Finance 資料有 15-20 分鐘延遲
7. **無保證**: 不保證系統準確性和穩定性

**使用本系統即表示您已了解並同意以上聲明。**

---

## 📈 版本歷史

### [v2.0] - 2026-01-10 (Advanced Analytics)

**新增**:
- ✅ 技術分析模組（700+ 行）
- ✅ 多股比較模組（400+ 行）
- ✅ 投資組合管理模組（500+ 行）
- ✅ 市場情緒分析模組（500+ 行）
- ✅ 完整文件（16000+ 字）

**改進**:
- ✨ 優化 UI 界面
- ✨ 提升計算效能
- ✨ 增強錯誤處理

### [v1.5] - 之前

**新增**:
- ✅ 權證查詢功能
- ✅ Black-Scholes 定價
- ✅ Greeks 計算

### [v1.0] - 最初

**新增**:
- ✅ 基本股票查詢
- ✅ K線圖顯示
- ✅ 風險評估
- ✅ 投資策略

---

## 📞 技術支援

### 遇到問題？

1. 檢查 [快速入門指南](快速入門指南.md) 的「常見問題」章節
2. 閱讀 [進階分析功能說明](進階分析功能說明.md)
3. 確認所有依賴套件已安裝

### 功能建議

歡迎提供功能建議和改進意見！

---

## 🎉 致謝

感謝所有使用和支持本專案的用戶！

特別感謝：
- **Streamlit** - 優秀的 Web 框架
- **Yahoo Finance** - 免費的股價 API
- **Plotly** - 互動式圖表工具

---

<div align="center">

**🚀 v2.0 - 開啟進階分析新時代！**

Made with ❤️ by Claude Sonnet 4.5

**系統版本**: v2.0 Professional | **更新日期**: 2026-01-10

[快速開始](快速入門指南.md) • [功能介紹](進階分析功能說明.md) • [更新總結](v2.0更新總結.md)

</div>

---

**注意**: 本系統僅供教育和研究用途，不構成投資建議。投資前請諮詢專業財務顧問。
