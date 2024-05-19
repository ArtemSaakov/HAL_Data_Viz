import requests
import json

class Counties:
    """
    represents the statistics tracked for each county based on the counties in the data tree.

    census data pulled is for the year 2022

    parameters
    ------------------------------

    state: the state in which the county is located
    county: the county for which the statistics are being tracked
    totalLynchings: the total number of lynchings in the county
    medianIncome: the median income in the county from the census data
    blackPopulation: the black population in the county from the census data
    hispanicPopulation: the hispanic population in the county from the census data
    whitePopulation: the white population in the county from the census data
    totalPopulation: the total population in the county from the census data

    attributes
    ------------------------------

    self.state: the state in which the county is located
    self.county: the county for which the statistics are being tracked
    self.totalLynchings: the total number of lynchings in the county
    self.medianIncome: the median income in the county from the census data
    self.blackPopulation: the black population in the county from the census data
    self.hispanicPopulation: the hispanic population in the county from the census data
    self.whitePopulation: the white population in the county from the census data
    self.totalPopulation: the total population in the county from the census data
    """

    def __init__(self, state, county, totalLynchings, medianIncome, blackPopulation, hispanicPopulation, whitePopulation, totalPopulation):
        self.state = state
        self.county = county
        self.totalLynchings = totalLynchings
        self.medianIncome = medianIncome
        self.blackPopulation = blackPopulation
        self.hispanicPopulation = hispanicPopulation
        self.whitePopulation = whitePopulation
        self.totalPopulation = totalPopulation

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
        params = {'in': 'state:26', 'key': '', 'for': 'tract:*'}
        resp = requests.get('https://api.census.gov/data/2018/acs/acs5?get=B19013_001E', params=params)
        if resp.status_code != 200:
            print(f"Error: status_code {resp.status_code}")
            return
        resp = resp.json()
        tract_to_income = {j[2]+j[3]: j[0] for j in resp}
        for district in self.districts:
            if int(tract_to_income.get(district.censusTract)) > 0 and tract_to_income.get(district.censusTract):
                district.medIncome = int(tract_to_income.get(district.censusTract))
            else:
                district.medIncome = 0
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

if __name__ == "__main__":
    pass