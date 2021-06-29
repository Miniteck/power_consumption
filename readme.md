# Power Consumption Prediction

### Description:
Prediction of Household Power Consumption using FBProphet and ARIMA models in Python.
The **GOAL** of this project is to predict the next 30 days of power consumption in a single household, based on daily interval.
Due to the nature of the dataset and the better result, the predicition will be also based on multiple inputs for a single output.
The **TARGET** variable will be Global Active Power.

For more detailed information regarding the dataset, please visit the link bellow.

### Tools used:
- **Language**: Python
- **Platform**: Jupyter-Lab
- **Application**: Streamlit lib
- **Link to app**: [power-usage-consumption]()

### Data Download
**Source**: UCI Repository<br>
**Data Name**: Individual household electric power consumption Data Set<br>
[Link to download](https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption)

### Process:
**1st step: Cleaning**<br>
The cleaning and manipulation of the dataset is done mainly using the Pandas library.
The purpose of this step is to eliminate all unnecessary data/attributes if there are any,
removing/manipulating all missing values in the data if there are any, 
sorting and manipulating of the data that will be used in the ML model.

**2nd step Exploratory**<br>
The exploratory part is done using the Pandas (data manipulation) and Plotly (data vizualization) libraries - due to the interactivity option and much modern look.
The purpose of this step is to learn the dataset, and because it is timeseries data - it's highly important to see how the data progresses over the time.
From here it's highly important to find out what kind of model parameters will be used for predicting the future of the power consumption.

**3rd step: Prediction**<br>
For the prediction of the target variable there are 2 ML algorithams used to find out which one performs better.
- [FBProphet](https://github.com/Miniteck/power_consumption/blob/main/workbooks/FBProphet_model.ipynb)
![image](https://user-images.githubusercontent.com/59763166/123873716-388b1600-d937-11eb-9ac0-f65a07dfc1a9.png)

- [ARIMA](https://github.com/Miniteck/power_consumption/blob/main/workbooks/ARIMA_model.ipynb)
![image](https://user-images.githubusercontent.com/59763166/123873741-45a80500-d937-11eb-984b-0d1048b5eb68.png)

These are picked because this is timeseries dataset and has seasonalities.
The conclusion and the results can be seen on the link above **Streamlit app**.

### Future goal:
- Build LSTM Prediction model and compare it with the above models.
