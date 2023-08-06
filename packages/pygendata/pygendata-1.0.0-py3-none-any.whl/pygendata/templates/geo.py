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
        self.keys = ['Latitude', 'Longitude']
        self.values = []
    
    def allowed_region(self, region):
        if region not in self._allowed_regions:
            return False
        return True
    
    def generate(self, rows):
        for _ in range(rows):
            coordinates = self.fake.local_latlng(country_code=self.region, coords_only=True)
            self.values.append(coordinates)
        self.values = list(map(lambda x: { 'Latitude': x[0], 'Longitude': x[1] }, self.values))
