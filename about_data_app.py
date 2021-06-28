import streamlit as st

def app():
    st.markdown(""" ## Page: **About Data**""")

    # Set the intro text of the page
    st.title("Individual Household Power Consumption")
    st.markdown("____")
    st.subheader("Abstract:")
    st.markdown('''Measurements of 
    electric power consumption in one household with a 
    one-minute sampling rate over a period of almost 4 years. 
    Different electrical quantities and some sub-metering 
    values are available.''')

    st.subheader('Source:')
    st.markdown('**Georges Hebrail** (georges.hebrail@edf.fr), Senior Researcher, EDF R&D, Clamart, France')
    st.markdown('**Alice Berard**, TELECOM ParisTech Master of Engineering Internship at EDF R&D, Clamart, France')

    link = '[Dataset Homepage](https://archive.ics.uci.edu/ml/datasets/Individual+household+electric+power+consumption)'
    st.markdown(link, unsafe_allow_html=True)
    st.markdown('___')

    st.subheader('Dataset Information:')
    st.markdown('''
        This archive contains 2075259 measurements gathered in a house 
        located in Sceaux (7km of Paris, France) between 
        December 2006 and November 2010 (47 months).
    ''')
    st.markdown('**NOTES:**')
    st.markdown("""
        1. (global_active_power*1000/60 - sub_metering_1 - sub_metering_2 - sub_metering_3) 
        represents the active energy consumed every minute (in watt hour) 
        in the household by electrical equipment not measured in 
        sub-meterings 1, 2 and 3.
    """)
    st.markdown("""
        2. The dataset contains some missing values in the measurements (nearly 1,25% of the rows).
        All calendar timestamps are present in the dataset but for some timestamps, 
        the measurement values are missing: 
        a missing value is represented by the absence of value 
        between two consecutive semi-colon attribute separators. 
        For instance, the dataset shows missing values on April 28, 2007.
    """)

    st.subheader('Attribute Information:')
    st.markdown('1. date: Date in format dd/mm/yyyy')
    st.markdown('2. time: time in format hh:mm:ss')
    st.markdown('3. global_active_power: household global minute-averaged active power (in kilowatt)')
    st.markdown('4. global_reactive_power: household global minute-averaged reactive power (in kilowatt)')
    st.markdown('5. voltage: minute-averaged voltage (in volt)')
    st.markdown('6. global_intensity: household global minute-averaged current intensity (in ampere)')
    st.markdown("""
        7. sub_metering_1: energy sub-metering No. 1 (in watt-hour of active energy). 
        It corresponds to the kitchen, containing mainly a dishwasher, an oven and a microwave 
        (hot plates are not electric but gas powered).
    """)
    st.markdown("""
        8. sub_metering_2: energy sub-metering No. 2 (in watt-hour of active energy). 
        It corresponds to the laundry room, containing a washing-machine, a tumble-drier, 
        a refrigerator and a light.
    """)
    st.markdown("""
        8. sub_metering_3: energy sub-metering No. 3 (in watt-hour of active energy). 
        It corresponds to an electric water-heater and an air-conditioner.
    """)
