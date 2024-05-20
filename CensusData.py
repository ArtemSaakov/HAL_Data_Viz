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

    def __init__(self, state=None, county=None, totalLynchings=None, medianIncome=None, blackPopulation=None, hispanicPopulation=None, whitePopulation=None, totalPopulation=None):
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

    def fetchCensus(self, counties):

        """
        fetches census data fr each county in the data list.


        """
        censusCallResponse =  {}
        for state in counties.keys():
            state = self._stateToFIPS(state)
            params = {'in': f'state:{state}', 'key': 'f1d963997c02d4fc8721f64ff181dd2ade46245b', 'for': 'county:*'}
            resp = requests.get('https://api.census.gov/data/2018/acs/acs5?get=B01003_001E,B19013_001E,B03002_001E,B03002_003E,B03002_004E,B03002_012E', params=params)
            if resp.status_code != 200:
                print(f"Error: status_code {resp.status_code}")
                return
            censusCallResponse[state] = resp.json()
        self.cacheData('data/censusCallResponse.json', censusCallResponse)


    def _stateToFIPS(self, state):
        with open('data/states.json', 'r') as f:
            states = json.load(f)
            return states[state]

    def cacheData(self, fileName, data):
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
        for i in data:
            cacheList.append(i.__dict__)
        with open(fileName, 'w') as f:
            f.write(json.dumps(cacheList, indent=2))

    def loadCache(self, fileName):
        """
        loads census data from a cache JSON file if it exists.
        only works for

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