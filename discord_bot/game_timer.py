import asyncio
import typing as tp

from .config.config import ADDRESSES_WAITING_TIME
from .logger import get_logger

logger = get_logger(__name__)

SECONDS_IN_MINUTE = 60


class GameTimer:
    def __init__(self) -> None:
        self._timeout: int = ADDRESSES_WAITING_TIME
        self._timeout_in_minutes: int = int(self._timeout / SECONDS_IN_MINUTE)
        self._callback: tp.Awaitable = None
        self._task = None
        self.is_running: bool = False

    def start(self, callback: tp.Awaitable):
        logger.info(f"Starting timer on {self._timeout}")
        self._task = asyncio.ensure_future(self._job())
        self._callback = callback

    async def _job(self):
        self.is_running = True
        for minute in range(self._timeout_in_minutes):
            await asyncio.sleep(SECONDS_IN_MINUTE)
            if self._callback is not None:
                minutes_gone = minute + 1
                left_minutes: int = self._timeout_in_minutes - minutes_gone
                await self._callback(left_minutes)
        self.is_running = False
        logger.info("Timer finished")

    def stop(self):
        logger.info("Timer stopped")
        if self._task is not None:
            self._task.cancel()
        self.is_running = False
