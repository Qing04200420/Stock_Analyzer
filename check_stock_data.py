"""
快速診斷腳本 - 檢查股價資料是否為最新

此腳本會：
1. 檢查終極版是否可用
2. 測試獲取台積電最新價格
3. 對比參考價格，判斷是否為最新資料
4. 提供升級建議
"""

import sys
from datetime import datetime, timedelta


def print_header(title: str):
    """打印標題"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def check_ultimate_fetcher():
    """檢查終極版資料獲取器"""
    print_header("檢查 1: 終極版資料獲取器")

    try:
        from backend.modules.data_fetcher_ultimate import UltimateTaiwanStockDataFetcher
        print("✅ 終極版資料獲取器：已安裝")
        return True
    except ImportError as e:
        print("❌ 終極版資料獲取器：未安裝")
        print(f"   錯誤: {e}")
        return False


def check_finmind():
    """檢查 FinMind"""
    print_header("檢查 2: FinMind 台股 API")

    try:
        import FinMind
        print("✅ FinMind：已安裝")
        print(f"   版本: {FinMind.__version__ if hasattr(FinMind, '__version__') else '未知'}")
        return True
    except ImportError:
        print("❌ FinMind：未安裝")
        print("   安裝指令: pip install FinMind")
        return False


def test_stock_data():
    """測試股價資料"""
    print_header("檢查 3: 測試台積電 (2330) 股價資料")

    # 舊的參考價格（2024-01）
    OLD_REFERENCE_PRICE = 618.0

    try:
        # 嘗試使用終極版
        try:
            from backend.modules.data_fetcher_ultimate import UltimateTaiwanStockDataFetcher
            fetcher = UltimateTaiwanStockDataFetcher()
            print("📊 使用終極版獲取資料...\n")
        except ImportError:
            # 降級到增強版
            try:
                from backend.modules.data_fetcher_enhanced import EnhancedTaiwanStockDataFetcher
                fetcher = EnhancedTaiwanStockDataFetcher()
                print("📊 使用增強版獲取資料...\n")
            except ImportError:
                # 降級到基礎版
                from backend.modules.data_fetcher import TaiwanStockDataFetcher
                fetcher = TaiwanStockDataFetcher()
                print("📊 使用基礎版獲取資料...\n")

        # 獲取資料
        df = fetcher.get_stock_price("2330", days=5)

        if df.empty:
            print("❌ 無法獲取資料")
            return False

        # 分析資料
        latest_date = df.index[-1]
        latest_price = df['收盤價'].iloc[-1]
        days_ago = (datetime.now() - latest_date).days

        print(f"最新日期: {latest_date.strftime('%Y-%m-%d')}")
        print(f"最新收盤價: {latest_price:.2f} TWD")
        print(f"資料落後: {days_ago} 天")
        print(f"\n資料範圍:")
        print(f"  開始: {df.index[0].strftime('%Y-%m-%d')}")
        print(f"  結束: {df.index[-1].strftime('%Y-%m-%d')}")
        print(f"  筆數: {len(df)}")

        # 判斷資料新鮮度
        print("\n" + "=" * 70)

        if days_ago <= 3:
            print("✅ 資料判定: 最新（3 天內）")
            print("   狀態: 正常，無需升級")
            is_fresh = True
        elif days_ago <= 7:
            print("⚠️ 資料判定: 稍舊（3-7 天）")
            print("   狀態: 可接受，建議檢查快取")
            is_fresh = True
        elif days_ago <= 30:
            print("⚠️ 資料判定: 過時（7-30 天）")
            print("   狀態: 需要升級或清除快取")
            is_fresh = False
        else:
            print("❌ 資料判定: 嚴重過時（>30 天）")
            print("   狀態: 使用參考資料，需要升級")
            is_fresh = False

        # 檢查是否為舊參考資料
        if abs(latest_price - OLD_REFERENCE_PRICE) < 10:
            print("\n⚠️ 警告: 價格接近舊參考價格（618 TWD）")
            print("   可能正在使用 2024-01 的參考資料")
            is_fresh = False

        print("=" * 70)

        return is_fresh

    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def provide_recommendations(ultimate_ok, finmind_ok, data_fresh):
    """提供建議"""
    print_header("診斷結果與建議")

    if ultimate_ok and finmind_ok and data_fresh:
        print("🎉 恭喜！您的系統狀態完美！\n")
        print("✅ 終極版資料獲取器：已啟用")
        print("✅ FinMind API：已安裝")
        print("✅ 股價資料：最新")
        print("\n💡 您的系統已是最佳配置，享受使用！")

    else:
        print("⚠️ 檢測到問題，需要採取行動：\n")

        # 問題 1: 終極版未安裝
        if not ultimate_ok:
            print("❌ 問題 1: 終極版資料獲取器未安裝")
            print("   影響: 無法獲取最新股價，容易遇到 429 錯誤")
            print("   解決: 檔案已創建，請重啟系統")
            print()

        # 問題 2: FinMind 未安裝
        if not finmind_ok:
            print("❌ 問題 2: FinMind 未安裝")
            print("   影響: 缺少台股專用備援資料源")
            print("   解決: 執行以下命令")
            print("   ```")
            print("   pip install FinMind")
            print("   ```")
            print()

        # 問題 3: 資料過時
        if not data_fresh:
            print("❌ 問題 3: 股價資料過時")
            print("   影響: 顯示幾年前的價格，無法用於實際投資")
            print("   解決:")
            print("   1. 確保 FinMind 已安裝")
            print("   2. 重新啟動系統: python -m streamlit run app.py")
            print("   3. 清除快取: 進入「系統設定」→「快取管理」→「清空快取」")
            print()

        print("\n📋 完整升級步驟:")
        print("=" * 70)
        print("1. 安裝 FinMind:")
        print("   pip install FinMind")
        print()
        print("2. 重啟系統:")
        print("   python -m streamlit run app.py")
        print()
        print("3. 驗證升級:")
        print("   - 首頁應顯示「🚀 終極版已啟用」")
        print("   - 股票分析頁面顯示最新價格")
        print()
        print("4. 如果仍有問題:")
        print("   python test_429_solution.py  # 運行完整測試")
        print("=" * 70)


def main():
    """主函數"""
    print("\n" + "=" * 70)
    print("  🔍 股價資料診斷工具")
    print("=" * 70)
    print(f"\n執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 執行檢查
    ultimate_ok = check_ultimate_fetcher()
    finmind_ok = check_finmind()
    data_fresh = test_stock_data()

    # 提供建議
    provide_recommendations(ultimate_ok, finmind_ok, data_fresh)

    print("\n" + "=" * 70)
    print("  診斷完成")
    print("=" * 70)

    # 返回狀態碼
    if ultimate_ok and finmind_ok and data_fresh:
        print("\n✅ 系統狀態: 完美")
        return 0
    else:
        print("\n⚠️ 系統狀態: 需要升級")
        return 1


if __name__ == "__main__":
    sys.exit(main())
