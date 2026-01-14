"""
測試增強功能的腳本
驗證快取管理器、日誌系統、配置管理和增強資料獲取器是否正常運作
"""

import sys
import os
import io

# 設定 UTF-8 輸出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加路徑
sys.path.append(os.path.dirname(__file__))

def test_cache_manager():
    """測試快取管理器"""
    print("\n🧪 測試快取管理器...")
    try:
        from backend.utils.cache_manager import cache_manager

        # 設定和獲取快取
        cache_manager.set('test_key', {'data': 'test_value'}, ttl=60)
        result = cache_manager.get('test_key')

        assert result is not None, "快取設定失敗"
        assert result['data'] == 'test_value', "快取資料不正確"

        # 獲取統計資訊
        stats = cache_manager.get_stats()
        assert stats['總快取項目'] >= 1, "快取統計不正確"

        # 清空快取
        cache_manager.clear()
        result = cache_manager.get('test_key')
        assert result is None, "快取清空失敗"

        print("✅ 快取管理器測試通過")
        return True
    except Exception as e:
        print(f"❌ 快取管理器測試失敗: {e}")
        return False


def test_logger():
    """測試日誌系統"""
    print("\n🧪 測試日誌系統...")
    try:
        from backend.utils.logger import system_logger

        # 測試不同級別的日誌
        system_logger.debug("這是除錯訊息")
        system_logger.info("這是資訊訊息")
        system_logger.warning("這是警告訊息")

        print("✅ 日誌系統測試通過")
        return True
    except Exception as e:
        print(f"❌ 日誌系統測試失敗: {e}")
        return False


def test_settings():
    """測試配置管理"""
    print("\n🧪 測試配置管理...")
    try:
        from backend.config.settings import system_settings

        # 測試獲取預設值
        cache_enabled = system_settings.get('cache.enabled', True)
        assert isinstance(cache_enabled, bool), "配置類型不正確"

        # 測試設定值
        system_settings.set('test.value', 123)
        result = system_settings.get('test.value')
        assert result == 123, "配置設定失敗"

        # 測試巢狀路徑
        ma_periods = system_settings.get('technical_analysis.ma_periods', [5, 20, 60])
        assert isinstance(ma_periods, list), "配置結構不正確"

        print("✅ 配置管理測試通過")
        return True
    except Exception as e:
        print(f"❌ 配置管理測試失敗: {e}")
        return False


def test_enhanced_data_fetcher():
    """測試增強資料獲取器"""
    print("\n🧪 測試增強資料獲取器...")
    try:
        from backend.modules.data_fetcher_enhanced import EnhancedTaiwanStockDataFetcher

        fetcher = EnhancedTaiwanStockDataFetcher()

        # 測試獲取股價資料（會使用參考資料）
        df = fetcher.get_stock_price('2330', days=5)

        assert not df.empty, "資料獲取失敗"
        assert len(df) > 0, "資料為空"
        assert '收盤價' in df.columns, "資料欄位不正確"

        print(f"✅ 增強資料獲取器測試通過 (獲取了 {len(df)} 筆資料)")
        return True
    except Exception as e:
        print(f"❌ 增強資料獲取器測試失敗: {e}")
        return False


def main():
    """執行所有測試"""
    print("=" * 60)
    print("🚀 台灣股市投資分析系統 - 增強功能測試")
    print("=" * 60)

    results = []

    # 執行測試
    results.append(("快取管理器", test_cache_manager()))
    results.append(("日誌系統", test_logger()))
    results.append(("配置管理", test_settings()))
    results.append(("增強資料獲取器", test_enhanced_data_fetcher()))

    # 總結
    print("\n" + "=" * 60)
    print("📊 測試總結")
    print("=" * 60)

    for name, passed in results:
        status = "✅ 通過" if passed else "❌ 失敗"
        print(f"{name:20s} : {status}")

    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)

    print(f"\n總計: {total_passed}/{total_tests} 測試通過")

    if total_passed == total_tests:
        print("\n🎉 所有增強功能運作正常！")
        print("💡 您可以執行以下命令啟動系統：")
        print("   python -m streamlit run app.py")
        return 0
    else:
        print("\n⚠️ 部分功能測試失敗，請檢查錯誤訊息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
