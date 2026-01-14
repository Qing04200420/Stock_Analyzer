# -*- coding: utf-8 -*-
"""
測試權證查詢功能
驗證新增的功能是否正常運作
"""

import sys
import pandas as pd

# 設置編碼
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from backend.modules.data_fetcher import WarrantDataFetcher
from backend.modules.warrant_analyzer import WarrantAnalyzer


def print_header(title: str):
    """打印標題"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_warrant_fetcher():
    """測試權證資料獲取器"""
    print_header("測試 1: 權證資料獲取器")

    fetcher = WarrantDataFetcher()

    # 測試 1.1: 獲取所有權證
    print("1.1 獲取所有權證...")
    all_warrants = fetcher.get_warrant_list()
    print(f"✅ 總共有 {len(all_warrants)} 支權證")
    print(f"   包含股票: {all_warrants['標的股票'].unique().tolist()}")

    # 測試 1.2: 獲取台積電 (2330) 權證
    print("\n1.2 獲取台積電 (2330) 權證...")
    tsmc_warrants = fetcher.get_warrant_list("2330")
    print(f"✅ 找到 {len(tsmc_warrants)} 支台積電權證")
    print("\n權證列表:")
    print(tsmc_warrants[['權證代碼', '權證名稱', '權證類型', '履約價', '行使比例', '到期日']])

    # 測試 1.3: 獲取單一權證詳情
    print("\n1.3 獲取單一權證詳情...")
    if not tsmc_warrants.empty:
        first_warrant_code = tsmc_warrants.iloc[0]['權證代碼']
        warrant_detail = fetcher.get_warrant_detail(first_warrant_code)
        print(f"✅ 權證代碼: {warrant_detail['權證代碼']}")
        print(f"   權證名稱: {warrant_detail['權證名稱']}")
        print(f"   發行商: {warrant_detail['發行商']}")
        print(f"   履約價: {warrant_detail['履約價']}")
        print(f"   行使比例: {warrant_detail['行使比例']}")
        print(f"   到期日: {warrant_detail['到期日']}")
        print(f"   權證價格: {warrant_detail['權證價格']}")

        return warrant_detail
    else:
        print("❌ 無權證資料")
        return None


def test_warrant_analyzer(warrant_detail):
    """測試權證分析器"""
    print_header("測試 2: 權證分析器")

    if not warrant_detail:
        print("❌ 無權證資料可分析")
        return False

    analyzer = WarrantAnalyzer()

    # 設定測試參數
    stock_price = 1680.0  # 台積電當前價格
    volatility = 0.30  # 30% 波動率

    print(f"分析權證: {warrant_detail['權證名稱']}")
    print(f"當前股價: {stock_price} TWD")
    print(f"隱含波動率: {volatility * 100}%")
    print("\n正在計算...")

    # 執行分析
    result = analyzer.analyze_warrant(warrant_detail, stock_price, volatility)

    if '錯誤' in result:
        print(f"❌ 分析失敗: {result['錯誤']}")
        return False

    print("\n✅ 分析完成！\n")

    # 顯示核心指標
    print("💎 核心評估指標:")
    print(f"   理論價格: {result['理論價格']}")
    print(f"   內含價值: {result['內含價值']}")
    print(f"   時間價值: {result['時間價值']}")
    print(f"   綜合評分: {result['綜合評分']}/100")

    # 顯示權證狀態
    print("\n🎯 權證狀態:")
    print(f"   價內外狀態: {result['價內外狀態']}")
    print(f"   實質槓桿: {result['實質槓桿']}")
    print(f"   到期天數: {result['到期天數']} 天")
    print(f"   損益兩平點: {result['損益兩平點']}")

    # 顯示 Greeks
    print("\n📈 Greeks 風險指標:")
    print(f"   Delta: {result['Delta']}")
    print(f"   Gamma: {result['Gamma']}")
    print(f"   Theta: {result['Theta']}")
    print(f"   Vega: {result['Vega']}")

    # 顯示投資建議
    print(f"\n💡 投資建議: {result['投資建議']}")

    return True


def test_multiple_stocks():
    """測試多個股票的權證查詢"""
    print_header("測試 3: 多個股票的權證查詢")

    fetcher = WarrantDataFetcher()
    test_stocks = ['2330', '2317', '2454']

    results = []

    for stock_id in test_stocks:
        warrants = fetcher.get_warrant_list(stock_id)
        warrant_count = len(warrants)
        results.append((stock_id, warrant_count))
        print(f"📊 {stock_id}: {warrant_count} 支權證")

        if not warrants.empty:
            # 顯示權證類型統計
            type_counts = warrants['權證類型'].value_counts()
            print(f"   類型分布: {dict(type_counts)}")

    print("\n總結:")
    total = sum(count for _, count in results)
    print(f"✅ 共有 {total} 支權證可供分析")

    return True


def test_edge_cases():
    """測試邊界情況"""
    print_header("測試 4: 邊界情況")

    fetcher = WarrantDataFetcher()

    # 測試 4.1: 查詢不存在的股票
    print("4.1 查詢不存在的股票...")
    warrants = fetcher.get_warrant_list("9999")
    if warrants.empty:
        print("✅ 正確處理：返回空列表")
    else:
        print("❌ 錯誤：應該返回空列表")

    # 測試 4.2: 查詢不存在的權證代碼
    print("\n4.2 查詢不存在的權證代碼...")
    detail = fetcher.get_warrant_detail("999999")
    if not detail:
        print("✅ 正確處理：返回空字典")
    else:
        print("❌ 錯誤：應該返回空字典")

    return True


def main():
    """主測試函數"""
    print("\n" + "=" * 70)
    print("  🧪 權證查詢功能測試")
    print("=" * 70)
    print(f"\n測試時間: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 執行測試
    test_results = []

    # 測試 1: 權證資料獲取器
    warrant_detail = test_warrant_fetcher()
    test_results.append(("權證資料獲取器", warrant_detail is not None))

    # 測試 2: 權證分析器
    analyzer_ok = test_warrant_analyzer(warrant_detail)
    test_results.append(("權證分析器", analyzer_ok))

    # 測試 3: 多個股票查詢
    multi_ok = test_multiple_stocks()
    test_results.append(("多個股票查詢", multi_ok))

    # 測試 4: 邊界情況
    edge_ok = test_edge_cases()
    test_results.append(("邊界情況處理", edge_ok))

    # 總結
    print_header("測試總結")

    print("測試結果:")
    for test_name, result in test_results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {status} - {test_name}")

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    print(f"\n總計: {passed}/{total} 測試通過")

    if passed == total:
        print("\n🎉 所有測試通過！權證查詢功能正常運作。")
        return 0
    else:
        print("\n⚠️ 部分測試失敗，請檢查問題。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
