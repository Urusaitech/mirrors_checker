import logging
import time

from proxy_connect_async import main
from logger_setup import setup_logger
from typing import Callable

logger = setup_logger('timer', 'timer.log', level=logging.DEBUG)


def timer() -> Callable:
    """
    Keeps itself alive, runs checks once a day
    :return:
    """
    logger.debug("entering timer")
    curr = int(str(time.asctime())[11:13])  # current hour
    logger.debug("starting a cycle")
    print("starting a cycle")
    while curr:
        if 8 < curr < 17:  # working hours from 9 to 18, ~1 hour to check required
            print("Launching a check")
            logger.debug("main()")
            try:
                main()
                logger.debug("main() worked out")
            except Exception as e:
                print(e)
                logger.error(f"error in main(): {e}")
                # send_crush_report(e)
                logger.debug("report sent")
            finally:
                logger.debug("sleeping till the next cycle")
                print("sleeping till the next cycle")
                time.sleep(60 * 60 * (18 - curr))
        else:
            print("not a time!")
            logger.debug("waiting for a working time")
            time.sleep(60 * 60)
    print("something went wrong")
    logger.error("something went wrong")
    # send_crush_report("crushed in timer")
    logger.error("sent crush report, retrying")
    return timer()


if __name__ == "__main__":
    logger.debug("first start")
    timer()
