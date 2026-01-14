"""
台灣股市投資分析系統 - 單元測試
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestTechnicalAnalyzer:
    """技術分析模組測試"""

    @pytest.fixture
    def analyzer(self):
        from backend.modules.technical_analyzer import TechnicalAnalyzer
        return TechnicalAnalyzer()

    @pytest.fixture
    def sample_data(self):
        """建立測試用股價資料"""
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        np.random.seed(42)

        # 生成模擬股價
        close_prices = 100 + np.cumsum(np.random.randn(100) * 2)

        df = pd.DataFrame({
            '開盤價': close_prices * (1 + np.random.randn(100) * 0.01),
            '最高價': close_prices * (1 + abs(np.random.randn(100) * 0.02)),
            '最低價': close_prices * (1 - abs(np.random.randn(100) * 0.02)),
            '收盤價': close_prices,
            '成交量': np.random.randint(1000000, 10000000, 100)
        }, index=dates)

        return df

    def test_calculate_ma(self, analyzer, sample_data):
        """測試移動平均線計算"""
        result = analyzer.calculate_ma(sample_data, periods=[5, 20])

        assert 'MA5' in result.columns
        assert 'MA20' in result.columns
        assert not result['MA5'].isna().all()

    def test_calculate_rsi(self, analyzer, sample_data):
        """測試 RSI 計算"""
        result = analyzer.calculate_rsi(sample_data, period=14)

        assert 'RSI' in result.columns
        # RSI 應該在 0-100 之間
        valid_rsi = result['RSI'].dropna()
        assert (valid_rsi >= 0).all() and (valid_rsi <= 100).all()

    def test_calculate_macd(self, analyzer, sample_data):
        """測試 MACD 計算"""
        result = analyzer.calculate_macd(sample_data)

        assert 'MACD' in result.columns
        assert 'Signal' in result.columns
        assert 'MACD_Hist' in result.columns

    def test_calculate_bollinger_bands(self, analyzer, sample_data):
        """測試布林通道計算"""
        result = analyzer.calculate_bollinger_bands(sample_data)

        assert 'BB_Upper' in result.columns
        assert 'BB_Middle' in result.columns
        assert 'BB_Lower' in result.columns

    def test_generate_signals(self, analyzer, sample_data):
        """測試交易訊號生成"""
        # 先計算所有指標
        df = analyzer.calculate_ma(sample_data, periods=[5, 20, 60])
        df = analyzer.calculate_rsi(df)
        df = analyzer.calculate_macd(df)
        df = analyzer.calculate_bollinger_bands(df)

        signals = analyzer.generate_signals(df)

        assert '綜合訊號' in signals
        assert signals['綜合訊號'] in ['買入', '賣出', '持有']


class TestWarrantAnalyzer:
    """權證分析模組測試"""

    @pytest.fixture
    def analyzer(self):
        from backend.modules.warrant_analyzer import WarrantAnalyzer
        return WarrantAnalyzer()

    def test_black_scholes_call(self, analyzer):
        """測試 Black-Scholes 買權定價"""
        # 標準測試參數
        result = analyzer.black_scholes(
            S=100,  # 股價
            K=100,  # 履約價
            T=1,    # 到期時間（年）
            r=0.05, # 無風險利率
            sigma=0.2,  # 波動率
            option_type='call'
        )

        # 價格應該為正數
        assert result > 0
        # ATM 選擇權約略等於某個合理範圍
        assert 5 < result < 15

    def test_black_scholes_put(self, analyzer):
        """測試 Black-Scholes 賣權定價"""
        result = analyzer.black_scholes(
            S=100,
            K=100,
            T=1,
            r=0.05,
            sigma=0.2,
            option_type='put'
        )

        assert result > 0

    def test_calculate_greeks(self, analyzer):
        """測試 Greeks 計算"""
        greeks = analyzer.calculate_greeks(
            S=100,
            K=100,
            T=1,
            r=0.05,
            sigma=0.2
        )

        assert 'delta' in greeks
        assert 'gamma' in greeks
        assert 'theta' in greeks
        assert 'vega' in greeks

        # Delta 應在 0-1 之間（買權）
        assert 0 <= greeks['delta'] <= 1


class TestWarrantDataFetcher:
    """權證資料獲取器測試"""

    @pytest.fixture
    def fetcher(self):
        from backend.modules.data_fetcher import WarrantDataFetcher
        return WarrantDataFetcher()

    def test_get_warrant_list(self, fetcher):
        """測試獲取權證列表"""
        # 測試獲取所有權證
        all_warrants = fetcher.get_warrant_list()
        assert not all_warrants.empty

        # 測試按股票代碼過濾
        tsmc_warrants = fetcher.get_warrant_list('2330')
        assert not tsmc_warrants.empty
        assert (tsmc_warrants['標的股票'] == '2330').all()

    def test_get_warrant_detail(self, fetcher):
        """測試獲取權證詳情"""
        # 先獲取一個權證代碼
        all_warrants = fetcher.get_warrant_list()
        if not all_warrants.empty:
            warrant_code = all_warrants.iloc[0]['權證代碼']
            detail = fetcher.get_warrant_detail(warrant_code)

            assert detail is not None
            assert '權證代碼' in detail or len(detail) > 0

    def test_nonexistent_stock(self, fetcher):
        """測試不存在的股票代碼"""
        result = fetcher.get_warrant_list('9999')
        assert result.empty


class TestStockComparator:
    """多股比較模組測試"""

    @pytest.fixture
    def mock_data_fetcher(self):
        """建立模擬的資料獲取器"""
        class MockDataFetcher:
            def get_stock_price(self, stock_id, days=90):
                dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
                np.random.seed(hash(stock_id) % 100)

                close_prices = 100 + np.cumsum(np.random.randn(days) * 2)

                return pd.DataFrame({
                    '開盤價': close_prices * 0.99,
                    '最高價': close_prices * 1.01,
                    '最低價': close_prices * 0.98,
                    '收盤價': close_prices,
                    '成交量': np.random.randint(1000000, 10000000, days)
                }, index=dates)

        return MockDataFetcher()

    def test_compare_stocks(self, mock_data_fetcher):
        """測試多股比較"""
        from backend.modules.stock_comparator import StockComparator

        comparator = StockComparator(mock_data_fetcher)
        result = comparator.compare_stocks(['2330', '2317'], days=30)

        assert 'comparison_table' in result
        assert 'stocks_data' in result
        assert result['stock_count'] == 2


class TestPortfolioManager:
    """投資組合管理模組測試"""

    @pytest.fixture
    def mock_data_fetcher(self):
        """建立模擬的資料獲取器"""
        class MockDataFetcher:
            def get_stock_price(self, stock_id, days=1):
                prices = {'2330': 680, '2317': 120, '2454': 900}
                price = prices.get(stock_id, 100)

                return pd.DataFrame({
                    '收盤價': [price]
                }, index=[datetime.now()])

        return MockDataFetcher()

    def test_add_position(self, mock_data_fetcher):
        """測試新增持倉"""
        from backend.modules.portfolio_manager import PortfolioManager

        manager = PortfolioManager(mock_data_fetcher)
        manager.add_position('2330', shares=1000, cost_price=600)

        assert '2330' in manager.portfolio
        assert manager.portfolio['2330']['shares'] == 1000

    def test_portfolio_value(self, mock_data_fetcher):
        """測試組合價值計算"""
        from backend.modules.portfolio_manager import PortfolioManager

        manager = PortfolioManager(mock_data_fetcher)
        manager.add_position('2330', shares=1000, cost_price=600)

        value = manager.get_portfolio_value()

        assert 'total_value' in value
        assert 'total_cost' in value
        assert 'positions' in value


class TestMarketSentiment:
    """市場情緒分析模組測試"""

    @pytest.fixture
    def mock_data_fetcher(self):
        """建立模擬的資料獲取器"""
        class MockDataFetcher:
            def get_stock_price(self, stock_id, days=30):
                dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
                np.random.seed(hash(stock_id) % 100)

                # 模擬上漲趨勢
                close_prices = 100 * (1 + np.cumsum(np.random.randn(days) * 0.02))

                return pd.DataFrame({
                    '開盤價': close_prices * 0.99,
                    '最高價': close_prices * 1.01,
                    '最低價': close_prices * 0.98,
                    '收盤價': close_prices,
                    '成交量': np.random.randint(1000000, 10000000, days)
                }, index=dates)

        return MockDataFetcher()

    def test_market_breadth(self, mock_data_fetcher):
        """測試市場廣度計算"""
        from backend.modules.market_sentiment import MarketSentimentAnalyzer

        analyzer = MarketSentimentAnalyzer(mock_data_fetcher)
        result = analyzer.calculate_market_breadth(
            ['2330', '2317', '2454'],
            days=30
        )

        assert '上漲家數' in result
        assert '下跌家數' in result
        assert '市場情緒' in result

    def test_fear_greed_index(self, mock_data_fetcher):
        """測試恐懼貪婪指數計算"""
        from backend.modules.market_sentiment import MarketSentimentAnalyzer

        analyzer = MarketSentimentAnalyzer(mock_data_fetcher)
        result = analyzer.calculate_fear_greed_index(
            ['2330', '2317', '2454'],
            days=30
        )

        assert '恐懼貪婪指數' in result
        # 指數應在 0-100 之間
        assert 0 <= result['恐懼貪婪指數'] <= 100


# ===== 執行測試 =====
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
