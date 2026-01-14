"""
卡片元件

包含各種資訊卡片的可重用元件。
"""

import streamlit as st
from typing import Optional, Dict, List


def page_header(title: str, description: Optional[str] = None, icon: str = "📊") -> None:
    """
    顯示頁面標題

    Args:
        title: 標題文字
        description: 描述文字（可選）
        icon: 圖示（可選）
    """
    desc_html = f"<p>{description}</p>" if description else ""

    st.markdown(f"""
        <div class='page-header'>
            <h1>{icon} {title}</h1>
            {desc_html}
        </div>
    """, unsafe_allow_html=True)


def metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: str = "normal"
) -> None:
    """
    顯示指標卡片

    Args:
        label: 指標名稱
        value: 指標值
        delta: 變化量（可選）
        delta_color: 變化量顏色 ("normal", "inverse", "off")
    """
    st.markdown(f"""
        <div class='metric-card'>
            <div class='stat-label'>{label}</div>
            <div class='stat-value'>{value}</div>
        </div>
    """, unsafe_allow_html=True)


def success_box(message: str, icon: str = "✅") -> None:
    """
    顯示成功訊息框

    Args:
        message: 訊息內容
        icon: 圖示
    """
    st.markdown(f"""
        <div class='success-box'>
            {icon} {message}
        </div>
    """, unsafe_allow_html=True)


def warning_box(message: str, icon: str = "⚠️") -> None:
    """
    顯示警告訊息框

    Args:
        message: 訊息內容
        icon: 圖示
    """
    st.markdown(f"""
        <div class='warning-box'>
            {icon} {message}
        </div>
    """, unsafe_allow_html=True)


def danger_box(message: str, icon: str = "❌") -> None:
    """
    顯示危險/錯誤訊息框

    Args:
        message: 訊息內容
        icon: 圖示
    """
    st.markdown(f"""
        <div class='danger-box'>
            {icon} {message}
        </div>
    """, unsafe_allow_html=True)


def info_box(message: str, icon: str = "ℹ️") -> None:
    """
    顯示資訊訊息框

    Args:
        message: 訊息內容
        icon: 圖示
    """
    st.markdown(f"""
        <div class='info-box'>
            {icon} {message}
        </div>
    """, unsafe_allow_html=True)


def feature_card(
    icon: str,
    title: str,
    description: str,
    key: Optional[str] = None
) -> None:
    """
    顯示功能卡片

    Args:
        icon: 圖示
        title: 標題
        description: 描述
        key: 按鈕鍵值（用於導航）
    """
    st.markdown(f"""
        <div class='feature-card'>
            <div class='feature-icon'>{icon}</div>
            <h3 style='color: #667eea; margin: 0.5rem 0;'>{title}</h3>
            <p style='color: #1e293b; margin: 0.5rem 0;'>{description}</p>
        </div>
    """, unsafe_allow_html=True)


def stat_cards_row(stats: List[Dict[str, str]]) -> None:
    """
    顯示一排統計卡片

    Args:
        stats: 統計資料列表，每個元素是包含 'label' 和 'value' 的字典
    """
    cols = st.columns(len(stats))

    for col, stat in zip(cols, stats):
        with col:
            st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-label'>{stat['label']}</div>
                    <div class='stat-value'>{stat['value']}</div>
                </div>
            """, unsafe_allow_html=True)


def risk_level_badge(risk_level: str) -> str:
    """
    返回風險等級徽章 HTML

    Args:
        risk_level: 風險等級 ("極低風險", "低風險", "中等風險", "高風險", "極高風險")

    Returns:
        HTML 字串
    """
    color_map = {
        "極低風險": "#28a745",
        "低風險": "#5cb85c",
        "中等風險": "#ffc107",
        "高風險": "#ff6b6b",
        "極高風險": "#dc3545"
    }

    color = color_map.get(risk_level, "#6c757d")

    return f"""
        <span style='
            background-color: {color};
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        '>
            {risk_level}
        </span>
    """


def signal_badge(signal: str) -> str:
    """
    返回交易訊號徽章 HTML

    Args:
        signal: 訊號類型 ("強烈買入", "買入", "持有", "賣出", "強烈賣出")

    Returns:
        HTML 字串
    """
    color_map = {
        "強烈買入": "#28a745",
        "買入": "#5cb85c",
        "持有": "#ffc107",
        "賣出": "#ff6b6b",
        "強烈賣出": "#dc3545"
    }

    icon_map = {
        "強烈買入": "📈⬆️",
        "買入": "📈",
        "持有": "➡️",
        "賣出": "📉",
        "強烈賣出": "📉⬇️"
    }

    color = color_map.get(signal, "#6c757d")
    icon = icon_map.get(signal, "")

    return f"""
        <span style='
            background-color: {color};
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        '>
            {icon} {signal}
        </span>
    """


def stock_info_card(stock_data: Dict) -> None:
    """
    顯示股票基本資訊卡片

    Args:
        stock_data: 包含股票資訊的字典
    """
    st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #667eea; margin: 0 0 1rem 0;'>
                {stock_data.get('name', 'N/A')} ({stock_data.get('code', 'N/A')})
            </h3>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                <div>
                    <div class='stat-label'>產業</div>
                    <div style='font-weight: 600; color: #1e293b;'>{stock_data.get('industry', 'N/A')}</div>
                </div>
                <div>
                    <div class='stat-label'>市場</div>
                    <div style='font-weight: 600; color: #1e293b;'>{stock_data.get('market', 'N/A')}</div>
                </div>
                <div>
                    <div class='stat-label'>最新價</div>
                    <div style='font-weight: 700; font-size: 1.5rem; color: #667eea;'>
                        {stock_data.get('latest_price', 'N/A')}
                    </div>
                </div>
                <div>
                    <div class='stat-label'>漲跌幅</div>
                    <div style='font-weight: 700; font-size: 1.5rem; color: {"#28a745" if stock_data.get("change_percent", 0) >= 0 else "#dc3545"};'>
                        {stock_data.get('change_percent', 'N/A')}%
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def progress_card(title: str, current: float, target: float, unit: str = "") -> None:
    """
    顯示進度卡片

    Args:
        title: 標題
        current: 當前值
        target: 目標值
        unit: 單位
    """
    percentage = min(int((current / target) * 100), 100) if target > 0 else 0
    color = "#28a745" if percentage >= 70 else "#ffc107" if percentage >= 40 else "#dc3545"

    st.markdown(f"""
        <div class='metric-card'>
            <div class='stat-label'>{title}</div>
            <div style='margin: 1rem 0;'>
                <div style='background-color: #e9ecef; border-radius: 10px; height: 20px; overflow: hidden;'>
                    <div style='
                        background-color: {color};
                        height: 100%;
                        width: {percentage}%;
                        transition: width 0.3s ease;
                        border-radius: 10px;
                    '></div>
                </div>
            </div>
            <div style='display: flex; justify-content: space-between; font-size: 0.9rem;'>
                <span style='color: #64748b;'>當前: {current}{unit}</span>
                <span style='color: #64748b;'>目標: {target}{unit}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
