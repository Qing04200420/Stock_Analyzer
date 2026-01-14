"""
FinMind 資料獲取器

使用 FinMind API 獲取台灣股市資料，作為 yfinance 的備援方案。
專門針對台股優化，避免 Yahoo Finance 429 錯誤。

FinMind API 文檔: https://finmindtrade.com/
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

try:
    from FinMind.data import DataLoader
    FINMIND_AVAILABLE = True
except ImportError:
    FINMIND_AVAILABLE = False
    logger.warning("⚠️ FinMind 未安裝，請執行: pip install FinMind")


class FinMindDataFetcher:
    """
    FinMind 資料獲取器

    優點：
    - 專門提供台股資料
    - 免費（每日 500 次請求）
    - 穩定可靠
    - 無需 VPN

    限制：
    - 僅支援台灣市場
    - 需要註冊（免費）
    - 資料延遲約 15 分鐘
    """

    def __init__(self, token: Optional[str] = None):
        """
        初始化 FinMind 資料獲取器

        Args:
            token: FinMind API Token（可選，無 token 有請求限制）
                   註冊網址: https://finmindtrade.com/
        """
        if not FINMIND_AVAILABLE:
            raise ImportError("FinMind 未安裝，請執行: pip install FinMind")

        self.dl = DataLoader()
        self.token = token

        if token:
            self.dl.login(token)
            logger.info("✅ FinMind 已使用 Token 登入（無請求限制）")
        else:
            logger.info("ℹ️ FinMind 使用訪客模式（每日 500 次請求）")

    def get_stock_price(
        self,
        stock_id: str,
        days: int = 90,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        獲取股票歷史價格

        Args:
            stock_id: 股票代碼（例如: "2330"）
            days: 天數（如果未指定 start_date）
            start_date: 起始日期（格式: "2024-01-01"）
            end_date: 結束日期（格式: "2024-12-31"）

        Returns:
            DataFrame: 包含 OHLCV 資料
                列: date, open, high, low, close, volume, Trading_turnover
        """
        try:
            # 計算日期範圍
            if not end_date:
                end_date = datetime.now().strftime("%Y-%m-%d")

            if not start_date:
                start_datetime = datetime.now() - timedelta(days=days)
                start_date = start_datetime.strftime("%Y-%m-%d")

            logger.info(f"📊 使用 FinMind 獲取 {stock_id} 資料 ({start_date} ~ {end_date})")

            # 獲取資料
            df = self.dl.taiwan_stock_daily(
                stock_id=stock_id,
                start_date=start_date,
                end_date=end_date
            )

            if df.empty:
                logger.warning(f"⚠️ FinMind 未找到 {stock_id} 的資料")
                return pd.DataFrame()

            # 轉換為統一格式
            df_formatted = self._format_dataframe(df)

            logger.info(f"✅ 成功從 FinMind 獲取 {len(df_formatted)} 筆資料")
            return df_formatted

        except Exception as e:
            logger.error(f"❌ FinMind 獲取失敗: {e}")
            return pd.DataFrame()

    def _format_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        將 FinMind 格式轉換為統一格式

        FinMind 欄位:
        - date: 日期
        - open: 開盤價
        - max: 最高價
        - min: 最低價
        - close: 收盤價
        - Trading_Volume: 成交股數
        - Trading_money: 成交金額

        統一格式:
        - 日期 (index)
        - 開盤價, 最高價, 最低價, 收盤價, 成交量
        """
        if df.empty:
            return pd.DataFrame()

        # Copy the data first to avoid SettingWithCopyWarning
        df = df.copy()

        # 重命名欄位 - create new DataFrame with explicit column assignment
        df_formatted = pd.DataFrame(index=pd.to_datetime(df['date']))
        df_formatted['開盤價'] = df['open'].astype(float).values
        df_formatted['最高價'] = df['max'].astype(float).values
        df_formatted['最低價'] = df['min'].astype(float).values
        df_formatted['收盤價'] = df['close'].astype(float).values
        df_formatted['成交量'] = df['Trading_Volume'].astype(int).values

        # 確保索引名稱
        df_formatted.index.name = 'Date'

        # 按日期排序
        df_formatted = df_formatted.sort_index()

        return df_formatted

    def get_stock_info(self, stock_id: str) -> Dict:
        """
        獲取股票基本資訊

        Args:
            stock_id: 股票代碼

        Returns:
            Dict: 包含股票名稱、產業等資訊
        """
        try:
            # 獲取台股列表
            stock_info = self.dl.taiwan_stock_info()

            # 查找指定股票
            stock_data = stock_info[stock_info['stock_id'] == stock_id]

            if stock_data.empty:
                return {'代碼': stock_id, '名稱': 'N/A', '產業': 'N/A'}

            row = stock_data.iloc[0]

            return {
                '代碼': stock_id,
                '名稱': row.get('stock_name', 'N/A'),
                '產業': row.get('industry_category', 'N/A'),
                '市場': row.get('type', '上市'),  # 上市/上櫃
            }

        except Exception as e:
            logger.error(f"❌ 獲取股票資訊失敗: {e}")
            return {'代碼': stock_id, '名稱': 'N/A', '產業': 'N/A'}

    def get_top_stocks(self, limit: int = 10) -> List[Dict]:
        """
        獲取熱門股票（依成交金額排序）

        Args:
            limit: 返回數量

        Returns:
            List[Dict]: 熱門股票列表
        """
        try:
            # 獲取最近交易日資料（避免假日無資料）
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)  # 往前查 7 天確保有資料

            # 預設熱門股票列表
            popular_stocks = ['2330', '2317', '2454', '2308', '2382', '2303', '2881', '2882', '2886', '2412']

            result = []
            for stock_id in popular_stocks[:limit]:
                try:
                    # 獲取個別股票資料
                    df = self.dl.taiwan_stock_daily(
                        stock_id=stock_id,
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d")
                    )

                    if isinstance(df, pd.DataFrame) and not df.empty:
                        # 獲取最新一筆資料
                        latest = df.iloc[-1]

                        # 獲取股票名稱
                        stock_info = self.get_stock_info(stock_id)

                        result.append({
                            '股票代碼': stock_id,
                            '股票名稱': stock_info.get('名稱', stock_id),
                            '當前價格': float(latest['close']),
                            '開盤價': float(latest['open']),
                            '最高價': float(latest['max']),
                            '最低價': float(latest['min']),
                            '成交量': int(latest.get('Trading_Volume', 0)),
                            '成交金額': int(latest.get('Trading_money', 0)),
                        })

                except Exception as e:
                    logger.warning(f"⚠️ 無法獲取 {stock_id} 資料: {e}")
                    continue

            if result:
                logger.info(f"✅ 獲取 {len(result)} 支熱門股票")
            else:
                logger.warning("⚠️ 無法獲取任何熱門股票資料")

            return result

        except Exception as e:
            logger.error(f"❌ 獲取熱門股票失敗: {e}")
            return []

    def search_stock(self, keyword: str) -> List[Dict]:
        """
        搜尋股票（依名稱或代碼）

        Args:
            keyword: 搜尋關鍵字

        Returns:
            List[Dict]: 符合的股票列表
        """
        try:
            stock_info = self.dl.taiwan_stock_info()

            # 搜尋代碼或名稱包含關鍵字的股票
            mask = (
                stock_info['stock_id'].str.contains(keyword, na=False) |
                stock_info['stock_name'].str.contains(keyword, na=False)
            )

            results = stock_info[mask]

            return [
                {
                    '代碼': row['stock_id'],
                    '名稱': row['stock_name'],
                    '產業': row.get('industry_category', 'N/A'),
                    '市場': row.get('type', '上市'),
                }
                for _, row in results.iterrows()
            ]

        except Exception as e:
            logger.error(f"❌ 搜尋股票失敗: {e}")
            return []

    @staticmethod
    def is_available() -> bool:
        """檢查 FinMind 是否可用"""
        return FINMIND_AVAILABLE


# 測試函數
def test_finmind():
    """測試 FinMind 連線"""
    if not FINMIND_AVAILABLE:
        print("❌ FinMind 未安裝")
        print("📦 安裝指令: pip install FinMind")
        return

    print("=" * 60)
    print("🧪 FinMind 連線測試")
    print("=" * 60)

    fetcher = FinMindDataFetcher()

    # 測試 1: 獲取台積電資料
    print("\n1️⃣ 測試獲取台積電 (2330) 30 天資料...")
    df = fetcher.get_stock_price("2330", days=30)
    if not df.empty:
        print(f"✅ 成功獲取 {len(df)} 筆資料")
        print(f"\n最新價格:")
        print(df.tail(1))
    else:
        print("❌ 獲取失敗")

    # 測試 2: 獲取股票資訊
    print("\n2️⃣ 測試獲取股票資訊...")
    info = fetcher.get_stock_info("2330")
    print(f"✅ 股票資訊: {info}")

    # 測試 3: 搜尋股票
    print("\n3️⃣ 測試搜尋股票（關鍵字: 台積）...")
    results = fetcher.search_stock("台積")
    if results:
        print(f"✅ 找到 {len(results)} 支股票:")
        for stock in results[:3]:
            print(f"  - {stock['代碼']}: {stock['名稱']}")
    else:
        print("❌ 搜尋失敗")

    print("\n" + "=" * 60)
    print("✅ FinMind 測試完成")
    print("=" * 60)


if __name__ == "__main__":
    test_finmind()
