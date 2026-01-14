"""
台灣股市資料串接模組
支援從多個來源獲取台股資料
"""

import twstock
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import requests
from bs4 import BeautifulSoup


class TaiwanStockDataFetcher:
    """台灣股票資料獲取器"""

    def __init__(self):
        self.stock = twstock.Stock

    def get_stock_price(self, stock_id: str, days: int = 30) -> pd.DataFrame:
        """
        獲取股票歷史價格

        Args:
            stock_id: 股票代碼 (如 '2330')
            days: 獲取天數

        Returns:
            包含價格資訊的 DataFrame
        """
        # 直接使用 yfinance，因為 twstock 有相容性問題
        return self._get_price_from_yfinance(stock_id, days)

    def _get_price_from_yfinance(self, stock_id: str, days: int = 30) -> pd.DataFrame:
        """使用 yfinance 獲取資料"""
        try:
            # 計算日期範圍
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 30)  # 多抓一些以確保有足夠資料

            # 台股代碼需要加上 .TW 後綴
            ticker = f"{stock_id}.TW"

            # 使用 download 方法，更穩定
            df = yf.download(
                ticker,
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                progress=False,
                show_errors=False
            )

            if df.empty:
                # 嘗試 .TWO (櫃買中心)
                ticker = f"{stock_id}.TWO"
                df = yf.download(
                    ticker,
                    start=start_date.strftime('%Y-%m-%d'),
                    end=end_date.strftime('%Y-%m-%d'),
                    progress=False,
                    show_errors=False
                )

            if df.empty:
                print(f"警告: 無法從 yfinance 獲取 {stock_id} 的資料")
                return pd.DataFrame()

            # 重新命名欄位為中文
            df = df.rename(columns={
                'Open': '開盤價',
                'High': '最高價',
                'Low': '最低價',
                'Close': '收盤價',
                'Volume': '成交量'
            })

            # 只保留需要的欄位，並取最近的天數
            available_columns = [col for col in ['開盤價', '最高價', '最低價', '收盤價', '成交量'] if col in df.columns]
            df = df[available_columns].tail(days)

            return df

        except Exception as e:
            print(f"從 yfinance 獲取資料時發生錯誤: {str(e)}")
            return pd.DataFrame()

    def get_realtime_price(self, stock_id: str) -> Dict:
        """
        獲取即時股價（使用最近的收盤價）

        Args:
            stock_id: 股票代碼

        Returns:
            包含即時資訊的字典
        """
        try:
            # 獲取最近1天的資料作為即時價格
            df = self.get_stock_price(stock_id, days=5)

            if df.empty:
                return {}

            latest = df.iloc[-1]

            return {
                '股票代碼': stock_id,
                '股票名稱': f'股票 {stock_id}',
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
        """
        獲取股票基本資訊

        Args:
            stock_id: 股票代碼

        Returns:
            股票基本資訊字典
        """
        try:
            # 使用 yfinance 獲取詳細資訊
            ticker = f"{stock_id}.TW"
            stock = yf.Ticker(ticker)

            # 使用 fast_info 獲取基本資訊（更快速穩定）
            try:
                info = stock.info
                if not info or len(info) <= 1:
                    # 如果 .TW 沒資料，嘗試 .TWO
                    ticker = f"{stock_id}.TWO"
                    stock = yf.Ticker(ticker)
                    info = stock.info
            except:
                # 如果獲取失敗，返回基本資訊
                info = {}

            # 安全地獲取各項資訊
            return {
                '股票代碼': stock_id,
                '公司名稱': info.get('longName') or info.get('shortName') or f'股票 {stock_id}',
                '產業': info.get('industry') or info.get('sector') or 'N/A',
                '市值': info.get('marketCap', 'N/A'),
                '本益比': info.get('trailingPE') or info.get('forwardPE') or 'N/A',
                '股價淨值比': info.get('priceToBook', 'N/A'),
                '52週最高': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52週最低': info.get('fiftyTwoWeekLow', 'N/A'),
            }

        except Exception as e:
            print(f"獲取股票資訊時發生錯誤: {str(e)}")
            # 返回基本資訊
            return {
                '股票代碼': stock_id,
                '公司名稱': f'股票 {stock_id}',
                '產業': 'N/A',
                '市值': 'N/A',
                '本益比': 'N/A',
                '股價淨值比': 'N/A',
                '52週最高': 'N/A',
                '52週最低': 'N/A',
            }

    def get_top_stocks(self) -> List[Dict]:
        """
        獲取熱門股票列表

        Returns:
            熱門股票列表
        """
        # 台灣常見的大型股
        popular_stocks = [
            '2330',  # 台積電
            '2317',  # 鴻海
            '2454',  # 聯發科
            '2412',  # 中華電
            '2882',  # 國泰金
            '2881',  # 富邦金
            '2886',  # 兆豐金
            '2891',  # 中信金
            '2303',  # 聯電
            '2308',  # 台達電
        ]

        result = []
        for stock_id in popular_stocks:
            realtime = self.get_realtime_price(stock_id)
            if realtime:
                result.append(realtime)

        return result


class WarrantDataFetcher:
    """權證資料獲取器"""

    def __init__(self):
        self.base_url = "https://www.cnyes.com/warrant/"

    def get_warrant_list(self, stock_id: str = None) -> pd.DataFrame:
        """
        獲取權證列表

        Args:
            stock_id: 標的股票代碼（選填）

        Returns:
            權證資料 DataFrame
        """
        # 這裡提供示範資料結構
        # 實際應用中需要從證交所或其他來源爬取
        sample_data = {
            '權證代碼': ['123456', '123457', '123458'],
            '權證名稱': ['XX認購01', 'YY認購02', 'ZZ認售01'],
            '標的股票': ['2330', '2317', '2454'],
            '行使比例': [0.5, 0.3, 0.4],
            '履約價': [600, 100, 800],
            '到期日': ['2024-12-31', '2024-11-30', '2024-10-31'],
            '隱含波動率': [25.5, 30.2, 28.7],
            '實質槓桿': [5.2, 6.1, 4.8],
        }

        df = pd.DataFrame(sample_data)

        if stock_id:
            df = df[df['標的股票'] == stock_id]

        return df

    def calculate_warrant_value(self, warrant_info: Dict) -> Dict:
        """
        計算權證價值

        Args:
            warrant_info: 權證資訊

        Returns:
            包含計算結果的字典
        """
        # 簡化的權證價值計算
        # 實際應使用 Black-Scholes 模型
        return {
            '理論價值': 'N/A',
            '內含價值': 'N/A',
            '時間價值': 'N/A',
            '建議': '需要更詳細的市場資料進行計算'
        }
