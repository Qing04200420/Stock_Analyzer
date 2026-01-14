"""
UI 元件模組

此模組包含所有可重用的 UI 元件。
遵循 DRY (Don't Repeat Yourself) 原則。
"""

# 圖表元件
from .charts import (
    plot_stock_candlestick,
    plot_technical_indicators,
    plot_volume_chart,
    plot_risk_metrics_radar,
    plot_backtest_equity_curve
)

# 卡片元件
from .cards import (
    page_header,
    metric_card,
    success_box,
    warning_box,
    danger_box,
    info_box,
    feature_card,
    stat_cards_row,
    risk_level_badge,
    signal_badge,
    stock_info_card,
    progress_card
)

__all__ = [
    # Charts
    'plot_stock_candlestick',
    'plot_technical_indicators',
    'plot_volume_chart',
    'plot_risk_metrics_radar',
    'plot_backtest_equity_curve',

    # Cards
    'page_header',
    'metric_card',
    'success_box',
    'warning_box',
    'danger_box',
    'info_box',
    'feature_card',
    'stat_cards_row',
    'risk_level_badge',
    'signal_badge',
    'stock_info_card',
    'progress_card',
]
