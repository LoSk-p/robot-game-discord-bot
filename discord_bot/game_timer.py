import typing as tp
import asyncio

from .config.config import ADDRESSES_WAITING_TIME

class GameTimer:
    def __init__(self) -> None:
        self._timeout: int = ADDRESSES_WAITING_TIME
        self._callback: tp.Awaitable = None
        self._task = None
        self.is_running: bool = False

    def start(self, callback: tp.Awaitable):
        self._task = asyncio.ensure_future(self._job())
        self._callback = callback

    async def _job(self):
        self.is_running = True
        await asyncio.sleep(self._timeout)
        if self._callback is not None:
            await self._callback()
        self.is_running = False
    
    def stop(self):
        if self._task is not None:
            self._task.cancel()
        self.is_running = False

