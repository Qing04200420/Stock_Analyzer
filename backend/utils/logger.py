"""
統一日誌記錄系統
提供結構化的日誌記錄功能，便於除錯和監控
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class StockSystemLogger:
    """股市系統日誌記錄器"""

    def __init__(self, name: str = "stock_system"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # 避免重複添加 handler
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """設定日誌處理器"""
        # 創建日誌目錄
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # 檔案處理器 - 詳細日誌
        log_file = log_dir / f"stock_system_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 錯誤日誌處理器
        error_file = log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.FileHandler(error_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)

        # 控制台處理器 - 僅重要訊息
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # 設定格式
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )

        file_handler.setFormatter(detailed_formatter)
        error_handler.setFormatter(detailed_formatter)
        console_handler.setFormatter(simple_formatter)

        # 添加處理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str, **kwargs):
        """記錄資訊級別日誌"""
        self.logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        """記錄警告級別日誌"""
        self.logger.warning(message, extra=kwargs)

    def error(self, message: str, exc_info: bool = True, **kwargs):
        """記錄錯誤級別日誌"""
        self.logger.error(message, exc_info=exc_info, extra=kwargs)

    def debug(self, message: str, **kwargs):
        """記錄除錯級別日誌"""
        self.logger.debug(message, extra=kwargs)

    def critical(self, message: str, exc_info: bool = True, **kwargs):
        """記錄嚴重錯誤級別日誌"""
        self.logger.critical(message, exc_info=exc_info, extra=kwargs)


# 建立全域日誌記錄器實例
system_logger = StockSystemLogger()
