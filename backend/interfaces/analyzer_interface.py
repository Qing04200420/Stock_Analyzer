"""
分析器介面定義

此模組定義所有分析器的抽象介面，包括風險分析、策略分析和權證分析。
遵循介面隔離原則（ISP），每個介面只包含相關的方法。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

from backend.domain.entities.stock import Stock, StockPrice
from backend.domain.entities.analysis import (
    RiskAnalysis,
    StrategyAnalysis,
    TechnicalIndicators,
    SignalType,
    StrategySignal
)


class IRiskAnalyzer(ABC):
    """
    風險分析器介面

    定義風險評估相關的抽象方法，包括波動率、VaR、Beta、Sharpe Ratio 等指標計算。
    實作類別必須實現所有抽象方法。
    """

    @abstractmethod
    def analyze_risk(self, stock: Stock, market_data: Optional[pd.DataFrame] = None) -> RiskAnalysis:
        """
        執行完整的風險分析

        Args:
            stock: 股票實體，包含歷史價格資料
            market_data: 市場指數資料（用於計算 Beta），可選

        Returns:
            RiskAnalysis: 完整的風險分析結果

        Raises:
            ValueError: 資料不足或參數無效
            CalculationError: 計算過程發生錯誤
        """
        pass

    @abstractmethod
    def calculate_volatility(self, prices: List[StockPrice], window: int = 20) -> float:
        """
        計算歷史波動率（標準差）

        Args:
            prices: 價格序列
            window: 計算視窗期間（預設 20 天）

        Returns:
            float: 年化波動率（百分比）
        """
        pass

    @abstractmethod
    def calculate_var(
        self,
        prices: List[StockPrice],
        confidence_level: float = 0.95,
        holding_period: int = 1
    ) -> float:
        """
        計算 Value at Risk (VaR)

        Args:
            prices: 價格序列
            confidence_level: 信賴水準（0.95 或 0.99）
            holding_period: 持有期間（天數）

        Returns:
            float: VaR 值（百分比）
        """
        pass

    @abstractmethod
    def calculate_beta(
        self,
        stock_prices: List[StockPrice],
        market_prices: pd.DataFrame,
        period: int = 252
    ) -> float:
        """
        計算 Beta 係數（相對於市場的系統性風險）

        Args:
            stock_prices: 個股價格序列
            market_prices: 市場指數價格
            period: 計算期間（預設 252 個交易日）

        Returns:
            float: Beta 係數
        """
        pass

    @abstractmethod
    def calculate_sharpe_ratio(
        self,
        prices: List[StockPrice],
        risk_free_rate: float = 0.01
    ) -> float:
        """
        計算 Sharpe Ratio（風險調整後報酬）

        Args:
            prices: 價格序列
            risk_free_rate: 無風險利率（年化，預設 1%）

        Returns:
            float: Sharpe Ratio
        """
        pass

    @abstractmethod
    def calculate_max_drawdown(self, prices: List[StockPrice]) -> float:
        """
        計算最大回撤（Maximum Drawdown）

        Args:
            prices: 價格序列

        Returns:
            float: 最大回撤百分比（負值）
        """
        pass

    @abstractmethod
    def get_risk_metrics_summary(self, stock: Stock) -> Dict:
        """
        獲取風險指標摘要

        Args:
            stock: 股票實體

        Returns:
            Dict: 包含所有風險指標的字典
        """
        pass


class IStrategyAnalyzer(ABC):
    """
    策略分析器介面

    定義投資策略分析相關的抽象方法，包括技術指標計算、訊號產生和回測功能。
    """

    @abstractmethod
    def analyze_strategy(self, stock: Stock) -> StrategyAnalysis:
        """
        執行完整的策略分析

        Args:
            stock: 股票實體，包含歷史價格資料

        Returns:
            StrategyAnalysis: 完整的策略分析結果，包含多種策略訊號和最終建議

        Raises:
            ValueError: 資料不足或參數無效
            CalculationError: 計算過程發生錯誤
        """
        pass

    @abstractmethod
    def calculate_technical_indicators(self, stock: Stock) -> TechnicalIndicators:
        """
        計算所有技術指標

        Args:
            stock: 股票實體

        Returns:
            TechnicalIndicators: 技術指標集合（MA、RSI、MACD、KDJ、布林通道等）
        """
        pass

    @abstractmethod
    def generate_ma_signal(self, prices: List[StockPrice], periods: List[int]) -> StrategySignal:
        """
        產生移動平均線（MA）交叉訊號

        Args:
            prices: 價格序列
            periods: MA 週期列表（如 [5, 20, 60]）

        Returns:
            StrategySignal: MA 策略訊號
        """
        pass

    @abstractmethod
    def generate_rsi_signal(self, prices: List[StockPrice], period: int = 14) -> StrategySignal:
        """
        產生 RSI 超買超賣訊號

        Args:
            prices: 價格序列
            period: RSI 週期（預設 14）

        Returns:
            StrategySignal: RSI 策略訊號
        """
        pass

    @abstractmethod
    def generate_macd_signal(
        self,
        prices: List[StockPrice],
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> StrategySignal:
        """
        產生 MACD 訊號

        Args:
            prices: 價格序列
            fast: 快線週期（預設 12）
            slow: 慢線週期（預設 26）
            signal: 訊號線週期（預設 9）

        Returns:
            StrategySignal: MACD 策略訊號
        """
        pass

    @abstractmethod
    def generate_kdj_signal(
        self,
        prices: List[StockPrice],
        period: int = 9
    ) -> StrategySignal:
        """
        產生 KDJ 指標訊號

        Args:
            prices: 價格序列
            period: KDJ 週期（預設 9）

        Returns:
            StrategySignal: KDJ 策略訊號
        """
        pass

    @abstractmethod
    def generate_bollinger_signal(
        self,
        prices: List[StockPrice],
        period: int = 20,
        std_dev: float = 2.0
    ) -> StrategySignal:
        """
        產生布林通道訊號

        Args:
            prices: 價格序列
            period: 計算週期（預設 20）
            std_dev: 標準差倍數（預設 2.0）

        Returns:
            StrategySignal: 布林通道策略訊號
        """
        pass

    @abstractmethod
    def backtest_strategy(
        self,
        stock: Stock,
        strategy_name: str,
        initial_capital: float = 1000000,
        commission_rate: float = 0.001425
    ) -> Dict:
        """
        回測策略績效

        Args:
            stock: 股票實體
            strategy_name: 策略名稱
            initial_capital: 初始資金（預設 100 萬）
            commission_rate: 手續費率（預設 0.1425%）

        Returns:
            Dict: 回測結果，包含總報酬率、勝率、最大回撤、交易次數等
        """
        pass

    @abstractmethod
    def compare_strategies(
        self,
        stock: Stock,
        strategy_names: List[str]
    ) -> pd.DataFrame:
        """
        比較多個策略的績效

        Args:
            stock: 股票實體
            strategy_names: 要比較的策略名稱列表

        Returns:
            DataFrame: 策略比較結果表格
        """
        pass


class IWarrantAnalyzer(ABC):
    """
    權證分析器介面

    定義權證相關的抽象方法，包括定價模型、Greeks 計算和篩選功能。
    """

    @abstractmethod
    def calculate_black_scholes_price(
        self,
        spot_price: float,
        strike_price: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str = "call"
    ) -> float:
        """
        使用 Black-Scholes 模型計算權證理論價格

        Args:
            spot_price: 標的股票現價
            strike_price: 履約價
            time_to_maturity: 距到期日時間（年）
            risk_free_rate: 無風險利率
            volatility: 波動率
            option_type: 選擇權類型（"call" 或 "put"）

        Returns:
            float: 理論價格
        """
        pass

    @abstractmethod
    def calculate_greeks(
        self,
        spot_price: float,
        strike_price: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str = "call"
    ) -> Dict[str, float]:
        """
        計算 Greeks 值（Delta, Gamma, Vega, Theta, Rho）

        Args:
            spot_price: 標的股票現價
            strike_price: 履約價
            time_to_maturity: 距到期日時間（年）
            risk_free_rate: 無風險利率
            volatility: 波動率
            option_type: 選擇權類型

        Returns:
            Dict: 包含所有 Greeks 值的字典
        """
        pass

    @abstractmethod
    def calculate_implied_volatility(
        self,
        market_price: float,
        spot_price: float,
        strike_price: float,
        time_to_maturity: float,
        risk_free_rate: float,
        option_type: str = "call"
    ) -> float:
        """
        計算隱含波動率（Implied Volatility）

        Args:
            market_price: 市場價格
            spot_price: 標的股票現價
            strike_price: 履約價
            time_to_maturity: 距到期日時間（年）
            risk_free_rate: 無風險利率
            option_type: 選擇權類型

        Returns:
            float: 隱含波動率
        """
        pass

    @abstractmethod
    def filter_warrants(
        self,
        underlying_stock: str,
        criteria: Dict
    ) -> List[Dict]:
        """
        根據條件篩選權證

        Args:
            underlying_stock: 標的股票代碼
            criteria: 篩選條件字典，可包含：
                - min_delta: 最小 Delta
                - max_delta: 最大 Delta
                - min_days_to_maturity: 最短到期日
                - max_days_to_maturity: 最長到期日
                - option_type: 選擇權類型

        Returns:
            List[Dict]: 符合條件的權證列表
        """
        pass

    @abstractmethod
    def analyze_warrant_value(
        self,
        warrant_code: str,
        underlying_stock: Stock
    ) -> Dict:
        """
        分析權證價值（是否高估/低估）

        Args:
            warrant_code: 權證代碼
            underlying_stock: 標的股票實體

        Returns:
            Dict: 包含理論價格、市場價格、價值評估等資訊
        """
        pass

    @abstractmethod
    def get_warrant_recommendation(
        self,
        underlying_stock: str,
        investment_horizon: int = 30,
        risk_preference: str = "moderate"
    ) -> List[Dict]:
        """
        獲取權證推薦

        Args:
            underlying_stock: 標的股票代碼
            investment_horizon: 投資期間（天數）
            risk_preference: 風險偏好（"conservative", "moderate", "aggressive"）

        Returns:
            List[Dict]: 推薦的權證列表（按評分排序）
        """
        pass
