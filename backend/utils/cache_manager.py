"""
資料快取管理器
提供記憶體快取功能，減少API請求次數，提升系統效能
"""

import time
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import threading


class CacheManager:
    """快取管理器 - 單例模式"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._default_ttl = 300  # 預設5分鐘過期
        self._initialized = True

    def get(self, key: str) -> Optional[Any]:
        """
        從快取中獲取資料

        Args:
            key: 快取鍵值

        Returns:
            快取的資料，如果不存在或已過期則返回 None
        """
        with self._lock:
            if key not in self._cache:
                return None

            cache_entry = self._cache[key]

            # 檢查是否過期
            if time.time() > cache_entry['expires_at']:
                del self._cache[key]
                return None

            # 更新存取時間
            cache_entry['last_accessed'] = time.time()
            cache_entry['access_count'] += 1

            return cache_entry['data']

    def set(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """
        將資料存入快取

        Args:
            key: 快取鍵值
            data: 要快取的資料
            ttl: 過期時間（秒），None 則使用預設值
        """
        if ttl is None:
            ttl = self._default_ttl

        with self._lock:
            self._cache[key] = {
                'data': data,
                'created_at': time.time(),
                'expires_at': time.time() + ttl,
                'last_accessed': time.time(),
                'access_count': 0
            }

    def delete(self, key: str) -> bool:
        """
        刪除快取項目

        Args:
            key: 快取鍵值

        Returns:
            是否成功刪除
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        """清空所有快取"""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> int:
        """
        清理已過期的快取項目

        Returns:
            清理的項目數量
        """
        current_time = time.time()
        expired_keys = []

        with self._lock:
            for key, entry in self._cache.items():
                if current_time > entry['expires_at']:
                    expired_keys.append(key)

            for key in expired_keys:
                del self._cache[key]

        return len(expired_keys)

    def get_stats(self) -> Dict[str, Any]:
        """
        獲取快取統計資訊

        Returns:
            快取統計資訊字典
        """
        with self._lock:
            total_items = len(self._cache)
            total_accesses = sum(entry['access_count'] for entry in self._cache.values())

            return {
                '總快取項目': total_items,
                '總存取次數': total_accesses,
                '平均存取次數': total_accesses / total_items if total_items > 0 else 0,
                '預設TTL': self._default_ttl
            }

    def set_default_ttl(self, ttl: int) -> None:
        """
        設定預設過期時間

        Args:
            ttl: 過期時間（秒）
        """
        self._default_ttl = ttl


# 建立全域快取管理器實例
cache_manager = CacheManager()
