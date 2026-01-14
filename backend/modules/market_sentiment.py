# -*- coding: utf-8 -*-
"""
市場情緒分析模組
提供市場情緒指標和分析功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import plotly.graph_objects as go
from datetime import datetime, timedelta


class MarketSentimentAnalyzer:
    """市場情緒分析器"""

    def __init__(self, data_fetcher):
        """
        初始化

        Args:
            data_fetcher: 資料獲取器實例
        """
        self.data_fetcher = data_fetcher

    def calculate_market_breadth(self, stock_ids: List[str], days: int = 30) -> Dict:
        """
        計算市場廣度指標

        Args:
            stock_ids: 股票代碼列表
            days: 計算週期

        Returns:
            市場廣度指標
        """
        advancing_count = 0
        declining_count = 0
        unchanged_count = 0

        volume_up = 0
        volume_down = 0

        for stock_id in stock_ids:
            df = self.data_fetcher.get_stock_price(stock_id, days=days)
            if df.empty or len(df) < 2:
                continue

            # 比較期初期末
            start_price = df['收盤價'].iloc[0]
            end_price = df['收盤價'].iloc[-1]
            volume = df['成交量'].sum()

            if end_price > start_price:
                advancing_count += 1
                volume_up += volume
            elif end_price < start_price:
                declining_count += 1
                volume_down += volume
            else:
                unchanged_count += 1

        total_stocks = advancing_count + declining_count + unchanged_count

        # 計算指標
        advance_decline_ratio = advancing_count / declining_count if declining_count > 0 else np.inf
        advance_pct = (advancing_count / total_stocks * 100) if total_stocks > 0 else 0

        # 成交量比率
        total_volume = volume_up + volume_down
        volume_ratio = volume_up / volume_down if volume_down > 0 else np.inf

        return {
            '上漲家數': advancing_count,
            '下跌家數': declining_count,
            '平盤家數': unchanged_count,
            '總家數': total_stocks,
            '上漲比例(%)': round(advance_pct, 2),
            '漲跌比': round(advance_decline_ratio, 2),
            '上漲成交量': volume_up,
            '下跌成交量': volume_down,
            '成交量比': round(volume_ratio, 2),
            '市場情緒': self._interpret_breadth(advance_pct)
        }

    def _interpret_breadth(self, advance_pct: float) -> str:
        """解釋市場廣度"""
        if advance_pct >= 70:
            return '極度樂觀 🟢'
        elif advance_pct >= 60:
            return '樂觀 🟢'
        elif advance_pct >= 45:
            return '中性 ⚪'
        elif advance_pct >= 35:
            return '悲觀 🔴'
        else:
            return '極度悲觀 🔴'

    def calculate_fear_greed_index(self, stock_ids: List[str], days: int = 30) -> Dict:
        """
        計算恐懼貪婪指數（簡化版）

        Args:
            stock_ids: 股票代碼列表
            days: 計算週期

        Returns:
            恐懼貪婪指數
        """
        # 1. 價格動能（30%權重）
        price_momentum_score = self._calculate_price_momentum(stock_ids, days)

        # 2. 市場廣度（25%權重）
        breadth = self.calculate_market_breadth(stock_ids, days)
        breadth_score = min(breadth['上漲比例(%)'] / 50 * 50, 50)  # 標準化到 0-50

        # 3. 波動率（20%權重）
        volatility_score = self._calculate_volatility_score(stock_ids, days)

        # 4. 成交量（15%權重）
        volume_score = self._calculate_volume_score(stock_ids, days)

        # 5. 新高新低（10%權重）
        high_low_score = self._calculate_high_low_score(stock_ids, days)

        # 加權計算總分
        total_score = (
            price_momentum_score * 0.30 +
            breadth_score * 0.25 +
            volatility_score * 0.20 +
            volume_score * 0.15 +
            high_low_score * 0.10
        )

        return {
            '恐懼貪婪指數': round(total_score, 1),
            '情緒': self._interpret_fear_greed(total_score),
            '各項得分': {
                '價格動能': round(price_momentum_score, 1),
                '市場廣度': round(breadth_score, 1),
                '波動率': round(volatility_score, 1),
                '成交量': round(volume_score, 1),
                '新高新低': round(high_low_score, 1)
            }
        }

    def _calculate_price_momentum(self, stock_ids: List[str], days: int) -> float:
        """計算價格動能得分"""
        returns = []
        for stock_id in stock_ids:
            df = self.data_fetcher.get_stock_price(stock_id, days=days)
            if not df.empty and len(df) >= 2:
                total_return = (df['收盤價'].iloc[-1] / df['收盤價'].iloc[0] - 1) * 100
                returns.append(total_return)

        if not returns:
            return 50

        avg_return = np.mean(returns)
        # 將平均報酬率轉換為 0-100 分數
        score = 50 + avg_return * 2  # 假設 ±25% 為極值
        return max(0, min(100, score))

    def _calculate_volatility_score(self, stock_ids: List[str], days: int) -> float:
        """計算波動率得分（波動率低 = 貪婪，波動率高 = 恐懼）"""
        volatilities = []
        for stock_id in stock_ids:
            df = self.data_fetcher.get_stock_price(stock_id, days=days)
            if not df.empty:
                returns = df['收盤價'].pct_change().dropna()
                if len(returns) > 0:
                    vol = returns.std() * np.sqrt(252) * 100  # 年化波動率
                    volatilities.append(vol)

        if not volatilities:
            return 50

        avg_vol = np.mean(volatilities)
        # 波動率 20% = 50 分，越低越貪婪，越高越恐懼
        score = 100 - (avg_vol / 40 * 100)
        return max(0, min(100, score))

    def _calculate_volume_score(self, stock_ids: List[str], days: int) -> float:
        """計算成交量得分（成交量放大 = 貪婪）"""
        volume_ratios = []
        for stock_id in stock_ids:
            df = self.data_fetcher.get_stock_price(stock_id, days=days*2)
            if not df.empty and len(df) >= days*2:
                recent_vol = df['成交量'].iloc[-days:].mean()
                past_vol = df['成交量'].iloc[-days*2:-days].mean()
                if past_vol > 0:
                    ratio = recent_vol / past_vol
                    volume_ratios.append(ratio)

        if not volume_ratios:
            return 50

        avg_ratio = np.mean(volume_ratios)
        # 比率 1.0 = 50 分
        score = 50 + (avg_ratio - 1) * 50
        return max(0, min(100, score))

    def _calculate_high_low_score(self, stock_ids: List[str], days: int) -> float:
        """計算新高新低得分"""
        new_highs = 0
        new_lows = 0

        for stock_id in stock_ids:
            df = self.data_fetcher.get_stock_price(stock_id, days=days)
            if not df.empty:
                current_price = df['收盤價'].iloc[-1]
                period_high = df['最高價'].max()
                period_low = df['最低價'].min()

                if current_price == period_high:
                    new_highs += 1
                elif current_price == period_low:
                    new_lows += 1

        total = new_highs + new_lows
        if total == 0:
            return 50

        high_pct = new_highs / total
        return high_pct * 100

    def _interpret_fear_greed(self, score: float) -> str:
        """解釋恐懼貪婪指數"""
        if score >= 75:
            return '極度貪婪 🔥'
        elif score >= 55:
            return '貪婪 😊'
        elif score >= 45:
            return '中性 😐'
        elif score >= 25:
            return '恐懼 😨'
        else:
            return '極度恐懼 😱'

    def create_sentiment_gauge_chart(self, score: float, title: str = "市場情緒指數") -> go.Figure:
        """創建情緒儀表盤圖表"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 24}},
            delta={'reference': 50, 'increasing': {'color': "#22c55e"}, 'decreasing': {'color': "#ef4444"}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 25], 'color': '#ef4444'},
                    {'range': [25, 45], 'color': '#f59e0b'},
                    {'range': [45, 55], 'color': '#94a3b8'},
                    {'range': [55, 75], 'color': '#22c55e'},
                    {'range': [75, 100], 'color': '#10b981'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))

        fig.update_layout(
            height=400,
            template='plotly_white',
            font={'size': 16}
        )

        return fig

    def create_breadth_chart(self, breadth_data: Dict) -> go.Figure:
        """創建市場廣度圖表"""
        fig = go.Figure()

        categories = ['上漲', '下跌', '平盤']
        values = [
            breadth_data['上漲家數'],
            breadth_data['下跌家數'],
            breadth_data['平盤家數']
        ]
        colors = ['#22c55e', '#ef4444', '#94a3b8']

        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=values,
            textposition='outside'
        ))

        fig.update_layout(
            title='市場廣度分析',
            xaxis_title='類別',
            yaxis_title='家數',
            height=400,
            template='plotly_white',
            showlegend=False
        )

        return fig

    def analyze_sector_rotation(self, days: int = 30) -> Dict:
        """
        分析產業輪動

        Args:
            days: 分析週期

        Returns:
            產業輪動分析結果
        """
        sectors = {
            '半導體': ['2330', '2454', '2303'],
            '金融': ['2881', '2882', '2886'],
            '電子製造': ['2317', '2382'],
            '傳產': ['2308', '1301'],
            '通訊': ['2412']
        }

        sector_performance = []

        for sector_name, stock_ids in sectors.items():
            returns = []
            for stock_id in stock_ids:
                df = self.data_fetcher.get_stock_price(stock_id, days=days)
                if not df.empty and len(df) >= 2:
                    ret = (df['收盤價'].iloc[-1] / df['收盤價'].iloc[0] - 1) * 100
                    returns.append(ret)

            if returns:
                avg_return = np.mean(returns)
                sector_performance.append({
                    '產業': sector_name,
                    '平均報酬率(%)': round(avg_return, 2),
                    '趨勢': '上升 ⬆️' if avg_return > 0 else '下降 ⬇️'
                })

        # 排序
        sector_performance.sort(key=lambda x: x['平均報酬率(%)'], reverse=True)

        return {
            '產業排名': sector_performance,
            '領漲產業': sector_performance[0]['產業'] if sector_performance else 'N/A',
            '落後產業': sector_performance[-1]['產業'] if sector_performance else 'N/A'
        }

    def create_sector_rotation_chart(self, sector_data: List[Dict]) -> go.Figure:
        """創建產業輪動圖表"""
        fig = go.Figure()

        sectors = [item['產業'] for item in sector_data]
        returns = [item['平均報酬率(%)'] for item in sector_data]
        colors = ['#22c55e' if r > 0 else '#ef4444' for r in returns]

        fig.add_trace(go.Bar(
            x=sectors,
            y=returns,
            marker_color=colors,
            text=[f"{r:.1f}%" for r in returns],
            textposition='outside'
        ))

        fig.update_layout(
            title='產業輪動分析',
            xaxis_title='產業',
            yaxis_title='報酬率 (%)',
            height=450,
            template='plotly_white',
            showlegend=False
        )

        fig.add_hline(y=0, line_dash="dash", line_color="#94a3b8")

        return fig

    def generate_market_outlook(self, stock_ids: List[str], days: int = 30) -> str:
        """
        生成市場展望報告

        Args:
            stock_ids: 股票代碼列表
            days: 分析週期

        Returns:
            市場展望文字報告
        """
        breadth = self.calculate_market_breadth(stock_ids, days)
        fear_greed = self.calculate_fear_greed_index(stock_ids, days)
        sector_rotation = self.analyze_sector_rotation(days)

        report = f"""
# 市場展望分析報告

生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
分析週期: {days} 天

## 📊 市場廣度

- **上漲家數**: {breadth['上漲家數']} ({breadth['上漲比例(%)']}%)
- **下跌家數**: {breadth['下跌家數']}
- **漲跌比**: {breadth['漲跌比']}
- **市場情緒**: {breadth['市場情緒']}

## 🎭 恐懼貪婪指數

- **指數得分**: {fear_greed['恐懼貪婪指數']}
- **情緒判斷**: {fear_greed['情緒']}

### 各項得分明細
"""
        for metric, score in fear_greed['各項得分'].items():
            report += f"- {metric}: {score}\n"

        report += f"""
## 🔄 產業輪動

- **領漲產業**: {sector_rotation['領漲產業']}
- **落後產業**: {sector_rotation['落後產業']}

### 產業表現排名
"""
        for idx, sector in enumerate(sector_rotation['產業排名'], 1):
            report += f"{idx}. {sector['產業']}: {sector['平均報酬率(%)']}% {sector['趨勢']}\n"

        report += """
## 💡 投資建議

基於以上分析：
"""
        # 根據指標給出建議
        if fear_greed['恐懼貪婪指數'] > 70:
            report += "- ⚠️ 市場情緒過度樂觀，建議謹慎追高，注意獲利了結\n"
        elif fear_greed['恐懼貪婪指數'] < 30:
            report += "- 💡 市場情緒悲觀，可能存在逢低布局機會\n"
        else:
            report += "- 📊 市場情緒中性，建議保持觀望或分批進場\n"

        if breadth['上漲比例(%)'] > 60:
            report += "- 📈 市場廣度良好，多數股票上漲，趨勢向上\n"
        elif breadth['上漲比例(%)'] < 40:
            report += "- 📉 市場廣度偏弱，下跌股票較多，宜注意風險\n"

        return report
