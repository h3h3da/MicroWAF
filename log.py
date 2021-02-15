import time
import pathlib
from loguru import logger
from config import LOG_PATH
from sql import insert_log


def log_block(addr, result):
    Format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | <level>{message}</level>"
    path = pathlib.Path(LOG_PATH)
    if not path.exists():
        path.mkdir(parents=True)
    filename = time.strftime("%Y-%m-%d", time.localtime()) + '.log'
    logfile = pathlib.Path(path, filename)
    insert_log(logfile)
    i = logger.add(logfile,
               rotation="00:00",
               retention="30 days",
               level="SUCCESS",
               enqueue=True,
               format=Format
               )
    if result["status"] == True:
        logger.warning("{type} | {addr} | {url}", addr=addr, type=result["type"], url=result["url"])
    elif result["status"] == False:
        logger.success("pass | {addr} | {url}", addr=addr, url=result["url"])
    logger.remove(i)
