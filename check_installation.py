"""
安裝檢查腳本
檢查 Python 版本和所需套件是否正確安裝
"""

import sys

def check_python_version():
    """檢查 Python 版本"""
    print("=" * 60)
    print("檢查 Python 版本")
    print("=" * 60)

    version = sys.version_info
    print(f"當前 Python 版本: {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 8:
        print("✓ Python 版本符合要求（3.8 或以上）\n")
        return True
    else:
        print("✗ Python 版本過舊，請升級至 3.8 或以上版本\n")
        return False


def check_packages():
    """檢查必要套件"""
    print("=" * 60)
    print("檢查必要套件")
    print("=" * 60)

    packages = {
        'streamlit': 'Streamlit Web 框架',
        'pandas': '資料處理工具',
        'numpy': '數值計算工具',
        'yfinance': 'Yahoo Finance API',
        'twstock': '台灣股市資料',
        'plotly': '圖表視覺化',
        'sklearn': '機器學習工具',
        'ta': '技術分析指標',
        'scipy': '科學計算',
    }

    all_installed = True

    for package_name, description in packages.items():
        try:
            if package_name == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package_name)
            print(f"✓ {package_name:15} - {description}")
        except ImportError:
            print(f"✗ {package_name:15} - {description} [未安裝]")
            all_installed = False

    print()

    if all_installed:
        print("✓ 所有必要套件已安裝\n")
    else:
        print("✗ 部分套件未安裝，請執行：pip install -r requirements.txt\n")

    return all_installed


def check_package_versions():
    """檢查套件版本"""
    print("=" * 60)
    print("套件版本資訊")
    print("=" * 60)

    packages_to_check = [
        'streamlit',
        'pandas',
        'numpy',
        'yfinance',
        'twstock',
        'plotly',
        'sklearn',
        'ta',
        'scipy',
    ]

    for package_name in packages_to_check:
        try:
            if package_name == 'sklearn':
                import sklearn
                module = sklearn
            else:
                module = __import__(package_name)

            version = getattr(module, '__version__', 'unknown')
            print(f"{package_name:15} : {version}")
        except ImportError:
            print(f"{package_name:15} : [未安裝]")

    print()


def test_imports():
    """測試模組導入"""
    print("=" * 60)
    print("測試後端模組導入")
    print("=" * 60)

    modules_to_test = [
        ('backend.modules.data_fetcher', 'TaiwanStockDataFetcher'),
        ('backend.modules.risk_predictor', 'RiskPredictor'),
        ('backend.modules.strategy_analyzer', 'StrategyAnalyzer'),
        ('backend.modules.warrant_analyzer', 'WarrantAnalyzer'),
    ]

    all_ok = True

    for module_path, class_name in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✓ {module_path}")
        except Exception as e:
            print(f"✗ {module_path} - 錯誤: {str(e)}")
            all_ok = False

    print()

    if all_ok:
        print("✓ 所有後端模組可正常導入\n")
    else:
        print("✗ 部分模組導入失敗\n")

    return all_ok


def check_system_info():
    """顯示系統資訊"""
    print("=" * 60)
    print("系統資訊")
    print("=" * 60)

    import platform

    print(f"作業系統: {platform.system()}")
    print(f"版本: {platform.release()}")
    print(f"架構: {platform.machine()}")
    print(f"處理器: {platform.processor()}")
    print()


def main():
    """主函數"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "台灣股市投資系統 - 安裝檢查" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")

    # 檢查系統資訊
    check_system_info()

    # 檢查 Python 版本
    python_ok = check_python_version()

    # 檢查套件
    packages_ok = check_packages()

    # 檢查套件版本
    check_package_versions()

    # 測試模組導入
    modules_ok = test_imports()

    # 總結
    print("=" * 60)
    print("檢查結果總結")
    print("=" * 60)

    if python_ok and packages_ok and modules_ok:
        print("✓ 所有檢查通過！系統已就緒。")
        print("\n下一步：")
        print("  1. 執行測試：python test_backend.py")
        print("  2. 啟動應用：streamlit run app.py")
        print("  3. 或直接執行：start.bat (Windows) / ./start.sh (Linux/macOS)")
    else:
        print("✗ 部分檢查未通過，請修正後再試。")
        print("\n建議步驟：")
        if not python_ok:
            print("  1. 升級 Python 至 3.8 或以上版本")
        if not packages_ok:
            print("  2. 安裝必要套件：pip install -r requirements.txt")
        if not modules_ok:
            print("  3. 檢查專案檔案是否完整")

    print("\n" + "=" * 60)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n檢查已中斷。")
    except Exception as e:
        print(f"\n✗ 發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
