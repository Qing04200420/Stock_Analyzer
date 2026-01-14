"""
頁面模組

此目錄包含所有功能頁面。
每個頁面是一個獨立的函數，負責單一功能的 UI 和邏輯。
"""

from .home import show_home_page
from .stock_analysis import show_stock_analysis_page
from .risk_assessment import show_risk_assessment_page
from .strategy import show_strategy_page
from .warrant import show_warrant_page
from .settings import show_settings_page

__all__ = [
    'show_home_page',
    'show_stock_analysis_page',
    'show_risk_assessment_page',
    'show_strategy_page',
    'show_warrant_page',
    'show_settings_page',
]
