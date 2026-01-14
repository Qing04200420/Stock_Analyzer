"""
實體層 (Entities)

定義核心業務實體，具有唯一識別符的對象。

特點：
- 具有唯一識別符 (ID)
- 生命週期內可變
- 身份可追蹤
"""

from .stock import Stock, StockPrice
from .analysis import RiskAnalysis, StrategyAnalysis, TechnicalIndicators

__all__ = [
    'Stock',
    'StockPrice',
    'RiskAnalysis',
    'StrategyAnalysis',
    'TechnicalIndicators'
]
