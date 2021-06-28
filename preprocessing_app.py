# Load Framework library
import fbprophet
from traitlets.traitlets import default
import streamlit as st

# Load Data libraries
import pandas as pd
import numpy as np

# Load Viz libraries
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

# Load ML libraries
from fbprophet import Prophet, models
from fbprophet.diagnostics import cross_validation, performance_metrics
from fbprophet.plot import plot, plot_plotly, plot_components_plotly
import pickle

def app():
    st.markdown(""" ## Page: **Forecasting**""")

    # Set the intro text of the page
    st.title("Individual Household Power Consumption")
    st.markdown("____")
    st.subheader('Introduction:')
    st.markdown("""After the exploration is done, our goal is to 
                    predict the next 30 days of Global Active Power
                    consumption.
                    """)

    st.markdown("""In this project we will be comparing the FBprophet model vs SARIMAX model.
    As it can be seen from the previous exploration, this timeseries data
    clearly has seasonalities and why we are going with the selected models.
                    """)

    # Loading the data
    data_url = ('household_power_consumption_final.csv')

    @st.cache(persist=True)
    def load_data():
        '''Loads the data and converts Date into Datetime'''
        data = pd.read_csv(data_url, low_memory=False)
        data['Date_time'] = pd.to_datetime(data['Date_time'])
        data_daily_grp = data.groupby(
        pd.Grouper(key='Date_time', freq='D')).agg({'Global_active_power':'sum', 
                                                    'Sub_metering_1':'sum', 
                                                    'Sub_metering_2':'sum', 
                                                    'Sub_metering_3':'sum'}).reset_index()
        
        # Converting all zero values to the mean of Global_active_power
        data_daily_grp['Global_active_power'] = data_daily_grp['Global_active_power'].replace(0, np.nan).fillna(data_daily_grp['Global_active_power'].mean())

        # Removing all outliers from Global_active_power
        data_daily_grp = data_daily_grp[((data_daily_grp['Global_active_power'] < 3000) & (data_daily_grp['Global_active_power'] > 100))]
        
        return data_daily_grp

    # Saving the data into df variable
    data_daily_grp = load_data()

    # FORECASTING - FBPROPHET
    # Renaming the columns
    # data_daily_grp = data_daily_grp.rename(columns={'Date_time':'ds', 'Global_active_power':'y'})

    # Train - Test Split -> test data will have 90 days
    threshold_date = pd.to_datetime('2010-09-13')

    # threashold_date1 = len(data_daily_grp)-90
    mask = data_daily_grp['Date_time'] < threshold_date

    # Spliting the data
    data_train = data_daily_grp[mask][['Date_time', 'Global_active_power']]
    data_test = data_daily_grp[~mask][['Date_time', 'Global_active_power']]

    # Plotting the train and test split
    st.subheader('Plot Train and Test split')
    st_train = len(data_train)
    st_test = len(data_test)

    st.markdown(f"""
        We will split the data between Train and Test datasets.
        The train data will contain {st_train} days, which will be
        used to train the model.
        While the test data will contain {st_test} days and preventing
        the model from observing that data, in order to evaluate it later.
    """)
    # Plotting the train and test dataset
    fig_split = make_subplots()
    fig_split.add_trace(go.Scatter(
        x=data_train['Date_time'],
        y=data_train['Global_active_power'],
        name='Y_Train'
        ))

    fig_split.add_trace(go.Scatter(
        x=data_test['Date_time'],
        y=data_test['Global_active_power'],
        name='Y_Test'
        ))

    # Setting up the names
    fig_split.update_yaxes(title_text="<b>Power</b> kilowatt [kW]", gridcolor='#4a4e69')
    fig_split.update_xaxes(title_text="<b>Dates", showgrid=False)

    # Setting up the layout
    fig_split.update_layout(
        title={
        'text': "<b>Train and Test data split</b>",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        paper_bgcolor='#2E3137', 
        autosize=True, 
        legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=1.12,
                    xanchor="center",
                    x=0.5))
    # Showing the plot
    st.plotly_chart(fig_split, use_container_width=True)
    st.markdown("____")

    # Decomposition
    st.subheader('FORECASTING')
    st.markdown('''
        The settings are done based on previous exploratory data which we did. 
        It is clear that this dataset contains multiple seasonalities and we have
        included them as parameters for training the model.
        Our target (Global_active_power) is highly dependend on the Sub_metering attributes,
        so the model performs much better than without those attributes.

        **The params are as follows for this FBProphet model:**
        >
        - Seasonality: Yearly / Monthly / Weekly / Daily
        - Target - Global Active Power
        - Train / test data - 1333 / 90 days
        - Fourier_order - 5
        - The multivar model includes: Sub_metering_1 / Sub_metering_2 / Sub_metering_3
    ''')

    # Loading the FBProphet Forecast
    path = 'FBProphet_model_pickle.sav'

    pickle_in_fbp = open(path, 'rb')
    forecast_fbp = pickle.load(pickle_in_fbp)

    # Loading the ARIMA Forecast
    path = 'ARIMA_model_pickle.sav'

    pickle_in_arm = open(path, 'rb')
    forecast_arm = pickle.load(pickle_in_arm)

    # Adding the Arima forecast to test data for ploting
    data_test['Forecast_Arima'] = forecast_arm

    # Ploting the Multivariate model
    attribute_select = st.multiselect(
    'Please select a model:', 
    options = ('Global_active_power', 'FBProphet', 'ARIMA'), 
    default = ['Global_active_power'])
        
    # Ploting the selected attribute
    fig_fore = go.Figure()

    # Looping through each attribute
    for name in attribute_select:
        if name == 'Global_active_power':
            fig_fore.add_trace(go.Scatter(
                x=data_test['Date_time'],
                y=data_test['Global_active_power'],
                name='Test data',
                marker=dict(color='#DB6443')
                ))

        if name == 'FBProphet':
            fig_fore.add_trace(go.Scatter(
                x=forecast_fbp['ds'],
                y=forecast_fbp['yhat'],
                name='FBProphet Forecast',
                marker=dict(color='#2a9d8f')
                ))
        if name == 'ARIMA':
            fig_fore.add_trace(go.Scatter(
                x=data_test['Date_time'],
                y=data_test['Forecast_Arima'],
                name='ARIMA Forecast',
                marker=dict(color='#f2cc8f')
                ))

    # Setting up the names
    fig_fore.update_yaxes(title_text="<b>Power</b> kilowatt [kW]", gridcolor='#4a4e69')
    fig_fore.update_xaxes(title_text="<b>Dates", showgrid=False)

    # Time range slider
    fig_fore.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True),
            type="date"
        )
    )

    # Setting up the layout
    fig_fore.update_layout(
        title={
        'text': "<b>Forecasting 90 days using FBProphet & ARIMA</b>",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        paper_bgcolor='#2E3137', 
        autosize=True,
        height=500,
        legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=1.2,
                    xanchor="center",
                    x=0.5))
    # Showing the plot
    st.plotly_chart(fig_fore, use_container_width=True)
    st.markdown("____")

    st.subheader('Conclusion:')
    st.markdown('''
        The Multivariate FBProphet Model performs signaficantly better than the Univariate SARIMAX Model.

        The additional data which is highly correlated with Global_active_power, 
        improves the Mutlivariate Model by more than half against the Univariate model 
        if we observe MAPE and RMSE metrics.

        A summary of the models bellow.

        ---
        >Comparing the performance of the models for <b>30 days</b> forecast:
        - Multivar vs Univar <b>RMSE</b>: ~160 vs ~290 - kWh on Global_active_power
        - Multivar vs Univar <b>MAPE</b>: ~7% vs ~13% - kWh on Global_active_power
        ---
        >Comparing the performance of the models for <b>60 days</b> forecast:
        - Multivar vs Univar <b>RMSE</b>: 197 vs 422 - kWh on Global_active_power
        - Multivar vs Univar <b>MAPE</b>: 9% vs 17% - kWh on Global_active_power
        ---
        >Comparing the performance of the models for <b>90 days</b> forecast:
        - Multivar vs Univar <b>RMSE</b>: 230 vs 409 - kWh on Global_active_power
        - Multivar vs Univar <b>MAPE</b>: 11% vs 24% - kWh on Global_active_power
    ''')
    st.markdown("____")

    st.subheader('Futher goal:')
    st.markdown('''
        - Improve the MAPE and RMSE metrics by modifying the parameters.
        - Run the data through LSTM model
        - Compare it against FBProphet
    ''')