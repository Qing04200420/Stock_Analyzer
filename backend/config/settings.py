"""
系統配置管理
集中管理所有系統參數和設定
"""

from typing import Dict, Any
import json
from pathlib import Path


class SystemSettings:
    """系統設定管理器"""

    def __init__(self):
        self.config_file = Path("config.json")
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        """載入設定檔案"""
        default_settings = {
            # 資料快取設定
            "cache": {
                "enabled": True,
                "default_ttl": 300,  # 5分鐘
                "stock_price_ttl": 300,
                "stock_info_ttl": 3600  # 1小時
            },

            # API 設定
            "api": {
                "max_retries": 3,
                "retry_delay": 2,  # 秒
                "timeout": 10,
                "rate_limit_delay": 1  # 請求間隔
            },

            # 技術分析參數
            "technical_analysis": {
                "ma_periods": [5, 20, 60],
                "rsi_period": 14,
                "rsi_overbought": 70,
                "rsi_oversold": 30,
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "kdj_period": 9,
                "bollinger_period": 20,
                "bollinger_std": 2
            },

            # 風險評估參數
            "risk_assessment": {
                "var_confidence": 0.95,
                "risk_free_rate": 0.015,  # 無風險利率 1.5%
                "market_return": 0.08,  # 市場平均報酬率 8%
                "volatility_threshold_low": 0.15,
                "volatility_threshold_high": 0.30
            },

            # 回測設定
            "backtest": {
                "initial_capital": 1000000,  # 初始資金 100萬
                "commission_rate": 0.001425,  # 手續費率 0.1425%
                "tax_rate": 0.003,  # 證交稅 0.3%
                "slippage": 0.001  # 滑價 0.1%
            },

            # UI 設定
            "ui": {
                "theme": "purple",  # 主題顏色
                "chart_height": 500,
                "max_display_rows": 20,
                "refresh_interval": 300,  # 自動刷新間隔（秒）
                "language": "zh-TW"
            },

            # 資料來源設定
            "data_source": {
                "primary": "yfinance",
                "fallback": "reference",
                "use_cache": True,
                "offline_mode": False
            },

            # 效能設定
            "performance": {
                "max_concurrent_requests": 5,
                "cache_cleanup_interval": 3600,  # 1小時清理一次快取
                "log_retention_days": 30
            }
        }

        # 如果設定檔存在，載入並合併
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_settings = json.load(f)
                    default_settings.update(user_settings)
            except Exception:
                pass

        return default_settings

    def save_settings(self) -> bool:
        """儲存設定到檔案"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        獲取設定值

        Args:
            key_path: 設定路徑，使用點號分隔，例如 "cache.enabled"
            default: 預設值

        Returns:
            設定值
        """
        keys = key_path.split('.')
        value = self.settings

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any) -> None:
        """
        設定值

        Args:
            key_path: 設定路徑，使用點號分隔
            value: 要設定的值
        """
        keys = key_path.split('.')
        current = self.settings

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value

    def reset_to_defaults(self) -> None:
        """重置為預設設定"""
        if self.config_file.exists():
            self.config_file.unlink()
        self._settings = self._load_settings()

    def reset_to_default(self) -> None:
        """重置為預設設定（向後兼容）"""
        self.reset_to_defaults()


# 建立全域設定管理器實例
system_settings = SystemSettings()

# 向後兼容的別名
settings = system_settings
