@echo off
chcp 65001 > nul
echo ========================================
echo 台灣股市投資系統 - 環境修復與啟動
echo ========================================
echo.

echo [步驟 1] 檢查 Python 環境...
python --version
echo.

echo [步驟 2] 升級 pip...
python -m pip install --upgrade pip
echo.

echo [步驟 3] 安裝所有必要套件...
python -m pip install -r requirements.txt --upgrade
echo.

echo [步驟 4] 驗證 streamlit 安裝...
python -c "import streamlit; print('Streamlit 版本:', streamlit.__version__)"
echo.

echo [步驟 5] 測試所有模組...
python -c "import pandas, numpy, yfinance, twstock, plotly; print('所有核心模組載入成功!')"
echo.

echo ========================================
echo 環境檢查完成！準備啟動應用程式...
echo ========================================
echo.

pause

echo 正在啟動 Streamlit 應用...
python -m streamlit run app.py

pause
