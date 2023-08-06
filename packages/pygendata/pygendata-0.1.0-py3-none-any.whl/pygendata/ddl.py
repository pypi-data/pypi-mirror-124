from pygendata.datatypes import datatypes
from pygendata.exceptions import TypeNotSupportedError

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

    def create_row(self):
        c = {}
        for column in self.columns:
            name, *type_info = column.split(' ')
            type_info = ''.join(type_info)
            if type_info in datatypes:
                c[name] = datatypes[type_info]
            else:
                raise TypeNotSupportedError(f"{c['type']} is not currently supported")
        self.column_data.append(c)
    
    def process(self):
        self.get_columns()
        self.get_column_types()