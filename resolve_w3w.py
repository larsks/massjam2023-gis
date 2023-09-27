import sys
import requests
import csv
import dotenv
import json


class Resolver:
    '''A caching wrapper for the what3words API.

    Contraryto the what3words documentation, it appears to be possible to access
    the API (at least the convert-to-coordinates route) without a valid API key.
    '''

    url = "https://mapapi.what3words.com/api/convert-to-coordinates"

    def __init__(self, cache=None, apikey=None):
        self.cache_path = cache or ".resolver_cache"
        self.apikey = apikey

        try:
            with open(self.cache_path) as fd:
                self.cache = json.load(fd)
        except OSError:
            self.cache = {}

    def resolve(self, words):
        if words not in self.cache:
            params = {'words': words}
            if self.apikey is not None:
                params['key'] = self.apikey
            res = requests.get(self.url, params=params)
            res.raise_for_status()
            self.cache[words] = res.json()

        return self.cache[words]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        with open(self.cache_path, "w") as fd:
            json.dump(self.cache, fd)


with Resolver() as resolver:
    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, reader.fieldnames + ["Lat", "Lng"], lineterminator='\n')
    writer.writeheader()
    for row in reader:
        res = resolver.resolve(row["What3Words"])
        if "coordinates" in res:
            row["Lat"] = res["coordinates"]["lat"]
            row["Lng"] = res["coordinates"]["lng"]
            writer.writerow(row)
        else:
            print(f"missing coordinates in response: {row['What3Words']}: {res}")
