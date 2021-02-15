from os import mkdir
from loguru import logger
from config import LOG_PATH
from pathlib import Path


def log_block(addr, result):
    Format = "<green>{time:YYYY-MM-DD  HH:mm:ss}</green> | {level} | <level>{message}</level>"
    path = Path(LOG_PATH)
    if not path.exists():
        path.mkdir(parents=True)
    log_name = Path(path, '{time:YYYY-MM-DD}.log')

    i = logger.add(log_name,
               rotation="00:00",
               retention="30 days",
               level="SUCCESS",
               enqueue=True,
               format=Format
               )
    if result["status"] == True:
        logger.warning("{type} | {addr} | {url}", addr=addr, type=result["type"], url=result["url"])
    elif result["status"] == False:
        logger.success("pass | {type} | {url}", addr=addr, url=result["url"])
    logger.remove(i)
