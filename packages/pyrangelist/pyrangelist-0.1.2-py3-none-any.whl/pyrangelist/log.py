import logging


LOGGER = logging.getLogger("pyrangelist")


def configure_logger(verbose=False):
    formatter_pre = (
        "[%(asctime)s.%(msecs)03d, pid%(process)6s, %(filename)20s:%(lineno)4d] "
    )
    formatter_post = "%(levelname)6s - %(message)s"
    formatter_time = "%m-%d %H:%M:%S"

    LOGGER.handlers = []
    log_level = logging.DEBUG if verbose else logging.INFO
    LOGGER.setLevel(log_level)

    log_handler = logging.StreamHandler()
    log_handler.setLevel(log_level)

    # Pre and post are split in case we want to extend with prefix
    # in the future
    this_layout = f"{formatter_pre}{formatter_post}"
    formatter = logging.Formatter(this_layout, formatter_time)
    log_handler.setFormatter(formatter)
    LOGGER.addHandler(log_handler)
