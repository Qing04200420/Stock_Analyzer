"""
股票實體模型

定義股票和股價的核心業務對象。
遵循領域驅動設計原則，不依賴外部框架。
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


@dataclass(frozen=True)
class StockPrice:
    """
    股價實體 (不可變)

    代表某一時間點的股票價格資訊。
    使用 frozen=True 確保不可變性，提高資料一致性。

    Attributes:
        date: 交易日期
        open: 開盤價
        high: 最高價
        low: 最低價
        close: 收盤價
        volume: 成交量
        adjusted_close: 調整後收盤價 (考慮股利、股票分割等)
    """
    date: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    adjusted_close: Optional[Decimal] = None

    def __post_init__(self):
        """資料驗證"""
        if self.high < self.low:
            raise ValueError(f"最高價 ({self.high}) 不能低於最低價 ({self.low})")
        if self.open < 0 or self.close < 0:
            raise ValueError("價格不能為負數")
        if self.volume < 0:
            raise ValueError("成交量不能為負數")

    @property
    def price_range(self) -> Decimal:
        """價格波動範圍"""
        return self.high - self.low

    @property
    def change(self) -> Decimal:
        """單日漲跌幅"""
        return self.close - self.open

    @property
    def change_percent(self) -> float:
        """單日漲跌幅百分比"""
        if self.open == 0:
            return 0.0
        return float((self.change / self.open) * 100)


@dataclass
class Stock:
    """
    股票實體

    代表一支股票的基本資訊和屬性。

    Attributes:
        code: 股票代碼 (例如: "2330")
        name: 公司名稱 (例如: "台積電")
        industry: 所屬產業
        market: 上市市場 (上市/上櫃/興櫃)
        market_cap: 市值
        pe_ratio: 本益比
        pb_ratio: 股價淨值比
        dividend_yield: 殖利率
        price_history: 歷史價格資料
    """
    code: str
    name: str
    industry: str = ""
    market: str = "上市"
    market_cap: Optional[str] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    price_history: List[StockPrice] = field(default_factory=list)

    def __post_init__(self):
        """資料驗證"""
        if not self.code:
            raise ValueError("股票代碼不能為空")
        if not self.name:
            raise ValueError("公司名稱不能為空")
        if self.market not in ["上市", "上櫃", "興櫃"]:
            raise ValueError(f"市場類型無效: {self.market}")

    @property
    def display_name(self) -> str:
        """顯示用的名稱 (代碼 + 名稱)"""
        return f"{self.code} {self.name}"

    @property
    def latest_price(self) -> Optional[StockPrice]:
        """最新價格"""
        if self.price_history:
            return max(self.price_history, key=lambda p: p.date)
        return None

    def add_price(self, price: StockPrice) -> None:
        """
        添加歷史價格

        Args:
            price: 股價實體
        """
        # 避免重複日期
        if not any(p.date == price.date for p in self.price_history):
            self.price_history.append(price)
            # 保持按日期排序
            self.price_history.sort(key=lambda p: p.date)

    def get_price_on_date(self, date: datetime) -> Optional[StockPrice]:
        """
        獲取指定日期的價格

        Args:
            date: 目標日期

        Returns:
            該日期的股價，若不存在則返回 None
        """
        for price in self.price_history:
            if price.date.date() == date.date():
                return price
        return None

    def calculate_return(self, start_date: datetime, end_date: datetime) -> Optional[float]:
        """
        計算區間報酬率

        Args:
            start_date: 起始日期
            end_date: 結束日期

        Returns:
            報酬率百分比，若資料不足則返回 None
        """
        start_price = self.get_price_on_date(start_date)
        end_price = self.get_price_on_date(end_date)

        if start_price and end_price and start_price.close > 0:
            return float((end_price.close - start_price.close) / start_price.close * 100)
        return None
