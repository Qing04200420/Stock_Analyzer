"""
主題樣式定義

此模組包含所有 CSS 樣式，支援深色和淺色主題。
"""

# 統一現代化 CSS 樣式 - 深色主題適配
MAIN_CSS = """
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
"""


def apply_theme():
    """應用主題樣式到 Streamlit 應用"""
    import streamlit as st
    st.markdown(MAIN_CSS, unsafe_allow_html=True)


# 顏色常數
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8',
    'white': '#ffffff',
    'dark': '#1e293b',
    'gray': '#64748b',
}

# 漸層樣式
GRADIENTS = {
    'primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'success': 'linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%)',
    'warning': 'linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%)',
    'danger': 'linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%)',
    'info': 'linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%)',
}
