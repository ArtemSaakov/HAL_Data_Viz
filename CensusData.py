import requests
import json
import csv

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

    def __init__(self, state=None, county=None, totalLynchings=None, medianIncome=None, blackPopulation=None, hispanicPopulation=None, whitePopulation=None, totalPopulation=None, povertyLevel=None):
        self.state = state
        self.county = county
        self.totalLynchings = totalLynchings
        self.medianIncome = medianIncome
        self.blackPopulation = blackPopulation
        self.hispanicPopulation = hispanicPopulation
        self.whitePopulation = whitePopulation
        self.totalPopulation = totalPopulation
        self.povertyLevel = povertyLevel

    def __str__(self):
        return  (
f"""
State: {self.state}
County: {self.county}
Total Lynchings: {self.totalLynchings}
Median Income: {self.medianIncome}
Black Population: {self.blackPopulation}
Hispanic Population: {self.hispanicPopulation}
White Population: {self.whitePopulation}
Total Population: {self.totalPopulation}
Population below poverty level: {self.povertyLevel}
"""
)
    __repr__ = __str__


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
    def __init__(self, cacheFile=None):
        self.data = []
        if cacheFile:
            self.loadCountiesCache(cacheFile)

    def createCountyInstances(self, countyData, censusCallData):
        """
        creates an instance of the Counties class for each county in the data list.

        parameters
        ------------------------------

        countyData: the data list to be used to create the instances.

        returns
        ------------------------------

        none
        """
        with open(censusCallData, 'r') as f:
            censusCallData = json.load(f)[0]

        for state in countyData.keys():
            for county in countyData[state]:
                stateFIPS = self._stateToFIPS(state)
                countyFIPS = self._countyToFIPS(stateFIPS, county)
                for i in censusCallData[stateFIPS]:
                    if i[7] == countyFIPS:
                        self.data.append(Counties(state=state, county=county, totalLynchings=countyData[state][county], totalPopulation=i[0], medianIncome=i[1], hispanicPopulation=i[4], whitePopulation=i[2], blackPopulation=i[3], povertyLevel=i[5]))
                        break

    def fetchCensus(self, counties):
        """
        fetches census data for each county in each state in the data list, then caches it.

        parameters
        ------------------------------

        counties: the data list to be used to fetch the census data.

        returns
        ------------------------------

        none
        """
        censusCallResponse =  {}
        for state in counties.keys():
            state = self._stateToFIPS(state)
            params = {'in': f'state:{state}', 'key': 'f1d963997c02d4fc8721f64ff181dd2ade46245b', 'for': 'county:*'}
            resp = requests.get('https://api.census.gov/data/2022/acs/acs5?get=B01003_001E,B19013_001E,B03002_003E,B03002_004E,B03002_012E,B17001_002E', params=params)
            if resp.status_code != 200:
                print(f"Error: status_code {resp.status_code}")
                return
            censusCallResponse[state] = resp.json()
        self.cacheData('data/censusCallResponse.json', [censusCallResponse])


    def _stateToFIPS(self, state):
        with open('data/stateCodeToFips.json', 'r') as f:
            states = json.load(f)
            return states[state]

    def _countyToFIPS(self, state, county):
        with open('data/US_FIPS_Codes.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for line in reader:
                if line['FIPS State'] == state and line['County Name'] == county:
                    return line['FIPS County']

    def cacheData(self, fileName, data):
        """
        tries to save the current state of a class object's data to a file in JSON format.
        otherwise dumps data in JSON format.

        parameters
        ------------------------------
        fileName: the name of the file where the district data will be saved.
        data: the data to be saved. expects a list of dictionaries.

        returns
        ------------------------------

        none
        """
        try:
            cacheList = []
            for i in data:
                cacheList.append(i.__dict__)
            with open(fileName, 'w') as f:
                f.write(json.dumps(cacheList, indent=2))
        except:
            with open(fileName, 'w') as f:
                f.write(json.dumps(data, indent=2))

    def loadCountiesCache(self, fileName):
        """
        loads census data from a cache JSON file if it exists.
        only works for class objects.

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
                self.data = [Counties(**i) for i in d]
                return True
        except:
            return False

if __name__ == "__main__":
    pass