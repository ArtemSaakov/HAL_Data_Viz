import csv
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=100)

class HALData:

    def __init__(self, state, year=None, month=None, day=None, victim=None, county=None, race=None, sex=None, offense=None):
        self.state = state
        self.date = datetime(int(year), int(month), int(day))
        self.victimName = victim
        self.county = county
        self.victimRace = race
        self.victimSex = sex
        self.allegedOffense  = offense

    def __str__(self) -> str:
        return f'''
State: {self.state}
Date: {self.date}
Victim Name: {self.victimName}
County: {self.county}
Victim Race: {self.victimRace}
Victim Sex: {self.victimSex}
Alleged Offense: {self.allegedOffense}
'''
class CensusData:

    def __init__(self):
        pass

class Node:

    def __init__(self, data=None):
        self.data = data
        self.leftChild = None
        self.rightChild = None

class DataTree:

    def __init__(self):
        self.root = None

    def insert_node(self, data):
        node = Node(data)

        if self.root == None:
            self.root = node
        else:
            self._insert_node(self.root, node)

    def _insert_node(self, curNode, newNode):
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


    def read_HAL_data(self, file):
        with open(file, 'r', encoding='UTF-8-SIG') as f:
            reader = csv.DictReader(f)
            for line in reader:
                newData = HALData(**line)
                self.insert_node(newData)




def main():

    tree = DataTree()
    tree.read_HAL_data("HAL_cleaned.csv")
    # pp.pprint()

if __name__ == '__main__':
    main()