import logging
import sys
import threading
import time
import traceback

logger = logging.getLogger(__name__)


def debug_threads(wait_time: float = 1):
    """
    A utility to help debug issues where a hanging thread is preventing a process from exiting.

    It's most useful to call this at the end of a test, where it will print out the stack trace of all running threads.
    """

    logger.info("\nCurrent threads:")
    time.sleep(wait_time)

    for thread in threading.enumerate():
        if not thread.ident:
            continue
        logger.info(f"\nThread {thread.name} ({thread.ident}):")
        frame = sys._current_frames().get(thread.ident)
        if frame:
            traceback.print_stack(frame)
