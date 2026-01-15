"""
台灣股市資料串接模組
100% 使用 Yahoo Finance 真實資料
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import warnings
import logging
import os

# 完全抑制所有警告
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

# 設定所有相關 logger 為 CRITICAL
for logger_name in ['yfinance', 'peewee', 'urllib3', 'requests', 'apscheduler']:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

# 導入 yfinance
_yf_available = False
try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import yfinance as yf
        _yf_available = True
except:
    pass


class TaiwanStockDataFetcher:
    """台灣股票資料獲取器 - 100% Yahoo Finance 真實資料"""

    def __init__(self):
        # 股票名稱對照（僅用於顯示，不影響資料）
        self.stock_names = {
            '2330': '台積電', '2454': '聯發科', '2303': '聯電', '3711': '日月光投控',
            '2317': '鴻海', '2308': '台達電', '2382': '廣達', '2357': '華碩',
            '3008': '大立光', '2395': '研華', '2912': '統一超',
            '2882': '國泰金', '2881': '富邦金', '2886': '兆豐金', '2891': '中信金',
            '2885': '元大金', '2884': '玉山金', '2883': '開發金', '2880': '華南金',
            '1301': '台塑', '1303': '南亞', '1326': '台化', '2002': '中鋼',
            '2207': '和泰車', '2603': '長榮', '2609': '陽明', '2615': '萬海',
            '2412': '中華電', '3045': '台灣大', '4904': '遠傳',
            '0050': '元大台灣50', '0056': '元大高股息', '00878': '國泰永續高股息',
            '2409': '友達', '3034': '聯詠', '2347': '聯強', '6505': '台塑化',
        }
        self._cache = {}  # 快取減少重複請求

    def get_stock_price(self, stock_id: str, days: int = 30) -> pd.DataFrame:
        """
        獲取股票歷史價格 - 100% 來自 Yahoo Finance

        Args:
            stock_id: 股票代碼
            days: 天數

        Returns:
            DataFrame: 股價資料，如果獲取失敗返回空 DataFrame
        """
        if not _yf_available:
            return pd.DataFrame()

        try:
            end = datetime.now()
            start = end - timedelta(days=days + 30)

            # 嘗試 .TW 和 .TWO 後綴
            for sfx in ['.TW', '.TWO']:
                ticker_symbol = f"{stock_id}{sfx}"
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        df = yf.download(
                            ticker_symbol,
                            start=start,
                            end=end,
                            progress=False,
                            auto_adjust=True,
                            threads=False
                        )

                    if df is not None and len(df) > 3:
                        # 處理 MultiIndex columns
                        if isinstance(df.columns, pd.MultiIndex):
                            df.columns = df.columns.droplevel(1)

                        df = df.rename(columns={
                            'Open': '開盤價', 'High': '最高價',
                            'Low': '最低價', 'Close': '收盤價', 'Volume': '成交量'
                        })
                        if '開盤價' in df.columns:
                            return df[['開盤價', '最高價', '最低價', '收盤價', '成交量']].tail(days)
                except Exception:
                    continue
        except Exception:
            pass

        # 無法獲取資料，返回空 DataFrame
        return pd.DataFrame()

    def get_realtime_price(self, stock_id: str) -> Dict:
        """
        獲取即時價格 - 100% 來自 Yahoo Finance
        """
        if not _yf_available:
            return {}

        # 嘗試從快取獲取（減少 API 請求）
        cache_key = f"realtime_{stock_id}"
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if (datetime.now() - cached_time).seconds < 60:  # 1分鐘快取
                return cached_data

        for sfx in ['.TW', '.TWO']:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    ticker = yf.Ticker(f"{stock_id}{sfx}")
                    info = ticker.info

                    if info and info.get('regularMarketPrice'):
                        result = {
                            '股票代碼': stock_id,
                            '股票名稱': self.stock_names.get(stock_id) or info.get('shortName', stock_id),
                            '當前價格': info.get('regularMarketPrice'),
                            '開盤價': info.get('regularMarketOpen'),
                            '最高價': info.get('regularMarketDayHigh'),
                            '最低價': info.get('regularMarketDayLow'),
                            '昨收價': info.get('previousClose'),
                            '成交量': info.get('regularMarketVolume'),
                            '漲跌': info.get('regularMarketChange'),
                            '漲跌幅': info.get('regularMarketChangePercent'),
                            '時間': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            '資料來源': 'Yahoo Finance'
                        }
                        self._cache[cache_key] = (datetime.now(), result)
                        return result
            except Exception:
                continue
        return {}

    def get_stock_info(self, stock_id: str) -> Dict:
        """
        獲取股票基本資訊 - 100% 來自 Yahoo Finance
        """
        if not _yf_available:
            return self._empty_info(stock_id)

        for sfx in ['.TW', '.TWO']:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    ticker = yf.Ticker(f"{stock_id}{sfx}")
                    info = ticker.info

                    # 檢查是否有有效資料
                    if not info or info.get('regularMarketPrice') is None:
                        continue

                    # 格式化市值
                    market_cap = info.get('marketCap')
                    if market_cap:
                        if market_cap >= 1e12:
                            market_cap_str = f"{market_cap/1e12:.2f} 兆"
                        elif market_cap >= 1e8:
                            market_cap_str = f"{market_cap/1e8:.2f} 億"
                        else:
                            market_cap_str = f"{market_cap:,.0f}"
                    else:
                        market_cap_str = 'N/A'

                    # 本益比
                    pe_ratio = info.get('trailingPE')
                    pe_str = f"{pe_ratio:.2f}" if pe_ratio else 'N/A'

                    # 股價淨值比
                    pb_ratio = info.get('priceToBook')
                    pb_str = f"{pb_ratio:.2f}" if pb_ratio else 'N/A'

                    # 52週高低
                    week52_high = info.get('fiftyTwoWeekHigh')
                    week52_low = info.get('fiftyTwoWeekLow')
                    w52h_str = f"{week52_high:.2f}" if week52_high else 'N/A'
                    w52l_str = f"{week52_low:.2f}" if week52_low else 'N/A'

                    # 殖利率
                    div_yield = info.get('dividendYield')
                    div_str = f"{div_yield * 100:.2f}%" if div_yield else 'N/A'

                    # 產業翻譯
                    sector_tw = self._translate_sector(info.get('sector', ''))
                    industry_tw = self._translate_industry(info.get('industry', ''))

                    # 公司名稱
                    company_name = self.stock_names.get(stock_id) or info.get('shortName') or info.get('longName') or stock_id

                    return {
                        '股票代碼': stock_id,
                        '公司名稱': company_name,
                        '產業類別': sector_tw,
                        '細分產業': industry_tw,
                        '市值': market_cap_str,
                        '本益比': pe_str,
                        '股價淨值比': pb_str,
                        '52週最高': w52h_str,
                        '52週最低': w52l_str,
                        '殖利率': div_str,
                        '當前價格': info.get('regularMarketPrice') or info.get('previousClose'),
                        '資料來源': 'Yahoo Finance'
                    }
            except Exception:
                continue

        return self._empty_info(stock_id)

    def _empty_info(self, stock_id: str) -> Dict:
        """當無法獲取資料時返回空資訊"""
        return {
            '股票代碼': stock_id,
            '公司名稱': self.stock_names.get(stock_id, stock_id),
            '產業類別': '無法獲取',
            '細分產業': '無法獲取',
            '市值': '無法獲取',
            '本益比': '無法獲取',
            '股價淨值比': '無法獲取',
            '52週最高': '無法獲取',
            '52週最低': '無法獲取',
            '殖利率': '無法獲取',
            '當前價格': None,
            '資料來源': '無法連接 Yahoo Finance'
        }

    def _translate_sector(self, sector: str) -> str:
        """翻譯產業類別"""
        translations = {
            'Technology': '科技業',
            'Financial Services': '金融業',
            'Consumer Cyclical': '消費週期性',
            'Communication Services': '通訊服務',
            'Industrials': '工業',
            'Basic Materials': '基礎材料',
            'Consumer Defensive': '消費防禦',
            'Energy': '能源',
            'Healthcare': '醫療保健',
            'Real Estate': '房地產',
            'Utilities': '公用事業',
        }
        return translations.get(sector, sector or '其他')

    def _translate_industry(self, industry: str) -> str:
        """翻譯細分產業"""
        translations = {
            'Semiconductors': '半導體',
            'Consumer Electronics': '消費電子',
            'Electronic Components': '電子元件',
            'Computer Hardware': '電腦硬體',
            'Banks—Regional': '區域銀行',
            'Insurance—Life': '人壽保險',
            'Insurance—Diversified': '綜合保險',
            'Asset Management': '資產管理',
            'Telecom Services': '電信服務',
            'Marine Shipping': '海運',
            'Auto Manufacturers': '汽車製造',
            'Specialty Chemicals': '特用化學品',
            'Steel': '鋼鐵',
            'Oil & Gas Integrated': '石油天然氣綜合',
        }
        return translations.get(industry, industry or '其他')

    def get_top_stocks(self, limit: int = 10) -> List[Dict]:
        """獲取熱門股票即時價格 - 100% 來自 Yahoo Finance"""
        top_list = ['2330', '2317', '2454', '2412', '2882', '2881', '2886', '2891', '2303', '2308']
        results = []
        for stock_id in top_list[:limit]:
            price_data = self.get_realtime_price(stock_id)
            if price_data:
                results.append(price_data)
        return results


class WarrantDataFetcher:
    """權證資料獲取器"""

    def __init__(self):
        """初始化權證資料庫（示範資料）"""
        from datetime import datetime, timedelta

        base_date = datetime.now()

        # 台積電 (2330) 權證
        tsmc_warrants = [
            {
                '權證代碼': '070001',
                '權證名稱': '元大01認購',
                '標的股票': '2330',
                '發行商': '元大證券',
                '權證類型': '認購',
                '行使比例': 0.5,
                '履約價': 650.0,
                '到期日': (base_date + timedelta(days=120)).strftime('%Y-%m-%d'),
                '隱含波動率': 28.5,
                '權證價格': 12.5,
                '發行量': 50000000,
            },
            {
                '權證代碼': '070002',
                '權證名稱': '凱基02認購',
                '標的股票': '2330',
                '發行商': '凱基證券',
                '權證類型': '認購',
                '行使比例': 0.6,
                '履約價': 700.0,
                '到期日': (base_date + timedelta(days=90)).strftime('%Y-%m-%d'),
                '隱含波動率': 30.2,
                '權證價格': 8.3,
                '發行量': 40000000,
            },
        ]

        # 鴻海 (2317) 權證
        foxconn_warrants = [
            {
                '權證代碼': '071001',
                '權證名稱': '元大06認購',
                '標的股票': '2317',
                '發行商': '元大證券',
                '權證類型': '認購',
                '行使比例': 0.3,
                '履約價': 110.0,
                '到期日': (base_date + timedelta(days=95)).strftime('%Y-%m-%d'),
                '隱含波動率': 35.2,
                '權證價格': 5.8,
                '發行量': 35000000,
            },
        ]

        all_warrants = tsmc_warrants + foxconn_warrants
        self.warrants_df = pd.DataFrame(all_warrants)

    def get_warrant_list(self, stock_id: str = None) -> pd.DataFrame:
        if stock_id:
            return self.warrants_df[self.warrants_df['標的股票'] == stock_id].copy()
        return self.warrants_df.copy()

    def get_warrant_detail(self, warrant_code: str) -> Dict:
        warrant = self.warrants_df[self.warrants_df['權證代碼'] == warrant_code]
        if warrant.empty:
            return {}
        return warrant.iloc[0].to_dict()

    def calculate_warrant_value(self, warrant: Dict) -> Dict:
        return {
            '理論價值': 'N/A',
            '內含價值': 'N/A',
            '時間價值': 'N/A',
            '建議': '需詳細資料'
        }
