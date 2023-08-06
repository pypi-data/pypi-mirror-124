import csv
import logging
from tqdm import tqdm

class CSVManager:
    def __init__(self, headers=None, rows=None):
        self.headers = headers
        self.rows = rows
    
    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers = headers

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows):
        self._rows = rows

    def read(self, file):
        try:
             with open(file, 'r') as f:
                statement  = f.read()
                return statement
        except IOError as e:
            logging.warning(str(e))
    
    def write(self, file):
        try:
            with open(file, 'w+') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.headers)
                writer.writeheader()
                print('Writing rows to csv file')
                for row in tqdm(self.rows):
                    writer.writerow(row)
        except Exception as e:
            logging.warn(str(e))
    
    def __eq__(self, other):
        if not isinstance(other, CSVManager):
            return NotImplemented
        return self.headers == other.headers and self.rows == other.rows
            