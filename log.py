import time
from loguru import logger
from config import LOG_PATH
from sql import insert_log
from pathlib import Path


def log_block(addr, result):
    Format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | <level>{message}</level>"
    current_path = Path.cwd()
    path = Path(current_path, LOG_PATH)
    if not path.exists():
        path.mkdir(parents=True)
    filename = time.strftime("%Y-%m-%d", time.localtime()) + '.log'
    logfile = Path(path, filename)
    insert_log(str(logfile))
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
