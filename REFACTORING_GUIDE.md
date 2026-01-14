# 🏗️ 程式碼重構實施指南

## 專業級重構 v1.0

**目標**: 將系統優化為高可讀性、高維護性、可擴充、有彈性的專業級架構

**日期**: 2026-01-10

---

## 📊 重構前後對比

### 當前架構問題

| 問題類型 | 嚴重程度 | 影響 |
|---------|---------|------|
| 巨大單體檔案 (app.py 2319 行) | 🔴 嚴重 | 難以維護、測試、協作 |
| 6 個重複的 data_fetcher 版本 | 🔴 嚴重 | 技術債務、混亂 |
| UI 與業務邏輯緊耦合 | 🔴 嚴重 | 無法獨立測試 |
| 缺乏介面抽象 | 🟡 中度 | 難以擴充、替換 |
| 重複程式碼過多 | 🟡 中度 | 維護成本高 |
| 錯誤處理不一致 | 🟡 中度 | 穩定性問題 |

### 重構後目標

| 指標 | 目標值 | 說明 |
|-----|-------|------|
| 單檔案行數 | < 300 行 | 每個檔案職責單一 |
| 程式碼重複率 | < 5% | DRY 原則 |
| 測試覆蓋率 | > 80% | 關鍵邏輯有測試 |
| 循環複雜度 | < 10 | 函數簡單易懂 |
| 耦合度 | 低 | 模組獨立 |
| 內聚度 | 高 | 相關邏輯集中 |

---

## 🎯 重構原則 (SOLID)

### 1. Single Responsibility Principle (單一職責原則)

**原則**: 一個類別只負責一個功能

**實踐**:
- ❌ 舊: `app.py` 包含 UI、業務邏輯、資料處理
- ✅ 新: 拆分為 Pages (UI)、Services (業務)、Repositories (資料)

### 2. Open/Closed Principle (開放封閉原則)

**原則**: 對擴充開放，對修改封閉

**實踐**:
- ❌ 舊: 要新增資料來源需修改 data_fetcher
- ✅ 新: 實作 `IStockDataFetcher` 介面即可新增

### 3. Liskov Substitution Principle (里氏替換原則)

**原則**: 子類別可以替換父類別

**實踐**:
- ✅ 所有實作 `IStockDataFetcher` 的類別可互換使用

### 4. Interface Segregation Principle (介面隔離原則)

**原則**: 不應強迫實作不需要的方法

**實踐**:
- ✅ 分離 `IStockDataFetcher` 和 `IWarrantDataFetcher`
- ✅ 各介面只包含必要方法

### 5. Dependency Inversion Principle (依賴反轉原則)

**原則**: 依賴抽象而非具體實作

**實踐**:
- ❌ 舊: `StockService` 直接 new `TaiwanStockDataFetcher()`
- ✅ 新: `StockService(data_fetcher: IStockDataFetcher)`

---

## 📁 新架構設計

### 目錄結構

```
d:\stockIDE\
├── frontend/                    # 前端層 (UI)
│   ├── app.py                   # 主入口 (< 100 行)
│   ├── pages/                   # 頁面模組
│   │   ├── __init__.py
│   │   ├── home_page.py
│   │   ├── stock_analysis_page.py
│   │   ├── risk_assessment_page.py
│   │   ├── strategy_page.py
│   │   ├── warrant_page.py
│   │   └── settings_page.py
│   ├── components/              # UI 元件
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   ├── cards.py
│   │   ├── tables.py
│   │   └── forms.py
│   ├── state/                   # 狀態管理
│   │   ├── __init__.py
│   │   ├── session_manager.py
│   │   └── app_context.py
│   └── styles/                  # 樣式
│       ├── __init__.py
│       └── theme.py
│
├── backend/                     # 後端層
│   ├── domain/                  # 領域層 (核心業務對象) ✨ 新增
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── stock.py         # Stock, StockPrice 實體
│   │   │   └── analysis.py      # RiskAnalysis, StrategyAnalysis
│   │   └── value_objects/
│   │       ├── __init__.py
│   │       └── technical_indicator.py
│   │
│   ├── interfaces/              # 介面層 (抽象契約) ✨ 新增
│   │   ├── __init__.py
│   │   ├── data_fetcher_interface.py
│   │   ├── analyzer_interface.py
│   │   └── repository_interface.py
│   │
│   ├── services/                # 服務層 (業務邏輯) ✨ 新增
│   │   ├── __init__.py
│   │   ├── stock_service.py
│   │   ├── risk_service.py
│   │   ├── strategy_service.py
│   │   ├── warrant_service.py
│   │   └── data_fetcher_factory.py
│   │
│   ├── repositories/            # 倉儲層 (資料存取) ✨ 新增
│   │   ├── __init__.py
│   │   ├── stock_repository.py
│   │   ├── warrant_repository.py
│   │   └── cache_repository.py
│   │
│   ├── modules/                 # 原有模組 (重構)
│   │   ├── data_fetcher.py      # 保留並實作介面
│   │   ├── data_fetcher_enhanced.py  # 保留
│   │   ├── risk_predictor.py    # 重構為 service
│   │   ├── strategy_analyzer.py # 重構為 service
│   │   └── warrant_analyzer.py  # 重構為 service
│   │
│   ├── utils/                   # 工具層 (增強)
│   │   ├── cache_manager.py     # 已有
│   │   ├── logger.py            # 已有
│   │   ├── validators.py        # ✨ 新增
│   │   ├── formatters.py        # ✨ 新增
│   │   ├── decorators.py        # ✨ 新增
│   │   └── exceptions.py        # ✨ 新增
│   │
│   └── config/
│       └── settings.py          # 已有
│
├── tests/                       # 測試 ✨ 新增
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_domain_models.py
│   │   ├── test_services.py
│   │   ├── test_repositories.py
│   │   └── test_analyzers.py
│   ├── integration/
│   │   ├── test_data_fetcher.py
│   │   └── test_end_to_end.py
│   └── fixtures/
│       ├── mock_data.py
│       └── test_config.py
│
└── docs/                        # 文檔
    ├── SYSTEM_UPGRADE_SUMMARY.md
    ├── REFACTORING_GUIDE.md (本文件)
    └── API.md                   # ✨ 新增
```

---

## 🚀 實施階段

### Phase 1: 基礎架構建立 (已完成 ✅)

**目標**: 建立核心抽象層

**完成項目**:
- ✅ 建立 `backend/domain/` 領域模型
  - `entities/stock.py` - Stock, StockPrice 實體
  - `entities/analysis.py` - RiskAnalysis, StrategyAnalysis 實體
- ✅ 建立 `backend/interfaces/` 介面層
  - `data_fetcher_interface.py` - IStockDataFetcher, IWarrantDataFetcher
  - `analyzer_interface.py` - 分析器介面 (待實作)
  - `repository_interface.py` - 倉儲介面 (待實作)

**成果**:
```python
# 現在可以這樣使用：
from backend.domain.entities import Stock, StockPrice, RiskAnalysis
from backend.interfaces import IStockDataFetcher

# 領域模型
stock = Stock(code="2330", name="台積電", industry="半導體業")
price = StockPrice(
    date=datetime.now(),
    open=Decimal("580.0"),
    high=Decimal("585.0"),
    low=Decimal("578.0"),
    close=Decimal("582.0"),
    volume=25000
)

# 介面抽象
class MyDataFetcher(IStockDataFetcher):
    def get_stock_price(self, stock_id: str, days: int):
        # 自訂實作...
```

### Phase 2: 拆分巨大檔案 (進行中 🔄)

**目標**: 將 app.py (2319 行) 拆分為多個小檔案

**步驟**:
1. ✅ 建立 `frontend/` 目錄結構
2. ⏳ 提取頁面函數到 `frontend/pages/`
3. ⏳ 提取 UI 元件到 `frontend/components/`
4. ⏳ 提取 CSS 到 `frontend/styles/theme.py`
5. ⏳ 重寫 `app.py` 為簡潔路由 (< 100 行)

**預期成果**:
- `frontend/app.py`: 100 行 (主入口 + 路由)
- 每個頁面檔案: 200-300 行
- 每個元件檔案: 50-150 行

### Phase 3: 清理重複檔案 (待執行 ⏳)

**目標**: 解決 data_fetcher 版本混亂問題

**行動**:
1. 保留:
   - `data_fetcher.py` (基礎版本)
   - `data_fetcher_enhanced.py` (增強版本)

2. 刪除 (6 → 2):
   - ❌ `data_fetcher_original.py`
   - ❌ `data_fetcher_fixed.py`
   - ❌ `data_fetcher_v2.py`
   - ❌ `data_fetcher_smart.py`

3. 建立工廠模式:
   ```python
   # backend/services/data_fetcher_factory.py
   class DataFetcherFactory:
       @staticmethod
       def create(source_type: str) -> IStockDataFetcher:
           if source_type == "basic":
               return TaiwanStockDataFetcher()
           elif source_type == "enhanced":
               return EnhancedTaiwanStockDataFetcher()
           else:
               raise ValueError(f"Unknown source: {source_type}")
   ```

### Phase 4: 建立服務層 (待執行 ⏳)

**目標**: 封裝業務邏輯，解耦 UI 和資料層

**實作**:
```python
# backend/services/stock_service.py
class StockService:
    def __init__(
        self,
        data_fetcher: IStockDataFetcher,
        risk_analyzer: IRiskAnalyzer,
        cache_repo: ICacheRepository
    ):
        self.data_fetcher = data_fetcher
        self.risk_analyzer = risk_analyzer
        self.cache_repo = cache_repo

    def analyze_stock(self, stock_id: str, days: int) -> Dict:
        """完整股票分析流程"""
        # 1. 獲取資料
        prices = self.data_fetcher.get_stock_price(stock_id, days)
        info = self.data_fetcher.get_stock_info(stock_id)

        # 2. 風險分析
        risk = self.risk_analyzer.analyze(prices)

        # 3. 快取結果
        self.cache_repo.set(f"analysis_{stock_id}", result, ttl=300)

        return {
            'info': info,
            'prices': prices,
            'risk': risk
        }
```

### Phase 5: 實作倉儲模式 (待執行 ⏳)

**目標**: 統一資料存取，支援多種資料來源

**實作**:
```python
# backend/repositories/stock_repository.py
class StockRepository(IStockRepository):
    def __init__(self, data_fetcher: IStockDataFetcher):
        self.data_fetcher = data_fetcher
        self.cache = cache_manager

    def get_by_id(self, stock_id: str) -> Stock:
        # 先檢查快取
        cached = self.cache.get(f"stock_{stock_id}")
        if cached:
            return cached

        # 從資料來源獲取
        data = self.data_fetcher.get_stock_info(stock_id)
        stock = self._map_to_entity(data)

        # 存入快取
        self.cache.set(f"stock_{stock_id}", stock, ttl=3600)

        return stock
```

### Phase 6: UI 元件化 (待執行 ⏳)

**目標**: 可重用的 UI 元件

**實作**:
```python
# frontend/components/charts.py
def plot_candlestick(df: pd.DataFrame, title: str = "股價走勢"):
    """K線圖元件 - 可在任何頁面重用"""
    fig = go.Figure(data=[go.Candlestick(...)])
    fig.update_layout(title=title, ...)
    st.plotly_chart(fig, use_container_width=True)

def plot_technical_indicators(df: pd.DataFrame, indicators: List[str]):
    """技術指標圖元件"""
    # ...
```

---

## 🎓 設計模式應用

### 1. Repository Pattern (倉儲模式)

**問題**: 資料存取邏輯散布各處，難以測試和切換資料來源

**解決方案**:
```python
# 定義介面
class IStockRepository(ABC):
    @abstractmethod
    def get_by_id(self, stock_id: str) -> Stock:
        pass

# 實作
class StockRepository(IStockRepository):
    def __init__(self, data_fetcher: IStockDataFetcher):
        self.data_fetcher = data_fetcher

    def get_by_id(self, stock_id: str) -> Stock:
        # 統一處理：快取、錯誤處理、資料映射
        ...

# 使用
stock = stock_repository.get_by_id("2330")
```

**優點**:
- ✅ 統一資料存取介面
- ✅ 易於切換資料來源
- ✅ 便於測試 (使用 MockRepository)
- ✅ 集中處理快取和錯誤

### 2. Factory Pattern (工廠模式)

**問題**: 多個 data_fetcher 版本，不知道該用哪個

**解決方案**:
```python
class DataFetcherFactory:
    @staticmethod
    def create(config: Dict) -> IStockDataFetcher:
        source_type = config.get('data_source', 'enhanced')

        if source_type == 'basic':
            return TaiwanStockDataFetcher()
        elif source_type == 'enhanced':
            return EnhancedTaiwanStockDataFetcher()
        elif source_type == 'mock':
            return MockDataFetcher()
        else:
            raise ValueError(f"Unknown source: {source_type}")

# 使用
data_fetcher = DataFetcherFactory.create(system_settings.get_config())
```

**優點**:
- ✅ 集中創建邏輯
- ✅ 易於新增新類型
- ✅ 配置驅動

### 3. Strategy Pattern (策略模式)

**問題**: 多種交易策略，難以動態切換

**解決方案**:
```python
# 定義策略介面
class ITradingStrategy(ABC):
    @abstractmethod
    def analyze(self, prices: pd.DataFrame) -> StrategySignal:
        pass

# 實作不同策略
class MAStrategy(ITradingStrategy):
    def analyze(self, prices: pd.DataFrame) -> StrategySignal:
        # MA 交叉策略
        ...

class RSIStrategy(ITradingStrategy):
    def analyze(self, prices: pd.DataFrame) -> StrategySignal:
        # RSI 超買超賣策略
        ...

# 策略管理器
class StrategyManager:
    def __init__(self):
        self.strategies: List[ITradingStrategy] = []

    def add_strategy(self, strategy: ITradingStrategy):
        self.strategies.append(strategy)

    def execute_all(self, prices: pd.DataFrame) -> StrategyAnalysis:
        signals = [s.analyze(prices) for s in self.strategies]
        return self._aggregate_signals(signals)
```

**優點**:
- ✅ 易於新增策略
- ✅ 策略可動態組合
- ✅ 符合開放封閉原則

### 4. Dependency Injection (依賴注入)

**問題**: 類別之間緊耦合，難以測試

**解決方案**:
```python
# ❌ 舊方式：緊耦合
class StockService:
    def __init__(self):
        self.data_fetcher = TaiwanStockDataFetcher()  # 緊耦合
        self.risk_analyzer = RiskPredictor()

# ✅ 新方式：依賴注入
class StockService:
    def __init__(
        self,
        data_fetcher: IStockDataFetcher,  # 依賴抽象
        risk_analyzer: IRiskAnalyzer
    ):
        self.data_fetcher = data_fetcher
        self.risk_analyzer = risk_analyzer

# 使用時注入依賴
service = StockService(
    data_fetcher=EnhancedTaiwanStockDataFetcher(),
    risk_analyzer=RiskService()
)

# 測試時注入 Mock
service = StockService(
    data_fetcher=MockDataFetcher(),
    risk_analyzer=MockRiskAnalyzer()
)
```

**優點**:
- ✅ 低耦合
- ✅ 易於測試
- ✅ 易於替換實作
- ✅ 符合依賴反轉原則

---

## 📝 程式碼品質標準

### 命名規範

```python
# 類別：PascalCase
class StockService:
    pass

# 函數/方法：snake_case
def get_stock_price():
    pass

# 常數：UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3

# 私有方法：前綴 _
def _internal_method():
    pass

# 介面：前綴 I
class IStockDataFetcher(ABC):
    pass
```

### 文檔字串

```python
def get_stock_price(stock_id: str, days: int = 90) -> pd.DataFrame:
    """
    獲取股票歷史價格

    詳細說明函數用途、參數和返回值。

    Args:
        stock_id: 股票代碼，例如 "2330"
        days: 查詢天數，預設 90 天

    Returns:
        包含歷史價格的 DataFrame

    Raises:
        ValueError: 當股票代碼無效時
        ConnectionError: 當網路連線失敗時

    Example:
        >>> df = get_stock_price("2330", 30)
        >>> print(df.head())
    """
    pass
```

### 型別提示 (Type Hints)

```python
from typing import List, Dict, Optional, Union

def analyze_stocks(
    stock_ids: List[str],
    days: int,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Union[Stock, RiskAnalysis]]:
    """使用完整的型別提示"""
    pass
```

### 錯誤處理

```python
# ❌ 不好的做法
try:
    data = fetch_data()
except:  # 捕捉所有例外
    pass  # 靜默失敗

# ✅ 好的做法
try:
    data = fetch_data()
except ConnectionError as e:
    logger.error(f"網路連線失敗: {e}")
    raise DataFetchError("無法獲取股票資料") from e
except ValueError as e:
    logger.warning(f"股票代碼無效: {e}")
    return None
```

---

## 🧪 測試策略

### 單元測試

```python
# tests/unit/test_domain_models.py
import pytest
from backend.domain.entities import Stock, StockPrice
from decimal import Decimal
from datetime import datetime

class TestStockPrice:
    def test_price_range_calculation(self):
        """測試價格波動範圍計算"""
        price = StockPrice(
            date=datetime.now(),
            open=Decimal("100"),
            high=Decimal("105"),
            low=Decimal("98"),
            close=Decimal("102"),
            volume=1000
        )

        assert price.price_range == Decimal("7")

    def test_invalid_high_low(self):
        """測試價格驗證：最高價不能低於最低價"""
        with pytest.raises(ValueError):
            StockPrice(
                date=datetime.now(),
                open=Decimal("100"),
                high=Decimal("95"),  # 錯誤：低於最低價
                low=Decimal("98"),
                close=Decimal("97"),
                volume=1000
            )
```

### 整合測試

```python
# tests/integration/test_stock_service.py
def test_stock_analysis_flow():
    """測試完整的股票分析流程"""
    # Arrange
    mock_fetcher = MockDataFetcher()
    service = StockService(data_fetcher=mock_fetcher)

    # Act
    result = service.analyze_stock("2330", 90)

    # Assert
    assert result['stock'].code == "2330"
    assert len(result['prices']) > 0
    assert result['risk'] is not None
```

---

## 🚀 實施時間表

| 階段 | 預計時間 | 優先級 | 狀態 |
|-----|---------|--------|------|
| Phase 1: 基礎架構 | 1 天 | 🔴 高 | ✅ 完成 |
| Phase 2: 拆分 app.py | 2 天 | 🔴 高 | 🔄 進行中 |
| Phase 3: 清理重複檔案 | 0.5 天 | 🔴 高 | ⏳ 待執行 |
| Phase 4: 服務層 | 1.5 天 | 🟡 中 | ⏳ 待執行 |
| Phase 5: 倉儲層 | 1 天 | 🟡 中 | ⏳ 待執行 |
| Phase 6: UI 元件化 | 1 天 | 🟡 中 | ⏳ 待執行 |
| 測試建立 | 2 天 | 🟢 低 | ⏳ 待執行 |
| 文檔完善 | 1 天 | 🟢 低 | ⏳ 待執行 |

**總計**: 約 10 工作天

---

## 💡 最佳實踐

### 1. 小步快跑

- 每次重構保持小範圍
- 確保每一步都能運行
- 頻繁提交 (每完成一個小模組就 commit)

### 2. 測試保護網

- 重構前先寫關鍵測試
- 重構後確保測試通過
- 新增功能同時寫測試

### 3. 漸進遷移

- 新舊程式碼可並存
- 逐步遷移功能
- 保持系統可用

### 4. 文檔同步

- 程式碼修改同時更新文檔
- 保持 API 文檔最新
- 記錄設計決策

---

## 🎯 成功指標

### 技術指標

- [ ] 單檔案行數 < 300 行
- [ ] 函數複雜度 < 10
- [ ] 程式碼重複率 < 5%
- [ ] 測試覆蓋率 > 80%
- [ ] 型別提示覆蓋率 > 90%

### 品質指標

- [ ] 所有公開 API 有文檔
- [ ] 關鍵業務邏輯有單元測試
- [ ] 無循環依賴
- [ ] 遵循 SOLID 原則
- [ ] 通過 pylint 檢查 (> 9.0/10)

### 維護性指標

- [ ] 新功能可在 1 天內完成
- [ ] Bug 修復時間 < 2 小時
- [ ] 新人上手時間 < 3 天
- [ ] 程式碼 review 通過率 > 95%

---

## 📚 參考資源

### 設計模式

- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
- [Python Design Patterns](https://python-patterns.guide/)

### 程式碼品質

- [PEP 8 - Python Style Guide](https://peps.python.org/pep-0008/)
- [Clean Code in Python](https://github.com/zedr/clean-code-python)
- [The Twelve-Factor App](https://12factor.net/)

### 測試

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

## 🤝 貢獻指南

### 重構步驟

1. **建立分支**
   ```bash
   git checkout -b refactor/phase-2-split-app
   ```

2. **實施重構**
   - 遵循本文件的設計原則
   - 保持小步快跑
   - 確保測試通過

3. **提交變更**
   ```bash
   git add .
   git commit -m "refactor: 拆分 app.py 為多個頁面檔案"
   ```

4. **Code Review**
   - 確保符合程式碼標準
   - 檢查測試覆蓋率
   - 驗證文檔完整性

5. **合併主分支**
   ```bash
   git checkout main
   git merge refactor/phase-2-split-app
   ```

---

**重構是持續的過程，保持程式碼整潔是每位開發者的責任！** 🌟
