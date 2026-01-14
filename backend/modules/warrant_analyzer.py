"""
權證分析與推薦模組
提供權證評估、篩選和推薦功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta
from scipy.stats import norm


class WarrantAnalyzer:
    """權證分析器"""

    def __init__(self):
        self.risk_free_rate = 0.01  # 無風險利率（年化）

    def black_scholes_call(self, S: float, K: float, T: float, r: float, sigma: float) -> float:
        """
        Black-Scholes 認購權證定價公式

        Args:
            S: 當前股價
            K: 履約價
            T: 到期時間（年）
            r: 無風險利率
            sigma: 波動率

        Returns:
            理論價格
        """
        if T <= 0:
            return max(S - K, 0)

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

        return call_price

    def black_scholes_put(self, S: float, K: float, T: float, r: float, sigma: float) -> float:
        """
        Black-Scholes 認售權證定價公式

        Args:
            S: 當前股價
            K: 履約價
            T: 到期時間（年）
            r: 無風險利率
            sigma: 波動率

        Returns:
            理論價格
        """
        if T <= 0:
            return max(K - S, 0)

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return put_price

    def calculate_warrant_greeks(self, warrant_type: str, S: float, K: float,
                                  T: float, r: float, sigma: float) -> Dict:
        """
        計算權證的 Greeks（敏感度指標）

        Args:
            warrant_type: 'call' 或 'put'
            S: 當前股價
            K: 履約價
            T: 到期時間（年）
            r: 無風險利率
            sigma: 波動率

        Returns:
            Greeks 字典
        """
        if T <= 0:
            return {
                'Delta': 0,
                'Gamma': 0,
                'Theta': 0,
                'Vega': 0,
                'Rho': 0
            }

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        # Delta
        if warrant_type.lower() == 'call':
            delta = norm.cdf(d1)
        else:
            delta = norm.cdf(d1) - 1

        # Gamma
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))

        # Theta（每日時間價值衰減）
        theta_annual = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
        theta = theta_annual / 365

        # Vega（波動率敏感度）
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100

        # Rho（利率敏感度）
        if warrant_type.lower() == 'call':
            rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
        else:
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

        return {
            'Delta': delta,
            'Gamma': gamma,
            'Theta': theta,
            'Vega': vega,
            'Rho': rho
        }

    def calculate_intrinsic_value(self, warrant_type: str, stock_price: float,
                                   strike_price: float, conversion_ratio: float) -> float:
        """
        計算權證內含價值

        Args:
            warrant_type: 'call' 或 'put'
            stock_price: 當前股價
            strike_price: 履約價
            conversion_ratio: 行使比例

        Returns:
            內含價值
        """
        if warrant_type.lower() == 'call':
            intrinsic = max(stock_price - strike_price, 0) * conversion_ratio
        else:
            intrinsic = max(strike_price - stock_price, 0) * conversion_ratio

        return intrinsic

    def calculate_time_value(self, warrant_price: float, intrinsic_value: float) -> float:
        """
        計算時間價值

        Args:
            warrant_price: 權證市價
            intrinsic_value: 內含價值

        Returns:
            時間價值
        """
        return max(warrant_price - intrinsic_value, 0)

    def calculate_leverage(self, stock_price: float, warrant_price: float,
                           delta: float, conversion_ratio: float) -> Dict:
        """
        計算槓桿指標

        Args:
            stock_price: 股票價格
            warrant_price: 權證價格
            delta: Delta 值
            conversion_ratio: 行使比例

        Returns:
            槓桿指標字典
        """
        if warrant_price == 0:
            return {'理論槓桿': 0, '實質槓桿': 0}

        # 理論槓桿 = (股票價格 × 行使比例) / 權證價格
        theoretical_leverage = (stock_price * conversion_ratio) / warrant_price

        # 實質槓桿 = 理論槓桿 × Delta
        effective_leverage = theoretical_leverage * abs(delta)

        return {
            '理論槓桿': theoretical_leverage,
            '實質槓桿': effective_leverage
        }

    def calculate_break_even(self, warrant_type: str, strike_price: float,
                             warrant_price: float, conversion_ratio: float) -> float:
        """
        計算損益兩平點

        Args:
            warrant_type: 'call' 或 'put'
            strike_price: 履約價
            warrant_price: 權證價格
            conversion_ratio: 行使比例

        Returns:
            損益兩平股價
        """
        if conversion_ratio == 0:
            return 0

        if warrant_type.lower() == 'call':
            break_even = strike_price + (warrant_price / conversion_ratio)
        else:
            break_even = strike_price - (warrant_price / conversion_ratio)

        return break_even

    def analyze_warrant(self, warrant_info: Dict, stock_price: float, volatility: float = 0.3) -> Dict:
        """
        完整的權證分析

        Args:
            warrant_info: 權證資訊字典
            stock_price: 當前股價
            volatility: 波動率（預設30%）

        Returns:
            分析結果
        """
        try:
            warrant_type = 'call' if '認購' in warrant_info.get('權證名稱', '') else 'put'
            strike_price = float(warrant_info.get('履約價', 0))
            conversion_ratio = float(warrant_info.get('行使比例', 0))
            expiry_date = pd.to_datetime(warrant_info.get('到期日', ''))
            current_date = pd.Timestamp.now()

            # 計算到期時間（年）
            days_to_expiry = (expiry_date - current_date).days
            time_to_expiry = max(days_to_expiry / 365, 0)

            # 計算理論價格
            if warrant_type == 'call':
                theoretical_price = self.black_scholes_call(
                    stock_price, strike_price, time_to_expiry, self.risk_free_rate, volatility
                ) * conversion_ratio
            else:
                theoretical_price = self.black_scholes_put(
                    stock_price, strike_price, time_to_expiry, self.risk_free_rate, volatility
                ) * conversion_ratio

            # 計算 Greeks
            greeks = self.calculate_warrant_greeks(
                warrant_type, stock_price, strike_price, time_to_expiry, self.risk_free_rate, volatility
            )

            # 計算內含價值和時間價值
            intrinsic_value = self.calculate_intrinsic_value(
                warrant_type, stock_price, strike_price, conversion_ratio
            )

            warrant_price = float(warrant_info.get('權證價格', theoretical_price))
            time_value = self.calculate_time_value(warrant_price, intrinsic_value)

            # 計算槓桿
            leverage = self.calculate_leverage(
                stock_price, warrant_price, greeks['Delta'], conversion_ratio
            )

            # 計算損益兩平點
            break_even = self.calculate_break_even(
                warrant_type, strike_price, warrant_price, conversion_ratio
            )

            # 價內外狀態
            moneyness = self._get_moneyness(warrant_type, stock_price, strike_price)

            # 評分
            score = self._calculate_warrant_score(
                intrinsic_value, time_value, leverage['實質槓桿'],
                greeks['Delta'], days_to_expiry, moneyness
            )

            return {
                '權證代碼': warrant_info.get('權證代碼', 'N/A'),
                '權證名稱': warrant_info.get('權證名稱', 'N/A'),
                '權證類型': '認購' if warrant_type == 'call' else '認售',
                '標的股票': warrant_info.get('標的股票', 'N/A'),
                '當前股價': stock_price,
                '履約價': strike_price,
                '行使比例': conversion_ratio,
                '到期天數': days_to_expiry,
                '理論價格': f'{theoretical_price:.2f}',
                '市場價格': f'{warrant_price:.2f}',
                '內含價值': f'{intrinsic_value:.2f}',
                '時間價值': f'{time_value:.2f}',
                '價內外狀態': moneyness,
                '損益兩平點': f'{break_even:.2f}',
                'Delta': f'{greeks["Delta"]:.4f}',
                'Gamma': f'{greeks["Gamma"]:.6f}',
                'Theta': f'{greeks["Theta"]:.4f}',
                'Vega': f'{greeks["Vega"]:.4f}',
                '理論槓桿': f'{leverage["理論槓桿"]:.2f}',
                '實質槓桿': f'{leverage["實質槓桿"]:.2f}',
                '綜合評分': score,
                '投資建議': self._get_recommendation(score, moneyness, days_to_expiry)
            }

        except Exception as e:
            return {'錯誤': f'分析失敗: {str(e)}'}

    def _get_moneyness(self, warrant_type: str, stock_price: float, strike_price: float) -> str:
        """判斷價內外狀態"""
        if warrant_type == 'call':
            if stock_price > strike_price * 1.05:
                return '深度價內'
            elif stock_price > strike_price:
                return '價內'
            elif stock_price > strike_price * 0.95:
                return '價平'
            else:
                return '價外'
        else:
            if stock_price < strike_price * 0.95:
                return '深度價內'
            elif stock_price < strike_price:
                return '價內'
            elif stock_price < strike_price * 1.05:
                return '價平'
            else:
                return '價外'

    def _calculate_warrant_score(self, intrinsic: float, time_value: float,
                                  leverage: float, delta: float, days: int, moneyness: str) -> int:
        """計算權證綜合評分（0-100）"""
        score = 50  # 基礎分數

        # 價內外狀態評分
        if moneyness == '深度價內':
            score += 15
        elif moneyness == '價內':
            score += 10
        elif moneyness == '價平':
            score += 5

        # 時間價值評分（時間價值越低越好）
        if time_value < intrinsic * 0.1:
            score += 15
        elif time_value < intrinsic * 0.3:
            score += 10
        elif time_value < intrinsic * 0.5:
            score += 5

        # 槓桿評分（適中的槓桿）
        if 3 <= leverage <= 6:
            score += 10
        elif 2 <= leverage <= 8:
            score += 5

        # Delta 評分
        if abs(delta) > 0.6:
            score += 10
        elif abs(delta) > 0.4:
            score += 5

        # 到期時間評分（太短不好）
        if days > 90:
            score += 10
        elif days > 60:
            score += 5
        elif days < 30:
            score -= 10

        return min(max(score, 0), 100)

    def _get_recommendation(self, score: int, moneyness: str, days: int) -> str:
        """根據評分給出建議"""
        if days < 30:
            return '⚠️ 到期時間過短，風險較高，不建議新進場'

        if score >= 80:
            return '✅ 優質標的，建議買入'
        elif score >= 65:
            return '👍 良好標的，可考慮買入'
        elif score >= 50:
            return '⚖️ 中等標的，謹慎評估'
        elif score >= 35:
            return '⚠️ 風險較高，不建議買入'
        else:
            return '❌ 不建議投資'

    def screen_warrants(self, warrants_df: pd.DataFrame, stock_price: float,
                        filters: Dict = None) -> pd.DataFrame:
        """
        篩選權證

        Args:
            warrants_df: 權證列表 DataFrame
            stock_price: 當前股價
            filters: 篩選條件字典

        Returns:
            篩選後的權證列表
        """
        if filters is None:
            filters = {
                '最小到期天數': 30,
                '最大實質槓桿': 10,
                '最小Delta': 0.3
            }

        result = []
        for _, warrant in warrants_df.iterrows():
            analysis = self.analyze_warrant(warrant.to_dict(), stock_price)

            if '錯誤' in analysis:
                continue

            # 套用篩選條件
            if analysis['到期天數'] < filters.get('最小到期天數', 0):
                continue

            if float(analysis['實質槓桿']) > filters.get('最大實質槓桿', 999):
                continue

            if abs(float(analysis['Delta'])) < filters.get('最小Delta', 0):
                continue

            result.append(analysis)

        return pd.DataFrame(result).sort_values('綜合評分', ascending=False)

    def recommend_warrants(self, warrants_df: pd.DataFrame, stock_price: float, top_n: int = 5) -> List[Dict]:
        """
        推薦權證

        Args:
            warrants_df: 權證列表
            stock_price: 當前股價
            top_n: 推薦數量

        Returns:
            推薦權證列表
        """
        screened = self.screen_warrants(warrants_df, stock_price)

        if screened.empty:
            return []

        return screened.head(top_n).to_dict('records')
