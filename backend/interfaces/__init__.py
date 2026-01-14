"""
介面層 (Interfaces)

定義所有核心服務的抽象介面（契約）。
使用 ABC (Abstract Base Class) 實現介面模式。

優點：
- 依賴抽象而非具體實作 (DIP - 依賴反轉原則)
- 支援多種實作（多型）
- 提高可測試性（可使用 Mock）
- 清晰的契約定義

使用範例：
    from backend.interfaces import IStockDataFetcher

    class MyDataFetcher(IStockDataFetcher):
        def get_stock_price(self, stock_id: str, days: int):
            # 實作...
"""

from .data_fetcher_interface import IStockDataFetcher, IWarrantDataFetcher
from .analyzer_interface import IRiskAnalyzer, IStrategyAnalyzer, IWarrantAnalyzer
from .repository_interface import (
    IStockRepository,
    IWarrantRepository,
    IAnalysisRepository,
    ICacheRepository
)

__all__ = [
    # Data Fetchers
    'IStockDataFetcher',
    'IWarrantDataFetcher',

    # Analyzers
    'IRiskAnalyzer',
    'IStrategyAnalyzer',
    'IWarrantAnalyzer',

    # Repositories
    'IStockRepository',
    'IWarrantRepository',
    'IAnalysisRepository',
    'ICacheRepository',
]
