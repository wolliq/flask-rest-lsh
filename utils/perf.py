import time
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
logger = logging.getLogger(__name__)


def st_time(func):
    """
        st decorator to calculate the total time of a func
    :param func:
    :return:
    """
    def st_func(*args, **kwargs):
        t1 = time.time()
        r = func(*args, **kwargs)
        t2 = time.time()
        logging.warning("Function=%s, Time=%s" % (func.__name__, t2 - t1))
        return r

    return st_func
