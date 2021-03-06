import logging
from datetime import datetime
from pathlib import Path

from termcolor import colored


# Modified from
# https://github.com/facebookresearch/detectron2/blob/master/detectron2/utils/logger.py
class _ColorfulFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super(_ColorfulFormatter, self).__init__(*args, **kwargs)

    def formatMessage(self, record):
        log = super(_ColorfulFormatter, self).formatMessage(record)
        if record.levelno == logging.WARNING:
            prefix = colored("WARNING", "red")
        elif record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            prefix = colored("ERROR", "red", attrs=["underline"])
        else:
            return log
        return prefix + " " + log


def add_time_to_path(logging_filepath):
    logging_filepath = Path(logging_filepath)
    now = datetime.now().strftime('%b%d-%H-%M-%S')
    return logging_filepath.with_name(logging_filepath.stem + '_' + now +
                                      logging_filepath.suffix)


def setup_logging(logging_filepath,
                  logger=logging.root,
                  console_level=logging.INFO,
                  file_level=logging.DEBUG):
    """Setup root logger to log to file and stdout.
    All calls to logging will log to `logging_filepath` as well as stdout.
    Also creates a file logger that only logs to , which can
    be retrieved with logging.getLogger(logging_filepath).
    Args:
        logging_filepath (str): Path to log to.
    """
    if isinstance(logging_filepath, Path):
        logging_filepath = str(logging_filepath)

    log_format = ('%(asctime)s %(filename)s:%(lineno)4d: ' '%(message)s')
    stream_date_format = '%H:%M:%S'
    file_date_format = '%m/%d %H:%M:%S'

    # Clear any previous changes to logging.
    logger.handlers = []
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(logging_filepath)
    file_handler.setFormatter(
        logging.Formatter(log_format, datefmt=file_date_format))
    logger.addHandler(file_handler)
    file_handler.setLevel(file_level)

    # Logger that logs only to file. We could also do this with levels, but
    # this allows logging specific messages regardless of level to the file
    # only (e.g. to save the diff of the current file to the log file).
    file_logger = logging.getLogger(logging_filepath)
    file_logger.addHandler(file_handler)
    file_logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        _ColorfulFormatter(log_format, datefmt=stream_date_format))
    console_handler.setLevel(console_level)
    if logger != logging.root:
        # Remove the default console handler.
        # TODO(achald): Make this more specific. Right now it removes all
        # StreamHandlers, which may not be what we want to do.
        logging.root.handlers = [
            x for x in logging.root.handlers
            if not isinstance(x, logging.StreamHandler)
        ]
    logging.root.addHandler(console_handler)

    logging.info('Writing log file to %s', logging_filepath)
    return file_logger
