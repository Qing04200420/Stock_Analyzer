# -*- coding: utf-8 -*-
"""
股票比較模組
提供多支股票的對比分析功能
"""

import pandas as pd
import numpy as np
from typing import List, Dict
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class StockComparator:
    """股票比較器"""

    def __init__(self, data_fetcher):
        """
        初始化

        Args:
            data_fetcher: 資料獲取器實例
        """
        self.data_fetcher = data_fetcher

    def compare_stocks(self, stock_ids: List[str], days: int = 90) -> Dict:
        """
        比較多支股票

        Args:
            stock_ids: 股票代碼列表
            days: 查詢天數

        Returns:
            比較結果字典
        """
        stocks_data = {}
        comparison_metrics = []

        for stock_id in stock_ids:
            # 獲取股票資料
            df = self.data_fetcher.get_stock_price(stock_id, days=days)
            if df.empty:
                continue

            stocks_data[stock_id] = df

            # 計算指標
            metrics = self._calculate_comparison_metrics(df, stock_id)
            comparison_metrics.append(metrics)

        return {
            'stocks_data': stocks_data,
            'comparison_table': pd.DataFrame(comparison_metrics),
            'stock_count': len(stocks_data)
        }

    def _calculate_comparison_metrics(self, df: pd.DataFrame, stock_id: str) -> Dict:
        """計算比較指標"""
        if df.empty:
            return {}

        latest_price = df['收盤價'].iloc[-1]
        first_price = df['收盤價'].iloc[0]

        # 價格變化
        price_change = latest_price - first_price
        price_change_pct = (price_change / first_price) * 100

        # 波動率（標準差）
        returns = df['收盤價'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252) * 100  # 年化波動率

        # 最高最低
        period_high = df['最高價'].max()
        period_low = df['最低價'].min()

        # 平均成交量
        avg_volume = df['成交量'].mean()

        # 夏普比率（簡化版，假設無風險利率為 1%）
        risk_free_rate = 0.01
        avg_return = returns.mean() * 252  # 年化收益率
        sharpe_ratio = (avg_return - risk_free_rate) / (returns.std() * np.sqrt(252))

        return {
            '股票代碼': stock_id,
            '最新價格': round(latest_price, 2),
            '期間漲跌': round(price_change, 2),
            '漲跌幅(%)': round(price_change_pct, 2),
            '波動率(%)': round(volatility, 2),
            '期間最高': round(period_high, 2),
            '期間最低': round(period_low, 2),
            '平均成交量': int(avg_volume),
            '夏普比率': round(sharpe_ratio, 2)
        }

    def create_comparison_chart(self, stocks_data: Dict, normalize: bool = True) -> go.Figure:
        """
        創建股票比較圖表

        Args:
            stocks_data: 股票資料字典
            normalize: 是否標準化（以第一個價格為 100）

        Returns:
            Plotly Figure 對象
        """
        fig = go.Figure()

        colors = ['#3b82f6', '#ef4444', '#22c55e', '#8b5cf6', '#f59e0b', '#14b8a6']

        for idx, (stock_id, df) in enumerate(stocks_data.items()):
            if df.empty:
                continue

            if normalize:
                # 標準化：第一個價格設為 100
                normalized_prices = (df['收盤價'] / df['收盤價'].iloc[0]) * 100
                y_data = normalized_prices
                y_label = '標準化價格（基準=100）'
            else:
                y_data = df['收盤價']
                y_label = '價格'

            fig.add_trace(go.Scatter(
                x=df.index,
                y=y_data,
                name=stock_id,
                line=dict(color=colors[idx % len(colors)], width=2),
                mode='lines'
            ))

        fig.update_layout(
            title='股票走勢比較',
            xaxis_title='日期',
            yaxis_title=y_label,
            height=500,
            template='plotly_white',
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')

        return fig

    def create_volume_comparison_chart(self, stocks_data: Dict) -> go.Figure:
        """創建成交量比較圖表"""
        fig = go.Figure()

        colors = ['#3b82f6', '#ef4444', '#22c55e', '#8b5cf6', '#f59e0b', '#14b8a6']

        for idx, (stock_id, df) in enumerate(stocks_data.items()):
            if df.empty:
                continue

            fig.add_trace(go.Bar(
                x=[stock_id],
                y=[df['成交量'].mean()],
                name=stock_id,
                marker_color=colors[idx % len(colors)],
                text=[f"{df['成交量'].mean()/1e6:.2f}M"],
                textposition='outside'
            ))

        fig.update_layout(
            title='平均成交量比較',
            xaxis_title='股票代碼',
            yaxis_title='成交量',
            height=400,
            template='plotly_white',
            showlegend=False
        )

        return fig

    def create_return_distribution_chart(self, stocks_data: Dict) -> go.Figure:
        """創建報酬率分佈圖"""
        fig = go.Figure()

        colors = ['#3b82f6', '#ef4444', '#22c55e', '#8b5cf6', '#f59e0b', '#14b8a6']

        for idx, (stock_id, df) in enumerate(stocks_data.items()):
            if df.empty:
                continue

            returns = df['收盤價'].pct_change().dropna() * 100

            fig.add_trace(go.Box(
                y=returns,
                name=stock_id,
                marker_color=colors[idx % len(colors)],
                boxmean='sd'  # 顯示平均值和標準差
            ))

        fig.update_layout(
            title='每日報酬率分佈',
            xaxis_title='股票代碼',
            yaxis_title='報酬率 (%)',
            height=500,
            template='plotly_white',
            showlegend=True
        )

        return fig

    def generate_comparison_report(self, comparison_table: pd.DataFrame) -> Dict:
        """
        生成比較報告

        Args:
            comparison_table: 比較指標表格

        Returns:
            報告字典
        """
        if comparison_table.empty:
            return {}

        # 找出最佳表現
        best_performer = comparison_table.loc[comparison_table['漲跌幅(%)'].idxmax()]
        worst_performer = comparison_table.loc[comparison_table['漲跌幅(%)'].idxmin()]

        # 最穩定（波動率最低）
        most_stable = comparison_table.loc[comparison_table['波動率(%)'].idxmin()]

        # 最高夏普比率
        best_sharpe = comparison_table.loc[comparison_table['夏普比率'].idxmax()]

        # 成交量最大
        highest_volume = comparison_table.loc[comparison_table['平均成交量'].idxmax()]

        return {
            '最佳表現': {
                '股票': best_performer['股票代碼'],
                '漲跌幅': f"{best_performer['漲跌幅(%)']}%"
            },
            '最差表現': {
                '股票': worst_performer['股票代碼'],
                '漲跌幅': f"{worst_performer['漲跌幅(%)']}%"
            },
            '最穩定': {
                '股票': most_stable['股票代碼'],
                '波動率': f"{most_stable['波動率(%)']}%"
            },
            '最佳風險調整報酬': {
                '股票': best_sharpe['股票代碼'],
                '夏普比率': round(best_sharpe['夏普比率'], 2)
            },
            '成交量最大': {
                '股票': highest_volume['股票代碼'],
                '平均成交量': f"{highest_volume['平均成交量']/1e6:.2f}M"
            }
        }


class SectorAnalyzer:
    """產業分析器"""

    def __init__(self, data_fetcher):
        self.data_fetcher = data_fetcher

        # 定義產業分類
        self.sectors = {
            '半導體': ['2330', '2454', '2303', '3034'],
            '金融': ['2881', '2882', '2886', '2891', '2892'],
            '電子製造': ['2317', '2382', '2357'],
            '傳產': ['2308', '1301', '1303'],
            '通訊': ['2412', '4904', '4938']
        }

    def analyze_sector(self, sector_name: str, days: int = 90) -> Dict:
        """
        分析特定產業

        Args:
            sector_name: 產業名稱
            days: 查詢天數

        Returns:
            產業分析結果
        """
        if sector_name not in self.sectors:
            return {}

        stock_ids = self.sectors[sector_name]
        sector_data = {}

        for stock_id in stock_ids:
            df = self.data_fetcher.get_stock_price(stock_id, days=days)
            if not df.empty:
                sector_data[stock_id] = df

        if not sector_data:
            return {}

        # 計算產業平均指標
        all_returns = []
        all_volatilities = []

        for stock_id, df in sector_data.items():
            returns = df['收盤價'].pct_change().dropna()
            all_returns.extend(returns.tolist())
            all_volatilities.append(returns.std())

        avg_return = np.mean(all_returns) * 252 * 100  # 年化報酬率
        avg_volatility = np.mean(all_volatilities) * np.sqrt(252) * 100  # 年化波動率

        return {
            'sector_name': sector_name,
            'stock_count': len(sector_data),
            'avg_return': round(avg_return, 2),
            'avg_volatility': round(avg_volatility, 2),
            'stocks_data': sector_data
        }

    def get_all_sectors(self) -> List[str]:
        """獲取所有產業列表"""
        return list(self.sectors.keys())

    def create_sector_heatmap(self, days: int = 30) -> go.Figure:
        """創建產業熱力圖"""
        sector_performance = []

        for sector_name in self.sectors.keys():
            result = self.analyze_sector(sector_name, days=days)
            if result:
                sector_performance.append({
                    '產業': sector_name,
                    '報酬率': result['avg_return'],
                    '波動率': result['avg_volatility']
                })

        if not sector_performance:
            return go.Figure()

        df = pd.DataFrame(sector_performance)

        fig = go.Figure(data=go.Scatter(
            x=df['波動率'],
            y=df['報酬率'],
            mode='markers+text',
            text=df['產業'],
            textposition='top center',
            marker=dict(
                size=15,
                color=df['報酬率'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="報酬率 (%)")
            )
        ))

        fig.update_layout(
            title='產業風險-報酬分析',
            xaxis_title='波動率 (%)',
            yaxis_title='報酬率 (%)',
            height=500,
            template='plotly_white',
            hovermode='closest'
        )

        # 添加象限線
        fig.add_hline(y=0, line_dash="dash", line_color="#94a3b8")
        fig.add_vline(x=df['波動率'].median(), line_dash="dash", line_color="#94a3b8")

        return fig
