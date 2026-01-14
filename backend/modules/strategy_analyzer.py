"""
投資策略分析模組
提供多種技術分析指標和交易策略
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import ta


class StrategyAnalyzer:
    """投資策略分析器"""

    def __init__(self):
        pass

    def calculate_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        計算移動平均線

        Args:
            df: 包含價格資料的 DataFrame

        Returns:
            添加了移動平均線的 DataFrame
        """
        if '收盤價' not in df.columns:
            return df

        df = df.copy()
        df['MA5'] = df['收盤價'].rolling(window=5).mean()
        df['MA10'] = df['收盤價'].rolling(window=10).mean()
        df['MA20'] = df['收盤價'].rolling(window=20).mean()
        df['MA60'] = df['收盤價'].rolling(window=60).mean()

        return df

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        計算 RSI 指標

        Args:
            df: 包含價格資料的 DataFrame
            period: RSI 週期

        Returns:
            添加了 RSI 的 DataFrame
        """
        if '收盤價' not in df.columns:
            return df

        df = df.copy()
        df['RSI'] = ta.momentum.RSIIndicator(df['收盤價'], window=period).rsi()

        return df

    def calculate_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        計算 MACD 指標

        Args:
            df: 包含價格資料的 DataFrame

        Returns:
            添加了 MACD 的 DataFrame
        """
        if '收盤價' not in df.columns:
            return df

        df = df.copy()
        macd = ta.trend.MACD(df['收盤價'])

        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Diff'] = macd.macd_diff()

        return df

    def calculate_bollinger_bands(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        計算布林通道

        Args:
            df: 包含價格資料的 DataFrame
            window: 計算窗口

        Returns:
            添加了布林通道的 DataFrame
        """
        if '收盤價' not in df.columns:
            return df

        df = df.copy()
        bollinger = ta.volatility.BollingerBands(df['收盤價'], window=window)

        df['BB_Upper'] = bollinger.bollinger_hband()
        df['BB_Middle'] = bollinger.bollinger_mavg()
        df['BB_Lower'] = bollinger.bollinger_lband()

        return df

    def calculate_kdj(self, df: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3) -> pd.DataFrame:
        """
        計算 KDJ 指標

        Args:
            df: 包含價格資料的 DataFrame
            n: KD 週期
            m1: K 平滑參數
            m2: D 平滑參數

        Returns:
            添加了 KDJ 的 DataFrame
        """
        if not all(col in df.columns for col in ['最高價', '最低價', '收盤價']):
            return df

        df = df.copy()

        low_list = df['最低價'].rolling(window=n, min_periods=n).min()
        high_list = df['最高價'].rolling(window=n, min_periods=n).max()

        rsv = (df['收盤價'] - low_list) / (high_list - low_list) * 100

        df['K'] = rsv.ewm(com=m1-1, adjust=False).mean()
        df['D'] = df['K'].ewm(com=m2-1, adjust=False).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']

        return df

    def generate_ma_signals(self, df: pd.DataFrame) -> Dict:
        """
        生成移動平均線交易信號

        Args:
            df: 包含移動平均線的 DataFrame

        Returns:
            交易信號字典
        """
        if not all(col in df.columns for col in ['收盤價', 'MA5', 'MA20']):
            return {'信號': '資料不足', '強度': 0}

        latest = df.iloc[-1]
        price = latest['收盤價']
        ma5 = latest['MA5']
        ma20 = latest['MA20']

        signals = []
        strength = 0

        # 黃金交叉 / 死亡交叉
        if ma5 > ma20:
            signals.append('短期均線在長期均線之上（多頭排列）')
            strength += 30
        else:
            signals.append('短期均線在長期均線之下（空頭排列）')
            strength -= 30

        # 價格與均線關係
        if price > ma5 > ma20:
            signals.append('價格突破所有均線（強勢上漲）')
            strength += 40
        elif price < ma5 < ma20:
            signals.append('價格跌破所有均線（弱勢下跌）')
            strength -= 40

        # 判斷信號
        if strength > 40:
            signal = '強烈買入'
        elif strength > 0:
            signal = '買入'
        elif strength > -40:
            signal = '賣出'
        else:
            signal = '強烈賣出'

        return {
            '信號': signal,
            '強度': strength,
            '原因': signals
        }

    def generate_rsi_signals(self, df: pd.DataFrame) -> Dict:
        """
        生成 RSI 交易信號

        Args:
            df: 包含 RSI 的 DataFrame

        Returns:
            交易信號字典
        """
        if 'RSI' not in df.columns:
            return {'信號': '資料不足', '強度': 0}

        latest_rsi = df['RSI'].iloc[-1]

        if pd.isna(latest_rsi):
            return {'信號': '資料不足', '強度': 0}

        if latest_rsi < 30:
            signal = '超賣，考慮買入'
            strength = 40
        elif latest_rsi < 50:
            signal = '偏空，觀望'
            strength = -20
        elif latest_rsi < 70:
            signal = '偏多，持有'
            strength = 20
        else:
            signal = '超買，考慮賣出'
            strength = -40

        return {
            '信號': signal,
            'RSI值': f'{latest_rsi:.2f}',
            '強度': strength,
            '說明': 'RSI < 30 為超賣，RSI > 70 為超買'
        }

    def generate_macd_signals(self, df: pd.DataFrame) -> Dict:
        """
        生成 MACD 交易信號

        Args:
            df: 包含 MACD 的 DataFrame

        Returns:
            交易信號字典
        """
        if 'MACD' not in df.columns or 'MACD_Signal' not in df.columns:
            return {'信號': '資料不足', '強度': 0}

        latest = df.iloc[-1]
        macd = latest['MACD']
        signal_line = latest['MACD_Signal']
        diff = latest['MACD_Diff']

        if pd.isna(macd) or pd.isna(signal_line):
            return {'信號': '資料不足', '強度': 0}

        signals = []
        strength = 0

        # MACD 與信號線交叉
        if macd > signal_line and diff > 0:
            signals.append('MACD 在信號線之上（黃金交叉）')
            strength += 35
        elif macd < signal_line and diff < 0:
            signals.append('MACD 在信號線之下（死亡交叉）')
            strength -= 35

        # MACD 正負值
        if macd > 0:
            signals.append('MACD 為正值（多頭市場）')
            strength += 15
        else:
            signals.append('MACD 為負值（空頭市場）')
            strength -= 15

        # 判斷信號
        if strength > 30:
            signal = '買入'
        elif strength > 0:
            signal = '偏多'
        elif strength > -30:
            signal = '偏空'
        else:
            signal = '賣出'

        return {
            '信號': signal,
            '強度': strength,
            '原因': signals
        }

    def generate_kdj_signals(self, df: pd.DataFrame) -> Dict:
        """
        生成 KDJ 交易信號

        Args:
            df: 包含 KDJ 的 DataFrame

        Returns:
            交易信號字典
        """
        if not all(col in df.columns for col in ['K', 'D', 'J']):
            return {'信號': '資料不足', '強度': 0}

        latest = df.iloc[-1]
        k = latest['K']
        d = latest['D']
        j = latest['J']

        if pd.isna(k) or pd.isna(d) or pd.isna(j):
            return {'信號': '資料不足', '強度': 0}

        signals = []
        strength = 0

        # 超買超賣判斷
        if k < 20 and d < 20:
            signals.append('KD 值低於 20（超賣區）')
            strength += 40
        elif k > 80 and d > 80:
            signals.append('KD 值高於 80（超買區）')
            strength -= 40

        # KD 交叉
        if k > d:
            signals.append('K 線在 D 線之上（黃金交叉）')
            strength += 20
        else:
            signals.append('K 線在 D 線之下（死亡交叉）')
            strength -= 20

        # 判斷信號
        if strength > 40:
            signal = '強烈買入'
        elif strength > 0:
            signal = '買入'
        elif strength > -40:
            signal = '賣出'
        else:
            signal = '強烈賣出'

        return {
            '信號': signal,
            'K值': f'{k:.2f}',
            'D值': f'{d:.2f}',
            'J值': f'{j:.2f}',
            '強度': strength,
            '原因': signals
        }

    def comprehensive_analysis(self, df: pd.DataFrame) -> Dict:
        """
        綜合技術分析

        Args:
            df: 價格資料 DataFrame

        Returns:
            綜合分析結果
        """
        # 計算所有指標
        df = self.calculate_moving_averages(df)
        df = self.calculate_rsi(df)
        df = self.calculate_macd(df)
        df = self.calculate_kdj(df)
        df = self.calculate_bollinger_bands(df)

        # 生成各項信號
        ma_signals = self.generate_ma_signals(df)
        rsi_signals = self.generate_rsi_signals(df)
        macd_signals = self.generate_macd_signals(df)
        kdj_signals = self.generate_kdj_signals(df)

        # 計算綜合強度
        total_strength = (
            ma_signals.get('強度', 0) +
            rsi_signals.get('強度', 0) +
            macd_signals.get('強度', 0) +
            kdj_signals.get('強度', 0)
        ) / 4

        # 綜合建議
        if total_strength > 30:
            recommendation = '強烈建議買入'
            action = 'BUY'
        elif total_strength > 10:
            recommendation = '建議買入'
            action = 'BUY'
        elif total_strength > -10:
            recommendation = '持有觀望'
            action = 'HOLD'
        elif total_strength > -30:
            recommendation = '建議賣出'
            action = 'SELL'
        else:
            recommendation = '強烈建議賣出'
            action = 'SELL'

        return {
            '綜合評分': f'{total_strength:.2f}',
            '操作建議': recommendation,
            '操作方向': action,
            '移動平均線分析': ma_signals,
            'RSI分析': rsi_signals,
            'MACD分析': macd_signals,
            'KDJ分析': kdj_signals,
            '分析資料': df,
            '分析時間': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def backtest_strategy(self, df: pd.DataFrame, initial_capital: float = 100000) -> Dict:
        """
        簡單的策略回測

        Args:
            df: 歷史資料
            initial_capital: 初始資金

        Returns:
            回測結果
        """
        if df.empty or '收盤價' not in df.columns:
            return {'錯誤': '資料不足'}

        df = self.calculate_moving_averages(df)
        df = self.calculate_rsi(df)

        capital = initial_capital
        position = 0
        trades = []

        for i in range(1, len(df)):
            if pd.isna(df['MA5'].iloc[i]) or pd.isna(df['MA20'].iloc[i]):
                continue

            # 簡單策略：MA5 突破 MA20 買入，跌破賣出
            if df['MA5'].iloc[i] > df['MA20'].iloc[i] and df['MA5'].iloc[i-1] <= df['MA20'].iloc[i-1]:
                # 買入信號
                if position == 0:
                    position = capital / df['收盤價'].iloc[i]
                    trades.append({
                        '日期': df.index[i],
                        '動作': '買入',
                        '價格': df['收盤價'].iloc[i],
                        '股數': position
                    })

            elif df['MA5'].iloc[i] < df['MA20'].iloc[i] and df['MA5'].iloc[i-1] >= df['MA20'].iloc[i-1]:
                # 賣出信號
                if position > 0:
                    capital = position * df['收盤價'].iloc[i]
                    trades.append({
                        '日期': df.index[i],
                        '動作': '賣出',
                        '價格': df['收盤價'].iloc[i],
                        '資金': capital
                    })
                    position = 0

        # 如果最後還有持倉，以最後價格計算
        if position > 0:
            capital = position * df['收盤價'].iloc[-1]

        profit = capital - initial_capital
        profit_rate = (profit / initial_capital) * 100

        return {
            '初始資金': initial_capital,
            '最終資金': capital,
            '獲利': profit,
            '報酬率': f'{profit_rate:.2f}%',
            '交易次數': len(trades),
            '交易明細': trades
        }
