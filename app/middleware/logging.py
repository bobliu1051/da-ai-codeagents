"""
Request logging middleware.
"""
import time
import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start = time.time()
        path = environ.get("PATH_INFO", "")
        method = environ.get("REQUEST_METHOD", "")

        def custom_start(status, headers, exc_info=None):
            duration = (time.time() - start) * 1000
            logger.info(f"{method} {path} {status} {duration:.1f}ms")
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start)
