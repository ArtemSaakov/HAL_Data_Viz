import requests
import json

class CensusData:
    """
        a class to manage the census data used for the project.

        parameters
        ------------------------------

        cachefile (optional): specify a file to pull cached data from

        attributes
        ------------------------------

        self.data: the data from the census API
        """
    def __init__(self, cachefile=None):
        self.data = []
        self.cachefile = self.loadCache(cachefile)

    def fetchCensus(self):

        """
        Fetches the census tract for each district in the list of districts using the FCC API.

        This method iterates over the all districts in `self.districts`, retrieves the census tract
        for each district based on its random latitude and longitude, and updates the district's
        `censusTract` attribute.

        Note
        ----
        The method fetches data from "https://geo.fcc.gov/api/census/area" and assumes that
        `randomLat` and `randomLong` attributes of each district are already set.

        The function `fetch` is an internal helper function that performs the actual API request.

        In the api call, check if the response.status_code is 200.
        If not, it might indicate the api call made is not correct, check your api call parameters.

        If you get status_code 200 and other code alternativly, it could indicate the fcc webiste is not
        stable. Using a while loop to make anther api request in fetch function, until you get the correct result.

        Important
        -----------
        The order of the API call parameter has to follow the following.
        'lat': xxx,'lon': xxx,'censusYear': xxx,'format': 'json' Or
        'lat': xxx,'lon': xxx,'censusYear': xxx

        """
        for district in self.districts:
            lat = district.randomLat
            lon = district.randomLong
            params = {'lat': lat, 'lon': lon, 'censusYear': '2010'}
            def fetch():
                while True:
                    resp = requests.get('https://geo.fcc.gov/api/census/area', params)
                    if resp.status_code == 200:
                        return resp.json()
                    else:
                        print(f"Error: status_code {resp.status_code}")
            resp = fetch()
            district.censusTract = resp['results'][0]['block_fips'][2:-4]

    def cacheData(self, fileName):
        """
        saves the current state of census data to a file in JSON format.

        parameters
        ------------------------------
        fileName: the name of the file where the district data will be saved.

        returns
        ------------------------------

        none
        """
        cacheList = []
        for i in self.data:
            cacheList.append(i.__dict__)
        with open(fileName, 'w') as f:
            f.write(json.dumps(cacheList, indent=2))

    def loadCache(self, fileName):
        """
        loads census data from a cache JSON file if it exists.

        parameters
        ------------------------------

        fileName: the name of the file from which to load the district data.

        returns
        ------------------------------

        bool: True if the data was successfully loaded, False otherwise.
        """
        try:
            with open(fileName, 'r') as f:
                d = json.load(f)
                self.data = [CensusData(**i) for i in d]
                return True
        except:
            return False