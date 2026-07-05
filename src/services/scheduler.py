"""Background scheduler for automated tasks."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class Task:
    """Represents a scheduled task."""

    def __init__(
        self,
        name: str,
        callback: Callable,
        interval: int,
        initial_delay: int = 0,
    ):
        """Initialize task.
        
        Args:
            name: Task name
            callback: Async callback function
            interval: Interval in seconds
            initial_delay: Initial delay before first execution in seconds
        """
        self.name = name
        self.callback = callback
        self.interval = interval
        self.initial_delay = initial_delay
        self.running = False
        self.task: Optional[asyncio.Task] = None
        self.last_run: Optional[datetime] = None

    async def start(self) -> None:
        """Start task execution."""
        self.running = True
        self.task = asyncio.create_task(self._run())
        logger.info(f"Task started: {self.name}")

    async def stop(self) -> None:
        """Stop task execution."""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info(f"Task stopped: {self.name}")

    async def _run(self) -> None:
        """Internal task runner loop."""
        if self.initial_delay > 0:
            await asyncio.sleep(self.initial_delay)

        while self.running:
            try:
                logger.debug(f"Executing task: {self.name}")
                await self.callback()
                self.last_run = datetime.now(timezone.utc)
                logger.debug(f"Task completed: {self.name}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Task error ({self.name}): {e}", exc_info=True)

            await asyncio.sleep(self.interval)


class Scheduler:
    """Background task scheduler."""

    def __init__(self):
        """Initialize scheduler."""
        self.tasks: dict[str, Task] = {}
        self.running = False

    def add_task(
        self,
        name: str,
        callback: Callable,
        interval: int,
        initial_delay: int = 0,
    ) -> None:
        """Add a task to the scheduler.
        
        Args:
            name: Task name
            callback: Async callback function
            interval: Interval in seconds
            initial_delay: Initial delay before first execution
        """
        if name in self.tasks:
            logger.warning(f"Task already exists: {name}")
            return

        task = Task(name, callback, interval, initial_delay)
        self.tasks[name] = task
        logger.info(f"Task added: {name}")

    async def start(self) -> None:
        """Start all tasks."""
        self.running = True
        for task in self.tasks.values():
            await task.start()
        logger.info("Scheduler started")

    async def stop(self) -> None:
        """Stop all tasks."""
        self.running = False
        for task in self.tasks.values():
            await task.stop()
        logger.info("Scheduler stopped")

    async def remove_task(self, name: str) -> None:
        """Remove and stop a task.
        
        Args:
            name: Task name
        """
        if name not in self.tasks:
            logger.warning(f"Task not found: {name}")
            return

        task = self.tasks[name]
        await task.stop()
        del self.tasks[name]
        logger.info(f"Task removed: {name}")
