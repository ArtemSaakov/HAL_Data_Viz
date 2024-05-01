from DataStructure import DataTree, Node, HALData
import streamlit as st

def main():
    st.title('Historical American Lynching')

    # load up a tree with the lynching data
    tree = DataTree()
    tree.read_HAL_data("data/HAL_cleaned.csv")

    # initialize attribute selections
    selected_attribute = st.sidebar.selectbox('Select Attribute to Filter', ['state', 'victimRace', 'victimSex', 'allegedOffense'])
    selected_value = st.sidebar.text_input(f'Enter Value for {selected_attribute}', '')

if __name__ == '__main__':
    main()