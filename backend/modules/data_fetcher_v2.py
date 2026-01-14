"""
台灣股市資料串接模組 V2
使用多種資料來源和備援方案
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
import requests
import time


class TaiwanStockDataFetcher:
    """台灣股票資料獲取器"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_stock_price(self, stock_id: str, days: int = 30) -> pd.DataFrame:
        """
        獲取股票歷史價格

        Args:
            stock_id: 股票代碼 (如 '2330')
            days: 獲取天數

        Returns:
            包含價格資訊的 DataFrame
        """
        # 嘗試多種方法
        df = self._get_from_yfinance(stock_id, days)

        if df.empty:
            print(f"提示: 使用模擬資料，因為無法從線上獲取 {stock_id} 的資料")
            df = self._generate_sample_data(stock_id, days)

        return df

    def _get_from_yfinance(self, stock_id: str, days: int) -> pd.DataFrame:
        """從 yfinance 獲取資料"""
        try:
            import yfinance as yf

            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 30)

            ticker = f"{stock_id}.TW"

            # 嘗試不同的方法
            try:
                df = yf.download(
                    ticker,
                    start=start_date,
                    end=end_date,
                    progress=False,
                    auto_adjust=True
                )
            except:
                # 嘗試使用 Ticker 物件
                stock = yf.Ticker(ticker)
                df = stock.history(start=start_date, end=end_date)

            if df.empty:
                ticker = f"{stock_id}.TWO"
                try:
                    df = yf.download(
                        ticker,
                        start=start_date,
                        end=end_date,
                        progress=False,
                        auto_adjust=True
                    )
                except:
                    stock = yf.Ticker(ticker)
                    df = stock.history(start=start_date, end=end_date)

            if not df.empty:
                df = df.rename(columns={
                    'Open': '開盤價',
                    'High': '最高價',
                    'Low': '最低價',
                    'Close': '收盤價',
                    'Volume': '成交量'
                })

                available_columns = [col for col in ['開盤價', '最高價', '最低價', '收盤價', '成交量']
                                   if col in df.columns]
                df = df[available_columns].tail(days)

            return df

        except Exception as e:
            print(f"yfinance 獲取失敗: {str(e)}")
            return pd.DataFrame()

    def _generate_sample_data(self, stock_id: str, days: int) -> pd.DataFrame:
        """
        生成模擬資料（當無法從線上獲取時使用）
        基於股票代碼生成不同的模擬價格
        """
        # 根據股票代碼設定基準價格
        base_prices = {
            '2330': 600,   # 台積電
            '2317': 100,   # 鴻海
            '2454': 800,   # 聯發科
            '2412': 120,   # 中華電
            '2882': 50,    # 國泰金
            '2881': 70,    # 富邦金
            '2886': 35,    # 兆豐金
            '2891': 25,    # 中信金
            '2303': 45,    # 聯電
            '2308': 300,   # 台達電
        }

        base_price = base_prices.get(stock_id, 100)

        # 生成日期序列
        end_date = datetime.now()
        dates = pd.date_range(end=end_date, periods=days, freq='D')

        # 生成隨機但合理的價格資料
        np.random.seed(int(stock_id))  # 使用股票代碼作為種子，確保每次生成相同

        # 生成價格趨勢
        trend = np.cumsum(np.random.randn(days) * base_price * 0.02)
        prices = base_price + trend

        # 生成 OHLC 資料
        data = []
        for i, date in enumerate(dates):
            price = prices[i]
            volatility = base_price * 0.02

            high = price + abs(np.random.randn() * volatility)
            low = price - abs(np.random.randn() * volatility)
            open_price = price + np.random.randn() * volatility * 0.5
            close_price = price + np.random.randn() * volatility * 0.5

            # 確保 high 是最高，low 是最低
            high = max(high, open_price, close_price)
            low = min(low, open_price, close_price)

            volume = abs(np.random.randn() * 10000000) + 5000000

            data.append({
                '開盤價': round(open_price, 2),
                '最高價': round(high, 2),
                '最低價': round(low, 2),
                '收盤價': round(close_price, 2),
                '成交量': int(volume)
            })

        df = pd.DataFrame(data, index=dates)
        return df

    def get_realtime_price(self, stock_id: str) -> Dict:
        """獲取即時股價"""
        try:
            df = self.get_stock_price(stock_id, days=5)

            if df.empty:
                return {}

            latest = df.iloc[-1]

            return {
                '股票代碼': stock_id,
                '股票名稱': self._get_stock_name(stock_id),
                '當前價格': float(latest['收盤價']),
                '開盤價': float(latest['開盤價']),
                '最高價': float(latest['最高價']),
                '最低價': float(latest['最低價']),
                '成交量': int(latest['成交量']),
                '時間': str(df.index[-1].date())
            }

        except Exception as e:
            print(f"獲取即時股價失敗: {str(e)}")
            return {}

    def get_stock_info(self, stock_id: str) -> Dict:
        """獲取股票基本資訊"""
        # 預設的股票資訊
        stock_names = {
            '2330': '台積電',
            '2317': '鴻海',
            '2454': '聯發科',
            '2412': '中華電',
            '2882': '國泰金',
            '2881': '富邦金',
            '2886': '兆豐金',
            '2891': '中信金',
            '2303': '聯電',
            '2308': '台達電',
        }

        industries = {
            '2330': '半導體業',
            '2317': '電子製造',
            '2454': '半導體業',
            '2412': '通信網路業',
            '2882': '金融保險業',
            '2881': '金融保險業',
            '2886': '金融保險業',
            '2891': '金融保險業',
            '2303': '半導體業',
            '2308': '電子零組件',
        }

        return {
            '股票代碼': stock_id,
            '公司名稱': stock_names.get(stock_id, f'股票 {stock_id}'),
            '產業': industries.get(stock_id, 'N/A'),
            '市值': 'N/A',
            '本益比': 'N/A',
            '股價淨值比': 'N/A',
            '52週最高': 'N/A',
            '52週最低': 'N/A',
        }

    def _get_stock_name(self, stock_id: str) -> str:
        """取得股票名稱"""
        names = {
            '2330': '台積電',
            '2317': '鴻海',
            '2454': '聯發科',
            '2412': '中華電',
            '2882': '國泰金',
            '2881': '富邦金',
            '2886': '兆豐金',
            '2891': '中信金',
            '2303': '聯電',
            '2308': '台達電',
        }
        return names.get(stock_id, f'股票 {stock_id}')

    def get_top_stocks(self) -> List[Dict]:
        """獲取熱門股票列表"""
        popular_stocks = ['2330', '2317', '2454', '2412', '2882',
                         '2881', '2886', '2891', '2303', '2308']

        result = []
        for stock_id in popular_stocks:
            realtime = self.get_realtime_price(stock_id)
            if realtime:
                result.append(realtime)

        return result


class WarrantDataFetcher:
    """權證資料獲取器"""

    def __init__(self):
        pass

    def get_warrant_list(self, stock_id: str = None) -> pd.DataFrame:
        """獲取權證列表（示範資料）"""
        sample_data = {
            '權證代碼': ['123456', '123457', '123458'],
            '權證名稱': ['XX認購01', 'YY認購02', 'ZZ認售01'],
            '標的股票': ['2330', '2317', '2454'],
            '行使比例': [0.5, 0.3, 0.4],
            '履約價': [600, 100, 800],
            '到期日': ['2024-12-31', '2024-11-30', '2024-10-31'],
            '隱含波動率': [25.5, 30.2, 28.7],
            '實質槓桿': [5.2, 6.1, 4.8],
            '權證價格': [10.0, 5.0, 12.0],
        }

        df = pd.DataFrame(sample_data)

        if stock_id:
            df = df[df['標的股票'] == stock_id]

        return df

    def calculate_warrant_value(self, warrant_info: Dict) -> Dict:
        """計算權證價值"""
        return {
            '理論價值': 'N/A',
            '內含價值': 'N/A',
            '時間價值': 'N/A',
            '建議': '需要更詳細的市場資料進行計算'
        }
