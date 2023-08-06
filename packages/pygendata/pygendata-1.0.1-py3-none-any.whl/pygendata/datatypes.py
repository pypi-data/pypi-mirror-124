from faker import Faker

fake = Faker()

# Point, Polygon, and Multipolygon currently not supported
datatypes = {
    'BIGINT': fake.pyint,
    'TIMESTAMP(0)': fake.date_time,
    'INTEGER': fake.pyint,
    'TEXTENCODINGDICT(32)': fake.pystr,
    'FLOAT': fake.pyfloat,
    'SMALLINT': fake.pyint,
    'BIGINTENCODINGFIXED(8)': fake.pyint,
    'BIGINTENCODINGFIXED(16)': fake.pyint,
    'BIGINTENCODINGFIXED(32)': fake.pyint,
    'BOOLEAN': True,
    'DATE[1]': fake.date,
    'DATEENCODINGFIXED(16)': fake.date_time,
    'DATEENCODINGFIXED(32)': fake.date_time,
    'DECIMAL': fake.pyfloat,
    'DOUBLE': fake.pyfloat,
    'EPOCH': fake.date_time,
    'FLOAT': fake.pyfloat,
    'INTEGERENCODINGFIXED(8)': fake.pyint,
    'INTEGERENCODINGFIXED(16)': fake.pyint,
    'SMALLINTENCODINGFIXED(8)': fake.pyint,
    'TEXTENCODINGDICT(8)': fake.pystr,
    'TEXTENCODINGDICT(16)': fake.pystr,
    'TEXTENCODINGNONE)': fake.pystr,
    'TIME': fake.date_time(),
    'TIMEENCODINGFIXED(32)': fake.date_time,
    'TIMESTAMP(3)': fake.date_time,
    'TIMESTAMP(6)': fake.date_time,
    'TIMESTAMP(9)': fake.date_time,
    'TIMESTAMPENCODINGFIXED(32)': fake.date_time,
    'TINYINT': fake.pyint
}

# we match on special types to make the data more realistic
special_types = {
    'EMAIL': fake.email,
    'NAME': fake.name,
}