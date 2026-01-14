"""
首頁

顯示系統概覽、核心功能卡片、熱門股票等資訊。
"""

import streamlit as st
from typing import Optional


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
    if st.session_state.get('enhanced_features', False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
             padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem;
             color: white; text-align: center; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
             font-size: 1.05rem;">
            <strong style='font-size: 1.15rem;'>✨ 專業版模式已啟用</strong> |
            快取系統 ✓ | 日誌記錄 ✓ | 配置管理 ✓ | 智慧重試 ✓
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("💡 使用標準模式運行。如需啟用專業功能，請確保已安裝所有增強模組。")

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
    _render_top_stocks_section()

    st.markdown("<br>", unsafe_allow_html=True)

    # 快速開始指南
    _render_quick_start_guide()

    st.markdown("<br>", unsafe_allow_html=True)

    # 系統特色
    _render_system_features()


def _render_top_stocks_section():
    """渲染熱門股票區塊"""
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


def _render_quick_start_guide():
    """渲染快速開始指南"""
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


def _render_system_features():
    """渲染系統特色區塊"""
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
