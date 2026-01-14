"""
圖表元件

包含所有圖表繪製相關的可重用元件。
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Optional


def plot_stock_candlestick(
    df: pd.DataFrame,
    title: str = "股價走勢圖",
    height: int = 500
) -> None:
    """
    繪製股價 K 線圖

    Args:
        df: 包含 OHLC 資料的 DataFrame (需要欄位: 開盤價, 最高價, 最低價, 收盤價)
        title: 圖表標題
        height: 圖表高度（像素）
    """
    if df.empty:
        st.warning("⚠️ 無資料可顯示")
        return

    required_columns = ['開盤價', '最高價', '最低價', '收盤價']
    if not all(col in df.columns for col in required_columns):
        st.error(f"❌ 資料格式錯誤：需要包含 {', '.join(required_columns)}")
        return

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['開盤價'],
        high=df['最高價'],
        low=df['最低價'],
        close=df['收盤價'],
        name='K線',
        increasing_line_color='#28a745',
        decreasing_line_color='#dc3545'
    )])

    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'weight': 'bold'}
        },
        xaxis_title="日期",
        yaxis_title="價格 (TWD)",
        template="plotly_white",
        height=height,
        hovermode='x unified',
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_technical_indicators(df: pd.DataFrame, height: int = 600) -> None:
    """
    繪製技術指標圖（K線 + RSI + MACD + 成交量）

    Args:
        df: 包含價格和技術指標的 DataFrame
        height: 圖表高度（像素）
    """
    if df.empty or '收盤價' not in df.columns:
        st.warning("⚠️ 無資料可顯示")
        return

    # 建立子圖
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.4, 0.2, 0.2, 0.2],
        subplot_titles=('K線圖', 'RSI', 'MACD', '成交量')
    )

    # 1. K線圖
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['開盤價'],
            high=df['最高價'],
            low=df['最低價'],
            close=df['收盤價'],
            name='K線',
            increasing_line_color='#28a745',
            decreasing_line_color='#dc3545'
        ),
        row=1, col=1
    )

    # 添加移動平均線
    for col in df.columns:
        if col.startswith('MA'):
            period = col.replace('MA', '')
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    name=f'MA{period}',
                    line=dict(width=1.5)
                ),
                row=1, col=1
            )

    # 2. RSI
    if 'RSI' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['RSI'],
                name='RSI',
                line=dict(color='#667eea', width=2)
            ),
            row=2, col=1
        )
        # RSI 超買超賣線
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1, opacity=0.5)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1, opacity=0.5)

    # 3. MACD
    if all(col in df.columns for col in ['MACD', 'MACD_Signal']):
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['MACD'],
                name='MACD',
                line=dict(color='blue', width=2)
            ),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['MACD_Signal'],
                name='Signal',
                line=dict(color='orange', width=2)
            ),
            row=3, col=1
        )
        if 'MACD_Hist' in df.columns:
            colors = ['green' if val >= 0 else 'red' for val in df['MACD_Hist']]
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['MACD_Hist'],
                    name='Histogram',
                    marker_color=colors,
                    opacity=0.5
                ),
                row=3, col=1
            )

    # 4. 成交量
    if '成交量' in df.columns:
        colors = ['#28a745' if df['收盤價'].iloc[i] >= df['開盤價'].iloc[i] else '#dc3545'
                  for i in range(len(df))]
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['成交量'],
                name='成交量',
                marker_color=colors,
                opacity=0.6
            ),
            row=4, col=1
        )

    # 更新佈局
    fig.update_layout(
        height=height,
        showlegend=True,
        template="plotly_white",
        hovermode='x unified',
        xaxis_rangeslider_visible=False
    )

    # 更新 y 軸標題
    fig.update_yaxes(title_text="價格 (TWD)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    fig.update_yaxes(title_text="成交量", row=4, col=1)

    st.plotly_chart(fig, use_container_width=True)


def plot_volume_chart(df: pd.DataFrame, title: str = "成交量圖", height: int = 400) -> None:
    """
    繪製成交量圖

    Args:
        df: 包含成交量資料的 DataFrame
        title: 圖表標題
        height: 圖表高度
    """
    if df.empty or '成交量' not in df.columns:
        st.warning("⚠️ 無成交量資料")
        return

    # 根據漲跌上色
    colors = []
    for i in range(len(df)):
        if i == 0:
            colors.append('#667eea')
        elif df['收盤價'].iloc[i] >= df['收盤價'].iloc[i-1]:
            colors.append('#28a745')
        else:
            colors.append('#dc3545')

    fig = go.Figure(data=[
        go.Bar(
            x=df.index,
            y=df['成交量'],
            name='成交量',
            marker_color=colors,
            opacity=0.7
        )
    ])

    fig.update_layout(
        title=title,
        xaxis_title="日期",
        yaxis_title="成交量",
        template="plotly_white",
        height=height
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_risk_metrics_radar(metrics: dict, title: str = "風險指標雷達圖") -> None:
    """
    繪製風險指標雷達圖

    Args:
        metrics: 包含各項風險指標的字典 (鍵: 指標名稱, 值: 0-100 的分數)
        title: 圖表標題
    """
    if not metrics:
        st.warning("⚠️ 無風險指標資料")
        return

    categories = list(metrics.keys())
    values = list(metrics.values())

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title=title,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_backtest_equity_curve(
    equity_curve: pd.Series,
    title: str = "回測權益曲線",
    height: int = 400
) -> None:
    """
    繪製回測權益曲線

    Args:
        equity_curve: 權益序列（索引為日期，值為權益）
        title: 圖表標題
        height: 圖表高度
    """
    if equity_curve.empty:
        st.warning("⚠️ 無回測資料")
        return

    fig = go.Figure()

    # 權益曲線
    fig.add_trace(go.Scatter(
        x=equity_curve.index,
        y=equity_curve.values,
        name='權益',
        line=dict(color='#667eea', width=2),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))

    # 初始權益水平線
    initial_equity = equity_curve.iloc[0]
    fig.add_hline(
        y=initial_equity,
        line_dash="dash",
        line_color="gray",
        annotation_text="初始資金",
        opacity=0.5
    )

    fig.update_layout(
        title=title,
        xaxis_title="日期",
        yaxis_title="權益 (TWD)",
        template="plotly_white",
        height=height,
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)
