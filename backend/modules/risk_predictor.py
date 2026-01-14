"""
風險預測模組
使用多種指標評估投資風險
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from sklearn.preprocessing import StandardScaler


class RiskPredictor:
    """風險預測器"""

    def __init__(self):
        self.scaler = StandardScaler()

    def calculate_volatility(self, prices: pd.Series, window: int = 20) -> float:
        """
        計算波動率（標準差）

        Args:
            prices: 價格序列
            window: 計算窗口

        Returns:
            波動率（年化）
        """
        returns = prices.pct_change().dropna()
        volatility = returns.rolling(window=window).std().iloc[-1]

        # 年化波動率（假設一年有 252 個交易日）
        annual_volatility = volatility * np.sqrt(252)

        return annual_volatility * 100  # 轉換為百分比

    def calculate_var(self, prices: pd.Series, confidence: float = 0.95) -> Dict:
        """
        計算 Value at Risk (VaR)

        Args:
            prices: 價格序列
            confidence: 信賴水準

        Returns:
            VaR 相關資訊
        """
        returns = prices.pct_change().dropna()

        # 歷史模擬法
        var_value = np.percentile(returns, (1 - confidence) * 100)

        # Conditional VaR (CVaR) - 超過 VaR 的平均損失
        cvar_value = returns[returns <= var_value].mean()

        return {
            'VaR': var_value * 100,  # 轉換為百分比
            'CVaR': cvar_value * 100,
            '信賴水準': confidence * 100,
            '解釋': f'有 {confidence*100}% 的信心，單日最大損失不會超過 {abs(var_value)*100:.2f}%'
        }

    def calculate_beta(self, stock_prices: pd.Series, market_prices: pd.Series) -> float:
        """
        計算 Beta 值（相對於大盤的波動）

        Args:
            stock_prices: 股票價格
            market_prices: 市場指數價格

        Returns:
            Beta 值
        """
        stock_returns = stock_prices.pct_change().dropna()
        market_returns = market_prices.pct_change().dropna()

        # 確保兩個序列長度一致
        common_index = stock_returns.index.intersection(market_returns.index)
        stock_returns = stock_returns.loc[common_index]
        market_returns = market_returns.loc[common_index]

        # 計算協方差和變異數
        covariance = np.cov(stock_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)

        beta = covariance / market_variance if market_variance != 0 else 1.0

        return beta

    def calculate_sharpe_ratio(self, prices: pd.Series, risk_free_rate: float = 0.01) -> float:
        """
        計算 Sharpe Ratio

        Args:
            prices: 價格序列
            risk_free_rate: 無風險利率（年化）

        Returns:
            Sharpe Ratio
        """
        returns = prices.pct_change().dropna()

        # 計算平均報酬率和標準差（年化）
        avg_return = returns.mean() * 252
        std_return = returns.std() * np.sqrt(252)

        sharpe_ratio = (avg_return - risk_free_rate) / std_return if std_return != 0 else 0

        return sharpe_ratio

    def calculate_max_drawdown(self, prices: pd.Series) -> Dict:
        """
        計算最大回撤

        Args:
            prices: 價格序列

        Returns:
            最大回撤資訊
        """
        # 計算累積報酬
        cumulative = (1 + prices.pct_change()).cumprod()

        # 計算滾動最大值
        running_max = cumulative.expanding().max()

        # 計算回撤
        drawdown = (cumulative - running_max) / running_max

        max_drawdown = drawdown.min()
        max_drawdown_date = drawdown.idxmin()

        return {
            '最大回撤': max_drawdown * 100,  # 轉換為百分比
            '發生日期': str(max_drawdown_date),
            '解釋': f'從歷史高點下跌的最大幅度為 {abs(max_drawdown)*100:.2f}%'
        }

    def assess_risk_level(self, volatility: float, beta: float, sharpe_ratio: float) -> Dict:
        """
        綜合評估風險等級

        Args:
            volatility: 波動率
            beta: Beta 值
            sharpe_ratio: Sharpe Ratio

        Returns:
            風險評估結果
        """
        risk_score = 0

        # 波動率評分（0-40分）
        if volatility < 20:
            vol_score = 0
            vol_level = '低'
        elif volatility < 30:
            vol_score = 15
            vol_level = '中'
        elif volatility < 40:
            vol_score = 30
            vol_level = '中高'
        else:
            vol_score = 40
            vol_level = '高'

        # Beta 評分（0-30分）
        if abs(beta) < 0.8:
            beta_score = 0
            beta_level = '低'
        elif abs(beta) < 1.2:
            beta_score = 15
            beta_level = '中'
        else:
            beta_score = 30
            beta_level = '高'

        # Sharpe Ratio 評分（0-30分，分數越高風險越低）
        if sharpe_ratio > 1:
            sharpe_score = 0
            sharpe_level = '優良'
        elif sharpe_ratio > 0:
            sharpe_score = 15
            sharpe_level = '尚可'
        else:
            sharpe_score = 30
            sharpe_level = '不佳'

        risk_score = vol_score + beta_score + sharpe_score

        # 判定總體風險等級
        if risk_score < 25:
            risk_level = '低風險'
            risk_color = 'green'
        elif risk_score < 50:
            risk_level = '中風險'
            risk_color = 'yellow'
        elif risk_score < 75:
            risk_level = '中高風險'
            risk_color = 'orange'
        else:
            risk_level = '高風險'
            risk_color = 'red'

        return {
            '風險等級': risk_level,
            '風險分數': risk_score,
            '風險顏色': risk_color,
            '波動率等級': vol_level,
            'Beta等級': beta_level,
            'Sharpe比率等級': sharpe_level,
            '建議': self._get_risk_recommendation(risk_level)
        }

    def _get_risk_recommendation(self, risk_level: str) -> str:
        """根據風險等級提供建議"""
        recommendations = {
            '低風險': '適合穩健型投資者，可考慮長期持有',
            '中風險': '適合一般投資者，建議設定停損點',
            '中高風險': '需要較高風險承受度，建議分批進場並嚴格控制部位',
            '高風險': '僅適合積極型投資者，務必做好風險管理並控制投資比例'
        }
        return recommendations.get(risk_level, '請謹慎評估')

    def predict_risk(self, df: pd.DataFrame, market_df: pd.DataFrame = None) -> Dict:
        """
        完整的風險預測分析

        Args:
            df: 股票歷史資料
            market_df: 市場指數資料（選填）

        Returns:
            完整風險分析報告
        """
        if df.empty or '收盤價' not in df.columns:
            return {'錯誤': '資料不足或格式錯誤'}

        prices = df['收盤價']

        # 計算各項指標
        volatility = self.calculate_volatility(prices)
        var_info = self.calculate_var(prices)
        max_dd_info = self.calculate_max_drawdown(prices)
        sharpe = self.calculate_sharpe_ratio(prices)

        # 如果有市場資料，計算 Beta
        beta = 1.0
        if market_df is not None and not market_df.empty and '收盤價' in market_df.columns:
            beta = self.calculate_beta(prices, market_df['收盤價'])

        # 綜合評估
        risk_assessment = self.assess_risk_level(volatility, beta, sharpe)

        return {
            '波動率': f'{volatility:.2f}%',
            'VaR資訊': var_info,
            'Beta': f'{beta:.2f}',
            'Sharpe Ratio': f'{sharpe:.2f}',
            '最大回撤': max_dd_info,
            '風險評估': risk_assessment,
            '分析時間': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }
