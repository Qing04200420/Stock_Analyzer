# -*- coding: utf-8 -*-
"""
技術分析模組
提供進階技術指標計算和圖表繪製
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class TechnicalAnalyzer:
    """技術分析器"""

    def __init__(self):
        pass

    # ==================== 移動平均線 ====================

    def calculate_ma(self, df: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> pd.DataFrame:
        """
        計算移動平均線

        Args:
            df: 包含收盤價的 DataFrame
            periods: 週期列表

        Returns:
            添加 MA 欄位的 DataFrame
        """
        df = df.copy()
        for period in periods:
            df[f'MA{period}'] = df['收盤價'].rolling(window=period).mean()
        return df

    def calculate_ema(self, df: pd.DataFrame, periods: List[int] = [12, 26]) -> pd.DataFrame:
        """
        計算指數移動平均線

        Args:
            df: 包含收盤價的 DataFrame
            periods: 週期列表

        Returns:
            添加 EMA 欄位的 DataFrame
        """
        df = df.copy()
        for period in periods:
            df[f'EMA{period}'] = df['收盤價'].ewm(span=period, adjust=False).mean()
        return df

    # ==================== MACD ====================

    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        計算 MACD 指標

        Args:
            df: 包含收盤價的 DataFrame
            fast: 快線週期
            slow: 慢線週期
            signal: 信號線週期

        Returns:
            添加 MACD 欄位的 DataFrame
        """
        df = df.copy()

        # 計算 EMA
        ema_fast = df['收盤價'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['收盤價'].ewm(span=slow, adjust=False).mean()

        # MACD 線
        df['MACD'] = ema_fast - ema_slow

        # 信號線
        df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()

        # MACD 柱狀圖
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']

        return df

    # ==================== RSI ====================

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        計算 RSI 相對強弱指標

        Args:
            df: 包含收盤價的 DataFrame
            period: 週期

        Returns:
            添加 RSI 欄位的 DataFrame
        """
        df = df.copy()

        # 計算價格變化
        delta = df['收盤價'].diff()

        # 分離上漲和下跌
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # 計算平均漲跌
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        # 計算 RS 和 RSI
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))

        return df

    # ==================== 布林通道 ====================

    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std_dev: float = 2.0) -> pd.DataFrame:
        """
        計算布林通道

        Args:
            df: 包含收盤價的 DataFrame
            period: 週期
            std_dev: 標準差倍數

        Returns:
            添加 BB 欄位的 DataFrame
        """
        df = df.copy()

        # 中軌 = 移動平均
        df['BB_Middle'] = df['收盤價'].rolling(window=period).mean()

        # 計算標準差
        std = df['收盤價'].rolling(window=period).std()

        # 上軌和下軌
        df['BB_Upper'] = df['BB_Middle'] + (std_dev * std)
        df['BB_Lower'] = df['BB_Middle'] - (std_dev * std)

        # 計算 %B (價格在布林通道中的位置)
        df['BB_Percent'] = (df['收盤價'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])

        # 計算帶寬
        df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']

        return df

    # ==================== KDJ ====================

    def calculate_kdj(self, df: pd.DataFrame, period: int = 9, k_period: int = 3, d_period: int = 3) -> pd.DataFrame:
        """
        計算 KDJ 指標

        Args:
            df: 包含 OHLC 的 DataFrame
            period: RSV 週期
            k_period: K 值平滑週期
            d_period: D 值平滑週期

        Returns:
            添加 KDJ 欄位的 DataFrame
        """
        df = df.copy()

        # 計算 RSV (未成熟隨機值)
        low_min = df['最低價'].rolling(window=period).min()
        high_max = df['最高價'].rolling(window=period).max()

        df['RSV'] = 100 * (df['收盤價'] - low_min) / (high_max - low_min)

        # 計算 K 值 (快線)
        df['K'] = df['RSV'].ewm(span=k_period, adjust=False).mean()

        # 計算 D 值 (慢線)
        df['D'] = df['K'].ewm(span=d_period, adjust=False).mean()

        # 計算 J 值
        df['J'] = 3 * df['K'] - 2 * df['D']

        return df

    # ==================== ATR ====================

    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        計算 ATR 平均真實波幅

        Args:
            df: 包含 OHLC 的 DataFrame
            period: 週期

        Returns:
            添加 ATR 欄位的 DataFrame
        """
        df = df.copy()

        # 計算真實波幅
        df['H-L'] = df['最高價'] - df['最低價']
        df['H-PC'] = abs(df['最高價'] - df['收盤價'].shift(1))
        df['L-PC'] = abs(df['最低價'] - df['收盤價'].shift(1))

        df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)

        # 計算 ATR
        df['ATR'] = df['TR'].rolling(window=period).mean()

        # 清理暫存欄位
        df.drop(['H-L', 'H-PC', 'L-PC', 'TR'], axis=1, inplace=True)

        return df

    # ==================== OBV ====================

    def calculate_obv(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        計算 OBV 能量潮指標

        Args:
            df: 包含收盤價和成交量的 DataFrame

        Returns:
            添加 OBV 欄位的 DataFrame
        """
        df = df.copy()

        # 價格變動方向
        price_change = df['收盤價'].diff()

        # OBV 計算
        obv = []
        obv_value = 0

        for i in range(len(df)):
            if i == 0:
                obv.append(df['成交量'].iloc[i])
            elif price_change.iloc[i] > 0:
                obv_value += df['成交量'].iloc[i]
                obv.append(obv_value)
            elif price_change.iloc[i] < 0:
                obv_value -= df['成交量'].iloc[i]
                obv.append(obv_value)
            else:
                obv.append(obv_value)

        df['OBV'] = obv

        return df

    # ==================== 綜合分析 ====================

    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        計算所有技術指標

        Args:
            df: 原始 OHLC DataFrame

        Returns:
            包含所有指標的 DataFrame
        """
        df = df.copy()

        # 移動平均線
        df = self.calculate_ma(df, [5, 10, 20, 60])
        df = self.calculate_ema(df, [12, 26])

        # MACD
        df = self.calculate_macd(df)

        # RSI
        df = self.calculate_rsi(df)

        # 布林通道
        df = self.calculate_bollinger_bands(df)

        # KDJ
        df = self.calculate_kdj(df)

        # ATR
        df = self.calculate_atr(df)

        # OBV
        df = self.calculate_obv(df)

        return df

    # ==================== 訊號生成 ====================

    def generate_signals(self, df: pd.DataFrame) -> Dict:
        """
        根據技術指標生成交易訊號

        Args:
            df: 包含所有指標的 DataFrame

        Returns:
            交易訊號字典
        """
        if df.empty or len(df) < 2:
            return {'綜合訊號': '資料不足', '訊號詳情': []}

        signals = []
        latest = df.iloc[-1]
        prev = df.iloc[-2]

        # 1. MA 訊號
        if 'MA5' in df.columns and 'MA20' in df.columns:
            if latest['MA5'] > latest['MA20'] and prev['MA5'] <= prev['MA20']:
                signals.append({'指標': 'MA', '訊號': '買入', '描述': 'MA5 上穿 MA20 (黃金交叉)'})
            elif latest['MA5'] < latest['MA20'] and prev['MA5'] >= prev['MA20']:
                signals.append({'指標': 'MA', '訊號': '賣出', '描述': 'MA5 下穿 MA20 (死亡交叉)'})

        # 2. MACD 訊號
        if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
            if latest['MACD'] > latest['MACD_Signal'] and prev['MACD'] <= prev['MACD_Signal']:
                signals.append({'指標': 'MACD', '訊號': '買入', '描述': 'MACD 上穿信號線'})
            elif latest['MACD'] < latest['MACD_Signal'] and prev['MACD'] >= prev['MACD_Signal']:
                signals.append({'指標': 'MACD', '訊號': '賣出', '描述': 'MACD 下穿信號線'})

        # 3. RSI 訊號
        if 'RSI' in df.columns:
            rsi = latest['RSI']
            if rsi < 30:
                signals.append({'指標': 'RSI', '訊號': '買入', '描述': f'RSI = {rsi:.1f} (超賣)'})
            elif rsi > 70:
                signals.append({'指標': 'RSI', '訊號': '賣出', '描述': f'RSI = {rsi:.1f} (超買)'})

        # 4. KDJ 訊號
        if 'K' in df.columns and 'D' in df.columns:
            k = latest['K']
            d = latest['D']
            if k > d and prev['K'] <= prev['D'] and k < 20:
                signals.append({'指標': 'KDJ', '訊號': '買入', '描述': f'K 線上穿 D 線於低檔 (K={k:.1f})'})
            elif k < d and prev['K'] >= prev['D'] and k > 80:
                signals.append({'指標': 'KDJ', '訊號': '賣出', '描述': f'K 線下穿 D 線於高檔 (K={k:.1f})'})

        # 5. 布林通道訊號
        if 'BB_Percent' in df.columns:
            bb_pct = latest['BB_Percent']
            if bb_pct < 0:
                signals.append({'指標': 'BB', '訊號': '買入', '描述': '價格跌破下軌'})
            elif bb_pct > 1:
                signals.append({'指標': 'BB', '訊號': '賣出', '描述': '價格突破上軌'})

        # 綜合訊號
        buy_count = sum(1 for s in signals if s['訊號'] == '買入')
        sell_count = sum(1 for s in signals if s['訊號'] == '賣出')

        if buy_count > sell_count and buy_count >= 2:
            overall = '強烈買入'
        elif buy_count > sell_count:
            overall = '買入'
        elif sell_count > buy_count and sell_count >= 2:
            overall = '強烈賣出'
        elif sell_count > buy_count:
            overall = '賣出'
        else:
            overall = '持有'

        return {
            '綜合訊號': overall,
            '買入訊號數': buy_count,
            '賣出訊號數': sell_count,
            '訊號詳情': signals
        }

    # ==================== 圖表繪製 ====================

    def create_candlestick_chart(self, df: pd.DataFrame, title: str = "股價走勢圖",
                                 show_volume: bool = True, show_ma: bool = True) -> go.Figure:
        """
        創建 K 線圖

        Args:
            df: 包含 OHLC 的 DataFrame
            title: 圖表標題
            show_volume: 是否顯示成交量
            show_ma: 是否顯示移動平均線

        Returns:
            Plotly Figure 對象
        """
        if show_volume:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3],
                subplot_titles=(title, '成交量')
            )
        else:
            fig = go.Figure()

        # K 線圖
        candlestick = go.Candlestick(
            x=df.index,
            open=df['開盤價'],
            high=df['最高價'],
            low=df['最低價'],
            close=df['收盤價'],
            name='K線',
            increasing_line_color='#ef4444',
            decreasing_line_color='#22c55e'
        )

        if show_volume:
            fig.add_trace(candlestick, row=1, col=1)
        else:
            fig.add_trace(candlestick)

        # 移動平均線
        if show_ma and 'MA5' in df.columns:
            ma_colors = {'MA5': '#8b5cf6', 'MA10': '#3b82f6', 'MA20': '#f59e0b', 'MA60': '#ef4444'}
            for ma in ['MA5', 'MA10', 'MA20', 'MA60']:
                if ma in df.columns:
                    trace = go.Scatter(
                        x=df.index,
                        y=df[ma],
                        name=ma,
                        line=dict(color=ma_colors[ma], width=1.5)
                    )
                    if show_volume:
                        fig.add_trace(trace, row=1, col=1)
                    else:
                        fig.add_trace(trace)

        # 成交量
        if show_volume:
            colors = ['#ef4444' if df['收盤價'].iloc[i] >= df['開盤價'].iloc[i] else '#22c55e'
                     for i in range(len(df))]

            volume_trace = go.Bar(
                x=df.index,
                y=df['成交量'],
                name='成交量',
                marker_color=colors,
                showlegend=False
            )
            fig.add_trace(volume_trace, row=2, col=1)

        # 更新版面
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            height=600 if show_volume else 500,
            hovermode='x unified',
            template='plotly_white',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')

        return fig

    def create_indicator_chart(self, df: pd.DataFrame, indicator: str) -> go.Figure:
        """
        創建技術指標圖表

        Args:
            df: 包含指標的 DataFrame
            indicator: 指標名稱 ('MACD', 'RSI', 'KDJ', 'BB')

        Returns:
            Plotly Figure 對象
        """
        if indicator == 'MACD':
            return self._create_macd_chart(df)
        elif indicator == 'RSI':
            return self._create_rsi_chart(df)
        elif indicator == 'KDJ':
            return self._create_kdj_chart(df)
        elif indicator == 'BB':
            return self._create_bb_chart(df)
        else:
            return go.Figure()

    def _create_macd_chart(self, df: pd.DataFrame) -> go.Figure:
        """創建 MACD 圖表"""
        fig = go.Figure()

        # MACD 線
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MACD'],
            name='MACD',
            line=dict(color='#3b82f6', width=2)
        ))

        # 信號線
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MACD_Signal'],
            name='Signal',
            line=dict(color='#ef4444', width=2)
        ))

        # 柱狀圖
        colors = ['#22c55e' if val >= 0 else '#ef4444' for val in df['MACD_Histogram']]
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['MACD_Histogram'],
            name='Histogram',
            marker_color=colors
        ))

        fig.update_layout(
            title='MACD 指標',
            xaxis_title='日期',
            yaxis_title='值',
            height=400,
            template='plotly_white',
            showlegend=True,
            hovermode='x unified'
        )

        return fig

    def _create_rsi_chart(self, df: pd.DataFrame) -> go.Figure:
        """創建 RSI 圖表"""
        fig = go.Figure()

        # RSI 線
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['RSI'],
            name='RSI',
            line=dict(color='#8b5cf6', width=2),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.1)'
        ))

        # 超買超賣線
        fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", annotation_text="超買 (70)")
        fig.add_hline(y=30, line_dash="dash", line_color="#22c55e", annotation_text="超賣 (30)")
        fig.add_hline(y=50, line_dash="dot", line_color="#94a3b8", annotation_text="中線 (50)")

        fig.update_layout(
            title='RSI 相對強弱指標',
            xaxis_title='日期',
            yaxis_title='RSI',
            height=400,
            template='plotly_white',
            yaxis_range=[0, 100],
            hovermode='x unified'
        )

        return fig

    def _create_kdj_chart(self, df: pd.DataFrame) -> go.Figure:
        """創建 KDJ 圖表"""
        fig = go.Figure()

        # K, D, J 線
        fig.add_trace(go.Scatter(x=df.index, y=df['K'], name='K', line=dict(color='#3b82f6', width=2)))
        fig.add_trace(go.Scatter(x=df.index, y=df['D'], name='D', line=dict(color='#ef4444', width=2)))
        fig.add_trace(go.Scatter(x=df.index, y=df['J'], name='J', line=dict(color='#8b5cf6', width=2)))

        # 超買超賣線
        fig.add_hline(y=80, line_dash="dash", line_color="#ef4444", annotation_text="超買 (80)")
        fig.add_hline(y=20, line_dash="dash", line_color="#22c55e", annotation_text="超賣 (20)")

        fig.update_layout(
            title='KDJ 隨機指標',
            xaxis_title='日期',
            yaxis_title='值',
            height=400,
            template='plotly_white',
            yaxis_range=[0, 100],
            hovermode='x unified'
        )

        return fig

    def _create_bb_chart(self, df: pd.DataFrame) -> go.Figure:
        """創建布林通道圖表"""
        fig = go.Figure()

        # 上軌
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BB_Upper'],
            name='上軌',
            line=dict(color='#ef4444', width=1, dash='dash')
        ))

        # 中軌
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BB_Middle'],
            name='中軌',
            line=dict(color='#3b82f6', width=2)
        ))

        # 下軌
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BB_Lower'],
            name='下軌',
            line=dict(color='#22c55e', width=1, dash='dash'),
            fill='tonexty',
            fillcolor='rgba(59, 130, 246, 0.1)'
        ))

        # 收盤價
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['收盤價'],
            name='收盤價',
            line=dict(color='#8b5cf6', width=2)
        ))

        fig.update_layout(
            title='布林通道',
            xaxis_title='日期',
            yaxis_title='價格',
            height=400,
            template='plotly_white',
            hovermode='x unified'
        )

        return fig

    # ==================== 公開圖表方法 (供 app.py 調用) ====================

    def create_ma_chart(self, df: pd.DataFrame) -> go.Figure:
        """創建移動平均線圖表"""
        fig = go.Figure()

        # 收盤價
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['收盤價'],
            name='收盤價',
            line=dict(color='#1e293b', width=2)
        ))

        # MA 線
        ma_colors = {'MA5': '#8b5cf6', 'MA10': '#3b82f6', 'MA20': '#f59e0b', 'MA60': '#ef4444'}
        for ma in ['MA5', 'MA10', 'MA20', 'MA60']:
            if ma in df.columns:
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[ma],
                    name=ma,
                    line=dict(color=ma_colors[ma], width=1.5)
                ))

        fig.update_layout(
            title='移動平均線',
            xaxis_title='日期',
            yaxis_title='價格',
            height=400,
            template='plotly_white',
            hovermode='x unified'
        )

        return fig

    def create_macd_chart(self, df: pd.DataFrame) -> go.Figure:
        """創建 MACD 圖表 (公開方法)"""
        return self._create_macd_chart(df)

    def create_rsi_chart(self, df: pd.DataFrame) -> go.Figure:
        """創建 RSI 圖表 (公開方法)"""
        return self._create_rsi_chart(df)

    def create_kdj_chart(self, df: pd.DataFrame) -> go.Figure:
        """創建 KDJ 圖表 (公開方法)"""
        return self._create_kdj_chart(df)

    def create_bollinger_chart(self, df: pd.DataFrame) -> go.Figure:
        """創建布林通道圖表 (公開方法)"""
        return self._create_bb_chart(df)
