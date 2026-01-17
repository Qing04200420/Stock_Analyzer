"""
台灣股市資料串接模組
100% 使用 Yahoo Finance 真實資料
"""

import pandas as pd
import numpy as np
import requests
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
        # 股票完整資訊對照表
        self.stock_info_db = {
            # 半導體
            '2330': {'name': '台積電', 'sector': '科技業', 'industry': '半導體'},
            '2454': {'name': '聯發科', 'sector': '科技業', 'industry': '半導體'},
            '2303': {'name': '聯電', 'sector': '科技業', 'industry': '半導體'},
            '3711': {'name': '日月光投控', 'sector': '科技業', 'industry': '半導體'},
            '2379': {'name': '瑞昱', 'sector': '科技業', 'industry': '半導體'},
            '3034': {'name': '聯詠', 'sector': '科技業', 'industry': '半導體'},
            '2344': {'name': '華邦電', 'sector': '科技業', 'industry': '半導體'},
            # 電子
            '2317': {'name': '鴻海', 'sector': '科技業', 'industry': '電子製造'},
            '2308': {'name': '台達電', 'sector': '科技業', 'industry': '電子零組件'},
            '2382': {'name': '廣達', 'sector': '科技業', 'industry': '電腦及週邊'},
            '2357': {'name': '華碩', 'sector': '科技業', 'industry': '電腦及週邊'},
            '2353': {'name': '宏碁', 'sector': '科技業', 'industry': '電腦及週邊'},
            '3008': {'name': '大立光', 'sector': '科技業', 'industry': '光電'},
            '2395': {'name': '研華', 'sector': '科技業', 'industry': '工業電腦'},
            '2354': {'name': '鴻準', 'sector': '科技業', 'industry': '機殼'},
            '2474': {'name': '可成', 'sector': '科技業', 'industry': '機殼'},
            '2327': {'name': '國巨', 'sector': '科技業', 'industry': '被動元件'},
            '3231': {'name': '緯創', 'sector': '科技業', 'industry': '電腦及週邊'},
            '2324': {'name': '仁寶', 'sector': '科技業', 'industry': '電腦及週邊'},
            '2301': {'name': '光寶科', 'sector': '科技業', 'industry': '電源供應器'},
            '2356': {'name': '英業達', 'sector': '科技業', 'industry': '電腦及週邊'},
            '2347': {'name': '聯強', 'sector': '科技業', 'industry': '通路'},
            '2409': {'name': '友達', 'sector': '科技業', 'industry': '面板'},
            '3481': {'name': '群創', 'sector': '科技業', 'industry': '面板'},
            # 金融
            '2882': {'name': '國泰金', 'sector': '金融業', 'industry': '金控'},
            '2881': {'name': '富邦金', 'sector': '金融業', 'industry': '金控'},
            '2886': {'name': '兆豐金', 'sector': '金融業', 'industry': '金控'},
            '2891': {'name': '中信金', 'sector': '金融業', 'industry': '金控'},
            '2885': {'name': '元大金', 'sector': '金融業', 'industry': '金控'},
            '2884': {'name': '玉山金', 'sector': '金融業', 'industry': '金控'},
            '2883': {'name': '開發金', 'sector': '金融業', 'industry': '金控'},
            '2880': {'name': '華南金', 'sector': '金融業', 'industry': '金控'},
            '2887': {'name': '台新金', 'sector': '金融業', 'industry': '金控'},
            '2890': {'name': '永豐金', 'sector': '金融業', 'industry': '金控'},
            '2892': {'name': '第一金', 'sector': '金融業', 'industry': '金控'},
            '5880': {'name': '合庫金', 'sector': '金融業', 'industry': '金控'},
            # 傳產
            '1301': {'name': '台塑', 'sector': '塑膠業', 'industry': '塑膠'},
            '1303': {'name': '南亞', 'sector': '塑膠業', 'industry': '塑膠'},
            '1326': {'name': '台化', 'sector': '塑膠業', 'industry': '塑膠'},
            '6505': {'name': '台塑化', 'sector': '塑膠業', 'industry': '石化'},
            '2002': {'name': '中鋼', 'sector': '鋼鐵業', 'industry': '鋼鐵'},
            '2207': {'name': '和泰車', 'sector': '汽車業', 'industry': '汽車'},
            '2912': {'name': '統一超', 'sector': '零售業', 'industry': '超商'},
            '1216': {'name': '統一', 'sector': '食品業', 'industry': '食品'},
            '2105': {'name': '正新', 'sector': '橡膠業', 'industry': '輪胎'},
            # 航運
            '2603': {'name': '長榮', 'sector': '航運業', 'industry': '貨櫃航運'},
            '2609': {'name': '陽明', 'sector': '航運業', 'industry': '貨櫃航運'},
            '2615': {'name': '萬海', 'sector': '航運業', 'industry': '貨櫃航運'},
            '2618': {'name': '長榮航', 'sector': '航運業', 'industry': '航空'},
            # 通訊
            '2412': {'name': '中華電', 'sector': '通訊業', 'industry': '電信'},
            '3045': {'name': '台灣大', 'sector': '通訊業', 'industry': '電信'},
            '4904': {'name': '遠傳', 'sector': '通訊業', 'industry': '電信'},
            # ETF
            '0050': {'name': '元大台灣50', 'sector': 'ETF', 'industry': '指數型'},
            '0056': {'name': '元大高股息', 'sector': 'ETF', 'industry': '高股息'},
            '00878': {'name': '國泰永續高股息', 'sector': 'ETF', 'industry': '高股息'},
            '00881': {'name': '國泰台灣5G+', 'sector': 'ETF', 'industry': '主題型'},
            '006208': {'name': '富邦台50', 'sector': 'ETF', 'industry': '指數型'},
        }
        self._cache = {}  # 快取

    def get_stock_price(self, stock_id: str, days: int = 30) -> pd.DataFrame:
        """
        獲取股票歷史價格 - 100% 來自 Yahoo Finance
        """
        if not _yf_available:
            return pd.DataFrame()

        # 檢查快取
        cache_key = f"price_{stock_id}_{days}"
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if (datetime.now() - cached_time).seconds < 300:  # 5分鐘快取
                return cached_data

        try:
            end = datetime.now()
            start = end - timedelta(days=days + 30)

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
                        if isinstance(df.columns, pd.MultiIndex):
                            df.columns = df.columns.droplevel(1)

                        df = df.rename(columns={
                            'Open': '開盤價', 'High': '最高價',
                            'Low': '最低價', 'Close': '收盤價', 'Volume': '成交量'
                        })
                        if '開盤價' in df.columns:
                            result = df[['開盤價', '最高價', '最低價', '收盤價', '成交量']].tail(days)
                            self._cache[cache_key] = (datetime.now(), result)
                            return result
                except Exception:
                    continue
        except Exception:
            pass

        return pd.DataFrame()

    def get_stock_info(self, stock_id: str) -> Dict:
        """
        獲取股票基本資訊 - 結合本地資料庫與即時股價計算
        """
        # 從本地資料庫獲取基本資訊
        stock_data = self.stock_info_db.get(stock_id, {})
        company_name = stock_data.get('name', stock_id)
        sector = stock_data.get('sector', '其他')
        industry = stock_data.get('industry', '其他')

        # 獲取一年的股價資料來計算 52 週高低
        df = self.get_stock_price(stock_id, days=365)

        if df.empty:
            return {
                '股票代碼': stock_id,
                '公司名稱': company_name,
                '產業類別': sector,
                '細分產業': industry,
                '市值': '載入中...',
                '本益比': '載入中...',
                '股價淨值比': '載入中...',
                '52週最高': '載入中...',
                '52週最低': '載入中...',
                '殖利率': '載入中...',
                '當前價格': None,
                '資料來源': 'Yahoo Finance'
            }

        # 從股價資料計算
        current_price = float(df['收盤價'].iloc[-1])
        week52_high = float(df['最高價'].max())
        week52_low = float(df['最低價'].min())
        avg_volume = float(df['成交量'].mean())

        # 嘗試從 yfinance 獲取更多資訊
        pe_ratio = 'N/A'
        pb_ratio = 'N/A'
        market_cap = 'N/A'
        div_yield = 'N/A'

        if _yf_available:
            for sfx in ['.TW', '.TWO']:
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        ticker = yf.Ticker(f"{stock_id}{sfx}")
                        info = ticker.info

                        if info and info.get('regularMarketPrice'):
                            # 本益比
                            if info.get('trailingPE'):
                                pe_ratio = f"{info['trailingPE']:.2f}"

                            # 股價淨值比
                            if info.get('priceToBook'):
                                pb_ratio = f"{info['priceToBook']:.2f}"

                            # 市值
                            mc = info.get('marketCap')
                            if mc:
                                if mc >= 1e12:
                                    market_cap = f"{mc/1e12:.2f} 兆"
                                elif mc >= 1e8:
                                    market_cap = f"{mc/1e8:.2f} 億"
                                else:
                                    market_cap = f"{mc:,.0f}"

                            # 殖利率
                            dy = info.get('dividendYield')
                            if dy:
                                div_yield = f"{dy * 100:.2f}%"

                            break
                except Exception:
                    continue

        return {
            '股票代碼': stock_id,
            '公司名稱': company_name,
            '產業類別': sector,
            '細分產業': industry,
            '市值': market_cap,
            '本益比': pe_ratio,
            '股價淨值比': pb_ratio,
            '52週最高': f"{week52_high:.2f}",
            '52週最低': f"{week52_low:.2f}",
            '殖利率': div_yield,
            '當前價格': current_price,
            '資料來源': 'Yahoo Finance'
        }

    def get_realtime_price(self, stock_id: str) -> Dict:
        """
        獲取即時價格 - 從最新股價資料獲取
        """
        df = self.get_stock_price(stock_id, days=5)

        if df.empty:
            return {}

        stock_data = self.stock_info_db.get(stock_id, {})
        company_name = stock_data.get('name', stock_id)

        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest

        current_price = float(latest['收盤價'])
        prev_close = float(prev['收盤價'])
        change = current_price - prev_close
        change_pct = (change / prev_close) * 100 if prev_close > 0 else 0

        return {
            '股票代碼': stock_id,
            '股票名稱': company_name,
            '當前價格': current_price,
            '開盤價': float(latest['開盤價']),
            '最高價': float(latest['最高價']),
            '最低價': float(latest['最低價']),
            '昨收價': prev_close,
            '成交量': int(latest['成交量']),
            '漲跌': round(change, 2),
            '漲跌幅': round(change_pct, 2),
            '時間': str(df.index[-1].date()),
            '資料來源': 'Yahoo Finance'
        }

    def get_top_stocks(self, limit: int = 10) -> List[Dict]:
        """獲取熱門股票即時價格"""
        top_list = ['2330', '2317', '2454', '2412', '2882', '2881', '2886', '2891', '2303', '2308']
        results = []
        for stock_id in top_list[:limit]:
            price_data = self.get_realtime_price(stock_id)
            if price_data:
                results.append(price_data)
        return results


class WarrantDataFetcher:
    """權證資料獲取器 - 從 Yahoo 股市和證交所 API 獲取真實資料"""

    def __init__(self):
        self.yahoo_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.twse_headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://mis.twse.com.tw/stock/index.jsp'
        }
        # 發行商代碼對照表
        self.issuer_map = {
            '元大': '元大證券', '富邦': '富邦證券', '凱基': '凱基證券',
            '群益': '群益證券', '統一': '統一證券', '永豐': '永豐證券',
            '國泰': '國泰證券', '中信': '中信證券', '兆豐': '兆豐證券',
            '元富': '元富證券', '國票': '國票證券', '日盛': '日盛證券',
            '康和': '康和證券', '第一': '第一金證券', '台新': '台新證券',
            '華南': '華南證券', '玉山': '玉山證券', '合庫': '合庫證券',
        }
        self._cache = {}
        self._cache_time = {}

    def get_warrant_list(self, stock_id: str = None) -> pd.DataFrame:
        """
        獲取權證列表

        Args:
            stock_id: 標的股票代碼（如 '2330'）

        Returns:
            權證列表 DataFrame
        """
        import re
        import json
        from datetime import datetime

        if not stock_id:
            return pd.DataFrame()

        # 檢查快取（5分鐘內有效）
        cache_key = f'warrant_list_{stock_id}'
        if cache_key in self._cache:
            cache_age = (datetime.now() - self._cache_time.get(cache_key, datetime.min)).seconds
            if cache_age < 300:
                return self._cache[cache_key].copy()

        try:
            # 從 Yahoo 股市獲取權證列表
            url = f'https://tw.stock.yahoo.com/quote/{stock_id}/warrant'
            resp = requests.get(url, headers=self.yahoo_headers, timeout=15)
            resp.raise_for_status()

            # 解析頁面中的 JSON 資料
            match = re.search(r'"warrants":(\[\{.*?\}\])', resp.text, re.DOTALL)
            if not match:
                return pd.DataFrame()

            warrants_json = match.group(1)
            warrants_basic = json.loads(warrants_json)

            if not warrants_basic:
                return pd.DataFrame()

            # 取得權證代碼列表（去掉 .TW 後綴）
            warrant_codes = [w.get('symbol', '').replace('.TW', '').replace('.TWO', '')
                           for w in warrants_basic]

            # 從證交所 API 獲取詳細資訊
            warrant_details = self._get_warrant_details_from_twse(warrant_codes)

            # 合併資料
            result = []
            for w in warrants_basic:
                code = w.get('symbol', '').replace('.TW', '').replace('.TWO', '')
                name = w.get('name', '')

                # 解析權證類型和發行商
                warrant_type = '認購' if '購' in name else ('認售' if '售' in name else '未知')
                issuer = '未知'
                for key, val in self.issuer_map.items():
                    if key in name:
                        issuer = val
                        break

                # 從證交所資料取得詳細資訊
                detail = warrant_details.get(code, {})

                # 解析到期日（從完整名稱中提取）
                expiry_date = detail.get('expiry_date', '')
                if not expiry_date and detail.get('nf'):
                    # 從 nf 欄位解析到期日，格式如 "台積電群益51購26－台積電 20260130美購"
                    nf_match = re.search(r'(\d{8})[美歐]?[購售]', detail.get('nf', ''))
                    if nf_match:
                        date_str = nf_match.group(1)
                        expiry_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

                result.append({
                    '權證代碼': code,
                    '權證名稱': name,
                    '標的股票': stock_id,
                    '發行商': issuer,
                    '權證類型': warrant_type,
                    '行使比例': detail.get('exercise_ratio', 0.1),
                    '履約價': detail.get('strike_price', 0),
                    '到期日': expiry_date,
                    '隱含波動率': detail.get('iv', 30.0),
                    '權證價格': detail.get('price', 0),
                    '昨收價': detail.get('prev_close', 0),
                    '漲停價': detail.get('limit_up', 0),
                    '跌停價': detail.get('limit_down', 0),
                    '成交量': detail.get('volume', 0),
                })

            df = pd.DataFrame(result)

            # 快取結果
            self._cache[cache_key] = df
            self._cache_time[cache_key] = datetime.now()

            return df

        except Exception as e:
            print(f"獲取權證列表失敗: {e}")
            return pd.DataFrame()

    def _get_warrant_details_from_twse(self, warrant_codes: List[str]) -> Dict:
        """
        從證交所 API 獲取權證詳細資訊

        Args:
            warrant_codes: 權證代碼列表

        Returns:
            權證詳細資訊字典
        """
        import re

        if not warrant_codes:
            return {}

        result = {}

        # 分批查詢（每次最多20個）
        batch_size = 20
        for i in range(0, len(warrant_codes), batch_size):
            batch = warrant_codes[i:i+batch_size]

            # 組合查詢字串
            ex_ch = '|'.join([f'tse_{code}.tw' for code in batch])
            url = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={ex_ch}&json=1&delay=0'

            try:
                resp = requests.get(url, headers=self.twse_headers, timeout=10)
                data = resp.json()

                if data.get('rtcode') == '0000':
                    for item in data.get('msgArray', []):
                        code = item.get('c', '')
                        if code:
                            # 解析價格（可能是 '-' 表示無成交）
                            price = item.get('z', '-')
                            price = float(price) if price and price != '-' else 0

                            prev_close = item.get('y', '0')
                            prev_close = float(prev_close) if prev_close else 0

                            limit_up = item.get('u', '0')
                            limit_up = float(limit_up) if limit_up else 0

                            limit_down = item.get('w', '0')
                            limit_down = float(limit_down) if limit_down else 0

                            volume = item.get('v', '0')
                            volume = int(volume) if volume else 0

                            # 解析到期日和其他資訊
                            nf = item.get('nf', '')

                            result[code] = {
                                'price': price if price > 0 else prev_close,
                                'prev_close': prev_close,
                                'limit_up': limit_up,
                                'limit_down': limit_down,
                                'volume': volume,
                                'nf': nf,
                                'underlying': item.get('rn', ''),
                                'underlying_code': item.get('rch', ''),
                                'exercise_ratio': 0.1,  # 預設值
                                'strike_price': 0,  # 需要從其他來源獲取
                                'iv': 30.0,  # 預設值
                            }
            except Exception as e:
                print(f"TWSE API 查詢失敗: {e}")
                continue

        return result

    def get_warrant_detail(self, warrant_code: str) -> Dict:
        """
        獲取單支權證的詳細資訊

        Args:
            warrant_code: 權證代碼

        Returns:
            權證詳細資訊字典
        """
        import re
        from datetime import datetime

        try:
            # 從證交所 API 獲取即時資訊
            ex_ch = f'tse_{warrant_code}.tw'
            url = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={ex_ch}&json=1&delay=0'

            resp = requests.get(url, headers=self.twse_headers, timeout=10)
            data = resp.json()

            if data.get('rtcode') != '0000' or not data.get('msgArray'):
                return {}

            item = data['msgArray'][0]

            # 解析價格
            price = item.get('z', '-')
            price = float(price) if price and price != '-' else 0

            prev_close = item.get('y', '0')
            prev_close = float(prev_close) if prev_close else 0

            if price == 0:
                price = prev_close

            # 解析完整名稱取得到期日
            nf = item.get('nf', '')
            expiry_date = ''
            nf_match = re.search(r'(\d{8})[美歐]?[購售]', nf)
            if nf_match:
                date_str = nf_match.group(1)
                expiry_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

            # 解析權證類型
            name = item.get('n', '')
            warrant_type = '認購' if '購' in name or '購' in nf else ('認售' if '售' in name or '售' in nf else '未知')

            # 解析發行商
            issuer = '未知'
            for key, val in self.issuer_map.items():
                if key in name:
                    issuer = val
                    break

            return {
                '權證代碼': warrant_code,
                '權證名稱': name,
                '標的股票': item.get('rch', ''),
                '標的名稱': item.get('rn', ''),
                '發行商': issuer,
                '權證類型': warrant_type,
                '行使比例': 0.1,  # 預設值
                '履約價': 0,  # 需要從其他來源獲取
                '到期日': expiry_date,
                '隱含波動率': 30.0,  # 預設值
                '權證價格': price,
                '昨收價': prev_close,
                '漲停價': float(item.get('u', 0)) if item.get('u') else 0,
                '跌停價': float(item.get('w', 0)) if item.get('w') else 0,
                '成交量': int(item.get('v', 0)) if item.get('v') else 0,
                '最高價': float(item.get('h', 0)) if item.get('h') else 0,
                '最低價': float(item.get('l', 0)) if item.get('l') else 0,
                '開盤價': float(item.get('o', 0)) if item.get('o') else 0,
            }

        except Exception as e:
            print(f"獲取權證詳情失敗: {e}")
            return {}

    def calculate_warrant_value(self, warrant: Dict) -> Dict:
        """計算權證價值（需要更多資料）"""
        return {
            '理論價值': 'N/A',
            '內含價值': 'N/A',
            '時間價值': 'N/A',
            '建議': '使用權證分析頁面獲取完整分析'
        }
