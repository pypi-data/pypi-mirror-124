from logging import getLogger
from logging.config import dictConfig

from setux.core.logger import Logger
from .config import config


dictConfig(config)

logger = Logger(getLogger('setux'))

debug = logger.debug
info = logger.info
error = logger.error
exception = logger.exception

