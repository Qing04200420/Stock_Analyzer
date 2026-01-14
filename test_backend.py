"""
後端功能測試腳本
用於測試各個模組是否正常運作
"""

import sys
import os

# 添加 backend 路徑
sys.path.append(os.path.dirname(__file__))

from backend.modules.data_fetcher import TaiwanStockDataFetcher
from backend.modules.risk_predictor import RiskPredictor
from backend.modules.strategy_analyzer import StrategyAnalyzer
from backend.modules.warrant_analyzer import WarrantAnalyzer

def test_data_fetcher():
    """測試資料獲取模組"""
    print("=" * 50)
    print("測試資料獲取模組")
    print("=" * 50)

    fetcher = TaiwanStockDataFetcher()

    # 測試獲取股票資料
    print("\n1. 測試獲取台積電(2330)最近30天資料...")
    df = fetcher.get_stock_price('2330', days=30)

    if not df.empty:
        print("✓ 成功獲取資料")
        print(f"  資料筆數: {len(df)}")
        print(f"  最新收盤價: {df['收盤價'].iloc[-1]:.2f}")
        print(f"  日期範圍: {df.index[0]} ~ {df.index[-1]}")
    else:
        print("✗ 無法獲取資料（可能是網路問題或市場休市）")

    # 測試獲取股票資訊
    print("\n2. 測試獲取股票基本資訊...")
    info = fetcher.get_stock_info('2330')

    if '錯誤' not in info:
        print("✓ 成功獲取資訊")
        print(f"  公司名稱: {info.get('公司名稱', 'N/A')}")
        print(f"  產業: {info.get('產業', 'N/A')}")
    else:
        print("✗ 無法獲取資訊")

    return df


def test_risk_predictor(df):
    """測試風險預測模組"""
    print("\n" + "=" * 50)
    print("測試風險預測模組")
    print("=" * 50)

    if df.empty:
        print("✗ 無測試資料，跳過風險預測測試")
        return

    predictor = RiskPredictor()

    print("\n1. 測試風險預測...")
    result = predictor.predict_risk(df)

    if '錯誤' not in result:
        print("✓ 風險預測成功")
        print(f"  波動率: {result['波動率']}")
        print(f"  Beta: {result['Beta']}")
        print(f"  Sharpe Ratio: {result['Sharpe Ratio']}")
        print(f"  風險等級: {result['風險評估']['風險等級']}")
        print(f"  建議: {result['風險評估']['建議']}")
    else:
        print(f"✗ 風險預測失敗: {result['錯誤']}")


def test_strategy_analyzer(df):
    """測試策略分析模組"""
    print("\n" + "=" * 50)
    print("測試策略分析模組")
    print("=" * 50)

    if df.empty:
        print("✗ 無測試資料，跳過策略分析測試")
        return

    analyzer = StrategyAnalyzer()

    print("\n1. 測試綜合策略分析...")
    result = analyzer.comprehensive_analysis(df)

    if result:
        print("✓ 策略分析成功")
        print(f"  綜合評分: {result['綜合評分']}")
        print(f"  操作建議: {result['操作建議']}")
        print(f"  操作方向: {result['操作方向']}")
        print(f"  MA信號: {result['移動平均線分析']['信號']}")
        print(f"  RSI信號: {result['RSI分析']['信號']}")
    else:
        print("✗ 策略分析失敗")

    print("\n2. 測試策略回測...")
    backtest = analyzer.backtest_strategy(df, initial_capital=100000)

    if '錯誤' not in backtest:
        print("✓ 回測成功")
        print(f"  初始資金: ${backtest['初始資金']:,.0f}")
        print(f"  最終資金: ${backtest['最終資金']:,.0f}")
        print(f"  報酬率: {backtest['報酬率']}")
        print(f"  交易次數: {backtest['交易次數']}")
    else:
        print(f"✗ 回測失敗: {backtest['錯誤']}")


def test_warrant_analyzer():
    """測試權證分析模組"""
    print("\n" + "=" * 50)
    print("測試權證分析模組")
    print("=" * 50)

    analyzer = WarrantAnalyzer()

    # 建立測試權證資料
    warrant_info = {
        '權證代碼': 'TEST01',
        '權證名稱': '測試認購01',
        '標的股票': '2330',
        '履約價': 650,
        '行使比例': 0.5,
        '到期日': '2024-12-31',
        '權證價格': 10.0
    }

    print("\n1. 測試權證分析...")
    result = analyzer.analyze_warrant(warrant_info, stock_price=600, volatility=0.3)

    if '錯誤' not in result:
        print("✓ 權證分析成功")
        print(f"  理論價格: {result['理論價格']}")
        print(f"  內含價值: {result['內含價值']}")
        print(f"  實質槓桿: {result['實質槓桿']}")
        print(f"  Delta: {result['Delta']}")
        print(f"  綜合評分: {result['綜合評分']}/100")
        print(f"  投資建議: {result['投資建議']}")
    else:
        print(f"✗ 權證分析失敗: {result['錯誤']}")


def main():
    """主測試函數"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "台灣股市投資系統 - 後端測試" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")

    try:
        # 測試資料獲取
        df = test_data_fetcher()

        # 測試風險預測
        test_risk_predictor(df)

        # 測試策略分析
        test_strategy_analyzer(df)

        # 測試權證分析
        test_warrant_analyzer()

        print("\n" + "=" * 50)
        print("測試完成！")
        print("=" * 50)
        print("\n提示：")
        print("- 如果某些測試失敗，可能是網路問題或市場休市")
        print("- 權證資料為示範資料，分析功能正常即可")
        print("- 執行 'streamlit run app.py' 啟動完整系統")
        print("\n")

    except Exception as e:
        print(f"\n✗ 測試過程發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
