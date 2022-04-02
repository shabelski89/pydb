import os
import csv
from datetime import datetime
from .dbms import ExecutionResponse


class Exporter:
    """
    Class to Export data from DataBase.
    """
    def __init__(self, filename: str):
        """
        :param filename: Filename to exported data.
        """
        self.filename = f'{os.path.splitext(filename)[0]}_{datetime.today().strftime("%d%m%Y_%H%M")}.csv'
        self.line_count = 0

    def to_csv(self, data: list):
        """
        Write data to CSV file
        :param data: instance of ExecutionResponse to save in file
        """
        with open(self.filename, "a", encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
            for row in data:
                writer.writerow(row)
        self.line_count = len(data)

    def to_csv_er(self, data: ExecutionResponse):
        """
        Write data to CSV file
        :param data: instance of ExecutionResponse to save in file
        """
        file_exist = False
        if os.path.isfile(self.filename):
            file_exist = True

        with open(self.filename, "a", encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
            if not file_exist:
                writer.writerow(data.header)
            for row in data.result:
                writer.writerow(row)
                self.line_count += 1
