import csv
import pprint
import datetime as dt

pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=100)

class HALData:
    """
    a class representing an instance of lynching.

    parameters
    ------------------------------

    state: state where the lynching occurred
    month (optional): month the lynching occurred
    day (optional): day the lynching occurred
    victim (optional): the victim that was lynched
    county (optional): county the lynching occurred in
    race (optional): the lynching victim's race
    sex (optional): the lynching victim's sex
    offense (optinoal): the perceived offense the victim committed

    attributes
    ------------------------------

    self.state: state where lynching occurred
    self.date: date the lynching occurred
    self.victimName: lynching victim's name
    self.victimSex: victim's sex
    self.allegedOffense: victim's alleged offense
    """

    def __init__(self, state, year=None, month=0, day=0, victim=None, county=None, race=None, sex=None, offense=None):
        # checks to see if month or day is valid in order
        # to properly call datetime function
        if month.isnumeric() and month != 0:
            month = int(month)
        else:
            month = 1
        if day.isnumeric() and day != 0:
            day = int(day)
        else:
            day = 1
        self.state = state
        self.date = dt.date(int(year), month, day)
        self.victimName = victim
        self.county = county
        self.victimRace = race
        self.victimSex = sex
        self.allegedOffense  = offense

    def __str__(self) -> str:
        return f"""
State: {self.state}
Date: {self.date}
Victim Name: {self.victimName}
County: {self.county}
Victim Race: {self.victimRace}
Victim Sex: {self.victimSex}
Alleged Offense: {self.allegedOffense}
"""
class CensusData:

    def __init__(self):
        pass

class Node:

    def __init__(self, data=None):
        self.data = data
        self.leftChild = None
        self.rightChild = None

class DataTree:
    """
    a binary tree to hold data.

    parameters
    ------------------------------

    none

    attributes
    ------------------------------

    self.root: the root of the data tree
    """

    def __init__(self):
        self.root = None

    def insert_node(self, data):
            """
            inserts a new node with the given data into the data structure.

            parameters
            ------------------------------

            data: the data to be stored in the new node.

            returns
            ------------------------------

            None
            """
            node = Node(data)

            if self.root == None:
                self.root = node
            else:
                self._insert_node(self.root, node)

    def _insert_node(self, curNode, newNode):
        """
        a helper functin for insert_node. recursively traverses the DataTree to find the appropriate place
        for the new node.

        parameters
        ------------------------------

        curNode: the current node being compared

        newNode: the new node being compared with the current node

        returns
        ------------------------------

        None
        """

        if curNode.data.date > newNode.data.date:
            if curNode.leftChild == None:
                curNode.leftChild = newNode
            else:
                self._insert_node(curNode.leftChild, newNode)
        else:
            if curNode.rightChild == None:
                curNode.rightChild = newNode
            else:
                self._insert_node(curNode.rightChild, newNode)

    def filter(self, attribute, value):
        """
        filters the data structure based on the given attribute and value.

        parameters
        ------------------------------

        attribute: the attribute to filter on
        value: the value to filter for

        returns
        ------------------------------

        list: a list of filtered data objects.
        """
        def filter_helper(node, attribute, value):
            if node is None:
                return []
            filtered = []
            if getattr(node.data, attribute) == value:
                filtered.append(node.data)
            filtered.extend(filter_helper(node.leftChild, attribute, value))
            filtered.extend(filter_helper(node.rightChild, attribute, value))
            return filtered
        return filter_helper(self.root, attribute, value)

    def read_HAL_data(self, file):
        """
        reads the lynching data from a CSV file and inserts it into the data structure.

        parameters
        ------------------------------

        file: the path to the CSV file containing the data.

        returns
        ------------------------------

        none
        """
        with open(file, 'r', encoding='UTF-8-SIG') as f:
            reader = csv.DictReader(f)
            for line in reader:
                newData = HALData(**line)
                self.insert_node(newData)

if __name__ == '__main__':
    pass