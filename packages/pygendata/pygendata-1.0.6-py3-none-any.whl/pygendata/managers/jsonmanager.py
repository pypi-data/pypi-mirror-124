import json
from json.decoder import JSONDecodeError
import logging
from tqdm import tqdm

class JSONManager:
    def __init__(self):
        self.headers = []
        self.rows = []
    
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
                data = f.read()
                json_data =json.load(data)
                return json_data
        except JSONDecodeError as e:
            logging.warning(str(e))
    
    def write(self, file):
        try:
            write_data = {"rows": []}
            with open(file, 'w+') as f:
                # json will always write a key with an array as a value like so {"rows": [....]}
                print('Writing rows to JSON file')
                for row in tqdm(self.rows):
                    write_data['rows'].append(row)
                f.write(json.dumps(write_data))
        except IOError as e:
            logging.warning(str(e))
        