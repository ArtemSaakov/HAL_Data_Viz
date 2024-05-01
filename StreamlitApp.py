from DataStructure import DataTree
import streamlit as st

def main():
    st.title('Historical American Lynching')

    # load up a tree with the lynching data
    tree = DataTree()
    tree.read_HAL_data("data/HAL_cleaned.csv")


    # initialize attribute selections for sidebar
    selected_attribute = st.sidebar.selectbox('Select Attribute to Filter', ['state', 'victimRace', 'victimSex', 'allegedOffense'])
    selected_value = st.sidebar.text_input(f'Enter Value for {selected_attribute}', '')

    # filter attribute selection
    while not selected_value:
        st.write(tree)

        if selected_value:
            filtered_data = tree.filter(selected_attribute, selected_value)

    # display filtered data
    st.subheader('Filtered Data')
    st.write(filtered_data)

if __name__ == '__main__':
    main()