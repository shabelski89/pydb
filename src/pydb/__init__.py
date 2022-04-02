import os
import sys
from .logger import ShLogger


logger_name = os.path.basename(sys.argv[0].replace(".py", ".log"))
logger = ShLogger(logger_name=logger_name, frmt=ShLogger.FORMATTER)
