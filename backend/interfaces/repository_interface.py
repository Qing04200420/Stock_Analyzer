"""
倉儲介面定義

此模組定義資料倉儲層的抽象介面，遵循 Repository Pattern。
倉儲層負責封裝資料存取邏輯，提供領域層與基礎設施層之間的抽象。

設計原則：
1. 介面隔離原則（ISP）- 每個倉儲介面只負責特定實體
2. 依賴反轉原則（DIP）- 業務邏輯依賴抽象而非具體實作
3. 單一職責原則（SRP）- 每個倉儲只負責一種實體的 CRUD 操作
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime

from backend.domain.entities.stock import Stock, StockPrice
from backend.domain.entities.analysis import RiskAnalysis, StrategyAnalysis


class IStockRepository(ABC):
    """
    股票資料倉儲介面

    定義股票相關資料的 CRUD 操作抽象方法。
    實作類別可以使用資料庫、檔案系統、外部 API 或快取等任何資料來源。
    """

    @abstractmethod
    def get_by_code(self, stock_code: str) -> Optional[Stock]:
        """
        根據股票代碼獲取股票實體

        Args:
            stock_code: 股票代碼（如 "2330"）

        Returns:
            Optional[Stock]: 股票實體，若不存在則返回 None

        Raises:
            RepositoryError: 資料存取錯誤
        """
        pass

    @abstractmethod
    def get_price_history(
        self,
        stock_code: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[StockPrice]:
        """
        獲取指定期間的歷史價格資料

        Args:
            stock_code: 股票代碼
            start_date: 起始日期
            end_date: 結束日期

        Returns:
            List[StockPrice]: 價格序列（按日期排序）

        Raises:
            ValueError: 日期範圍無效
            RepositoryError: 資料存取錯誤
        """
        pass

    @abstractmethod
    def get_latest_price(self, stock_code: str) -> Optional[StockPrice]:
        """
        獲取最新價格

        Args:
            stock_code: 股票代碼

        Returns:
            Optional[StockPrice]: 最新價格，若無資料則返回 None
        """
        pass

    @abstractmethod
    def save(self, stock: Stock) -> None:
        """
        儲存或更新股票資料

        Args:
            stock: 股票實體

        Raises:
            ValidationError: 資料驗證失敗
            RepositoryError: 儲存失敗
        """
        pass

    @abstractmethod
    def save_price_history(self, stock_code: str, prices: List[StockPrice]) -> None:
        """
        批次儲存歷史價格資料

        Args:
            stock_code: 股票代碼
            prices: 價格序列

        Raises:
            ValidationError: 資料驗證失敗
            RepositoryError: 儲存失敗
        """
        pass

    @abstractmethod
    def delete(self, stock_code: str) -> bool:
        """
        刪除股票資料

        Args:
            stock_code: 股票代碼

        Returns:
            bool: 是否成功刪除

        Raises:
            RepositoryError: 刪除失敗
        """
        pass

    @abstractmethod
    def exists(self, stock_code: str) -> bool:
        """
        檢查股票是否存在

        Args:
            stock_code: 股票代碼

        Returns:
            bool: 是否存在
        """
        pass

    @abstractmethod
    def get_all_codes(self) -> List[str]:
        """
        獲取所有股票代碼

        Returns:
            List[str]: 股票代碼列表

        Raises:
            RepositoryError: 資料存取錯誤
        """
        pass

    @abstractmethod
    def search(self, criteria: Dict) -> List[Stock]:
        """
        根據條件搜尋股票

        Args:
            criteria: 搜尋條件字典，可包含：
                - name: 股票名稱（部分匹配）
                - industry: 產業類別
                - market: 市場別（上市/上櫃）
                - min_price: 最低價格
                - max_price: 最高價格

        Returns:
            List[Stock]: 符合條件的股票列表

        Raises:
            RepositoryError: 資料存取錯誤
        """
        pass

    @abstractmethod
    def get_by_industry(self, industry: str) -> List[Stock]:
        """
        獲取特定產業的所有股票

        Args:
            industry: 產業名稱

        Returns:
            List[Stock]: 該產業的股票列表
        """
        pass

    @abstractmethod
    def get_top_volume(self, limit: int = 10, date: Optional[datetime] = None) -> List[Stock]:
        """
        獲取成交量最大的股票

        Args:
            limit: 返回數量（預設 10）
            date: 指定日期（預設為最新交易日）

        Returns:
            List[Stock]: 依成交量排序的股票列表
        """
        pass


class IWarrantRepository(ABC):
    """
    權證資料倉儲介面

    定義權證相關資料的 CRUD 操作抽象方法。
    """

    @abstractmethod
    def get_by_code(self, warrant_code: str) -> Optional[Dict]:
        """
        根據權證代碼獲取權證資訊

        Args:
            warrant_code: 權證代碼

        Returns:
            Optional[Dict]: 權證資訊字典，若不存在則返回 None
        """
        pass

    @abstractmethod
    def get_by_underlying(self, stock_code: str) -> List[Dict]:
        """
        獲取特定標的股票的所有權證

        Args:
            stock_code: 標的股票代碼

        Returns:
            List[Dict]: 權證列表
        """
        pass

    @abstractmethod
    def get_price_history(
        self,
        warrant_code: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        獲取權證歷史價格

        Args:
            warrant_code: 權證代碼
            start_date: 起始日期
            end_date: 結束日期

        Returns:
            List[Dict]: 價格資料列表
        """
        pass

    @abstractmethod
    def save(self, warrant_data: Dict) -> None:
        """
        儲存或更新權證資料

        Args:
            warrant_data: 權證資料字典

        Raises:
            ValidationError: 資料驗證失敗
            RepositoryError: 儲存失敗
        """
        pass

    @abstractmethod
    def delete(self, warrant_code: str) -> bool:
        """
        刪除權證資料

        Args:
            warrant_code: 權證代碼

        Returns:
            bool: 是否成功刪除
        """
        pass

    @abstractmethod
    def search(self, criteria: Dict) -> List[Dict]:
        """
        根據條件搜尋權證

        Args:
            criteria: 搜尋條件字典，可包含：
                - underlying_stock: 標的股票代碼
                - option_type: 選擇權類型（"call" 或 "put"）
                - min_days_to_maturity: 最短到期日
                - max_days_to_maturity: 最長到期日
                - min_delta: 最小 Delta
                - max_delta: 最大 Delta
                - issuer: 發行券商

        Returns:
            List[Dict]: 符合條件的權證列表
        """
        pass

    @abstractmethod
    def get_active_warrants(self, underlying_stock: str) -> List[Dict]:
        """
        獲取尚未到期的權證

        Args:
            underlying_stock: 標的股票代碼

        Returns:
            List[Dict]: 有效權證列表（未到期）
        """
        pass

    @abstractmethod
    def get_warrant_greeks(self, warrant_code: str) -> Optional[Dict]:
        """
        獲取權證的 Greeks 值

        Args:
            warrant_code: 權證代碼

        Returns:
            Optional[Dict]: Greeks 值字典（Delta, Gamma, Vega, Theta, Rho）
        """
        pass


class IAnalysisRepository(ABC):
    """
    分析結果倉儲介面

    定義分析結果的儲存和檢索抽象方法。
    用於快取分析結果，避免重複計算。
    """

    @abstractmethod
    def save_risk_analysis(self, analysis: RiskAnalysis) -> None:
        """
        儲存風險分析結果

        Args:
            analysis: 風險分析實體

        Raises:
            RepositoryError: 儲存失敗
        """
        pass

    @abstractmethod
    def get_risk_analysis(
        self,
        stock_code: str,
        analysis_date: Optional[datetime] = None
    ) -> Optional[RiskAnalysis]:
        """
        獲取風險分析結果

        Args:
            stock_code: 股票代碼
            analysis_date: 分析日期（預設為最新）

        Returns:
            Optional[RiskAnalysis]: 風險分析結果，若不存在則返回 None
        """
        pass

    @abstractmethod
    def save_strategy_analysis(self, analysis: StrategyAnalysis) -> None:
        """
        儲存策略分析結果

        Args:
            analysis: 策略分析實體

        Raises:
            RepositoryError: 儲存失敗
        """
        pass

    @abstractmethod
    def get_strategy_analysis(
        self,
        stock_code: str,
        analysis_date: Optional[datetime] = None
    ) -> Optional[StrategyAnalysis]:
        """
        獲取策略分析結果

        Args:
            stock_code: 股票代碼
            analysis_date: 分析日期（預設為最新）

        Returns:
            Optional[StrategyAnalysis]: 策略分析結果，若不存在則返回 None
        """
        pass

    @abstractmethod
    def get_analysis_history(
        self,
        stock_code: str,
        start_date: datetime,
        end_date: datetime,
        analysis_type: str
    ) -> List[Dict]:
        """
        獲取歷史分析記錄

        Args:
            stock_code: 股票代碼
            start_date: 起始日期
            end_date: 結束日期
            analysis_type: 分析類型（"risk" 或 "strategy"）

        Returns:
            List[Dict]: 分析記錄列表
        """
        pass

    @abstractmethod
    def delete_old_analysis(self, days_old: int = 30) -> int:
        """
        刪除舊的分析記錄

        Args:
            days_old: 保留天數（預設 30 天）

        Returns:
            int: 刪除的記錄數量
        """
        pass

    @abstractmethod
    def clear_cache(self, stock_code: Optional[str] = None) -> None:
        """
        清除快取的分析結果

        Args:
            stock_code: 股票代碼（若為 None 則清除所有）
        """
        pass


class ICacheRepository(ABC):
    """
    快取倉儲介面

    定義通用快取操作的抽象方法。
    可用於實作記憶體快取、Redis 快取或其他快取機制。
    """

    @abstractmethod
    def get(self, key: str) -> Optional[any]:
        """
        從快取獲取資料

        Args:
            key: 快取鍵

        Returns:
            Optional[any]: 快取的資料，若不存在或已過期則返回 None
        """
        pass

    @abstractmethod
    def set(self, key: str, value: any, ttl: Optional[int] = None) -> None:
        """
        設定快取資料

        Args:
            key: 快取鍵
            value: 要快取的資料
            ttl: 存活時間（秒），若為 None 則使用預設值

        Raises:
            CacheError: 快取設定失敗
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        刪除快取資料

        Args:
            key: 快取鍵

        Returns:
            bool: 是否成功刪除
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        檢查快取是否存在且有效

        Args:
            key: 快取鍵

        Returns:
            bool: 是否存在
        """
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """
        清除所有快取
        """
        pass

    @abstractmethod
    def clear_pattern(self, pattern: str) -> int:
        """
        清除符合模式的快取

        Args:
            pattern: 鍵值模式（如 "stock:*"）

        Returns:
            int: 清除的數量
        """
        pass

    @abstractmethod
    def get_stats(self) -> Dict:
        """
        獲取快取統計資訊

        Returns:
            Dict: 包含命中率、快取數量等資訊
        """
        pass

    @abstractmethod
    def cleanup_expired(self) -> int:
        """
        清理過期的快取項目

        Returns:
            int: 清理的數量
        """
        pass
