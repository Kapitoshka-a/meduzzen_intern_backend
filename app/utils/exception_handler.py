import logging
from functools import wraps
from fastapi import HTTPException

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def handle_exceptions():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException as http_exc:
                raise http_exc
            except Exception as e:
                logger.exception(f"An exception occurred: {e}")
                raise HTTPException(status_code=500, detail="Internal Server Error")

        return wrapper

    return decorator
