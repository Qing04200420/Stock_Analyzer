"""
分析結果實體

包含各種分析結果的業務對象。
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum


class RiskLevel(Enum):
    """風險等級枚舉"""
    VERY_LOW = "極低風險"
    LOW = "低風險"
    MEDIUM = "中等風險"
    HIGH = "高風險"
    VERY_HIGH = "極高風險"


class SignalType(Enum):
    """交易信號類型"""
    STRONG_BUY = "強烈買入"
    BUY = "買入"
    HOLD = "持有"
    SELL = "賣出"
    STRONG_SELL = "強烈賣出"


@dataclass
class TechnicalIndicators:
    """
    技術指標集合

    包含所有技術分析指標的計算結果。

    Attributes:
        ma: 移動平均線字典 (例如: {"MA5": 100.5, "MA20": 98.3})
        rsi: RSI 指標值
        macd: MACD 指標字典
        kdj: KDJ 指標字典
        bollinger: 布林通道字典
        timestamp: 計算時間戳
    """
    ma: Dict[str, float] = field(default_factory=dict)
    rsi: Optional[float] = None
    macd: Dict[str, float] = field(default_factory=dict)
    kdj: Dict[str, float] = field(default_factory=dict)
    bollinger: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def is_overbought(self) -> bool:
        """RSI 是否超買 (> 70)"""
        return self.rsi is not None and self.rsi > 70

    @property
    def is_oversold(self) -> bool:
        """RSI 是否超賣 (< 30)"""
        return self.rsi is not None and self.rsi < 30

    @property
    def ma_trend(self) -> Optional[str]:
        """
        均線趨勢判斷

        Returns:
            "多頭排列" | "空頭排列" | "糾結" | None
        """
        if "MA5" in self.ma and "MA20" in self.ma and "MA60" in self.ma:
            ma5, ma20, ma60 = self.ma["MA5"], self.ma["MA20"], self.ma["MA60"]
            if ma5 > ma20 > ma60:
                return "多頭排列"
            elif ma5 < ma20 < ma60:
                return "空頭排列"
            else:
                return "糾結"
        return None


@dataclass
class RiskAnalysis:
    """
    風險分析結果

    包含完整的風險評估指標和結論。

    Attributes:
        stock_code: 股票代碼
        volatility: 波動率 (標準差)
        var_95: 95% 信心水準的風險值
        var_99: 99% 信心水準的風險值
        beta: Beta 係數 (市場敏感度)
        sharpe_ratio: 夏普比率 (風險調整後報酬)
        max_drawdown: 最大回撤 (最大跌幅)
        risk_level: 風險等級
        analysis_date: 分析日期
        period_days: 分析期間天數
    """
    stock_code: str
    volatility: float
    var_95: float
    var_99: float
    beta: float
    sharpe_ratio: float
    max_drawdown: float
    risk_level: RiskLevel
    analysis_date: datetime = field(default_factory=datetime.now)
    period_days: int = 90

    @property
    def risk_score(self) -> int:
        """
        風險評分 (0-100)

        綜合各項指標計算風險分數，分數越高風險越大。
        """
        # 權重: 波動率 30%, Beta 25%, 最大回撤 25%, Sharpe 20%
        volatility_score = min(self.volatility * 100, 40)  # 最高 40 分
        beta_score = min(abs(self.beta) * 12.5, 25)  # 最高 25 分
        drawdown_score = min(abs(self.max_drawdown), 25)  # 最高 25 分
        sharpe_score = max(0, 10 - self.sharpe_ratio * 5)  # Sharpe 越低分數越高，最高 10 分

        return int(volatility_score + beta_score + drawdown_score + sharpe_score)

    @property
    def risk_description(self) -> str:
        """風險等級描述"""
        return self.risk_level.value

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式"""
        return {
            "股票代碼": self.stock_code,
            "波動率": f"{self.volatility:.2%}",
            "VaR (95%)": f"{self.var_95:.2%}",
            "VaR (99%)": f"{self.var_99:.2%}",
            "Beta 係數": f"{self.beta:.2f}",
            "Sharpe Ratio": f"{self.sharpe_ratio:.2f}",
            "最大回撤": f"{self.max_drawdown:.2%}",
            "風險等級": self.risk_description,
            "風險評分": self.risk_score,
            "分析日期": self.analysis_date.strftime("%Y-%m-%d"),
            "分析期間": f"{self.period_days} 天"
        }


@dataclass
class StrategySignal:
    """
    策略信號

    單一策略產生的交易信號。

    Attributes:
        strategy_name: 策略名稱
        signal: 信號類型
        strength: 信號強度 (0-100)
        reason: 信號原因說明
        timestamp: 產生時間
    """
    strategy_name: str
    signal: SignalType
    strength: int  # 0-100
    reason: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """驗證"""
        if not 0 <= self.strength <= 100:
            raise ValueError("信號強度必須在 0-100 之間")


@dataclass
class StrategyAnalysis:
    """
    策略分析結果

    綜合多個策略的分析結論。

    Attributes:
        stock_code: 股票代碼
        signals: 各策略信號列表
        technical_indicators: 技術指標
        final_signal: 綜合信號
        confidence: 信心度 (0-100)
        recommendation: 操作建議
        analysis_date: 分析日期
    """
    stock_code: str
    signals: List[StrategySignal] = field(default_factory=list)
    technical_indicators: Optional[TechnicalIndicators] = None
    final_signal: Optional[SignalType] = None
    confidence: int = 0  # 0-100
    recommendation: str = ""
    analysis_date: datetime = field(default_factory=datetime.now)

    def add_signal(self, signal: StrategySignal) -> None:
        """添加策略信號"""
        self.signals.append(signal)
        self._calculate_final_signal()

    def _calculate_final_signal(self) -> None:
        """計算綜合信號"""
        if not self.signals:
            return

        # 加權平均計算
        signal_values = {
            SignalType.STRONG_BUY: 2,
            SignalType.BUY: 1,
            SignalType.HOLD: 0,
            SignalType.SELL: -1,
            SignalType.STRONG_SELL: -2
        }

        total_weight = sum(s.strength for s in self.signals)
        if total_weight == 0:
            self.final_signal = SignalType.HOLD
            self.confidence = 0
            return

        weighted_sum = sum(
            signal_values[s.signal] * s.strength
            for s in self.signals
        )

        avg_value = weighted_sum / total_weight

        # 決定最終信號
        if avg_value >= 1.5:
            self.final_signal = SignalType.STRONG_BUY
        elif avg_value >= 0.5:
            self.final_signal = SignalType.BUY
        elif avg_value <= -1.5:
            self.final_signal = SignalType.STRONG_SELL
        elif avg_value <= -0.5:
            self.final_signal = SignalType.SELL
        else:
            self.final_signal = SignalType.HOLD

        # 計算信心度
        self.confidence = int(min(abs(avg_value) * 40, 100))

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式"""
        return {
            "股票代碼": self.stock_code,
            "綜合信號": self.final_signal.value if self.final_signal else "無",
            "信心度": f"{self.confidence}%",
            "策略數量": len(self.signals),
            "操作建議": self.recommendation,
            "分析日期": self.analysis_date.strftime("%Y-%m-%d %H:%M:%S")
        }
