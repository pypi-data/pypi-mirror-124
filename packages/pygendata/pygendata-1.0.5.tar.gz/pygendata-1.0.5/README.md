# Pygendata

`pygendata` is a python library for generating test data from files (csv, tsv, ddl, json) or extending the libraries built in `template` system
to generate data

# Installation
To install pygendata you can use your favorite python package installer
```
pip install pygendata
```

The `pygendata` command automatically gets added to your path when you do pip install

To test if the installation worked correctly you can use the python repl and try importing the package
```
python

import pygendata
```

# Templates
`pygendata` has the concept of a template, a template should be just that, a template for you do generate data

`pygendata` provides a `GeoTemplate` object that generates a list of `latitude/longitude` points

```
from faker import Faker

class GeoTemplate:
    """
    A geo template generates Lat/Lon values particular to a specified region
    """

    # TODO: support more regions
    _allowed_regions = {'US': True, 'GB': True}

    def __init__(self, region):
        self.fake = Faker()
        if self.allowed_region(region):
            self.region = region
        else:
            self.region = 'US' # defaults to US
        self.keys = ['latitude', 'longitude']
        self.values = []
    
    def allowed_region(self, region):
        if region not in self._allowed_regions:
            return False
        return True
    
    def generate(self, row):
        latitude, longitude = self.fake.local_latlng(country_code=self.region, coords_only=True)
        return { 'latitude': latitude, 'longitude': longitude }
```

You can use the `pygendata` command to generate a JSON file with these values
```
pygendata --generate json --template geo US --to us_lat_lon.json --rows 1000000
```

An output file with 1000000 `lat/long` points should be created

Every json file has the key `"rows": [....]`

# Example Usage
Generating data from a DDL file to a CSV

1. Create a DDL File `users.txt`
```
create table users (
id INTEGER,
name TEXT ENCODING DICT(32),
email TEXT ENCODING DICT(32),
password TEXT ENCODING DICT(32)
);
```

2. Run the pygendata command
```
pygdendata --generate csv --base ddl users.txt --to users.csv --rows 1000000
```

3. You should now have a users.csv file in your current working directory with 1million users