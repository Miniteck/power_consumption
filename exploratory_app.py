# Load Framework library
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
import seaborn as sns
import matplotlib.pyplot as plt

# Load statistic libraries
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller

# Configurating the layout of the page
st.set_page_config(
    page_title="Household Power Consumption",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

def app():
    st.markdown(""" ## Page: **Exploratory Data Analysis**""")

    # Set the title of the page
    st.title("Individual Household Power Consumption")

    # Description of the project
    st.markdown("""
    ### **Abstract:**
    This dataset is representation on 
    measurements of electric power consumption in one household 
    with a one-minute sampling rate over a period of almost 4 years. 
    Different electrical quantities and some sub-metering values are 
    available.
    The data ranges from '2006-12-16' up to 2010-11-26.
    """)

    #create a canvas for each item
    interactive =  st.beta_container()

    # Loading the data
    # data_url = ('household_power_consumption_final.csv')
    data_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip'

    # @st.cache(persist=True)
    # def load_data():
    #     '''Loads the data and converts Date into Datetime'''
    #     data = pd.read_csv(data_url, low_memory=False)
    #     data['Date_time'] = pd.to_datetime(data['Date_time'])
    #     return data

    @st.cache(persist=True)
    def load_data():
        '''Loads the data and converts Date into Datetime'''
        data = pd.read_csv(data_url, delimiter=';', low_memory=False)
        # Converting the date and time columns into Datetime series
        data['Date_time'] = pd.to_datetime(data.pop('Date')) + pd.to_timedelta(data.pop('Time'))
        # Replacing '?' to NaN values
        data.replace('?', np.nan, inplace=True)
        # Dropping all NaN values
        # data.dropna(how="any", inplace=True)
        # Converting the data types for all columns except date_time and week_num
        cols = [i for i in data.columns if i not in ['Date_time']]
        for col in cols:
            data[col] = pd.to_numeric(data[col], downcast='integer')

        return data

    # Saving the data into df variable
    data = load_data()

    # Data preview
    st.markdown('Data preview: _contains the first 20 records_')

    # Showing first 5 rows
    st.write(data.head(20))

    # Calculate memory usage
    memory_usage = round(data.memory_usage(deep=True).sum()/1048576,2)

    # Warning message
    st.warning(
        f'The full data uses **{memory_usage} MB** and has over 2 Mil records. It takes lots of time to load!')

    # Display full data base on checkbox.
    if st.checkbox('Show full data'):
        data

    st.markdown("""____""")

    # Grouping the data on daily interval by ascending date
    data_daily_grp = data.groupby(
        pd.Grouper(key='Date_time', freq='D')).agg({'Global_active_power':'sum', 
                                                    'Sub_metering_1':'sum', 
                                                    'Sub_metering_2':'sum', 
                                                    'Sub_metering_3':'sum'}).reset_index()

    st.markdown(""" ### **EXPLORATORY DATA ANALYSES** """)

    st.markdown("""
    **NOTE:** The following visualizations and suggestions are done based
    on previous EDA done on Jupyter Notebook which can be found in the page: xx.""")
    st.markdown("""After observing the sub_meterings 
    1(kitchen) / 2(laundry_room) / 3(heater_air-conditioner), 
    the biggest usage of energy power (Wh) is the Sub_metering_3 which contains 
    the electric water-heater and air-conditioner.""")

    st.markdown("""**Suggestion:** Select Global Active Power and Sub_metering_3 
    attributes to compare and see the correlation between them.
    """)

    # Excluding all 0 values
    data_daily_grp = data_daily_grp.loc[data_daily_grp.ne(0).all(axis=1)]

    # Creating list of all columns/attributes to select
    attribute_select = st.multiselect(
        'Which attributes to plot?', 
        options = list(data_daily_grp.columns[1:]), 
        default = ['Global_active_power'])

    # Plotting the Line chart
    # Activating secondary Y axes
    fig = make_subplots(specs=[[{'secondary_y':True}]])

    # Creating bool variable
    secondary_y=True

    # Looping through each attribute to append on correct axes
    for name in attribute_select:
        if name != 'Global_active_power':
            secondary_y=False
        else:
            secondary_y=True
        
        # Ploting the selected attribute
        fig.add_trace(go.Scatter(
        x=data_daily_grp['Date_time'],
        y=data_daily_grp[name],
        name=name
        ), secondary_y=secondary_y)

        # Setting up the names
        fig.update_yaxes(title_text="<b>Power</b> watt-hour [W/h]", secondary_y=False, gridcolor='#4a4e69')
        fig.update_yaxes(title_text="<b>Power</b> kilowatt [kW]", secondary_y=True, gridcolor='#4a4e69')
        fig.update_xaxes(title_text="<b>Dates", showgrid=False)

        # Setting up the layout
        fig.update_layout(
            title={
            'text': "<b>Daily Power Consumption - 2006 - 2010</b>",
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
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""We can confirm the suggestion from above by showing
    the correlation between each attributes.""")

    st.markdown("""On the scale of 0.1 up to 1 - the correlation between 
    Global Active Power and Sub Metering 3 is 0.65.
    Meanwhile the correlation with Sub Metering 1 & 2 is 0.46.
    """)

    # Setting up the plot
    st.subheader('Correlation Matrix')

    z=data_daily_grp.corr().values
    x=['Global Active Power','Sub 1','Sub 2','Sub 3']
    y=['Global Active Power','Sub 1','Sub 2','Sub 3']
    z_text = np.round(z, decimals=2)

    fig_corr = ff.create_annotated_heatmap(
                                        z, 
                                        x=x, 
                                        y=y, 
                                        annotation_text=z_text,
                                        colorscale='blues',
                                        hoverinfo='z')

        # Setting up the layout
    fig_corr.update_layout(title_text='<b>Correlation Matrix</b>', 
                            title_x=0.5,
                            xaxis_showgrid=False,
                            yaxis_showgrid=False,
                            yaxis_autorange='reversed',
                            paper_bgcolor='#2E3137',
                            showlegend=True,
                            autosize=True)

    # Showing the plot
    st.plotly_chart(fig_corr, use_container_width=True)

    st.subheader("""Boxplot""")

    # Activating seconday Y axes
    fig_box = make_subplots(specs=[[{'secondary_y':True}]])

    # Plotting each attribute
    fig_box.add_trace(go.Box(y=data_daily_grp['Sub_metering_1'], 
                            name='Sub_1'), secondary_y=False)

    fig_box.add_trace(go.Box(y=data_daily_grp['Sub_metering_2'], 
                            name='Sub_2'), secondary_y=False)

    fig_box.add_trace(go.Box(y=data_daily_grp['Sub_metering_3'], 
                            name='Sub_3'), secondary_y=False)

    fig_box.add_trace(go.Box(y=data_daily_grp['Global_active_power'], 
                            name='Active Power'), secondary_y=True)

    # Setting the names of y axes for each plot
    fig_box.update_yaxes(title_text="Watt-hour <b>[Wh]</b>")
    fig_box.update_yaxes(title_text="Kilowatt <b>[kW]</b>", secondary_y=True)

    # Setting the grid lines and their colors
    fig_box.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#4a4e69')
    fig_box.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#4a4e69')

    # Fixing the tickval on the x axes
    fig_box.update_xaxes(tickfont=dict(size=10))

    # Setting the layout
    fig_box.update_layout(title_text='<b>Sub Metering and Active Power Averages</b>', 
                    title_x=0.5,
                    paper_bgcolor='#2E3137',
                    autosize=True,
                    yaxis=dict(showgrid=True),
                    legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1,
                    xanchor="center",
                    x=0.5))
    # Showing the plot
    st.plotly_chart(fig_box, use_container_width=True)

    # Distribution plot
    st.subheader('Distribution Plots')

    # Creating a single value selection box
    attribute_select_sng = st.selectbox("Please select an attribute", list(data_daily_grp.columns[1:]))

    # Creating variable that holds the data
    hist_data = [list(data_daily_grp[attribute_select_sng].values)]
    # Creating variable to hold the names of the attributes
    group_labels = [attribute_select_sng]

    # Plotting the data using displot
    fig_displot = ff.create_distplot(hist_data, group_labels=group_labels,
                            bin_size=190, show_rug=False)
    
    # Setting the grid lines and their colors
    fig_displot.update_xaxes(showgrid=True, gridcolor='#4a4e69')
    fig_displot.update_yaxes(showgrid=True, gridcolor='#4a4e69')

    # Updating the layout
    fig_displot.update_layout(title_text=(f'<b>Displot for {attribute_select_sng}</b>'), 
                title_x=0.5,
                paper_bgcolor='#2E3137',
                autosize=True,
                yaxis=dict(showgrid=True),
                showlegend=False)
    # Showing the plot
    st.plotly_chart(fig_displot, use_container_width=True)

    # PAIRPLOT
    st.subheader('Pairplot')
    # Setting up the plot
    fig_pair = go.Figure(data=go.Splom(
                dimensions=[dict(label='Global Active Power',
                                 values=data_daily_grp['Global_active_power']),
                            dict(label='Sub 1',
                                 values=data_daily_grp['Sub_metering_1']),
                            dict(label='Sub 2',
                                 values=data_daily_grp['Sub_metering_2']),
                            dict(label='Sub 3',
                                 values=data_daily_grp['Sub_metering_3'])], 
                showupperhalf=False,
                diagonal_visible=False,
                marker=dict(
                            showscale=False, # colors encode categorical variables
                            line_color='white', line_width=0.5)
                ))

    # Setting up the layout
    fig_pair.update_layout(
        title_text='<b>All attributes - Scatter plot</b>',
        title_x=0.5,
        dragmode='select',
        paper_bgcolor='#2E3137',
        autosize=True,
        hovermode='closest')
    # Showing the plot
    st.plotly_chart(fig_pair, use_container_width=True)

    # MOVING AVERAGES
    st.subheader('Moving Average')

    #Testing stationary
    ts = data_daily_grp[['Date_time', 'Global_active_power']]
    ts.set_index('Date_time', inplace=True)
    mte = data_daily_grp['Global_active_power']

    #
    def TestStationaryAdfuller(ts, cutoff = 0.01):
        ts_test = adfuller(ts, autolag = 'AIC')
        ts_test_output = pd.Series(ts_test[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
        
        for key,value in ts_test[4].items():
            ts_test_output['Critical Value (%s)'%key] = value
        print(ts_test_output)
        
        if ts_test[1] <= cutoff:
            print("Strong evidence against the null hypothesis, reject the null hypothesis. Data has no unit root, hence it is stationary")
        else:
            print("Weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")

    # Moving Averages
    moving_avg = mte.rolling(12).mean()

    fig_mv = go.Figure()

    fig_mv.add_trace(go.Scatter(
        y=mte, name='Global Active Power'
    ))

    fig_mv.add_trace(go.Scatter(
        y=moving_avg, name='Moving Average'
    ))

    # Title settings
    fig_mv.update_layout(
        title={
            'text': '<b>Moving Average on Global Active Power</b>',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    # Legend settings
    fig_mv.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1),
        paper_bgcolor='#2E3137'
        )
    st.plotly_chart(fig_mv, use_container_width=True)

    # DECOMPOSITION
    st.subheader('Daily Seasonal Decompose')
    mte.index = pd.to_datetime(data_daily_grp['Date_time'])
    decomposition = seasonal_decompose(mte, freq=7)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    fig_dec = make_subplots(rows=4, cols=1)

    fig_dec.add_trace(go.Scatter(
        y=mte, name='Original'
    ), row=1, col=1)

    fig_dec.add_trace(go.Scatter(
        y=trend, name='Trend'
    ), row=2, col=1)

    fig_dec.add_trace(go.Scatter(
        y=seasonal, name='Seasonality'
    ), row=3, col=1)

    fig_dec.add_trace(go.Scatter(
        y=residual, name='Residuals'
    ), row=4, col=1)

    # Title settings
    fig_dec.update_layout(
        title={
            'text': '<b>Daily Decomposition of Trend/Seasonality/Residuality</b>',
            'y':0.96,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            height=800)

    # Legend settings
    fig_dec.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1),
        paper_bgcolor='#2E3137'
        )

    st.plotly_chart(fig_dec, use_container_width=True)

    
    # CONCLUSION
    st.subheader("""Conclusion""")

    st.markdown("""After completing the Exploratory step of the dataset,
    we can conclude the following:

    1. The dataset is stationary, which means that the statistical properties such as mean,
    variance, autocorrelation, etc. are all constant over time.

    2. There are yearly, monthly, daily seasonalities, which further helps us
    to build the model for prediciting the target variable.

    3. The target variable is highly correlated with the attributes Sub_metering_1/2/3.

    4. It is very noticeable that the dataset contains outliers which might improve
    the prediction model if they are removed.
    """)

    st.markdown('Now, we can move on to the **Forecasting.**')
