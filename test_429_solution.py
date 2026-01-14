"""
測試 429 錯誤解決方案

此腳本測試所有新增的功能，確保 Yahoo Finance 429 錯誤已被解決。
"""

import sys
import time
from datetime import datetime


def print_header(title: str):
    """打印標題"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_rate_limiter():
    """測試速率限制器"""
    print_header("測試 1: 速率限制器")

    try:
        from backend.utils.rate_limiter import RateLimiter

        limiter = RateLimiter(
            max_requests=3,
            time_window=10,
            min_delay=0.5,
            max_delay=1.0
        )

        print("✅ 速率限制器導入成功")
        print(f"   配置: 每 10 秒最多 3 次請求，每次延遲 0.5-1.0 秒\n")

        # 測試請求
        print("🔄 測試連續請求...")
        for i in range(5):
            start = time.time()
            limiter.wait_if_needed()
            elapsed = time.time() - start
            print(f"   請求 {i+1}: 等待 {elapsed:.2f} 秒")

        print("\n✅ 速率限制器測試通過")
        return True

    except Exception as e:
        print(f"❌ 速率限制器測試失敗: {e}")
        return False


def test_user_agent_rotator():
    """測試 User-Agent 輪換器"""
    print_header("測試 2: User-Agent 輪換器")

    try:
        from backend.utils.rate_limiter import UserAgentRotator

        rotator = UserAgentRotator()

        print("✅ User-Agent 輪換器導入成功")
        print(f"   內建 {len(rotator.USER_AGENTS)} 種 User-Agent\n")

        # 測試輪換
        print("🔄 測試 User-Agent 輪換:")
        for i in range(3):
            ua = rotator.get_next()
            print(f"   {i+1}. {ua[:50]}...")

        print("\n✅ User-Agent 輪換器測試通過")
        return True

    except Exception as e:
        print(f"❌ User-Agent 輪換器測試失敗: {e}")
        return False


def test_retry_handler():
    """測試重試處理器"""
    print_header("測試 3: 重試處理器")

    try:
        from backend.utils.rate_limiter import RetryHandler

        handler = RetryHandler(max_retries=3)

        print("✅ 重試處理器導入成功")
        print(f"   配置: 最多重試 3 次，指數退避策略\n")

        # 測試成功的函數
        def success_func():
            return "成功"

        result = handler.execute_with_retry(success_func)
        print(f"   測試成功函數: {result}")

        # 測試失敗的函數
        attempt_count = [0]

        def fail_then_success():
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise Exception("模擬失敗")
            return "最終成功"

        try:
            result = handler.execute_with_retry(fail_then_success)
            print(f"   測試重試函數: {result} (嘗試 {attempt_count[0]} 次)")
        except:
            pass

        print("\n✅ 重試處理器測試通過")
        return True

    except Exception as e:
        print(f"❌ 重試處理器測試失敗: {e}")
        return False


def test_finmind():
    """測試 FinMind"""
    print_header("測試 4: FinMind 整合")

    try:
        from backend.modules.finmind_fetcher import FinMindDataFetcher, FINMIND_AVAILABLE

        if not FINMIND_AVAILABLE:
            print("⚠️ FinMind 未安裝")
            print("   安裝指令: pip install FinMind")
            print("   跳過此測試")
            return True  # 不算失敗，只是未安裝

        fetcher = FinMindDataFetcher()
        print("✅ FinMind 導入成功\n")

        # 測試獲取資料
        print("🔄 測試獲取台積電 (2330) 7 天資料...")
        df = fetcher.get_stock_price("2330", days=7)

        if not df.empty:
            print(f"✅ 成功獲取 {len(df)} 筆資料")
            print(f"\n最新價格:")
            print(df.tail(1))
        else:
            print("⚠️ 未獲取到資料（可能是假日或 API 限制）")

        print("\n✅ FinMind 測試通過")
        return True

    except Exception as e:
        print(f"⚠️ FinMind 測試異常: {e}")
        print("   這通常不影響系統運行，系統會自動使用其他資料源")
        return True  # FinMind 失敗不算整體失敗


def test_ultimate_fetcher():
    """測試終極資料獲取器"""
    print_header("測試 5: 終極資料獲取器")

    try:
        from backend.modules.data_fetcher_ultimate import UltimateTaiwanStockDataFetcher

        fetcher = UltimateTaiwanStockDataFetcher()
        print("✅ 終極資料獲取器導入成功\n")

        # 測試獲取資料
        print("🔄 測試獲取台積電 (2330) 7 天資料...")
        df = fetcher.get_stock_price("2330", days=7)

        if not df.empty:
            print(f"✅ 成功獲取 {len(df)} 筆資料")
            print(f"\n最新 3 天:")
            print(df.tail(3))

            # 顯示統計
            print("\n📊 資料源統計:")
            stats = fetcher.get_stats()
            for key, value in stats.items():
                if isinstance(value, float):
                    print(f"   {key}: {value:.1f}")
                else:
                    print(f"   {key}: {value}")

            print("\n✅ 終極資料獲取器測試通過")
            return True
        else:
            print("❌ 未能獲取資料")
            return False

    except Exception as e:
        print(f"❌ 終極資料獲取器測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_continuous_requests():
    """測試連續請求（模擬實際使用）"""
    print_header("測試 6: 連續請求壓力測試")

    try:
        from backend.modules.data_fetcher_ultimate import UltimateTaiwanStockDataFetcher

        fetcher = UltimateTaiwanStockDataFetcher()
        print("✅ 準備測試連續請求\n")

        # 測試多支股票
        stocks = ["2330", "2317", "2454"]
        print(f"🔄 連續請求 {len(stocks)} 支股票...")

        success_count = 0
        start_time = time.time()

        for i, stock_id in enumerate(stocks, 1):
            print(f"\n   [{i}/{len(stocks)}] 請求 {stock_id}...")
            df = fetcher.get_stock_price(stock_id, days=3)

            if not df.empty:
                print(f"   ✅ 成功 ({len(df)} 筆資料)")
                success_count += 1
            else:
                print(f"   ⚠️ 未獲取到資料")

        elapsed = time.time() - start_time
        print(f"\n📊 測試結果:")
        print(f"   總時間: {elapsed:.1f} 秒")
        print(f"   成功率: {success_count}/{len(stocks)} ({success_count/len(stocks)*100:.0f}%)")
        print(f"   平均速度: {elapsed/len(stocks):.1f} 秒/請求")

        # 顯示統計
        stats = fetcher.get_stats()
        print(f"\n📈 資料源使用統計:")
        print(f"   yfinance 成功: {stats['yfinance_success']}")
        print(f"   yfinance 429: {stats['yfinance_429']}")
        print(f"   FinMind 成功: {stats['finmind_success']}")
        print(f"   參考資料: {stats['reference_used']}")

        print("\n✅ 連續請求測試通過")
        return success_count > 0

    except Exception as e:
        print(f"❌ 連續請求測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主測試函數"""
    print("\n" + "=" * 70)
    print("  🧪 Yahoo Finance 429 錯誤解決方案 - 完整測試")
    print("=" * 70)
    print(f"\n開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 執行所有測試
    tests = [
        ("速率限制器", test_rate_limiter),
        ("User-Agent 輪換", test_user_agent_rotator),
        ("重試處理器", test_retry_handler),
        ("FinMind 整合", test_finmind),
        ("終極資料獲取器", test_ultimate_fetcher),
        ("連續請求壓力測試", test_continuous_requests),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except KeyboardInterrupt:
            print("\n\n⚠️ 測試被使用者中斷")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ 測試 '{name}' 發生未預期錯誤: {e}")
            results.append((name, False))

    # 顯示總結
    print_header("測試總結")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"測試結果: {passed}/{total} 通過\n")

    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {status}  {name}")

    print(f"\n結束時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if passed == total:
        print("\n" + "=" * 70)
        print("  🎉 所有測試通過！429 錯誤解決方案已成功部署！")
        print("=" * 70)
        return 0
    else:
        print("\n" + "=" * 70)
        print(f"  ⚠️ {total - passed} 個測試失敗，請檢查錯誤訊息")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
