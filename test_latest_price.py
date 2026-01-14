"""
測試獲取最新股價

此腳本會測試不同的資料來源，找出哪個能獲取最新價格。
"""

from datetime import datetime, timedelta
import pandas as pd


def print_section(title):
    """打印區塊標題"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_yfinance():
    """測試 yfinance"""
    print_section("測試 1: yfinance（直接）")

    try:
        import yfinance as yf

        print("📊 獲取台積電 (2330.TW) 最近 5 天資料...")

        # 設定日期範圍
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # 下載資料
        df = yf.download(
            "2330.TW",
            start=start_date,
            end=end_date,
            progress=False
        )

        if not df.empty:
            print(f"✅ 成功獲取 {len(df)} 筆資料\n")
            print("最新 3 天資料:")
            print(df.tail(3)[['Open', 'High', 'Low', 'Close', 'Volume']])

            latest_date = df.index[-1]
            latest_close = df['Close'].iloc[-1]
            days_ago = (datetime.now() - latest_date).days

            print(f"\n📅 最新日期: {latest_date.strftime('%Y-%m-%d')}")
            print(f"💰 最新收盤價: {latest_close:.2f} TWD")
            print(f"⏰ 資料落後: {days_ago} 天")

            return True, latest_close, days_ago

        else:
            print("❌ 未獲取到資料")
            return False, None, None

    except Exception as e:
        print(f"❌ yfinance 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None


def test_finmind():
    """測試 FinMind"""
    print_section("測試 2: FinMind API")

    try:
        from FinMind.data import DataLoader

        dl = DataLoader()
        print("📊 獲取台積電 (2330) 最近 5 天資料...")

        # 計算日期
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        print(f"   日期範圍: {start_date} ~ {end_date}")

        # 獲取資料
        df = dl.taiwan_stock_daily(
            stock_id="2330",
            start_date=start_date,
            end_date=end_date
        )

        print(f"   返回類型: {type(df)}")
        print(f"   是否為空: {df.empty if isinstance(df, pd.DataFrame) else 'N/A'}")

        if isinstance(df, pd.DataFrame) and not df.empty:
            print(f"✅ 成功獲取 {len(df)} 筆資料\n")

            # 顯示欄位
            print(f"欄位列表: {list(df.columns)}")

            # 顯示資料
            print("\n最新 3 天資料:")
            print(df.tail(3))

            # 分析最新資料
            latest_row = df.iloc[-1]
            latest_date = pd.to_datetime(latest_row['date'])
            latest_close = float(latest_row['close'])
            days_ago = (datetime.now() - latest_date).days

            print(f"\n📅 最新日期: {latest_date.strftime('%Y-%m-%d')}")
            print(f"💰 最新收盤價: {latest_close:.2f} TWD")
            print(f"⏰ 資料落後: {days_ago} 天")

            return True, latest_close, days_ago

        else:
            print("❌ 未獲取到資料或返回格式錯誤")
            print(f"   返回內容: {df}")
            return False, None, None

    except Exception as e:
        print(f"❌ FinMind 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None


def test_ultimate_fetcher():
    """測試終極資料獲取器"""
    print_section("測試 3: 終極資料獲取器")

    try:
        from backend.modules.data_fetcher_ultimate import UltimateTaiwanStockDataFetcher

        fetcher = UltimateTaiwanStockDataFetcher()
        print("📊 使用終極版獲取台積電 (2330) 最近 5 天資料...\n")

        # 獲取資料
        df = fetcher.get_stock_price("2330", days=5)

        if not df.empty:
            print(f"✅ 成功獲取 {len(df)} 筆資料\n")

            print("最新 3 天資料:")
            print(df.tail(3))

            # 分析最新資料
            latest_date = df.index[-1]
            latest_close = df['收盤價'].iloc[-1]
            days_ago = (datetime.now() - latest_date).days

            print(f"\n📅 最新日期: {latest_date.strftime('%Y-%m-%d')}")
            print(f"💰 最新收盤價: {latest_close:.2f} TWD")
            print(f"⏰ 資料落後: {days_ago} 天")

            # 顯示統計
            print("\n📊 資料來源統計:")
            stats = fetcher.get_stats()
            print(f"   yfinance 成功: {stats['yfinance_success']}")
            print(f"   yfinance 429: {stats['yfinance_429']}")
            print(f"   FinMind 成功: {stats['finmind_success']}")
            print(f"   參考資料: {stats['reference_used']}")

            return True, latest_close, days_ago

        else:
            print("❌ 未獲取到資料")
            return False, None, None

    except Exception as e:
        print(f"❌ 終極版測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None


def main():
    """主函數"""
    # Set UTF-8 encoding for Windows console
    import sys
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    print("\n" + "=" * 70)
    print("  🔍 測試最新股價獲取")
    print("=" * 70)
    print(f"\n執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("測試標的: 台積電 (2330)")

    results = []

    # 測試 1: yfinance
    success1, price1, days1 = test_yfinance()
    results.append(("yfinance", success1, price1, days1))

    # 測試 2: FinMind
    success2, price2, days2 = test_finmind()
    results.append(("FinMind", success2, price2, days2))

    # 測試 3: 終極版
    success3, price3, days3 = test_ultimate_fetcher()
    results.append(("終極版", success3, price3, days3))

    # 總結
    print_section("測試總結")

    print("資料來源測試結果:\n")
    for name, success, price, days in results:
        if success:
            freshness = "✅ 最新" if days <= 3 else "⚠️ 稍舊" if days <= 7 else "❌ 過時"
            print(f"  {name:12s} {freshness}   價格: {price:8.2f} TWD   落後: {days} 天")
        else:
            print(f"  {name:12s} ❌ 失敗")

    # 建議
    print("\n" + "=" * 70)

    successful_sources = [name for name, success, _, _ in results if success]

    if successful_sources:
        best_source = successful_sources[0]
        print(f"✅ 推薦使用: {best_source}")

        # 檢查資料新鮮度
        fresh_sources = [(name, days) for name, success, _, days in results if success and days is not None and days <= 3]

        if fresh_sources:
            print(f"✅ 資料狀態: 最新（{fresh_sources[0][1]} 天前）")
            print("✅ 系統正常，可以使用")
        else:
            print("⚠️ 資料狀態: 所有來源都不夠新鮮")
            print("💡 建議:")
            print("   1. 檢查網路連線")
            print("   2. 使用 VPN（如果遇到 429 錯誤）")
            print("   3. 稍後再試")

    else:
        print("❌ 所有資料來源都失敗")
        print("💡 建議:")
        print("   1. 確認 FinMind 已安裝: pip install FinMind")
        print("   2. 檢查網路連線")
        print("   3. 運行完整測試: python test_429_solution.py")

    print("=" * 70)


if __name__ == "__main__":
    main()
