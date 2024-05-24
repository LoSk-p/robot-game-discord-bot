import typing as tp
import asyncio

from .config.config import ADDRESSES_WAITING_TIME, NOTIFY_TIMEOUT
from .logger import get_logger

logger = get_logger(__name__)

class GameTimer:
    def __init__(self) -> None:
        self._timeout: int = ADDRESSES_WAITING_TIME
        self._notify_timeout: int = NOTIFY_TIMEOUT
        self._callback: tp.Awaitable = None
        self._task = None
        self.is_running: bool = False

    def start(self, callback: tp.Awaitable):
        logger.info(f"Starting timer on {self._timeout}")
        self._task = asyncio.ensure_future(self._job())
        self._callback = callback

    async def _job(self):
        self.is_running = True
        for i in range(int(self._timeout/self._notify_timeout)):
            await asyncio.sleep(self._notify_timeout)
        self.is_running = False
        logger.info("Timer finished")
        if self._callback is not None:
            await self._callback()

    
    def stop(self):
        logger.info("Timer stopped")
        if self._task is not None:
            self._task.cancel()
        self.is_running = False

