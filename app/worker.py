"""
后台 Worker 入口

按配置启动 scheduler 和 queue consumer。默认不启用任何后台角色，避免 API 进程隐式执行后台任务。
"""

from __future__ import annotations

import asyncio
import os
import signal
import socket

from app.config.settings import settings
from app.core.logging import logger, setup_logging
from app.db.postgres import close_db, get_session_factory, init_db
from app.db.redis import close_redis, get_redis, init_redis
from app.queue import ConsumerManager, ExampleConsumer

CONSUMER_REGISTRY = {
    "example": ExampleConsumer,
}


def _get_instance_id() -> str:
    """获取当前 worker 实例 ID。"""
    if settings.WORKER_INSTANCE_ID:
        return settings.WORKER_INSTANCE_ID
    return f"{socket.gethostname()}-{os.getpid()}"


def _has_enabled_role() -> bool:
    """判断是否启用了任意后台角色。"""
    return settings.SCHEDULER_ENABLED or settings.QUEUE_WORKER_ENABLED


async def _start_scheduler() -> None:
    """按配置启动定时任务调度器。"""
    if not settings.SCHEDULER_ENABLED:
        logger.info("Scheduler worker disabled")
        return

    from app.scheduler import init_scheduler, load_jobs, start_scheduler

    init_scheduler()
    loaded_count = load_jobs(only_enabled=settings.SCHEDULER_LOAD_ONLY_ENABLED_JOBS)
    if loaded_count == 0:
        logger.warning("Scheduler enabled but no jobs loaded")
    start_scheduler()
    logger.info(f"Scheduler worker started, loaded jobs: {loaded_count}")


async def _start_queue_worker(instance_id: str) -> ConsumerManager:
    """按配置启动 Redis Streams 消费者。"""
    manager = ConsumerManager.get_instance()
    if not settings.QUEUE_WORKER_ENABLED:
        logger.info("Queue worker disabled")
        return manager

    redis = get_redis()
    session_factory = get_session_factory()
    for consumer_name in settings.QUEUE_WORKER_CONSUMERS:
        consumer_class = CONSUMER_REGISTRY.get(consumer_name)
        if consumer_class is None:
            raise ValueError(f"未知队列消费者: {consumer_name}")
        manager.register(consumer_class(redis, session_factory, instance_id=instance_id))

    await manager.start_all()
    logger.info(f"Queue worker started, consumers: {settings.QUEUE_WORKER_CONSUMERS}")
    return manager


def _install_signal_handlers(stop_event: asyncio.Event) -> None:
    """安装退出信号处理器。"""
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)


async def _shutdown(manager: ConsumerManager) -> None:
    """关闭后台角色和基础设施连接。"""
    try:
        await asyncio.wait_for(manager.stop_all(), timeout=settings.WORKER_SHUTDOWN_TIMEOUT_SECONDS)
    except TimeoutError:
        logger.warning("Queue worker shutdown timed out")

    if settings.SCHEDULER_ENABLED:
        from app.scheduler import stop_scheduler

        stop_scheduler(wait=True)
    await close_redis()
    await close_db()
    logger.info("Worker stopped")


async def run_worker() -> None:
    """启动后台 worker。"""
    setup_logging()
    if not _has_enabled_role():
        logger.warning("No worker role enabled; set SCHEDULER_ENABLED or QUEUE_WORKER_ENABLED to true")
        return

    await init_db()
    await init_redis()

    instance_id = _get_instance_id()
    logger.info(f"Worker starting, instance_id={instance_id}")

    stop_event = asyncio.Event()
    _install_signal_handlers(stop_event)

    manager = await _start_queue_worker(instance_id)
    await _start_scheduler()

    logger.info("Worker started")
    try:
        await stop_event.wait()
    finally:
        await _shutdown(manager)


def main() -> None:
    """命令行入口。"""
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
