# -*- coding: utf-8 -*-
"""
投資組合管理模組
提供投資組合分析和優化功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import plotly.graph_objects as go
from datetime import datetime, timedelta


class PortfolioManager:
    """投資組合管理器"""

    def __init__(self, data_fetcher):
        """
        初始化

        Args:
            data_fetcher: 資料獲取器實例
        """
        self.data_fetcher = data_fetcher
        self.portfolio = {}  # {stock_id: {'shares': int, 'cost': float}}

    def add_position(self, stock_id: str, shares: int, cost_per_share: float):
        """
        新增持股

        Args:
            stock_id: 股票代碼
            shares: 股數
            cost_per_share: 買入成本（每股）
        """
        if stock_id in self.portfolio:
            # 計算加權平均成本
            total_shares = self.portfolio[stock_id]['shares'] + shares
            total_cost = (self.portfolio[stock_id]['shares'] * self.portfolio[stock_id]['cost'] +
                         shares * cost_per_share)
            avg_cost = total_cost / total_shares

            self.portfolio[stock_id] = {
                'shares': total_shares,
                'cost': avg_cost
            }
        else:
            self.portfolio[stock_id] = {
                'shares': shares,
                'cost': cost_per_share
            }

    def remove_position(self, stock_id: str):
        """移除持股"""
        if stock_id in self.portfolio:
            del self.portfolio[stock_id]

    def update_position(self, stock_id: str, shares: int, cost_per_share: float):
        """更新持股"""
        self.portfolio[stock_id] = {
            'shares': shares,
            'cost': cost_per_share
        }

    def get_portfolio_value(self) -> Dict:
        """
        計算投資組合價值

        Returns:
            投資組合價值資訊
        """
        if not self.portfolio:
            return {
                'total_cost': 0,
                'total_value': 0,
                'total_profit': 0,
                'total_return': 0,
                'positions': []
            }

        positions = []
        total_cost = 0
        total_value = 0

        for stock_id, holding in self.portfolio.items():
            # 獲取當前價格
            df = self.data_fetcher.get_stock_price(stock_id, days=1)
            if df.empty:
                current_price = holding['cost']  # 無資料時使用成本價
            else:
                current_price = float(df['收盤價'].iloc[-1])

            # 計算各項指標
            shares = holding['shares']
            cost_price = holding['cost']
            cost = shares * cost_price
            value = shares * current_price
            profit = value - cost
            return_pct = (profit / cost) * 100 if cost > 0 else 0

            positions.append({
                '股票代碼': stock_id,
                '股數': shares,
                '買入成本': round(cost_price, 2),
                '當前價格': round(current_price, 2),
                '成本金額': round(cost, 2),
                '當前市值': round(value, 2),
                '損益': round(profit, 2),
                '報酬率(%)': round(return_pct, 2),
                '權重(%)': 0  # 稍後計算
            })

            total_cost += cost
            total_value += value

        # 計算權重
        for pos in positions:
            pos['權重(%)'] = round((pos['當前市值'] / total_value) * 100, 2) if total_value > 0 else 0

        total_profit = total_value - total_cost
        total_return = (total_profit / total_cost) * 100 if total_cost > 0 else 0

        return {
            'total_cost': round(total_cost, 2),
            'total_value': round(total_value, 2),
            'total_profit': round(total_profit, 2),
            'total_return': round(total_return, 2),
            'positions': positions,
            'position_count': len(positions)
        }

    def calculate_portfolio_risk(self, days: int = 90) -> Dict:
        """
        計算投資組合風險指標

        Args:
            days: 計算週期

        Returns:
            風險指標字典
        """
        if not self.portfolio:
            return {}

        # 獲取所有持股的收益率資料
        returns_data = {}
        weights = {}

        # 計算當前權重
        portfolio_value = self.get_portfolio_value()
        total_value = portfolio_value['total_value']

        for position in portfolio_value['positions']:
            stock_id = position['股票代碼']
            weights[stock_id] = position['當前市值'] / total_value if total_value > 0 else 0

            # 獲取價格資料
            df = self.data_fetcher.get_stock_price(stock_id, days=days)
            if not df.empty:
                returns_data[stock_id] = df['收盤價'].pct_change().dropna()

        if not returns_data:
            return {}

        # 轉換為 DataFrame
        returns_df = pd.DataFrame(returns_data)

        # 計算投資組合收益率
        weights_series = pd.Series(weights)
        portfolio_returns = (returns_df * weights_series).sum(axis=1)

        # 計算風險指標
        portfolio_std = portfolio_returns.std()
        portfolio_var_95 = portfolio_returns.quantile(0.05)
        portfolio_var_99 = portfolio_returns.quantile(0.01)

        # 年化指標
        annual_return = portfolio_returns.mean() * 252 * 100
        annual_volatility = portfolio_std * np.sqrt(252) * 100
        annual_var_95 = portfolio_var_95 * np.sqrt(252) * 100
        annual_var_99 = portfolio_var_99 * np.sqrt(252) * 100

        # 夏普比率（假設無風險利率 1%）
        risk_free_rate = 0.01
        sharpe_ratio = (annual_return/100 - risk_free_rate) / (annual_volatility/100)

        # 最大回撤
        cumulative_returns = (1 + portfolio_returns).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min() * 100

        return {
            '年化報酬率(%)': round(annual_return, 2),
            '年化波動率(%)': round(annual_volatility, 2),
            '夏普比率': round(sharpe_ratio, 2),
            '最大回撤(%)': round(max_drawdown, 2),
            'VaR_95(%)': round(annual_var_95, 2),
            'VaR_99(%)': round(annual_var_99, 2),
            '相關係數矩陣': returns_df.corr().round(3).to_dict()
        }

    def optimize_portfolio(self, target_return: float = None) -> Dict:
        """
        投資組合優化（簡化版）

        Args:
            target_return: 目標報酬率

        Returns:
            優化建議
        """
        if not self.portfolio:
            return {}

        portfolio_value = self.get_portfolio_value()
        risk_metrics = self.calculate_portfolio_risk()

        if not risk_metrics:
            return {}

        # 提供簡單的再平衡建議
        positions = portfolio_value['positions']
        avg_weight = 100 / len(positions) if positions else 0

        rebalance_suggestions = []
        for pos in positions:
            current_weight = pos['權重(%)']
            diff = current_weight - avg_weight

            if abs(diff) > 5:  # 偏離超過 5%
                action = '減持' if diff > 0 else '加碼'
                amount = abs(diff)
                rebalance_suggestions.append({
                    '股票': pos['股票代碼'],
                    '當前權重': f"{current_weight:.1f}%",
                    '建議權重': f"{avg_weight:.1f}%",
                    '建議': f"{action} {amount:.1f}%"
                })

        return {
            '當前配置': {
                '股票數': len(positions),
                '總市值': portfolio_value['total_value'],
                '總報酬率': f"{portfolio_value['total_return']:.2f}%"
            },
            '風險指標': {
                '年化波動率': f"{risk_metrics['年化波動率(%)']}%",
                '夏普比率': risk_metrics['夏普比率'],
                '最大回撤': f"{risk_metrics['最大回撤(%)']}%"
            },
            '再平衡建議': rebalance_suggestions if rebalance_suggestions else ['當前配置均衡']
        }

    def create_portfolio_pie_chart(self) -> go.Figure:
        """創建投資組合配置餅圖"""
        portfolio_value = self.get_portfolio_value()

        if not portfolio_value['positions']:
            return go.Figure()

        positions = portfolio_value['positions']

        fig = go.Figure(data=[go.Pie(
            labels=[pos['股票代碼'] for pos in positions],
            values=[pos['當前市值'] for pos in positions],
            hole=0.4,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(
                colors=['#3b82f6', '#ef4444', '#22c55e', '#8b5cf6', '#f59e0b', '#14b8a6'],
                line=dict(color='#ffffff', width=2)
            )
        )])

        fig.update_layout(
            title='投資組合配置',
            height=500,
            template='plotly_white',
            annotations=[dict(
                text=f'總市值<br>{portfolio_value["total_value"]:,.0f}',
                x=0.5, y=0.5,
                font_size=14,
                showarrow=False
            )]
        )

        return fig

    def create_portfolio_performance_chart(self, days: int = 90) -> go.Figure:
        """創建投資組合績效圖"""
        if not self.portfolio:
            return go.Figure()

        # 計算投資組合每日價值
        portfolio_value = self.get_portfolio_value()
        weights = {}

        for pos in portfolio_value['positions']:
            weights[pos['股票代碼']] = pos['權重(%)'] / 100

        # 獲取歷史價格
        all_data = {}
        for stock_id in weights.keys():
            df = self.data_fetcher.get_stock_price(stock_id, days=days)
            if not df.empty:
                all_data[stock_id] = df['收盤價']

        if not all_data:
            return go.Figure()

        # 計算投資組合價值變化
        prices_df = pd.DataFrame(all_data).fillna(method='ffill')

        # 標準化為第一天 = 100
        normalized_prices = prices_df / prices_df.iloc[0] * 100

        # 計算加權組合
        portfolio_value_series = (normalized_prices * pd.Series(weights)).sum(axis=1)

        fig = go.Figure()

        # 繪製投資組合線
        fig.add_trace(go.Scatter(
            x=portfolio_value_series.index,
            y=portfolio_value_series,
            name='投資組合',
            line=dict(color='#3b82f6', width=3),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)'
        ))

        # 繪製個別股票線（淡化）
        colors = ['#ef4444', '#22c55e', '#8b5cf6', '#f59e0b', '#14b8a6']
        for idx, (stock_id, prices) in enumerate(normalized_prices.items()):
            fig.add_trace(go.Scatter(
                x=prices.index,
                y=prices,
                name=stock_id,
                line=dict(color=colors[idx % len(colors)], width=1, dash='dot'),
                opacity=0.5
            ))

        fig.update_layout(
            title='投資組合績效表現',
            xaxis_title='日期',
            yaxis_title='標準化價值（基準=100）',
            height=500,
            template='plotly_white',
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig.add_hline(y=100, line_dash="dash", line_color="#94a3b8", annotation_text="基準線")

        return fig

    def generate_portfolio_report(self) -> str:
        """生成投資組合報告"""
        portfolio_value = self.get_portfolio_value()
        risk_metrics = self.calculate_portfolio_risk()

        if not portfolio_value['positions']:
            return "投資組合為空"

        report = f"""
# 投資組合分析報告

生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 投資組合概況

- **持股數量**: {portfolio_value['position_count']} 支
- **總成本**: {portfolio_value['total_cost']:,.2f} TWD
- **當前市值**: {portfolio_value['total_value']:,.2f} TWD
- **總損益**: {portfolio_value['total_profit']:,.2f} TWD
- **總報酬率**: {portfolio_value['total_return']:.2f}%

## 🎯 持股明細

"""
        for pos in portfolio_value['positions']:
            report += f"""
### {pos['股票代碼']}
- 股數: {pos['股數']:,}
- 買入成本: {pos['買入成本']:.2f} TWD
- 當前價格: {pos['當前價格']:.2f} TWD
- 損益: {pos['損益']:,.2f} TWD ({pos['報酬率(%)']:.2f}%)
- 權重: {pos['權重(%)']}%
"""

        if risk_metrics:
            report += f"""
## 📈 風險指標

- **年化報酬率**: {risk_metrics['年化報酬率(%)']}%
- **年化波動率**: {risk_metrics['年化波動率(%)']}%
- **夏普比率**: {risk_metrics['夏普比率']:.2f}
- **最大回撤**: {risk_metrics['最大回撤(%)']}%
- **VaR (95%)**: {risk_metrics['VaR_95(%)']}%
- **VaR (99%)**: {risk_metrics['VaR_99(%)']}%
"""

        return report


class TradeRecorder:
    """交易記錄器"""

    def __init__(self):
        self.trades = []

    def record_trade(self, stock_id: str, action: str, shares: int,
                    price: float, date: str = None):
        """
        記錄交易

        Args:
            stock_id: 股票代碼
            action: 交易動作（買入/賣出）
            shares: 股數
            price: 價格
            date: 交易日期
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        self.trades.append({
            '日期': date,
            '股票': stock_id,
            '動作': action,
            '股數': shares,
            '價格': price,
            '金額': shares * price
        })

    def get_trade_history(self) -> pd.DataFrame:
        """獲取交易歷史"""
        if not self.trades:
            return pd.DataFrame()

        return pd.DataFrame(self.trades)

    def calculate_realized_pnl(self) -> Dict:
        """計算已實現損益"""
        if not self.trades:
            return {'realized_profit': 0, 'win_rate': 0, 'trades_count': 0}

        df = self.get_trade_history()

        # 簡化版：配對買賣計算損益
        buy_trades = df[df['動作'] == '買入']
        sell_trades = df[df['動作'] == '賣出']

        total_profit = 0
        win_count = 0
        total_count = 0

        for stock_id in df['股票'].unique():
            stock_buys = buy_trades[buy_trades['股票'] == stock_id]
            stock_sells = sell_trades[sell_trades['股票'] == stock_id]

            if not stock_sells.empty and not stock_buys.empty:
                avg_buy_price = (stock_buys['股數'] * stock_buys['價格']).sum() / stock_buys['股數'].sum()
                avg_sell_price = (stock_sells['股數'] * stock_sells['價格']).sum() / stock_sells['股數'].sum()

                profit = (avg_sell_price - avg_buy_price) * min(stock_buys['股數'].sum(), stock_sells['股數'].sum())
                total_profit += profit

                if profit > 0:
                    win_count += 1
                total_count += 1

        win_rate = (win_count / total_count * 100) if total_count > 0 else 0

        return {
            'realized_profit': round(total_profit, 2),
            'win_rate': round(win_rate, 2),
            'trades_count': len(self.trades),
            'win_count': win_count,
            'loss_count': total_count - win_count
        }
