"""
請求限流器

解決 Yahoo Finance API 429 錯誤（Too Many Requests）的核心模組。
實現智能請求限流、自動重試、User-Agent 輪換等功能。
"""

import time
import random
from typing import Optional, Callable, Any
from datetime import datetime, timedelta
from collections import deque
from threading import Lock
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    請求速率限制器

    功能：
    - 自動限制請求頻率
    - 追蹤請求歷史
    - 智能延遲計算
    - 線程安全
    """

    def __init__(
        self,
        max_requests: int = 5,
        time_window: int = 60,
        min_delay: float = 2.0,
        max_delay: float = 5.0
    ):
        """
        初始化速率限制器

        Args:
            max_requests: 時間視窗內最大請求數
            time_window: 時間視窗（秒）
            min_delay: 最小延遲（秒）
            max_delay: 最大延遲（秒）
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.min_delay = min_delay
        self.max_delay = max_delay

        self.request_times: deque = deque()
        self.lock = Lock()
        self.last_429_time: Optional[datetime] = None
        self.backoff_until: Optional[datetime] = None

    def wait_if_needed(self) -> None:
        """
        如果需要，等待直到可以發送請求

        實現策略：
        1. 檢查是否在退避期內
        2. 檢查請求歷史
        3. 計算需要等待的時間
        4. 執行延遲
        """
        with self.lock:
            now = datetime.now()

            # 1. 檢查退避期
            if self.backoff_until and now < self.backoff_until:
                wait_seconds = (self.backoff_until - now).total_seconds()
                logger.warning(f"⏸️ 退避期中，等待 {wait_seconds:.1f} 秒")
                time.sleep(wait_seconds)
                return

            # 2. 清理過期的請求記錄
            cutoff_time = now - timedelta(seconds=self.time_window)
            while self.request_times and self.request_times[0] < cutoff_time:
                self.request_times.popleft()

            # 3. 檢查是否達到請求上限
            if len(self.request_times) >= self.max_requests:
                # 計算需要等待的時間
                oldest_request = self.request_times[0]
                wait_seconds = (oldest_request + timedelta(seconds=self.time_window) - now).total_seconds()
                wait_seconds = max(0, wait_seconds) + 1  # 額外加1秒確保安全

                logger.info(f"⏳ 達到速率限制，等待 {wait_seconds:.1f} 秒")
                time.sleep(wait_seconds)

                # 清理過期記錄
                cutoff_time = datetime.now() - timedelta(seconds=self.time_window)
                while self.request_times and self.request_times[0] < cutoff_time:
                    self.request_times.popleft()

            # 4. 隨機延遲（防止模式識別）
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)

            # 5. 記錄請求時間
            self.request_times.append(datetime.now())

    def record_429_error(self) -> None:
        """
        記錄 429 錯誤，啟動指數退避

        退避策略：
        - 第1次: 60秒
        - 第2次: 120秒
        - 第3次: 300秒（5分鐘）
        - 第4次+: 600秒（10分鐘）
        """
        with self.lock:
            now = datetime.now()
            self.last_429_time = now

            # 計算退避時間（指數增長）
            if not self.backoff_until:
                backoff_seconds = 60
            else:
                # 計算已經發生的 429 錯誤次數
                backoff_seconds = min(600, 60 * (2 ** self._get_429_count()))

            self.backoff_until = now + timedelta(seconds=backoff_seconds)

            logger.error(f"❌ 收到 429 錯誤，啟動退避 {backoff_seconds} 秒")

    def _get_429_count(self) -> int:
        """計算最近的 429 錯誤次數"""
        if not self.last_429_time:
            return 0

        # 如果距離上次 429 超過 1 小時，重置計數
        if (datetime.now() - self.last_429_time).total_seconds() > 3600:
            return 0

        return 1

    def reset(self) -> None:
        """重置限流器"""
        with self.lock:
            self.request_times.clear()
            self.last_429_time = None
            self.backoff_until = None
            logger.info("🔄 速率限制器已重置")


class UserAgentRotator:
    """
    User-Agent 輪換器

    模擬不同的瀏覽器，避免被識別為爬蟲
    """

    USER_AGENTS = [
        # Chrome on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',

        # Firefox on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',

        # Edge on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',

        # Safari on Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',

        # Chrome on Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]

    def __init__(self):
        self.current_index = 0
        self.lock = Lock()

    def get_random(self) -> str:
        """獲取隨機 User-Agent"""
        return random.choice(self.USER_AGENTS)

    def get_next(self) -> str:
        """獲取下一個 User-Agent（輪換）"""
        with self.lock:
            ua = self.USER_AGENTS[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.USER_AGENTS)
            return ua


class RetryHandler:
    """
    智能重試處理器

    實現指數退避重試策略
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0
    ):
        """
        初始化重試處理器

        Args:
            max_retries: 最大重試次數
            base_delay: 基礎延遲（秒）
            max_delay: 最大延遲（秒）
            exponential_base: 指數基數
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base

    def execute_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        執行函數並在失敗時重試

        Args:
            func: 要執行的函數
            *args: 函數參數
            **kwargs: 函數關鍵字參數

        Returns:
            函數執行結果

        Raises:
            最後一次失敗的異常
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)

            except Exception as e:
                last_exception = e
                error_code = getattr(e, 'response', None)
                if error_code and hasattr(error_code, 'status_code'):
                    status_code = error_code.status_code
                else:
                    status_code = None

                # 如果是最後一次嘗試，直接拋出異常
                if attempt >= self.max_retries:
                    logger.error(f"❌ 重試 {self.max_retries} 次後仍然失敗")
                    raise last_exception

                # 計算延遲時間（指數退避 + 隨機抖動）
                delay = min(
                    self.base_delay * (self.exponential_base ** attempt),
                    self.max_delay
                )
                jitter = random.uniform(0, delay * 0.1)  # 10% 抖動
                total_delay = delay + jitter

                logger.warning(
                    f"⚠️ 嘗試 {attempt + 1}/{self.max_retries} 失敗 "
                    f"(狀態碼: {status_code})，{total_delay:.1f} 秒後重試..."
                )

                time.sleep(total_delay)

        # 理論上不會到這裡，但為了安全
        raise last_exception


# 全域實例（單例模式）
_rate_limiter = RateLimiter(
    max_requests=5,      # 每分鐘最多 5 次請求
    time_window=60,      # 60 秒視窗
    min_delay=2.0,       # 最小延遲 2 秒
    max_delay=5.0        # 最大延遲 5 秒
)

_user_agent_rotator = UserAgentRotator()
_retry_handler = RetryHandler(max_retries=3)


def get_rate_limiter() -> RateLimiter:
    """獲取全域速率限制器"""
    return _rate_limiter


def get_user_agent_rotator() -> UserAgentRotator:
    """獲取全域 User-Agent 輪換器"""
    return _user_agent_rotator


def get_retry_handler() -> RetryHandler:
    """獲取全域重試處理器"""
    return _retry_handler
