"""
台灣股市投資系統 - Streamlit 主程式
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import sys
import os

# 添加 backend 路徑
sys.path.append(os.path.dirname(__file__))

from backend.modules.data_fetcher import TaiwanStockDataFetcher, WarrantDataFetcher

# 嘗試導入終極版資料獲取器（優先）
ULTIMATE_FETCHER_AVAILABLE = False
ENHANCED_FEATURES_AVAILABLE = False

try:
    from backend.modules.data_fetcher_ultimate import UltimateTaiwanStockDataFetcher
    ULTIMATE_FETCHER_AVAILABLE = True
except ImportError:
    pass

# 如果終極版不可用，嘗試增強版
if not ULTIMATE_FETCHER_AVAILABLE:
    try:
        from backend.modules.data_fetcher_enhanced import EnhancedTaiwanStockDataFetcher
        from backend.utils.cache_manager import cache_manager
        from backend.utils.logger import system_logger
        from backend.config.settings import system_settings
        ENHANCED_FEATURES_AVAILABLE = True
    except ImportError:
        pass
from backend.modules.risk_predictor import RiskPredictor
from backend.modules.strategy_analyzer import StrategyAnalyzer
from backend.modules.warrant_analyzer import WarrantAnalyzer
from backend.modules.technical_analyzer import TechnicalAnalyzer
from backend.modules.stock_comparator import StockComparator
from backend.modules.portfolio_manager import PortfolioManager
from backend.modules.market_sentiment import MarketSentimentAnalyzer

# 頁面設定
st.set_page_config(
    page_title="台灣股市投資系統",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 統一現代化 CSS 樣式 - 深色主題適配
st.markdown("""
    <style>
    /* 主標題 - 增強對比度，適配深色主題 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        border: 3px solid rgba(102, 126, 234, 0.6);
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
    }

    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        color: #ffffff !important;
        text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.5);
    }

    /* 頁面標題 - 增強對比度 */
    .page-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        border: 3px solid rgba(102, 126, 234, 0.6);
    }

    .page-header h1 {
        color: #ffffff !important;
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
        font-weight: 700;
    }

    .page-header p {
        color: #ffffff !important;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.5);
    }

    /* 卡片樣式 - 適配深色主題 */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }

    /* 漸變卡片 */
    .gradient-card {
        border-radius: 10px;
        padding: 1.5rem;
        transition: transform 0.2s;
    }

    .gradient-card:hover {
        transform: translateY(-2px);
    }

    /* 成功/警告/危險框 - 深色主題適配 */
    .success-box {
        background: rgba(40, 167, 69, 0.15);
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #28a745;
        font-weight: 500;
    }

    .warning-box {
        background: rgba(255, 193, 7, 0.15);
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #ff9800;
        font-weight: 500;
    }

    .danger-box {
        background: rgba(220, 53, 69, 0.15);
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #dc3545;
        font-weight: 500;
    }

    .info-box {
        background: rgba(23, 162, 184, 0.15);
        border: 2px solid #17a2b8;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #17a2b8;
        font-weight: 500;
    }

    /* 功能卡片 - 深色主題適配 */
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        border-color: #667eea;
        background: rgba(255, 255, 255, 1);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    /* 統計卡片 - 深色主題適配 */
    .stat-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        text-align: center;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }

    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
        color: #667eea;
    }

    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
    }

    /* 按鈕樣式 */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #7c8ef7 0%, #8a5db8 100%);
    }

    .stButton>button:active {
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
    }

    /* 側邊欄樣式 */
    .css-1d391kg {
        background-color: #f8f9fa;
    }

    /* 標籤頁樣式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }

    /* 展開面板樣式 */
    .streamlit-expanderHeader {
        border-radius: 10px;
        background-color: #f8f9fa;
        font-weight: 600;
    }

    /* 進度條樣式 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    /* 滑塊樣式 */
    .stSlider > div > div > div > div {
        background-color: #667eea;
    }

    /* 輸入框樣式 */
    .stTextInput > div > div > input {
        border-radius: 10px;
    }

    .stNumberInput > div > div > input {
        border-radius: 10px;
    }

    /* 選擇框樣式 */
    .stSelectbox > div > div > div {
        border-radius: 10px;
    }

    /* 隱藏 Streamlit 預設元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 響應式設計 */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        .feature-card {
            padding: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 初始化 Session State
if 'data_fetcher' not in st.session_state:
    # 優先使用終極版資料獲取器（最新資料 + 429 錯誤解決）
    if ULTIMATE_FETCHER_AVAILABLE:
        st.session_state.data_fetcher = UltimateTaiwanStockDataFetcher()
        st.session_state.fetcher_version = "ultimate"
        if ENHANCED_FEATURES_AVAILABLE:
            system_logger.info("✅ 使用終極版資料獲取器（多層備援 + 最新資料）")
    # 降級到增強版
    elif ENHANCED_FEATURES_AVAILABLE:
        st.session_state.data_fetcher = EnhancedTaiwanStockDataFetcher()
        st.session_state.fetcher_version = "enhanced"
        system_logger.info("⚠️ 使用增強版資料獲取器（建議升級）")
    # 最後降級到基礎版
    else:
        st.session_state.data_fetcher = TaiwanStockDataFetcher()
        st.session_state.fetcher_version = "basic"

if 'risk_predictor' not in st.session_state:
    st.session_state.risk_predictor = RiskPredictor()
if 'strategy_analyzer' not in st.session_state:
    st.session_state.strategy_analyzer = StrategyAnalyzer()
if 'warrant_analyzer' not in st.session_state:
    st.session_state.warrant_analyzer = WarrantAnalyzer()
if 'warrant_fetcher' not in st.session_state:
    st.session_state.warrant_fetcher = WarrantDataFetcher()
if 'technical_analyzer' not in st.session_state:
    st.session_state.technical_analyzer = TechnicalAnalyzer()
if 'stock_comparator' not in st.session_state:
    st.session_state.stock_comparator = StockComparator(st.session_state.data_fetcher)
if 'portfolio_manager' not in st.session_state:
    st.session_state.portfolio_manager = PortfolioManager(st.session_state.data_fetcher)
if 'market_sentiment' not in st.session_state:
    st.session_state.market_sentiment = MarketSentimentAnalyzer(st.session_state.data_fetcher)

# 初始化系統狀態標記
if 'enhanced_features' not in st.session_state:
    st.session_state.enhanced_features = ENHANCED_FEATURES_AVAILABLE


def plot_stock_price(df: pd.DataFrame, title: str = "股價走勢圖"):
    """繪製股價K線圖"""
    if df.empty:
        st.warning("無資料可顯示")
        return

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['開盤價'],
        high=df['最高價'],
        low=df['最低價'],
        close=df['收盤價'],
        name='K線'
    )])

    fig.update_layout(
        title=title,
        xaxis_title="日期",
        yaxis_title="價格",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_technical_indicators(df: pd.DataFrame):
    """繪製技術指標圖"""
    if df.empty or '收盤價' not in df.columns:
        st.warning("無資料可顯示")
        return

    # 建立子圖
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('價格與均線', 'MACD', 'RSI'),
        row_heights=[0.5, 0.25, 0.25]
    )

    # 價格與均線
    fig.add_trace(go.Scatter(x=df.index, y=df['收盤價'], name='收盤價', line=dict(color='blue')), row=1, col=1)

    if 'MA5' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MA5'], name='MA5', line=dict(color='orange')), row=1, col=1)
    if 'MA20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20', line=dict(color='red')), row=1, col=1)
    if 'MA60' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MA60'], name='MA60', line=dict(color='purple')), row=1, col=1)

    # MACD
    if 'MACD' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal', line=dict(color='red')), row=2, col=1)
        fig.add_trace(go.Bar(x=df.index, y=df['MACD_Diff'], name='Diff', marker_color='gray'), row=2, col=1)

    # RSI
    if 'RSI' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')), row=3, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

    fig.update_layout(height=800, template="plotly_white", showlegend=True)
    fig.update_xaxes(title_text="日期", row=3, col=1)
    fig.update_yaxes(title_text="價格", row=1, col=1)
    fig.update_yaxes(title_text="MACD", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)

    st.plotly_chart(fig, use_container_width=True)


def main():
    """主程式"""
    # 主標題 - 使用更鮮明的樣式
    st.markdown("""
    <div class="main-header">
        <h1 style='text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>📈 台灣股市投資分析系統</h1>
        <p style='text-shadow: 1px 1px 2px rgba(0,0,0,0.15);'>專業級技術分析 | 智能風險評估 | 策略回測驗證</p>
    </div>
    """, unsafe_allow_html=True)

    # 初始化當前頁面狀態
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 首頁"

    # 側邊欄設計
    with st.sidebar:
        st.markdown("### 🎯 功能選單")
        st.markdown("<br>", unsafe_allow_html=True)

        # 使用 session_state 來同步頁面選擇
        page_options = ["🏠 首頁", "📊 股票分析", "📈 技術分析", "📊 多股比較",
                       "💼 投資組合", "🎭 市場情緒", "⚠️ 風險評估",
                       "💡 投資策略", "🎯 權證分析", "⚙️ 系統設定"]
        page = st.radio(
            "選擇分析功能",
            page_options,
            index=page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0,
            label_visibility="collapsed"
        )

        # 更新 session_state
        st.session_state.current_page = page

        st.markdown("---")
        st.markdown("### 📌 快速提示")
        st.info("💡 每個功能都提供詳細的技術指標和專業分析")

        st.markdown("---")
        st.markdown("### 📊 系統狀態")
        st.success("✅ 系統運行正常")
        st.caption("資料來源: Yahoo Finance + 本地參考資料")

    if page == "🏠 首頁":
        show_home_page()
    elif page == "📊 股票分析":
        show_stock_analysis_page()
    elif page == "📈 技術分析":
        show_technical_analysis_page()
    elif page == "📊 多股比較":
        show_stock_comparison_page()
    elif page == "💼 投資組合":
        show_portfolio_page()
    elif page == "🎭 市場情緒":
        show_market_sentiment_page()
    elif page == "⚠️ 風險評估":
        show_risk_assessment_page()
    elif page == "💡 投資策略":
        show_strategy_page()
    elif page == "🎯 權證分析":
        show_warrant_page()
    elif page == "⚙️ 系統設定":
        show_settings_page()


def show_home_page():
    """首頁 - 全新設計"""

    # 歡迎橫幅 - 深色主題適配
    st.markdown("""
    <div style='text-align: center; padding: 2.5rem;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
                border-radius: 15px;
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
                margin-bottom: 1.5rem;
                border: 3px solid rgba(102, 126, 234, 0.6);'>
        <h1 style='color: #ffffff; font-size: 2.5rem; margin-bottom: 1rem; font-weight: 700; text-shadow: 2px 2px 8px rgba(0,0,0,0.6);'>
            🎉 歡迎使用台灣股市投資分析系統
        </h1>
        <p style='color: #ffffff; font-size: 1.2rem; margin: 0; text-shadow: 1px 1px 6px rgba(0,0,0,0.5);'>
            結合多項技術指標，提供專業投資決策支援
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 系統狀態指示器
    fetcher_version = st.session_state.get('fetcher_version', 'basic')

    if fetcher_version == 'ultimate':
        st.markdown("""
        <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
             padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem;
             color: white; text-align: center; box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
             font-size: 1.05rem;">
            <strong style='font-size: 1.15rem;'>🚀 終極版已啟用</strong> |
            最新股價 ✓ | 智能限流 ✓ | 多層備援 ✓ | 429錯誤解決 ✓ | User-Agent輪換 ✓
        </div>
        """, unsafe_allow_html=True)
    elif fetcher_version == 'enhanced':
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
             padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem;
             color: white; text-align: center; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
             font-size: 1.05rem;">
            <strong style='font-size: 1.15rem;'>✨ 專業版模式已啟用</strong> |
            快取系統 ✓ | 日誌記錄 ✓ | 配置管理 ✓ | 智慧重試 ✓
        </div>
        """, unsafe_allow_html=True)
        # 靜默模式：不顯示升級建議
    else:
        # 標準模式無需提示
        pass

    # 核心功能卡片 - 可點擊跳轉
    st.markdown("### 🚀 核心功能")
    st.markdown("<p style='color: #64748b; margin-bottom: 1rem;'>點擊下方卡片快速進入對應功能</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # 使用容器製作可點擊的卡片效果
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 style='color: #667eea; margin-bottom: 0.5rem; font-weight: 700;'>股票分析</h3>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.6;'>
                • K線圖表<br>
                • 歷史走勢<br>
                • 即時報價<br>
                • 基本資訊
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📊 進入股票分析", key="nav_stock", use_container_width=True):
            st.session_state.current_page = "📊 股票分析"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚠️</div>
            <h3 style='color: #f59e0b; margin-bottom: 0.5rem; font-weight: 700;'>風險評估</h3>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.6;'>
                • 波動率分析<br>
                • VaR 風險值<br>
                • Beta 係數<br>
                • Sharpe Ratio
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚠️ 進入風險評估", key="nav_risk", use_container_width=True):
            st.session_state.current_page = "⚠️ 風險評估"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <h3 style='color: #22c55e; margin-bottom: 0.5rem; font-weight: 700;'>投資策略</h3>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.6;'>
                • 技術指標分析<br>
                • 操作建議<br>
                • 策略回測<br>
                • 績效評估
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💡 進入投資策略", key="nav_strategy", use_container_width=True):
            st.session_state.current_page = "💡 投資策略"
            st.rerun()

    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 style='color: #ef4444; margin-bottom: 0.5rem; font-weight: 700;'>權證分析</h3>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.6;'>
                • Black-Scholes<br>
                • Greeks 計算<br>
                • 權證篩選<br>
                • 槓桿分析
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 進入權證分析", key="nav_warrant", use_container_width=True):
            st.session_state.current_page = "🎯 權證分析"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 新增進階功能
    st.markdown("### 🔥 進階分析功能")
    st.markdown("<p style='color: #64748b; margin-bottom: 1rem;'>專業級分析工具，深度挖掘市場機會</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3 style='color: #667eea; margin-bottom: 0.5rem; font-weight: 700;'>技術分析</h3>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.6;'>
                • MA/EMA/MACD<br>
                • RSI/KDJ<br>
                • 布林通道<br>
                • 交易訊號
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📈 進入技術分析", key="nav_tech", use_container_width=True):
            st.session_state.current_page = "📈 技術分析"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 style='color: #3b82f6; margin-bottom: 0.5rem; font-weight: 700;'>多股比較</h3>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.6;'>
                • 橫向比較<br>
                • 報酬率分析<br>
                • 波動率對比<br>
                • 相對強弱
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📊 進入多股比較", key="nav_compare", use_container_width=True):
            st.session_state.current_page = "📊 多股比較"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💼</div>
            <h3 style='color: #10b981; margin-bottom: 0.5rem; font-weight: 700;'>投資組合</h3>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.6;'>
                • 持倉管理<br>
                • 績效追蹤<br>
                • 風險評估<br>
                • 優化建議
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💼 進入投資組合", key="nav_portfolio", use_container_width=True):
            st.session_state.current_page = "💼 投資組合"
            st.rerun()

    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎭</div>
            <h3 style='color: #8b5cf6; margin-bottom: 0.5rem; font-weight: 700;'>市場情緒</h3>
            <p style='color: #1e293b; font-size: 0.95rem; line-height: 1.6;'>
                • 恐懼貪婪指數<br>
                • 市場廣度<br>
                • 產業輪動<br>
                • 市場展望
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎭 進入市場情緒", key="nav_sentiment", use_container_width=True):
            st.session_state.current_page = "🎭 市場情緒"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 技術指標介紹
    st.markdown("### 📈 支援的技術指標")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-box">
            <h4 style='color: #17a2b8; margin-top: 0;'>趨勢型指標</h4>
            <ul style='margin-bottom: 0;'>
                <li><strong>MA (移動平均線)</strong> - 判斷趨勢方向</li>
                <li><strong>MACD</strong> - 動能與趨勢變化</li>
                <li><strong>布林通道</strong> - 價格波動範圍</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box">
            <h4 style='color: #17a2b8; margin-top: 0;'>震盪型指標</h4>
            <ul style='margin-bottom: 0;'>
                <li><strong>RSI</strong> - 超買超賣判斷</li>
                <li><strong>KDJ</strong> - 隨機指標</li>
                <li><strong>Stochastic</strong> - 相對位置</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 熱門股票看板
    st.markdown("### 🔥 市場熱門股票")

    with st.spinner("⏳ 載入股票資料..."):
        try:
            top_stocks = st.session_state.data_fetcher.get_top_stocks()

            if top_stocks:
                cols = st.columns(5)
                for idx, stock in enumerate(top_stocks[:5]):
                    with cols[idx]:
                        price = stock['當前價格']
                        open_price = stock['開盤價']
                        change = price - open_price
                        change_pct = (change / open_price * 100) if open_price > 0 else 0

                        color = '#22c55e' if change >= 0 else '#ef4444'
                        arrow = '▲' if change >= 0 else '▼'

                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-label">{stock['股票名稱']}</div>
                            <div class="stat-value" style="color: {color};">
                                ${price:.2f}
                            </div>
                            <div style="color: {color}; font-size: 0.85rem; font-weight: 600;">
                                {arrow} {abs(change):.2f} ({abs(change_pct):.2f}%)
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # 更多股票資訊（5-10）
                if len(top_stocks) > 5:
                    with st.expander("📊 查看更多股票"):
                        cols2 = st.columns(5)
                        for idx, stock in enumerate(top_stocks[5:10]):
                            with cols2[idx % 5]:
                                price = stock['當前價格']
                                st.metric(
                                    label=stock['股票名稱'],
                                    value=f"${price:.2f}",
                                    delta=f"{stock['開盤價']:.2f}"
                                )
            else:
                st.info("📊 目前無法取得熱門股票資料，請稍後再試")

        except Exception as e:
            st.warning("⚠️ 載入股票資料時發生問題，系統將使用參考資料")

    st.markdown("<br>", unsafe_allow_html=True)

    # 快速開始指南
    st.markdown("### 🎯 快速開始")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="success-box">
            <h4 style='margin-top: 0;'>1️⃣ 選擇功能</h4>
            <p style='margin-bottom: 0;'>
                從左側選單選擇您需要的分析功能
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="success-box">
            <h4 style='margin-top: 0;'>2️⃣ 輸入代碼</h4>
            <p style='margin-bottom: 0;'>
                輸入台股代碼（例如：2330）
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="success-box">
            <h4 style='margin-top: 0;'>3️⃣ 開始分析</h4>
            <p style='margin-bottom: 0;'>
                點擊分析按鈕，查看詳細報告
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 系統特色
    st.markdown("### ✨ 系統特色")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style='color: #667eea;'>🎨 現代化介面</h4>
            <p style='color: #64748b;'>
                直觀易用的操作介面，視覺化圖表展示，
                讓複雜的技術分析變得簡單明瞭
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <h4 style='color: #667eea;'>📊 專業分析</h4>
            <p style='color: #64748b;'>
                整合多項專業技術指標，提供全方位的
                市場分析和投資建議
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style='color: #667eea;'>🔬 回測驗證</h4>
            <p style='color: #64748b;'>
                支援策略回測功能，驗證投資策略的
                實際效果和風險特性
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <h4 style='color: #667eea;'>⚡ 即時更新</h4>
            <p style='color: #64748b;'>
                自動獲取最新市場資料，確保分析結果
                基於最新的市場狀況
            </p>
        </div>
        """, unsafe_allow_html=True)


def show_stock_analysis_page():
    """股票分析頁面 - 現代化設計"""

    # 頁面標題
    st.markdown("""
    <div class='page-header'>
        <h1>📊 股票分析</h1>
        <p>深入了解股票走勢、價格統計與基本面資訊</p>
    </div>
    """, unsafe_allow_html=True)

    # 側邊欄參數設置
    with st.sidebar:
        st.markdown("### 📊 分析參數")
        stock_id = st.text_input("🔍 股票代碼", "2330", help="輸入台股代碼，例如：2330")
        days = st.slider("📅 查詢天數", min_value=30, max_value=365, value=90, step=10)
        st.markdown("---")
        analyze_button = st.button("🚀 開始分析", type="primary", use_container_width=True)

    if analyze_button:
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("⏳ 正在獲取股票資料...")
        progress_bar.progress(30)

        # 獲取股票資料
        df = st.session_state.data_fetcher.get_stock_price(stock_id, days)

        if df.empty:
            st.error(f"❌ 無法獲取股票 {stock_id} 的資料，請確認代碼是否正確")
            return

        progress_bar.progress(60)
        status_text.text("📊 正在分析數據...")

        # 獲取股票資訊
        stock_info = st.session_state.data_fetcher.get_stock_info(stock_id)

        progress_bar.progress(100)
        status_text.text("✅ 分析完成！")

        import time
        time.sleep(0.3)
        progress_bar.empty()
        status_text.empty()

        # 基本資訊卡片
        st.markdown("### 📋 基本資訊")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">公司名稱</div>
                <div class="stat-value" style="font-size: 1.5rem; color: #667eea;">
                    {stock_info.get('公司名稱', 'N/A')}
                </div>
                <div style="color: #94a3b8; font-size: 0.85rem;">
                    代碼: {stock_id}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # 支援新舊兩種鍵名
            industry = stock_info.get('產業類別') or stock_info.get('產業', 'N/A')
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">產業類別</div>
                <div class="stat-value" style="font-size: 1.3rem; color: #22c55e;">
                    {industry}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            market_cap = stock_info.get('市值', 'N/A')
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">市值</div>
                <div class="stat-value" style="font-size: 1.3rem; color: #f59e0b;">
                    {market_cap}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">本益比</div>
                <div class="stat-value" style="font-size: 1.3rem; color: #8b5cf6;">
                    {stock_info.get('本益比', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 新增第二行詳細資訊
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">股價淨值比</div>
                <div class="stat-value" style="font-size: 1.3rem; color: #06b6d4;">
                    {stock_info.get('股價淨值比', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col6:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">殖利率</div>
                <div class="stat-value" style="font-size: 1.3rem; color: #10b981;">
                    {stock_info.get('殖利率', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col7:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">52週最高</div>
                <div class="stat-value" style="font-size: 1.3rem; color: #ef4444;">
                    {stock_info.get('52週最高', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col8:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">52週最低</div>
                <div class="stat-value" style="font-size: 1.3rem; color: #3b82f6;">
                    {stock_info.get('52週最低', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 顯示資料來源
        data_source = stock_info.get('資料來源', 'Yahoo Finance')
        st.markdown(f"""
        <div style="text-align: right; color: #64748b; font-size: 0.8rem; margin-top: 0.5rem;">
            📡 資料來源: {data_source} | 更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # K線圖
        st.markdown("### 📈 K線圖表")
        plot_stock_price(df, f"{stock_id} - {stock_info.get('公司名稱', '')} 股價走勢")

        st.markdown("<br>", unsafe_allow_html=True)

        # 價格統計儀表板
        st.markdown("### 📊 價格統計分析")

        col1, col2, col3, col4, col5 = st.columns(5)

        current_price = df['收盤價'].iloc[-1]
        highest = df['最高價'].max()
        lowest = df['最低價'].min()
        change = ((df['收盤價'].iloc[-1] - df['收盤價'].iloc[0]) / df['收盤價'].iloc[0]) * 100
        avg_volume = df['成交量'].mean()

        change_color = '#22c55e' if change >= 0 else '#ef4444'
        change_arrow = '▲' if change >= 0 else '▼'

        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea15 0%, #667eea30 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea;'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>最新收盤價</p>
                <h2 style='color: #667eea; margin: 0.5rem 0; font-size: 2rem;'>
                    ${current_price:.2f}
                </h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #22c55e15 0%, #22c55e30 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #22c55e;'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>區間最高</p>
                <h2 style='color: #22c55e; margin: 0.5rem 0; font-size: 2rem;'>
                    ${highest:.2f}
                </h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ef444415 0%, #ef444430 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #ef4444;'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>區間最低</p>
                <h2 style='color: #ef4444; margin: 0.5rem 0; font-size: 2rem;'>
                    ${lowest:.2f}
                </h2>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {change_color}15 0%, {change_color}30 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid {change_color};'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>區間漲跌</p>
                <h2 style='color: {change_color}; margin: 0.5rem 0; font-size: 2rem;'>
                    {change_arrow} {abs(change):.2f}%
                </h2>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f59e0b15 0%, #f59e0b30 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #f59e0b;'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>平均成交量</p>
                <h3 style='color: #f59e0b; margin: 0.5rem 0; font-size: 1.3rem;'>
                    {avg_volume:,.0f}
                </h3>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 歷史資料表
        with st.expander("📋 查看歷史交易資料"):
            st.dataframe(df.tail(20).style.background_gradient(cmap='RdYlGn', subset=['收盤價']),
                        use_container_width=True)

    else:
        # 未開始分析時顯示引導
        st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem;'>
            <h2 style='color: #94a3b8;'>👈 請在左側輸入股票代碼</h2>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin-top: 1rem;'>
                輸入台股代碼（如：2330）後，點擊「開始分析」
            </p>
            <div style='margin-top: 3rem;'>
                <div style='background: #f8fafc; padding: 2rem; border-radius: 10px; display: inline-block;'>
                    <h3 style='color: #667eea; margin: 0;'>💡 提示</h3>
                    <p style='color: #64748b; margin-top: 1rem;'>
                        本功能提供K線圖表、價格統計<br>
                        以及基本面資訊查詢
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_risk_assessment_page():
    """風險評估頁面 - 現代化設計"""

    # 頁面標題
    st.markdown("""
    <div class='page-header'>
        <h1>⚠️ 風險評估</h1>
        <p>全方位風險分析 | VaR計算 | Beta係數 | 投資風險量化</p>
    </div>
    """, unsafe_allow_html=True)

    # 側邊欄參數設置
    with st.sidebar:
        st.markdown("### ⚙️ 評估參數")
        stock_id = st.text_input("🔍 股票代碼", "2330", help="輸入台股代碼")
        days = st.slider("📅 分析天數", min_value=60, max_value=365, value=180, step=10)
        st.markdown("---")
        assess_button = st.button("🚀 開始評估", type="primary", use_container_width=True)

    if assess_button:
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("⏳ 正在獲取股票資料...")
        progress_bar.progress(25)

        # 獲取股票資料
        df = st.session_state.data_fetcher.get_stock_price(stock_id, days)

        if df.empty:
            st.error(f"❌ 無法獲取股票 {stock_id} 的資料")
            return

        progress_bar.progress(50)
        status_text.text("🔍 正在分析風險指標...")

        # 風險分析
        risk_result = st.session_state.risk_predictor.predict_risk(df)

        if '錯誤' in risk_result:
            st.error(f"❌ {risk_result['錯誤']}")
            return

        progress_bar.progress(100)
        status_text.text("✅ 評估完成！")

        import time
        time.sleep(0.3)
        progress_bar.empty()
        status_text.empty()

        # 風險評估結果
        risk_assessment = risk_result['風險評估']
        risk_level = risk_assessment['風險等級']
        risk_color = risk_assessment['風險顏色']
        risk_score = risk_assessment['風險分數']

        st.markdown("### 🎯 風險評估結果")

        col1, col2, col3, col4 = st.columns(4)

        # 風險等級
        with col1:
            risk_emoji = '🔴' if '高風險' in risk_level else ('🟡' if '中風險' in risk_level else '🟢')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {risk_color}15 0%, {risk_color}30 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid {risk_color};'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>風險等級</p>
                <h2 style='color: {risk_color}; margin: 0.5rem 0; font-size: 2rem;'>
                    {risk_emoji} {risk_level}
                </h2>
                <p style='color: #94a3b8; margin: 0; font-size: 0.85rem;'>
                    評分: {risk_score}/100
                </p>
            </div>
            """, unsafe_allow_html=True)

        # 波動率
        with col2:
            volatility = risk_result['波動率']
            vol_level = risk_assessment['波動率等級']
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f59e0b15 0%, #f59e0b30 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #f59e0b;'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>波動率</p>
                <h2 style='color: #f59e0b; margin: 0.5rem 0; font-size: 2rem;'>
                    {volatility}
                </h2>
                <p style='color: #94a3b8; margin: 0; font-size: 0.85rem;'>
                    等級: {vol_level}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Sharpe Ratio
        with col3:
            sharpe = risk_result['Sharpe Ratio']
            sharpe_level = risk_assessment['Sharpe比率等級']
            sharpe_color = '#22c55e' if '優秀' in sharpe_level else ('#f59e0b' if '良好' in sharpe_level else '#ef4444')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {sharpe_color}15 0%, {sharpe_color}30 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid {sharpe_color};'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>Sharpe Ratio</p>
                <h2 style='color: {sharpe_color}; margin: 0.5rem 0; font-size: 2rem;'>
                    {sharpe}
                </h2>
                <p style='color: #94a3b8; margin: 0; font-size: 0.85rem;'>
                    等級: {sharpe_level}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Beta 係數
        with col4:
            beta = risk_result['Beta']
            beta_level = risk_assessment['Beta等級']
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #8b5cf615 0%, #8b5cf630 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #8b5cf6;'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>Beta 係數</p>
                <h2 style='color: #8b5cf6; margin: 0.5rem 0; font-size: 2rem;'>
                    {beta}
                </h2>
                <p style='color: #94a3b8; margin: 0; font-size: 0.85rem;'>
                    等級: {beta_level}
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 詳細風險指標
        st.markdown("### 📊 詳細風險指標分析")

        col1, col2 = st.columns(2)

        with col1:
            # VaR 風險值
            var_info = risk_result['VaR資訊']
            st.markdown("""
            <div class="metric-card">
                <h4 style='color: #667eea; margin-top: 0;'>📉 VaR 風險值 (Value at Risk)</h4>
            </div>
            """, unsafe_allow_html=True)

            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("VaR (95% 信心水準)", f"{var_info['VaR']:.2f}%")
            with metric_col2:
                st.metric("CVaR (條件風險值)", f"{var_info['CVaR']:.2f}%")

            st.info(f"💡 {var_info['解釋']}")

            st.markdown("<br>", unsafe_allow_html=True)

            # Beta 係數詳細說明
            st.markdown("""
            <div class="metric-card">
                <h4 style='color: #667eea; margin-top: 0;'>📈 Beta 係數分析</h4>
            </div>
            """, unsafe_allow_html=True)

            st.write(f"**Beta 值:** {risk_result['Beta']}")
            st.write(f"**市場相對性:** {risk_assessment['Beta等級']}")

            if float(risk_result['Beta']) > 1:
                st.warning("⚠️ Beta > 1：股價波動大於市場，風險較高")
            elif float(risk_result['Beta']) < 1:
                st.success("✅ Beta < 1：股價波動小於市場，風險較低")
            else:
                st.info("ℹ️ Beta = 1：股價波動與市場一致")

        with col2:
            # 最大回撤
            max_dd = risk_result['最大回撤']
            st.markdown("""
            <div class="metric-card">
                <h4 style='color: #667eea; margin-top: 0;'>⬇️ 最大回撤分析</h4>
            </div>
            """, unsafe_allow_html=True)

            dd_value = max_dd['最大回撤']
            dd_color = '#22c55e' if dd_value > -10 else ('#f59e0b' if dd_value > -20 else '#ef4444')

            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: {dd_color}20;
                        border-radius: 10px; margin: 1rem 0;'>
                <h2 style='color: {dd_color}; margin: 0; font-size: 2.5rem;'>
                    {dd_value:.2f}%
                </h2>
                <p style='color: #64748b; margin: 0.5rem 0 0 0;'>
                    發生日期: {max_dd['發生日期']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.info(f"💡 {max_dd['解釋']}")

            st.markdown("<br>", unsafe_allow_html=True)

            # 風險分散建議
            st.markdown("""
            <div class="info-box">
                <h4 style='margin-top: 0;'>💼 風險管理建議</h4>
                <ul style='margin-bottom: 0;'>
                    <li>定期檢視投資組合</li>
                    <li>適度分散投資風險</li>
                    <li>設定停損停利點</li>
                    <li>關注市場變化</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 投資建議
        st.markdown("### 💡 綜合投資建議")

        suggestion = risk_assessment['建議']
        if '謹慎' in suggestion or '高風險' in suggestion:
            st.error(f"🔴 **高風險警示：** {suggestion}")
        elif '適中' in suggestion or '中風險' in suggestion:
            st.warning(f"🟡 **中等風險：** {suggestion}")
        else:
            st.success(f"🟢 **相對安全：** {suggestion}")

    else:
        # 未開始評估時顯示引導
        st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem;'>
            <h2 style='color: #94a3b8;'>👈 請在左側設定評估參數</h2>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin-top: 1rem;'>
                輸入股票代碼後，點擊「開始評估」
            </p>
            <div style='margin-top: 3rem; display: flex; justify-content: center; gap: 2rem;'>
                <div style='background: #f8fafc; padding: 1.5rem; border-radius: 10px; width: 200px;'>
                    <h3 style='color: #f59e0b; margin: 0;'>⚠️ VaR 分析</h3>
                    <p style='color: #64748b; font-size: 0.9rem; margin-top: 0.5rem;'>
                        量化投資風險
                    </p>
                </div>
                <div style='background: #f8fafc; padding: 1.5rem; border-radius: 10px; width: 200px;'>
                    <h3 style='color: #f59e0b; margin: 0;'>📊 Beta 係數</h3>
                    <p style='color: #64748b; font-size: 0.9rem; margin-top: 0.5rem;'>
                        市場相對風險
                    </p>
                </div>
                <div style='background: #f8fafc; padding: 1.5rem; border-radius: 10px; width: 200px;'>
                    <h3 style='color: #f59e0b; margin: 0;'>📉 最大回撤</h3>
                    <p style='color: #64748b; font-size: 0.9rem; margin-top: 0.5rem;'>
                        歷史最大損失
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_strategy_page():
    """投資策略頁面 - 全新UI設計"""

    # 頁面標題
    st.markdown("""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-weight: 700;'>💡 投資策略分析</h1>
        <p style='color: #e0e7ff; margin: 0.5rem 0 0 0; font-size: 1.1rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);'>
            運用多項技術指標，提供全方位投資建議
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 側邊欄 - 參數設置
    with st.sidebar:
        st.markdown("### ⚙️ 分析參數設置")
        stock_id = st.text_input("🔍 股票代碼", "2330", help="輸入台股代碼，例如：2330 (台積電)")
        days = st.slider("📅 分析天數", min_value=60, max_value=365, value=120, step=10)

        st.markdown("---")
        st.markdown("### 📊 技術指標選擇")
        show_ma = st.checkbox("移動平均線 (MA)", value=True)
        show_rsi = st.checkbox("相對強弱指標 (RSI)", value=True)
        show_macd = st.checkbox("MACD", value=True)
        show_kdj = st.checkbox("KDJ", value=True)

        st.markdown("---")
        analyze_button = st.button("🚀 開始分析", type="primary", use_container_width=True)

    # 主要內容區域
    if analyze_button:
        # 進度指示器
        progress_bar = st.progress(0)
        status_text = st.empty()

        # 步驟1: 獲取資料
        status_text.text("⏳ 正在獲取股票資料...")
        progress_bar.progress(20)
        df = st.session_state.data_fetcher.get_stock_price(stock_id, days)

        if df.empty:
            st.error(f"❌ 無法獲取股票 {stock_id} 的資料")
            return

        # 步驟2: 分析策略
        status_text.text("🔍 正在分析技術指標...")
        progress_bar.progress(50)
        result = st.session_state.strategy_analyzer.comprehensive_analysis(df)

        # 步驟3: 生成報告
        status_text.text("📊 正在生成分析報告...")
        progress_bar.progress(80)

        # 完成
        progress_bar.progress(100)
        status_text.text("✅ 分析完成！")

        # 清除進度指示器
        import time
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()

        # ====== 區塊1: 核心指標儀表板 ======
        st.markdown("### 🎯 核心分析儀表板")

        score = float(result['綜合評分'])
        action = result['操作方向']
        suggestion = result['操作建議']

        # 使用4列布局展示關鍵指標
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # 綜合評分 - 帶有顏色漸變
            score_color = '#22c55e' if score > 20 else ('#ef4444' if score < -20 else '#f59e0b')
            score_emoji = '📈' if score > 20 else ('📉' if score < -20 else '➡️')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {score_color}15 0%, {score_color}30 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid {score_color};'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>綜合評分</p>
                <h2 style='color: {score_color}; margin: 0.5rem 0; font-size: 2.5rem;'>
                    {score_emoji} {score:.1f}
                </h2>
                <p style='color: #94a3b8; margin: 0; font-size: 0.85rem;'>
                    範圍: -100 ~ +100
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # 操作方向 - 醒目展示
            action_color = '#22c55e' if action == 'BUY' else ('#ef4444' if action == 'SELL' else '#f59e0b')
            action_text = '買進' if action == 'BUY' else ('賣出' if action == 'SELL' else '觀望')
            action_emoji = '🟢' if action == 'BUY' else ('🔴' if action == 'SELL' else '🟡')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {action_color}15 0%, {action_color}30 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid {action_color};'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>操作方向</p>
                <h2 style='color: {action_color}; margin: 0.5rem 0; font-size: 2rem;'>
                    {action_emoji} {action_text}
                </h2>
                <p style='color: #94a3b8; margin: 0; font-size: 0.85rem;'>
                    {action}
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            # 操作建議
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #3b82f615 0%, #3b82f630 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #3b82f6;'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>操作建議</p>
                <h3 style='color: #3b82f6; margin: 0.5rem 0; font-size: 1.3rem;'>
                    💼 {suggestion}
                </h3>
                <p style='color: #94a3b8; margin: 0; font-size: 0.85rem;'>
                    基於多指標分析
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            # 分析天數和數據量
            data_count = len(df)
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #8b5cf615 0%, #8b5cf630 100%);
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #8b5cf6;'>
                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>資料範圍</p>
                <h3 style='color: #8b5cf6; margin: 0.5rem 0; font-size: 1.5rem;'>
                    📅 {days} 天
                </h3>
                <p style='color: #94a3b8; margin: 0; font-size: 0.85rem;'>
                    共 {data_count} 筆資料
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ====== 區塊2: 技術指標圖表 ======
        st.markdown("### 📈 技術指標圖表")
        plot_technical_indicators(result['分析資料'])

        st.markdown("<br>", unsafe_allow_html=True)

        # ====== 區塊3: 技術指標詳細分析 ======
        st.markdown("### 🔬 技術指標深度解析")

        # 創建指標卡片
        indicator_tabs = []
        if show_ma: indicator_tabs.append("📊 移動平均線")
        if show_rsi: indicator_tabs.append("📉 RSI")
        if show_macd: indicator_tabs.append("📈 MACD")
        if show_kdj: indicator_tabs.append("🎯 KDJ")

        if indicator_tabs:
            tabs = st.tabs(indicator_tabs)
            tab_index = 0

            # MA 分析
            if show_ma:
                with tabs[tab_index]:
                    ma_signals = result['移動平均線分析']
                    signal = ma_signals['信號']
                    strength = ma_signals['強度']

                    # 信號顏色
                    signal_color = '#22c55e' if '買進' in signal else ('#ef4444' if '賣出' in signal else '#f59e0b')

                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"""
                        <div style='background: {signal_color}20; padding: 1.5rem;
                                    border-radius: 10px; text-align: center;'>
                            <h3 style='color: {signal_color}; margin: 0;'>{signal}</h3>
                            <p style='color: #64748b; margin-top: 0.5rem;'>信號強度: {strength}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        if '原因' in ma_signals:
                            st.markdown("**📝 分析原因:**")
                            for reason in ma_signals['原因']:
                                st.markdown(f"- {reason}")

                    # 添加說明
                    with st.expander("ℹ️ 移動平均線原理"):
                        st.markdown("""
                        **移動平均線 (Moving Average, MA)** 是技術分析中最常用的指標之一：
                        - **短期均線向上穿越長期均線** → 黃金交叉，買進信號
                        - **短期均線向下穿越長期均線** → 死亡交叉，賣出信號
                        - **價格在均線之上** → 多頭趨勢
                        - **價格在均線之下** → 空頭趨勢
                        """)
                tab_index += 1

            # RSI 分析
            if show_rsi:
                with tabs[tab_index]:
                    rsi_signals = result['RSI分析']
                    signal = rsi_signals['信號']

                    signal_color = '#22c55e' if '買進' in signal else ('#ef4444' if '賣出' in signal else '#f59e0b')

                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"""
                        <div style='background: {signal_color}20; padding: 1.5rem;
                                    border-radius: 10px; text-align: center;'>
                            <h3 style='color: {signal_color}; margin: 0;'>{signal}</h3>
                        </div>
                        """, unsafe_allow_html=True)

                        if 'RSI值' in rsi_signals:
                            try:
                                rsi_value = float(rsi_signals['RSI值'])
                            except (ValueError, TypeError):
                                rsi_value = 50.0  # 默认值
                            st.metric("RSI 數值", f"{rsi_value:.2f}")

                            # RSI 視覺化進度條
                            if rsi_value >= 70:
                                bar_color = '#ef4444'
                                zone = '超買區'
                            elif rsi_value <= 30:
                                bar_color = '#22c55e'
                                zone = '超賣區'
                            else:
                                bar_color = '#3b82f6'
                                zone = '正常區'

                            st.markdown(f"""
                            <div style='background: #f1f5f9; border-radius: 10px; padding: 0.5rem;'>
                                <div style='background: {bar_color}; width: {rsi_value}%;
                                            height: 20px; border-radius: 5px;
                                            transition: width 0.3s;'></div>
                                <p style='text-align: center; margin: 0.5rem 0 0 0; color: #64748b;'>
                                    {zone}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                    with col2:
                        if '說明' in rsi_signals:
                            st.info(rsi_signals['說明'])

                    with st.expander("ℹ️ RSI 原理"):
                        st.markdown("""
                        **相對強弱指標 (Relative Strength Index, RSI)** 用於判斷超買超賣：
                        - **RSI > 70** → 超買區，可能回調
                        - **RSI < 30** → 超賣區，可能反彈
                        - **RSI 50左右** → 多空平衡
                        """)
                tab_index += 1

            # MACD 分析
            if show_macd:
                with tabs[tab_index]:
                    macd_signals = result['MACD分析']
                    signal = macd_signals['信號']
                    strength = macd_signals['強度']

                    signal_color = '#22c55e' if '買進' in signal else ('#ef4444' if '賣出' in signal else '#f59e0b')

                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"""
                        <div style='background: {signal_color}20; padding: 1.5rem;
                                    border-radius: 10px; text-align: center;'>
                            <h3 style='color: {signal_color}; margin: 0;'>{signal}</h3>
                            <p style='color: #64748b; margin-top: 0.5rem;'>信號強度: {strength}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        if '原因' in macd_signals:
                            st.markdown("**📝 分析原因:**")
                            for reason in macd_signals['原因']:
                                st.markdown(f"- {reason}")

                    with st.expander("ℹ️ MACD 原理"):
                        st.markdown("""
                        **MACD (Moving Average Convergence Divergence)** 是趨勢追蹤指標：
                        - **MACD 線向上穿越信號線** → 黃金交叉，買進信號
                        - **MACD 線向下穿越信號線** → 死亡交叉，賣出信號
                        - **柱狀圖由負轉正** → 上升動能增強
                        - **柱狀圖由正轉負** → 下降動能增強
                        """)
                tab_index += 1

            # KDJ 分析
            if show_kdj:
                with tabs[tab_index]:
                    kdj_signals = result['KDJ分析']
                    signal = kdj_signals['信號']

                    signal_color = '#22c55e' if '買進' in signal else ('#ef4444' if '賣出' in signal else '#f59e0b')

                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"""
                        <div style='background: {signal_color}20; padding: 1.5rem;
                                    border-radius: 10px; text-align: center;'>
                            <h3 style='color: {signal_color}; margin: 0;'>{signal}</h3>
                        </div>
                        """, unsafe_allow_html=True)

                        if 'K值' in kdj_signals:
                            col_k, col_d, col_j = st.columns(3)
                            with col_k:
                                k_val = kdj_signals['K值']
                                st.metric("K值", f"{float(k_val):.2f}" if isinstance(k_val, (int, float)) else k_val)
                            with col_d:
                                d_val = kdj_signals['D值']
                                st.metric("D值", f"{float(d_val):.2f}" if isinstance(d_val, (int, float)) else d_val)
                            with col_j:
                                j_val = kdj_signals['J值']
                                st.metric("J值", f"{float(j_val):.2f}" if isinstance(j_val, (int, float)) else j_val)

                    with col2:
                        if '原因' in kdj_signals:
                            st.markdown("**📝 分析原因:**")
                            for reason in kdj_signals['原因']:
                                st.markdown(f"- {reason}")

                    with st.expander("ℹ️ KDJ 原理"):
                        st.markdown("""
                        **KDJ 指標** 是隨機指標的延伸：
                        - **K值 > 80, D值 > 80** → 超買區
                        - **K值 < 20, D值 < 20** → 超賣區
                        - **K線向上穿越D線** → 買進信號
                        - **K線向下穿越D線** → 賣出信號
                        - **J值** → 領先指標，更敏感
                        """)

        st.markdown("<br>", unsafe_allow_html=True)

        # ====== 區塊4: 策略回測 ======
        st.markdown("### 🔬 策略回測模擬")
        st.markdown("""
        <div style='background: #f8fafc; padding: 1rem; border-radius: 10px; border-left: 4px solid #3b82f6;'>
            <p style='color: #64748b; margin: 0;'>
                💡 <strong>回測說明：</strong>根據當前分析策略，模擬過去的交易表現，
                評估策略的實際效果。這有助於了解策略的獲利能力和風險特性。
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col2:
            backtest_button = st.button("🚀 執行回測", type="secondary", use_container_width=True)

        if backtest_button:
            with st.spinner("⏳ 正在執行回測分析..."):
                backtest_result = st.session_state.strategy_analyzer.backtest_strategy(df)

            if '錯誤' not in backtest_result:
                # 回測結果儀表板
                col1, col2, col3, col4 = st.columns(4)

                profit = backtest_result['獲利']
                profit_rate = backtest_result['報酬率']
                profit_color = '#22c55e' if profit > 0 else '#ef4444'

                with col1:
                    st.metric("💰 初始資金", f"${backtest_result['初始資金']:,.0f}")

                with col2:
                    st.metric("💎 最終資金", f"${backtest_result['最終資金']:,.0f}")

                with col3:
                    st.markdown(f"""
                    <div style='background: {profit_color}20; padding: 1rem;
                                border-radius: 10px; text-align: center;'>
                        <p style='color: #64748b; margin: 0; font-size: 0.85rem;'>獲利金額</p>
                        <h3 style='color: {profit_color}; margin: 0.5rem 0;'>
                            ${profit:,.0f}
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)

                with col4:
                    st.markdown(f"""
                    <div style='background: {profit_color}20; padding: 1rem;
                                border-radius: 10px; text-align: center;'>
                        <p style='color: #64748b; margin: 0; font-size: 0.85rem;'>報酬率</p>
                        <h3 style='color: {profit_color}; margin: 0.5rem 0;'>
                            {profit_rate}
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)

                # 交易統計
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background: #f8fafc; padding: 1rem; border-radius: 10px;'>
                    <p style='color: #64748b; margin: 0;'>
                        📊 <strong>交易次數:</strong> {backtest_result['交易次數']} 次 |
                        📅 <strong>分析期間:</strong> {days} 天 |
                        🎯 <strong>平均持有:</strong> {days // max(backtest_result['交易次數'], 1)} 天
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # 交易明細
                if backtest_result['交易明細']:
                    with st.expander("📋 查看詳細交易記錄"):
                        trades_df = pd.DataFrame(backtest_result['交易明細'])
                        st.dataframe(trades_df, use_container_width=True)
            else:
                st.error(f"❌ 回測失敗: {backtest_result['錯誤']}")

    else:
        # 未點擊分析時，顯示引導訊息
        st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem;'>
            <h2 style='color: #94a3b8; font-size: 1.8rem;'>👈 請在左側設定分析參數</h2>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin-top: 1rem;'>
                輸入股票代碼後，點擊「開始分析」按鈕
            </p>
            <div style='margin-top: 3rem; display: flex; justify-content: center; gap: 2rem;'>
                <div style='background: #f8fafc; padding: 1.5rem; border-radius: 10px; width: 200px;'>
                    <h3 style='color: #667eea; margin: 0;'>📊 多項指標</h3>
                    <p style='color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;'>
                        MA, RSI, MACD, KDJ
                    </p>
                </div>
                <div style='background: #f8fafc; padding: 1.5rem; border-radius: 10px; width: 200px;'>
                    <h3 style='color: #667eea; margin: 0;'>🎯 智能建議</h3>
                    <p style='color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;'>
                        買進、賣出或觀望
                    </p>
                </div>
                <div style='background: #f8fafc; padding: 1.5rem; border-radius: 10px; width: 200px;'>
                    <h3 style='color: #667eea; margin: 0;'>🔬 策略回測</h3>
                    <p style='color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;'>
                        驗證策略有效性
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_warrant_page():
    """權證分析頁面 - 現代化設計"""

    # 頁面標題
    st.markdown("""
    <div class='page-header'>
        <h1>🎯 權證分析</h1>
        <p>Black-Scholes定價模型 | Greeks計算 | 權證篩選推薦</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔍 權證查詢", "📊 權證篩選"])

    with tab1:
        st.markdown("""
        <div class="info-box">
            <h4 style='margin-top: 0;'>🔍 權證查詢說明</h4>
            <p style='margin-bottom: 0;'>
                輸入股票代碼，系統將列出所有相關的權證標的。選取權證後，將使用 Black-Scholes 模型進行完整分析。
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 步驟 1: 輸入股票代碼查詢權證
        st.markdown("### 📝 步驟 1: 輸入標的股票代碼")

        col1, col2 = st.columns([2, 1])

        with col1:
            search_stock_id = st.text_input(
                "🔍 請輸入股票代碼",
                value="2330",
                placeholder="例如: 2330, 2317, 2454",
                key="warrant_search_stock"
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_button = st.button("🔍 查詢權證", type="primary", use_container_width=True)

        # 查詢權證列表
        if search_button or 'warrant_search_result' in st.session_state:
            if search_button:
                with st.spinner("⏳ 正在查詢權證列表..."):
                    warrants_df = st.session_state.warrant_fetcher.get_warrant_list(search_stock_id)
                    st.session_state.warrant_search_result = warrants_df
                    st.session_state.warrant_searched_stock_id = search_stock_id

            warrants_df = st.session_state.get('warrant_search_result', pd.DataFrame())

            if not warrants_df.empty:
                st.markdown("<br>", unsafe_allow_html=True)

                # 步驟 2: 顯示權證列表
                st.markdown("### 📋 步驟 2: 選擇權證標的")

                # 顯示簡潔的摘要資訊
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 權證數量", f"{len(warrants_df)} 支")
                with col2:
                    call_count = len(warrants_df[warrants_df['權證類型'] == '認購'])
                    st.metric("📈 認購權證", f"{call_count} 支")
                with col3:
                    put_count = len(warrants_df[warrants_df['權證類型'] == '認售'])
                    st.metric("📉 認售權證", f"{put_count} 支")

                # 使用 expander 來折疊權證列表，減少閃爍
                with st.expander("📊 查看完整權證列表明細", expanded=False):
                    # 顯示權證列表表格
                    display_df = warrants_df[[
                        '權證代碼', '權證名稱', '權證類型', '發行商',
                        '履約價', '行使比例', '到期日', '權證價格'
                    ]].copy()

                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "權證代碼": st.column_config.TextColumn("權證代碼", width="small"),
                            "權證名稱": st.column_config.TextColumn("權證名稱", width="medium"),
                            "權證類型": st.column_config.TextColumn("類型", width="small"),
                            "發行商": st.column_config.TextColumn("發行商", width="small"),
                            "履約價": st.column_config.NumberColumn("履約價", format="%.2f"),
                            "行使比例": st.column_config.NumberColumn("行使比例", format="%.2f"),
                            "到期日": st.column_config.TextColumn("到期日", width="small"),
                            "權證價格": st.column_config.NumberColumn("權證價格", format="%.2f"),
                        }
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # 選擇權證進行分析
                warrant_codes = warrants_df['權證代碼'].tolist()
                warrant_names = [f"{code} - {name}" for code, name in
                                zip(warrants_df['權證代碼'], warrants_df['權證名稱'])]

                selected_warrant_display = st.selectbox(
                    "🎯 選擇要分析的權證",
                    warrant_names,
                    key="selected_warrant_display"
                )

                selected_warrant_code = selected_warrant_display.split(' - ')[0]

                # 步驟 3: 獲取當前股價並分析
                st.markdown("### ⚙️ 步驟 3: 設定分析參數")

                col1, col2 = st.columns(2)

                with col1:
                    # 嘗試獲取最新股價
                    try:
                        stock_df = st.session_state.data_fetcher.get_stock_price(
                            search_stock_id,
                            days=5
                        )
                        if not stock_df.empty:
                            latest_price = float(stock_df['收盤價'].iloc[-1])
                            st.info(f"📊 最新股價: {latest_price:.2f} TWD")
                        else:
                            latest_price = 600.0
                    except:
                        latest_price = 600.0

                    stock_price = st.number_input(
                        "💰 當前股價",
                        min_value=0.0,
                        value=latest_price,
                        step=1.0,
                        key="warrant_stock_price"
                    )

                with col2:
                    volatility = st.slider(
                        "📈 隱含波動率 (%)",
                        min_value=10,
                        max_value=60,
                        value=30,
                        key="warrant_volatility"
                    ) / 100

                st.markdown("<br>", unsafe_allow_html=True)

                if st.button("🚀 開始分析", type="primary", use_container_width=True, key="analyze_warrant"):
                    with st.spinner("⏳ 正在計算權證價值..."):
                        # 獲取選中的權證詳細資訊
                        warrant_detail = st.session_state.warrant_fetcher.get_warrant_detail(selected_warrant_code)

                        if warrant_detail:
                            result = st.session_state.warrant_analyzer.analyze_warrant(
                                warrant_detail, stock_price, volatility
                            )
                            st.session_state.warrant_analysis_result = result
                        else:
                            st.error("❌ 無法獲取權證詳細資訊")

                # 顯示分析結果
                if 'warrant_analysis_result' in st.session_state:
                    result = st.session_state.warrant_analysis_result

                    if '錯誤' in result:
                        st.error(f"❌ {result['錯誤']}")
                    else:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.success("✅ 分析完成！")

                        # 顯示權證基本資訊
                        st.markdown("### 📋 權證基本資訊")
                        info_col1, info_col2, info_col3, info_col4 = st.columns(4)

                        with info_col1:
                            st.metric("權證代碼", result['權證代碼'])
                            st.metric("標的股票", result['標的股票'])

                        with info_col2:
                            st.metric("權證名稱", result['權證名稱'])
                            st.metric("權證類型", result['權證類型'])

                        with info_col3:
                            st.metric("履約價", f"${result['履約價']:.2f}")
                            st.metric("行使比例", f"{result['行使比例']:.2f}")

                        with info_col4:
                            st.metric("當前股價", f"${result['當前股價']:.2f}")
                            st.metric("到期天數", f"{result['到期天數']} 天")

                        st.markdown("<br>", unsafe_allow_html=True)

                        # 核心指標卡片
                        st.markdown("### 💎 核心評估指標")

                        val_col1, val_col2, val_col3, val_col4 = st.columns(4)

                        with val_col1:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #667eea15 0%, #667eea30 100%);
                                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea;'>
                                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>理論價格</p>
                                <h2 style='color: #667eea; margin: 0.5rem 0; font-size: 2rem;'>
                                    {result['理論價格']}
                                </h2>
                            </div>
                            """, unsafe_allow_html=True)

                        with val_col2:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #22c55e15 0%, #22c55e30 100%);
                                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #22c55e;'>
                                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>內含價值</p>
                                <h2 style='color: #22c55e; margin: 0.5rem 0; font-size: 2rem;'>
                                    {result['內含價值']}
                                </h2>
                            </div>
                            """, unsafe_allow_html=True)

                        with val_col3:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #f59e0b15 0%, #f59e0b30 100%);
                                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #f59e0b;'>
                                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>時間價值</p>
                                <h2 style='color: #f59e0b; margin: 0.5rem 0; font-size: 2rem;'>
                                    {result['時間價值']}
                                </h2>
                            </div>
                            """, unsafe_allow_html=True)

                        with val_col4:
                            score = result['綜合評分']
                            score_color = '#22c55e' if score >= 70 else ('#f59e0b' if score >= 40 else '#ef4444')
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, {score_color}15 0%, {score_color}30 100%);
                                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid {score_color};'>
                                <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>綜合評分</p>
                                <h2 style='color: {score_color}; margin: 0.5rem 0; font-size: 2rem;'>
                                    {score}/100
                                </h2>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                        # 詳細資訊
                        st.markdown("### 📊 詳細資訊")

                        detail_col1, detail_col2 = st.columns(2)

                        with detail_col1:
                            st.markdown("""
                            <div class="metric-card">
                                <h4 style='color: #667eea; margin-top: 0;'>🎯 權證狀態</h4>
                            </div>
                            """, unsafe_allow_html=True)

                            metric_col1, metric_col2 = st.columns(2)
                            with metric_col1:
                                st.metric("價內外狀態", result['價內外狀態'])
                                st.metric("實質槓桿", result['實質槓桿'])
                            with metric_col2:
                                st.metric("到期天數", f"{result['到期天數']} 天")
                                st.metric("損益兩平點", result['損益兩平點'])

                        with detail_col2:
                            st.markdown("""
                            <div class="metric-card">
                                <h4 style='color: #667eea; margin-top: 0;'>📈 Greeks 風險指標</h4>
                            </div>
                            """, unsafe_allow_html=True)

                            greeks_data = [
                                ("Delta Δ", result['Delta'], "價格敏感度"),
                                ("Gamma Γ", result['Gamma'], "Delta變化率"),
                                ("Theta Θ", result['Theta'], "時間價值衰減"),
                                ("Vega ν", result['Vega'], "波動率敏感度")
                            ]

                            for name, value, desc in greeks_data:
                                greek_col_a, greek_col_b = st.columns([1, 2])
                                with greek_col_a:
                                    st.metric(name, value)
                                with greek_col_b:
                                    st.caption(desc)

                        st.markdown("<br>", unsafe_allow_html=True)

                        # 投資建議
                        st.markdown("### 💡 投資建議")

                        recommendation = result['投資建議']
                        if '✅' in recommendation:
                            st.success(f"🟢 **推薦買進：** {recommendation}")
                        elif '⚠️' in recommendation or '⚖️' in recommendation:
                            st.warning(f"🟡 **謹慎評估：** {recommendation}")
                        else:
                            st.error(f"🔴 **不建議買進：** {recommendation}")
            else:
                st.info("💡 請輸入股票代碼並點擊「查詢權證」按鈕開始查詢")

    with tab2:
        st.markdown("""
        <div class="info-box">
            <h4 style='margin-top: 0;'>🔍 篩選說明</h4>
            <p style='margin-bottom: 0;'>
                根據您設定的條件，系統將篩選出最適合的權證標的，並提供詳細的評估資訊。
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚙️ 篩選條件設定")

        col1, col2 = st.columns(2)

        with col1:
            stock_id_filter = st.text_input("🔍 標的股票代碼", "2330", key="filter_stock")
            stock_price_filter = st.number_input("💰 當前股價", min_value=0.0, value=600.0, step=1.0, key="filter_price")

        with col2:
            min_days = st.number_input("📅 最小到期天數", min_value=1, value=30)
            max_leverage = st.number_input("📊 最大實質槓桿", min_value=1.0, value=10.0, step=0.5)

        min_delta = st.slider("📈 最小Delta值", min_value=0.0, max_value=1.0, value=0.3, step=0.1)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔍 開始篩選", type="primary", use_container_width=True):
            with st.spinner("⏳ 正在篩選權證..."):
                # 獲取權證列表
                warrants_df = st.session_state.warrant_fetcher.get_warrant_list(stock_id_filter)

                if warrants_df.empty:
                    st.warning("⚠️ 目前沒有可用的權證資料（這是示範系統）")
                    st.info("""
                    💡 **提示：** 本系統使用示範資料。在實際應用中，這裡會顯示：
                    - 符合條件的權證列表
                    - 各項權證的評分與排名
                    - 詳細的比較分析
                    """)
                else:
                    st.success("✅ 篩選完成！")

                    # 顯示篩選條件摘要
                    st.markdown("### 📋 篩選條件摘要")
                    st.markdown(f"""
                    <div class="metric-card">
                        <p><strong>標的股票：</strong>{stock_id_filter} |
                        <strong>當前股價：</strong>${stock_price_filter} |
                        <strong>最小到期天數：</strong>{min_days}天 |
                        <strong>最大槓桿：</strong>{max_leverage}倍 |
                        <strong>最小Delta：</strong>{min_delta}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # 篩選條件
                    filters = {
                        '最小到期天數': min_days,
                        '最大實質槓桿': max_leverage,
                        '最小Delta': min_delta
                    }

                    # 推薦權證
                    recommendations = st.session_state.warrant_analyzer.recommend_warrants(
                        warrants_df, stock_price_filter, top_n=10
                    )

                    if recommendations:
                        st.markdown("### 🏆 推薦權證列表")
                        st.markdown("""
                        <div class="success-box">
                            <p style='margin: 0;'>
                                以下是根據您的篩選條件推薦的權證，按綜合評分排序
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                        # 使用更美觀的表格顯示
                        st.dataframe(
                            pd.DataFrame(recommendations).style.background_gradient(
                                subset=['綜合評分'] if '綜合評分' in pd.DataFrame(recommendations).columns else [],
                                cmap='RdYlGn'
                            ),
                            use_container_width=True,
                            height=400
                        )

                        st.markdown("<br>", unsafe_allow_html=True)

                        # 統計資訊
                        st.markdown("### 📊 統計資訊")
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div class="stat-label">推薦數量</div>
                                <div class="stat-value" style="color: #667eea;">
                                    {len(recommendations)}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col2:
                            st.markdown("""
                            <div class="stat-card">
                                <div class="stat-label">資料來源</div>
                                <div class="stat-value" style="color: #22c55e; font-size: 1.3rem;">
                                    示範資料
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col3:
                            st.markdown("""
                            <div class="stat-card">
                                <div class="stat-label">更新狀態</div>
                                <div class="stat-value" style="color: #f59e0b; font-size: 1.3rem;">
                                    即時
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("ℹ️ 沒有符合篩選條件的權證")


def show_settings_page():
    """系統設定頁面"""

    # 載入配置管理器
    try:
        from backend.config.settings import system_settings
        settings_available = True
    except:
        settings_available = False
        st.warning("⚠️ 配置系統未載入，設定將不會被保存")

    # 頁面標題
    st.markdown("""
    <div class='page-header'>
        <h1>⚙️ 系統設定</h1>
        <p>自訂系統參數 | 效能調整 | 個人化設定</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h4 style='margin-top: 0;'>ℹ️ 設定說明</h4>
        <p style='margin-bottom: 0;'>
            在這裡您可以調整系統的各項參數，以符合您的使用需求。所有設定將即時生效。
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 使用標籤頁組織不同類型的設定
    tab1, tab2, tab3, tab4 = st.tabs(["📊 技術分析參數", "⚡ 效能設定", "🎨 介面設定", "💾 快取管理"])

    with tab1:
        st.markdown("### 📊 技術指標參數設定")

        # 從配置載入當前值（確保類型正確）
        if settings_available:
            current_ma_periods = system_settings.get('technical_analysis.ma_periods', [5, 20, 60])
            current_rsi_period = int(system_settings.get('technical_analysis.rsi_period', 14))
            current_rsi_overbought = int(system_settings.get('technical_analysis.rsi_overbought', 70))
            current_rsi_oversold = int(system_settings.get('technical_analysis.rsi_oversold', 30))
            current_macd = system_settings.get('technical_analysis.macd', [12, 26, 9])
            current_kdj = int(system_settings.get('technical_analysis.kdj_period', 9))
            current_bb_period = int(system_settings.get('technical_analysis.bollinger_period', 20))
            current_bb_std = float(system_settings.get('technical_analysis.bollinger_std', 2.0))
        else:
            current_ma_periods = [5, 20, 60]
            current_rsi_period = 14
            current_rsi_overbought = 70
            current_rsi_oversold = 30
            current_macd = [12, 26, 9]
            current_kdj = 9
            current_bb_period = 20
            current_bb_std = 2.0

        # 確保 ma_periods 和 macd 中的值都是 int
        current_ma_periods = [int(x) for x in current_ma_periods]
        current_macd = [int(x) for x in current_macd]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**移動平均線 (MA)**")
            ma5 = st.number_input("短期均線週期", min_value=3, max_value=20, value=current_ma_periods[0], step=1)
            ma20 = st.number_input("中期均線週期", min_value=10, max_value=50, value=current_ma_periods[1], step=1)
            ma60 = st.number_input("長期均線週期", min_value=30, max_value=120, value=current_ma_periods[2], step=1)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**RSI 指標**")
            rsi_period = st.number_input("RSI 週期", min_value=5, max_value=30, value=current_rsi_period, step=1)
            rsi_overbought = st.slider("超買閾值", min_value=60, max_value=90, value=current_rsi_overbought, step=5)
            rsi_oversold = st.slider("超賣閾值", min_value=10, max_value=40, value=current_rsi_oversold, step=5)

        with col2:
            st.markdown("**MACD 指標**")
            macd_fast = st.number_input("快線週期", min_value=8, max_value=20, value=current_macd[0], step=1)
            macd_slow = st.number_input("慢線週期", min_value=20, max_value=40, value=current_macd[1], step=1)
            macd_signal = st.number_input("信號線週期", min_value=5, max_value=15, value=current_macd[2], step=1)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**KDJ 指標**")
            kdj_period = st.number_input("KDJ 週期", min_value=5, max_value=20, value=current_kdj, step=1)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**布林通道**")
            bb_period = st.number_input("布林通道週期", min_value=10, max_value=30, value=current_bb_period, step=1)
            bb_std = st.number_input("標準差倍數", min_value=1.0, max_value=3.0, value=current_bb_std, step=0.1)

        if st.button("💾 儲存技術分析參數", type="primary", use_container_width=True):
            if settings_available:
                # 儲存到配置系統
                system_settings.set('technical_analysis.ma_periods', [ma5, ma20, ma60])
                system_settings.set('technical_analysis.rsi_period', rsi_period)
                system_settings.set('technical_analysis.rsi_overbought', rsi_overbought)
                system_settings.set('technical_analysis.rsi_oversold', rsi_oversold)
                system_settings.set('technical_analysis.macd', [macd_fast, macd_slow, macd_signal])
                system_settings.set('technical_analysis.kdj_period', kdj_period)
                system_settings.set('technical_analysis.bollinger_period', bb_period)
                system_settings.set('technical_analysis.bollinger_std', bb_std)
                system_settings.save()
                st.success("✅ 技術分析參數已儲存！")
            else:
                st.warning("⚠️ 配置系統未載入，無法儲存設定")

            st.info(f"""
            **已設定的參數：**
            - MA 週期: {ma5}, {ma20}, {ma60}
            - RSI: 週期 {rsi_period}, 超買 {rsi_overbought}, 超賣 {rsi_oversold}
            - MACD: {macd_fast}, {macd_slow}, {macd_signal}
            - KDJ 週期: {kdj_period}
            - 布林通道: 週期 {bb_period}, 標準差 {bb_std}
            """)

    with tab2:
        st.markdown("### ⚡ 效能與快取設定")

        # 從配置載入當前值
        if settings_available:
            current_cache_enabled = system_settings.get('cache.enabled', True)
            current_cache_ttl = system_settings.get('cache.default_ttl', 300) // 60  # 轉換為分鐘
            current_max_retries = system_settings.get('api.max_retries', 3)
            current_retry_delay = system_settings.get('api.retry_delay', 2)
            current_timeout = system_settings.get('api.timeout', 10)
            current_max_concurrent = system_settings.get('api.max_concurrent_requests', 5)
        else:
            current_cache_enabled = True
            current_cache_ttl = 5
            current_max_retries = 3
            current_retry_delay = 2
            current_timeout = 10
            current_max_concurrent = 5

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**快取設定**")
            enable_cache = st.checkbox("啟用資料快取", value=current_cache_enabled, help="啟用後可減少 API 請求次數")
            cache_ttl = st.slider("快取有效期（分鐘）", min_value=1, max_value=60, value=current_cache_ttl, step=1)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**API 請求設定**")
            max_retries = st.number_input("最大重試次數", min_value=1, max_value=5, value=current_max_retries, step=1)
            retry_delay = st.number_input("重試延遲（秒）", min_value=1, max_value=10, value=current_retry_delay, step=1)
            request_timeout = st.number_input("請求超時（秒）", min_value=5, max_value=30, value=current_timeout, step=1)

        with col2:
            st.markdown("**資料來源設定**")
            data_source = st.selectbox(
                "主要資料來源",
                ["yfinance (Yahoo Finance)", "本地參考資料", "混合模式（優先線上）"],
                index=2
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**並發設定**")
            max_concurrent = st.number_input("最大並發請求數", min_value=1, max_value=10, value=current_max_concurrent, step=1)

            st.markdown("<br>", unsafe_allow_html=True)

            # 顯示當前快取狀態
            st.markdown("**快取統計資訊**")
            stats_placeholder = st.empty()

            try:
                from backend.utils.cache_manager import cache_manager
                stats = cache_manager.get_stats()
                stats_placeholder.info(f"""
                📊 **快取狀態：**
                - 快取項目數：{stats.get('總快取項目', 0)}
                - 總存取次數：{stats.get('總存取次數', 0)}
                - 平均存取次數：{stats.get('平均存取次數', 0):.2f}
                """)
            except:
                stats_placeholder.caption("快取管理器未載入")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 儲存效能設定", type="primary", use_container_width=True):
                if settings_available:
                    # 儲存到配置系統
                    system_settings.set('cache.enabled', enable_cache)
                    system_settings.set('cache.default_ttl', cache_ttl * 60)  # 轉換為秒
                    system_settings.set('api.max_retries', max_retries)
                    system_settings.set('api.retry_delay', retry_delay)
                    system_settings.set('api.timeout', request_timeout)
                    system_settings.set('api.max_concurrent_requests', max_concurrent)
                    system_settings.save()

                    # 更新快取管理器的 TTL
                    try:
                        from backend.utils.cache_manager import cache_manager
                        cache_manager.set_default_ttl(cache_ttl * 60)
                    except:
                        pass

                    st.success("✅ 效能設定已儲存！")
                else:
                    st.warning("⚠️ 配置系統未載入，無法儲存設定")

        with col2:
            if st.button("🗑️ 清空快取", type="secondary", use_container_width=True):
                try:
                    from backend.utils.cache_manager import cache_manager
                    cache_manager.clear()
                    st.success("✅ 快取已清空！")
                    st.rerun()
                except:
                    st.warning("⚠️ 無法清空快取")

    with tab3:
        st.markdown("### 🎨 介面個人化設定")

        # 從配置載入當前值
        if settings_available:
            current_theme = system_settings.get('ui.theme', '紫色漸變（預設）')
            current_chart_height = system_settings.get('ui.chart_height', 500)
            current_max_rows = system_settings.get('ui.max_display_rows', 20)
            current_language = system_settings.get('ui.language', '繁體中文')
            current_show_tips = system_settings.get('ui.show_tips', True)
            current_show_guide = system_settings.get('ui.show_guide', True)
            current_show_hotkeys = system_settings.get('ui.show_hotkeys', False)
            current_show_success = system_settings.get('ui.show_success_messages', True)
            current_show_warnings = system_settings.get('ui.show_warning_messages', True)
            current_auto_refresh = system_settings.get('ui.auto_refresh', False)
            current_refresh_interval = system_settings.get('ui.refresh_interval', 300)
        else:
            current_theme = '紫色漸變（預設）'
            current_chart_height = 500
            current_max_rows = 20
            current_language = '繁體中文'
            current_show_tips = True
            current_show_guide = True
            current_show_hotkeys = False
            current_show_success = True
            current_show_warnings = True
            current_auto_refresh = False
            current_refresh_interval = 300

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**顯示設定**")
            theme_options = ["紫色漸變（預設）", "藍色", "綠色", "橙色"]
            theme_index = theme_options.index(current_theme) if current_theme in theme_options else 0
            theme_color = st.selectbox("主題色調", theme_options, index=theme_index)

            chart_height = st.slider("圖表高度（像素）", min_value=300, max_value=800, value=current_chart_height, step=50)

            max_rows = st.number_input("資料表最大顯示行數", min_value=10, max_value=100, value=current_max_rows, step=5)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**語言設定**")
            language_options = ["繁體中文", "簡體中文", "English"]
            language_index = language_options.index(current_language) if current_language in language_options else 0
            language = st.selectbox("介面語言", language_options, index=language_index)

        with col2:
            st.markdown("**功能顯示**")
            show_tips = st.checkbox("顯示操作提示", value=current_show_tips)
            show_guide = st.checkbox("顯示新手引導", value=current_show_guide)
            show_hotkeys = st.checkbox("啟用快捷鍵", value=current_show_hotkeys)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**通知設定**")
            show_success = st.checkbox("顯示成功訊息", value=current_show_success)
            show_warnings = st.checkbox("顯示警告訊息", value=current_show_warnings)
            auto_refresh = st.checkbox("啟用自動刷新", value=current_auto_refresh)

            if auto_refresh:
                refresh_interval = st.slider("刷新間隔（秒）", min_value=30, max_value=600, value=current_refresh_interval, step=30)
            else:
                refresh_interval = current_refresh_interval

        if st.button("💾 儲存介面設定", type="primary", use_container_width=True):
            if settings_available:
                # 儲存到配置系統
                system_settings.set('ui.theme', theme_color)
                system_settings.set('ui.chart_height', chart_height)
                system_settings.set('ui.max_display_rows', max_rows)
                system_settings.set('ui.language', language)
                system_settings.set('ui.show_tips', show_tips)
                system_settings.set('ui.show_guide', show_guide)
                system_settings.set('ui.show_hotkeys', show_hotkeys)
                system_settings.set('ui.show_success_messages', show_success)
                system_settings.set('ui.show_warning_messages', show_warnings)
                system_settings.set('ui.auto_refresh', auto_refresh)
                system_settings.set('ui.refresh_interval', refresh_interval)
                system_settings.save()
                st.success("✅ 介面設定已儲存！")
                st.balloons()
            else:
                st.warning("⚠️ 配置系統未載入，無法儲存設定")

    with tab4:
        st.markdown("### 💾 快取與資料管理")

        st.markdown("""
        <div class="warning-box">
            <h4 style='margin-top: 0;'>⚠️ 注意事項</h4>
            <p style='margin-bottom: 0;'>
                清除快取會刪除所有暫存的股票資料，下次查詢時需要重新獲取。
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**快取操作**")
            if st.button("🗑️ 清空所有快取", use_container_width=True):
                try:
                    from backend.utils.cache_manager import cache_manager
                    cache_manager.clear()
                    st.success("✅ 所有快取已清空")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 清空快取失敗：{str(e)}")

            if st.button("🧹 清理過期快取", use_container_width=True):
                try:
                    from backend.utils.cache_manager import cache_manager
                    count = cache_manager.cleanup_expired()
                    st.success(f"✅ 已清理 {count} 個過期項目")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 清理失敗：{str(e)}")

        with col2:
            st.markdown("**資料管理**")
            if st.button("📥 匯出系統設定", use_container_width=True):
                if settings_available:
                    try:
                        import json
                        settings_json = json.dumps(system_settings._settings, indent=2, ensure_ascii=False)
                        st.download_button(
                            label="💾 下載設定檔",
                            data=settings_json,
                            file_name="stock_system_settings.json",
                            mime="application/json",
                            use_container_width=True
                        )
                        st.success("✅ 準備好下載設定檔")
                    except Exception as e:
                        st.error(f"❌ 匯出失敗：{str(e)}")
                else:
                    st.warning("⚠️ 配置系統未載入")

            if st.button("📤 匯入系統設定", use_container_width=True):
                st.info("💡 請使用檔案上傳功能匯入設定（開發中）")

        with col3:
            st.markdown("**系統維護**")
            if st.button("🔄 重置為預設值", use_container_width=True):
                if settings_available:
                    try:
                        system_settings.reset_to_defaults()
                        st.success("✅ 已重置為預設值")
                        st.info("💡 部分設定需要重新啟動系統才能生效")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 重置失敗：{str(e)}")
                else:
                    st.warning("⚠️ 配置系統未載入")

            if st.button("ℹ️ 查看系統資訊", use_container_width=True):
                st.info("""
                **系統資訊：**
                - 版本：v2.0 Professional
                - Python：3.11+
                - Streamlit：1.31.0
                - 最後更新：2026-01-10
                - 配置系統：已啟用
                - 快取系統：已啟用
                - 日誌系統：已啟用
                """)

    # 底部資訊
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94a3b8;'>
        <p>💡 <strong>提示：</strong>修改設定後請記得儲存。部分設定需要重新啟動系統才能生效。</p>
    </div>
    """, unsafe_allow_html=True)


def show_technical_analysis_page():
    """技術分析頁面"""
    st.markdown("""
    <div class='page-header'>
        <h1>📈 技術分析</h1>
        <p>專業技術指標 | K線圖表 | 交易訊號</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h4 style='margin-top: 0;'>📊 技術分析工具</h4>
        <p style='margin-bottom: 0;'>
            提供完整的技術指標分析，包括 MA、MACD、RSI、KDJ、布林通道等，幫助您掌握股價走勢。
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        stock_id = st.text_input("🔍 請輸入股票代碼", value="2330", key="tech_stock_id")
    with col2:
        days = st.selectbox("📅 分析週期", [30, 60, 90, 180, 365], index=2, key="tech_days")

    if st.button("🚀 開始分析", type="primary", use_container_width=True):
        with st.spinner("正在進行技術分析..."):
            try:
                # 獲取股價資料
                df = st.session_state.data_fetcher.get_stock_price(stock_id, days=days)

                if df.empty:
                    st.error("❌ 無法獲取股票資料，請檢查股票代碼是否正確")
                    return

                analyzer = st.session_state.technical_analyzer

                # K線圖
                st.markdown("### 📊 K線圖與成交量")
                candlestick_fig = analyzer.create_candlestick_chart(df)
                st.plotly_chart(candlestick_fig, use_container_width=True)

                # 計算所有指標
                df = analyzer.calculate_ma(df, periods=[5, 20, 60])
                df = analyzer.calculate_macd(df)
                df = analyzer.calculate_rsi(df)
                df = analyzer.calculate_kdj(df)
                df = analyzer.calculate_bollinger_bands(df)

                # 顯示指標圖表
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 📈 移動平均線 (MA)")
                    ma_fig = analyzer.create_ma_chart(df)
                    st.plotly_chart(ma_fig, use_container_width=True)

                    st.markdown("### 📊 MACD")
                    macd_fig = analyzer.create_macd_chart(df)
                    st.plotly_chart(macd_fig, use_container_width=True)

                    st.markdown("### 📉 布林通道")
                    bb_fig = analyzer.create_bollinger_chart(df)
                    st.plotly_chart(bb_fig, use_container_width=True)

                with col2:
                    st.markdown("### 📊 RSI")
                    rsi_fig = analyzer.create_rsi_chart(df)
                    st.plotly_chart(rsi_fig, use_container_width=True)

                    st.markdown("### 📈 KDJ")
                    kdj_fig = analyzer.create_kdj_chart(df)
                    st.plotly_chart(kdj_fig, use_container_width=True)

                # 生成交易訊號
                st.markdown("### 🎯 交易訊號分析")
                signals = analyzer.generate_signals(df)

                # 顯示綜合訊號
                signal_emoji = "🟢" if signals['綜合訊號'] == "買入" else "🔴" if signals['綜合訊號'] == "賣出" else "🟡"
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                     padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 1rem;'>
                    <h2 style='color: white; margin: 0;'>{signal_emoji} 綜合訊號：{signals['綜合訊號']}</h2>
                </div>
                """, unsafe_allow_html=True)

                # 顯示訊號詳情
                if signals['訊號詳情']:
                    signal_df = pd.DataFrame(signals['訊號詳情'])
                    st.dataframe(signal_df, use_container_width=True)
                else:
                    st.info("當前沒有明確的交易訊號")

            except Exception as e:
                st.error(f"❌ 分析過程發生錯誤: {str(e)}")


def show_stock_comparison_page():
    """多股比較頁面"""
    st.markdown("""
    <div class='page-header'>
        <h1>📊 多股比較</h1>
        <p>橫向比較 | 產業分析 | 相對表現</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h4 style='margin-top: 0;'>📊 比較分析工具</h4>
        <p style='margin-bottom: 0;'>
            同時分析多支股票，比較報酬率、波動率、夏普比率等關鍵指標。
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 輸入股票代碼
    stock_input = st.text_input(
        "🔍 請輸入要比較的股票代碼（用逗號分隔）",
        value="2330,2317,2454",
        help="例如: 2330,2317,2454,2881,2882"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        days = st.slider("📅 分析週期（天）", 30, 365, 90, key="compare_days")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 開始比較", type="primary", use_container_width=True):
        stock_ids = [s.strip() for s in stock_input.split(',')]

        if len(stock_ids) < 2:
            st.error("❌ 請至少輸入 2 支股票進行比較")
            return

        with st.spinner("正在比較股票..."):
            try:
                comparator = st.session_state.stock_comparator
                comparison = comparator.compare_stocks(stock_ids, days=days)

                if comparison['stock_count'] == 0:
                    st.error("❌ 無法獲取任何股票資料")
                    return

                # 顯示比較表格
                st.markdown("### 📊 比較摘要")
                st.dataframe(
                    comparison['comparison_table'].style.background_gradient(
                        subset=['漲跌幅(%)', '夏普比率'],
                        cmap='RdYlGn'
                    ),
                    use_container_width=True
                )

                # 價格走勢比較
                st.markdown("### 📈 價格走勢比較（標準化）")
                price_fig = comparator.create_comparison_chart(comparison['stocks_data'])
                st.plotly_chart(price_fig, use_container_width=True)

                # 成交量比較
                st.markdown("### 📊 成交量比較")
                volume_fig = comparator.create_volume_comparison_chart(comparison['stocks_data'])
                st.plotly_chart(volume_fig, use_container_width=True)

                # 報酬率分布
                st.markdown("### 📊 日報酬率分布")
                return_fig = comparator.create_return_distribution_chart(comparison['stocks_data'])
                st.plotly_chart(return_fig, use_container_width=True)

                # 生成比較報告
                st.markdown("### 📝 比較報告")
                report = comparator.generate_comparison_report(stock_ids, days)
                st.markdown(report)

            except Exception as e:
                st.error(f"❌ 比較過程發生錯誤: {str(e)}")


def show_portfolio_page():
    """投資組合管理頁面"""
    st.markdown("""
    <div class='page-header'>
        <h1>💼 投資組合管理</h1>
        <p>持倉追蹤 | 績效分析 | 風險管理</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h4 style='margin-top: 0;'>💼 組合管理工具</h4>
        <p style='margin-bottom: 0;'>
            管理您的投資組合，追蹤持倉、計算報酬率、評估風險指標。
        </p>
    </div>
    """, unsafe_allow_html=True)

    portfolio_manager = st.session_state.portfolio_manager

    # 標籤頁
    tab1, tab2, tab3 = st.tabs(["📊 組合概覽", "➕ 新增持倉", "📈 績效分析"])

    with tab1:
        st.markdown("### 💼 當前投資組合")

        if not portfolio_manager.portfolio:
            st.info("💡 您的投資組合是空的，請在「新增持倉」標籤中添加股票")
        else:
            # 獲取組合價值
            portfolio_value = portfolio_manager.get_portfolio_value()

            # 顯示總覽
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("總投資成本", f"${portfolio_value['total_cost']:,.0f}")
            with col2:
                st.metric("當前市值", f"${portfolio_value['total_value']:,.0f}")
            with col3:
                profit_color = "normal" if portfolio_value['total_profit'] >= 0 else "inverse"
                st.metric("總損益", f"${portfolio_value['total_profit']:,.0f}",
                         delta=f"{portfolio_value['total_return']:.2f}%",
                         delta_color=profit_color)
            with col4:
                st.metric("持股檔數", len(portfolio_value['positions']))

            # 持倉明細
            st.markdown("### 📋 持倉明細")
            positions_df = pd.DataFrame(portfolio_value['positions'])
            st.dataframe(
                positions_df.style.background_gradient(subset=['報酬率(%)'], cmap='RdYlGn'),
                use_container_width=True
            )

            # 組合圖表
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🥧 持倉分布")
                pie_fig = portfolio_manager.create_portfolio_pie_chart(portfolio_value)
                st.plotly_chart(pie_fig, use_container_width=True)

            with col2:
                st.markdown("### 📊 損益排名")
                # 顯示前3名和後3名
                sorted_positions = sorted(portfolio_value['positions'],
                                        key=lambda x: x['報酬率(%)'], reverse=True)

                st.markdown("**📈 表現最佳**")
                for pos in sorted_positions[:3]:
                    st.success(f"{pos['股票代碼']}: {pos['報酬率(%)']}%")

                st.markdown("**📉 表現最差**")
                for pos in sorted_positions[-3:]:
                    st.error(f"{pos['股票代碼']}: {pos['報酬率(%)']}%")

    with tab2:
        st.markdown("### ➕ 新增持倉")

        col1, col2, col3 = st.columns(3)
        with col1:
            add_stock_id = st.text_input("股票代碼", value="2330")
        with col2:
            add_shares = st.number_input("股數", min_value=1, value=1000, step=100)
        with col3:
            add_cost = st.number_input("成本價", min_value=0.0, value=600.0, step=0.5)

        if st.button("➕ 加入組合", type="primary", use_container_width=True):
            portfolio_manager.add_position(add_stock_id, add_shares, add_cost)
            st.success(f"✅ 已成功加入 {add_stock_id}")
            st.rerun()

        st.markdown("---")
        st.markdown("### 🗑️ 移除持倉")

        if portfolio_manager.portfolio:
            remove_stock = st.selectbox("選擇要移除的股票", list(portfolio_manager.portfolio.keys()))
            if st.button("🗑️ 移除", type="secondary", use_container_width=True):
                portfolio_manager.remove_position(remove_stock)
                st.success(f"✅ 已移除 {remove_stock}")
                st.rerun()

    with tab3:
        st.markdown("### 📈 績效與風險分析")

        if not portfolio_manager.portfolio:
            st.info("💡 請先新增持倉")
        else:
            days = st.slider("分析週期（天）", 30, 365, 90, key="portfolio_days")

            if st.button("🔍 分析績效", type="primary"):
                with st.spinner("正在分析..."):
                    try:
                        risk_metrics = portfolio_manager.calculate_portfolio_risk(days=days)

                        # 顯示風險指標
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("年化報酬率", f"{risk_metrics['年化報酬率(%)']}%")
                        with col2:
                            st.metric("年化波動率", f"{risk_metrics['年化波動率(%)']}%")
                        with col3:
                            st.metric("夏普比率", f"{risk_metrics['夏普比率']:.2f}")
                        with col4:
                            st.metric("最大回撤", f"{risk_metrics['最大回撤(%)']}%")

                        # 組合價值走勢
                        st.markdown("### 📊 組合價值走勢")
                        value_fig = portfolio_manager.create_portfolio_value_chart(days=days)
                        st.plotly_chart(value_fig, use_container_width=True)

                        # 生成報告
                        st.markdown("### 📝 組合分析報告")
                        report = portfolio_manager.generate_portfolio_report(days=days)
                        st.markdown(report)

                    except Exception as e:
                        st.error(f"❌ 分析過程發生錯誤: {str(e)}")


def show_market_sentiment_page():
    """市場情緒分析頁面"""
    st.markdown("""
    <div class='page-header'>
        <h1>🎭 市場情緒分析</h1>
        <p>恐懼貪婪指數 | 市場廣度 | 產業輪動</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h4 style='margin-top: 0;'>🎭 情緒分析工具</h4>
        <p style='margin-bottom: 0;'>
            分析市場整體情緒，包括恐懼貪婪指數、市場廣度、產業輪動等關鍵指標。
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 股票池設定
    stock_pool = st.text_area(
        "📋 請輸入分析股票池（用逗號分隔）",
        value="2330,2317,2454,2308,2881,2882,2886,2891,2892,2303",
        help="建議至少 10 支股票以獲得較準確的市場情緒"
    )

    days = st.slider("📅 分析週期（天）", 7, 90, 30, key="sentiment_days")

    if st.button("🚀 分析市場情緒", type="primary", use_container_width=True):
        stock_ids = [s.strip() for s in stock_pool.split(',')]

        if len(stock_ids) < 5:
            st.error("❌ 建議至少輸入 5 支股票進行分析")
            return

        with st.spinner("正在分析市場情緒..."):
            try:
                sentiment_analyzer = st.session_state.market_sentiment

                # 計算市場廣度
                st.markdown("### 📊 市場廣度分析")
                breadth = sentiment_analyzer.calculate_market_breadth(stock_ids, days=days)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("上漲家數", breadth['上漲家數'])
                with col2:
                    st.metric("下跌家數", breadth['下跌家數'])
                with col3:
                    st.metric("上漲比例", f"{breadth['上漲比例(%)']}%")
                with col4:
                    st.metric("市場情緒", breadth['市場情緒'])

                # 市場廣度圖表
                breadth_fig = sentiment_analyzer.create_breadth_chart(breadth)
                st.plotly_chart(breadth_fig, use_container_width=True)

                # 恐懼貪婪指數
                st.markdown("### 🎭 恐懼貪婪指數")
                fear_greed = sentiment_analyzer.calculate_fear_greed_index(stock_ids, days=days)

                # 顯示指數儀表盤
                gauge_fig = sentiment_analyzer.create_sentiment_gauge_chart(
                    fear_greed['恐懼貪婪指數'],
                    title="恐懼貪婪指數"
                )
                st.plotly_chart(gauge_fig, use_container_width=True)

                # 各項得分
                st.markdown("### 📊 各項得分明細")
                scores_df = pd.DataFrame([fear_greed['各項得分']]).T
                scores_df.columns = ['得分']
                st.dataframe(
                    scores_df.style.background_gradient(cmap='RdYlGn', vmin=0, vmax=100),
                    use_container_width=True
                )

                # 產業輪動分析
                st.markdown("### 🔄 產業輪動分析")
                sector_rotation = sentiment_analyzer.analyze_sector_rotation(days=days)

                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"📈 領漲產業: {sector_rotation['領漲產業']}")
                with col2:
                    st.error(f"📉 落後產業: {sector_rotation['落後產業']}")

                # 產業表現圖表
                sector_fig = sentiment_analyzer.create_sector_rotation_chart(sector_rotation['產業排名'])
                st.plotly_chart(sector_fig, use_container_width=True)

                # 市場展望報告
                st.markdown("### 📝 市場展望報告")
                outlook = sentiment_analyzer.generate_market_outlook(stock_ids, days=days)
                st.markdown(outlook)

            except Exception as e:
                st.error(f"❌ 分析過程發生錯誤: {str(e)}")


if __name__ == "__main__":
    main()
