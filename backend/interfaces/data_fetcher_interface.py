"""
資料獲取介面

定義資料獲取器的抽象契約。
所有資料獲取實作必須遵循此介面。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import pandas as pd


class IStockDataFetcher(ABC):
    """
    股票資料獲取器介面

    定義獲取股票資料的標準方法。
    實作可以來自不同資料源（yfinance, twstock, API 等）。

    實作類別：
        - TaiwanStockDataFetcher (yfinance)
        - EnhancedTaiwanStockDataFetcher (yfinance + cache + retry)
        - TwstockDataFetcher (twstock 套件)
        - MockDataFetcher (測試用)
    """

    @abstractmethod
    def get_stock_price(self, stock_id: str, days: int = 90) -> pd.DataFrame:
        """
        獲取股票歷史價格

        Args:
            stock_id: 股票代碼 (例如: "2330")
            days: 查詢天數 (預設 90 天)

        Returns:
            包含價格資料的 DataFrame，欄位包含：
            - 日期 (index)
            - 開盤價
            - 最高價
            - 最低價
            - 收盤價
            - 成交量

        Raises:
            ValueError: 股票代碼無效
            ConnectionError: 網路連線失敗
            DataNotFoundError: 資料不存在
        """
        pass

    @abstractmethod
    def get_stock_info(self, stock_id: str) -> Dict:
        """
        獲取股票基本資訊

        Args:
            stock_id: 股票代碼

        Returns:
            包含基本資訊的字典：
            {
                "股票代碼": "2330",
                "公司名稱": "台積電",
                "產業": "半導體業",
                "市值": "10.5兆",
                "本益比": 25.3,
                ...
            }

        Raises:
            ValueError: 股票代碼無效
            DataNotFoundError: 資料不存在
        """
        pass

    @abstractmethod
    def get_realtime_price(self, stock_id: str) -> Dict:
        """
        獲取即時報價

        Args:
            stock_id: 股票代碼

        Returns:
            包含即時報價的字典：
            {
                "current_price": 580.0,
                "change": 5.0,
                "change_percent": 0.87,
                "volume": 25000,
                "time": "2024-01-10 13:30:00"
            }

        Raises:
            ValueError: 股票代碼無效
            MarketClosedError: 非交易時間
        """
        pass

    @abstractmethod
    def get_top_stocks(self, limit: int = 10) -> List[Dict]:
        """
        獲取熱門股票列表

        Args:
            limit: 返回數量限制

        Returns:
            熱門股票列表，每個元素為字典：
            [
                {
                    "code": "2330",
                    "name": "台積電",
                    "price": 580.0,
                    "change_percent": 0.87
                },
                ...
            ]
        """
        pass

    def is_market_open(self) -> bool:
        """
        檢查市場是否開盤

        Returns:
            True 表示市場開盤中，False 表示已收盤

        Note:
            此方法有預設實作，子類可選擇覆寫
        """
        from datetime import datetime
        now = datetime.now()
        # 簡化判斷：週一到週五 09:00-13:30
        is_weekday = now.weekday() < 5
        is_trading_hours = (9 <= now.hour < 13) or (now.hour == 13 and now.minute <= 30)
        return is_weekday and is_trading_hours


class IWarrantDataFetcher(ABC):
    """
    權證資料獲取器介面

    定義獲取權證資料的標準方法。
    """

    @abstractmethod
    def get_warrant_list(self, underlying_stock: str) -> List[Dict]:
        """
        獲取指定標的股票的權證列表

        Args:
            underlying_stock: 標的股票代碼

        Returns:
            權證列表，每個元素包含：
            {
                "warrant_code": "1234P",
                "warrant_name": "XX購01",
                "type": "認購" | "認售",
                "exercise_price": 600.0,
                "expiry_date": "2024-12-31",
                ...
            }
        """
        pass

    @abstractmethod
    def get_warrant_price(self, warrant_code: str, days: int = 30) -> pd.DataFrame:
        """
        獲取權證歷史價格

        Args:
            warrant_code: 權證代碼
            days: 查詢天數

        Returns:
            價格 DataFrame
        """
        pass

    @abstractmethod
    def get_warrant_greeks(self, warrant_code: str) -> Dict:
        """
        獲取權證 Greeks 值

        Args:
            warrant_code: 權證代碼

        Returns:
            Greeks 字典：
            {
                "delta": 0.6,
                "gamma": 0.05,
                "theta": -0.02,
                "vega": 0.15,
                "rho": 0.03
            }
        """
        pass
