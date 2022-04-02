import gzip
import os
import shutil
from . import logger


class Zip:
    """
    Class to compress and decompress files.
    """
    def __init__(self, filename):
        self.filename = filename
        logger.debug(self.filename)

    def compress(self, output=None):
        """
        Return file with gz compress
        :param output: filename to compress data.
        """
        if output is not None:
            output_filename = output
        else:
            output_filename = f'{self.filename}.gz'
            logger.debug(output_filename)

        with open(self.filename, "rb") as input_file:
            with gzip.open(output_filename, "wb") as output_file:
                shutil.copyfileobj(input_file, output_file)
        result = {self.filename: os.stat(self.filename).st_size, output_filename: os.stat(output_filename).st_size}
        logger.debug(result)
        return result

    def decompress(self):
        """
        Return file with gz decompress
        """
        try:
            output_filename = self.filename[:-3]
            logger.debug(output_filename)

            with open(output_filename, "wb") as output_file:
                with gzip.open(self.filename, "rb") as input_file:
                    shutil.copyfileobj(input_file, output_file)
            result = {self.filename: os.stat(self.filename).st_size, output_filename: os.stat(output_filename).st_size}
            return result
        except Exception as Error:
            logger.exception(Error)
