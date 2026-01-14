# -*- coding: utf-8 -*-
"""
測試 App 首頁顯示最新股價
模擬實際使用情況
"""

import sys
from datetime import datetime

# 設置編碼
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from backend.modules.data_fetcher_ultimate import UltimateTaiwanStockDataFetcher

def test_home_page_stock_display():
    """模擬首頁顯示熱門股票"""
    print("=" * 70)
    print("🏠 模擬首頁熱門股票顯示")
    print("=" * 70)

    # 初始化資料獲取器（與 app.py 相同）
    fetcher = UltimateTaiwanStockDataFetcher()

    # 測試獲取單支股票（首頁會這樣做）
    print("\n測試獲取台積電 (2330)...")
    df = fetcher.get_stock_price("2330", days=5)

    if not df.empty:
        latest = df.iloc[-1]
        latest_date = df.index[-1]
        days_ago = (datetime.now() - latest_date).days

        print(f"\n✅ 成功獲取資料")
        print(f"   股票代碼: 2330 (台積電)")
        print(f"   最新日期: {latest_date.strftime('%Y-%m-%d')}")
        print(f"   資料落後: {days_ago} 天")
        print(f"\n📊 股價資訊:")
        print(f"   開盤價: {latest['開盤價']:.2f} TWD")
        print(f"   最高價: {latest['最高價']:.2f} TWD")
        print(f"   最低價: {latest['最低價']:.2f} TWD")
        print(f"   收盤價: {latest['收盤價']:.2f} TWD")
        print(f"   成交量: {latest['成交量']:,} 股")

        # 計算漲跌
        if len(df) > 1:
            prev_close = df.iloc[-2]['收盤價']
            change = latest['收盤價'] - prev_close
            change_pct = (change / prev_close) * 100
            change_symbol = "📈" if change > 0 else "📉" if change < 0 else "➡️"

            print(f"\n{change_symbol} 漲跌:")
            print(f"   漲跌額: {change:+.2f} TWD")
            print(f"   漲跌幅: {change_pct:+.2f}%")

        # 顯示資料來源
        stats = fetcher.get_stats()
        print(f"\n📊 資料來源統計:")
        print(f"   yfinance 成功: {stats['yfinance_success']}")
        print(f"   FinMind 成功: {stats['finmind_success']}")
        print(f"   參考資料使用: {stats['reference_used']}")

        print("\n✅ 首頁顯示測試通過")
        return True
    else:
        print("❌ 未獲取到資料")
        return False


def test_multiple_stocks():
    """測試獲取多支股票（首頁熱門股票列表）"""
    print("\n" + "=" * 70)
    print("📋 測試熱門股票列表")
    print("=" * 70)

    fetcher = UltimateTaiwanStockDataFetcher()

    # 熱門股票列表
    popular_stocks = [
        ('2330', '台積電'),
        ('2317', '鴻海'),
        ('2454', '聯發科'),
    ]

    results = []

    for stock_id, stock_name in popular_stocks:
        try:
            df = fetcher.get_stock_price(stock_id, days=5)
            if not df.empty:
                latest = df.iloc[-1]
                results.append({
                    '代碼': stock_id,
                    '名稱': stock_name,
                    '收盤價': latest['收盤價'],
                    '成交量': latest['成交量'],
                    '日期': df.index[-1]
                })
        except Exception as e:
            print(f"⚠️ 無法獲取 {stock_name} ({stock_id}): {e}")

    if results:
        print(f"\n✅ 成功獲取 {len(results)} 支股票\n")
        print("股票列表:")
        print("-" * 70)
        print(f"{'代碼':<8} {'名稱':<10} {'收盤價':>12} {'成交量':>15} {'日期':<12}")
        print("-" * 70)
        for stock in results:
            print(f"{stock['代碼']:<8} {stock['名稱']:<10} {stock['收盤價']:>12.2f} {stock['成交量']:>15,} {stock['日期'].strftime('%Y-%m-%d'):<12}")
        print("-" * 70)
        print("\n✅ 熱門股票列表測試通過")
        return True
    else:
        print("❌ 無法獲取任何股票資料")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🧪 首頁功能測試")
    print("=" * 70)
    print(f"\n執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 測試 1: 單支股票顯示
    test1 = test_home_page_stock_display()

    # 測試 2: 多支股票列表
    test2 = test_multiple_stocks()

    # 總結
    print("\n" + "=" * 70)
    print("測試總結")
    print("=" * 70)
    if test1 and test2:
        print("\n✅ 所有測試通過！")
        print("✅ 首頁可以正常顯示最新股價")
        print("✅ 系統準備就緒")
    else:
        print("\n❌ 部分測試失敗")
        if not test1:
            print("   - 單支股票顯示: 失敗")
        if not test2:
            print("   - 熱門股票列表: 失敗")

    print("\n" + "=" * 70)
