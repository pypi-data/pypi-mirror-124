from pygendata.datatypes import datatypes, special_types
from pygendata.exceptions import TypeNotSupportedError

import re

class DDL:
    def __init__(self, statement):
        self.statement = statement
        self.columns = []
        self.column_data = [] # {'name': <column_name>, 'type': <column_type> }
        self.headers = []

    @property
    def column_data(self):
        return self._column_data
    
    @column_data.setter
    def column_data(self, column_data):
        self._column_data = column_data
    
    def get_columns(self):
        _, *cols = self.statement.split('\n')
        cols = [x.rstrip(',') for x in cols]
        cols = [x for x in cols if x != ');'] # remove );
        cols = list(filter(None, cols)) # remove empty strings
        self.columns = cols
    
    def create_headers(self):
        for column in self.columns:
            name, *_ = column.split(' ')
            self.headers.append(name)

    def create_row(self, current_row):
        c = {}
        for column in self.columns:
            name, *type_info = column.split(' ')
            type_info = ''.join(type_info)
            if type_info in datatypes:
                # is name special?
                patterns = re.compile(r'(email)|(name)', re.IGNORECASE)
                matches = patterns.match(name)
                id_pattern = re.compile(r'(id)', re.IGNORECASE)
                id_matches = id_pattern.match(name)
                if matches:
                    c[name] = special_types[name.upper()]()
                elif id_matches:
                    c[name] = current_row
                else:
                    c[name] = datatypes[type_info]() # expensive
            else:
                raise TypeNotSupportedError(f"{c['type']} is not currently supported")
        return c