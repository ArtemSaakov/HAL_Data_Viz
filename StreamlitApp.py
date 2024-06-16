from DataStructure import DataTree, HALData
from CensusData import CensusData
import streamlit as st
import networkx as nx
from pathlib import Path
from typing import List

class HALNetwork:
    """
    Represents a network of HALData instances connected to county census data.

    Attributes:
        graph: The NetworkX graph representing the relationships between HALData instances and county census data.
    """

    def __init__(self):
        self.graph = nx.Graph()

    def add_hal_data(self, hal_data_list: List[HALData]):
        """
        Adds HALData instances to the network and establishes relationships between them and county instances.

        Args:
            hal_data_list: A list of HALData instances to be added to the network.
        """
        for hal_data in hal_data_list:
            self.graph.add_node(hal_data)
            # Assuming each HALData instance has a county attribute representing where the incident occurred
            county_instance = self._get_county_instance(hal_data.county)
            if county_instance:
                self.graph.add_node(county_instance)
                self.graph.add_edge(hal_data, county_instance)

    def _get_county_instance(self, county_name: str):
        """
        Retrieves the county instance based on the county name.

        Args:
            county_name: Name of the county.

        Returns:
            Counties: County instance if found, None otherwise.
        """
        # Assuming you have a method to retrieve county instances based on the county name
        # You can implement this method based on your existing logic
        pass

    def visualize_network(self):
        """
        Visualizes the network using NetworkX built-in functions.

        Note: You may need to install additional libraries such as matplotlib to visualize the network.
        """
        # Example visualization using NetworkX's draw function
        nx.draw(self.graph, with_labels=True)
        # You can customize the visualization based on your requirements.



def main():

    network = HALNetwork()
    network.visualize_network()

    # st.title('Historical American Lynching')
    # st.header('Data Collection Project Visualization')

    # # load up a tree with the lynching data
    # tree = DataTree()
    # tree.read_HAL_data("data/HAL_cleaned.csv")

    # # initialize attribute selections for sidebar
    # selected_attribute = st.sidebar.selectbox('Select Attribute to Filter', ['state', 'victimRace', 'victimSex', 'allegedOffense'])
    # selected_value = st.sidebar.text_input(f'Enter Value for {selected_attribute}', '')

    # # filter attribute selection
    # if selected_value:
    #     filtered_data = tree.filter(selected_attribute, selected_value)
    # else:
    #     filtered_data = tree.read_HAL_data("data/HAL_cleaned.csv")

    # # display filtered data
    # st.subheader('Filtered Data')
    # st.write(filtered_data)

if __name__ == '__main__':
    main()