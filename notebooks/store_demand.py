# -*- coding: utf-8 -*-
"""store_demand

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jw5AOry2B5om3ZOUqhrUk01ogzQqldwj

# Store Demand Forecasting
## Author github.com/tushar2704

# Table of contents
>[Importing Libraries](#scrollTo=d56c9940)

>[Exploring Data Analysis](#scrollTo=30510c91)

>[Feature Engineering](#scrollTo=490e899e)

>[Random Noise (Gürültü](#scrollTo=fb1e4bda)

>[Lag/Shifted Features (Gecikmeler)](#scrollTo=47f8ab82)

>[Rolling Mean Features (Hareketli Ortalamalar)](#scrollTo=b99cb837)

>[Exponentially Weighted Mean Features (Üssel Ağırlıklı Ortalama Featureları)](#scrollTo=6b9429d6)

>[LightGBM Model](#scrollTo=c75cb858)

>[Custom Cost Function](#scrollTo=c08b6548)

<a id = "1"></a><h1 id="Salary Prediction with Machine Learning"><span class="label label-default" style="background-color:#f5c0c0; font-size:30px;
color: Black; ">Store Item Demand Forecasting</span></h1>

**You are given 5 years of store-item sales data, and asked to predict 3 months of sales for 50 different items at 10 different stores.**

<a id = "1"></a><h1 id="Salary Prediction with Machine Learning"><span class="label label-default" style="background-color:#f5c0c0; font-size:30px;
color: Black; ">Variables</span></h1>


- date
- store
- item
- sales

#Importing Libraries
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import lightgbm as lgb
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
import itertools

import warnings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
warnings.filterwarnings('ignore')

"""#Exploring Data Analysis

The code reads two CSV files, 'train.csv' and 'test.csv', and parses the 'date' column as dates during the reading process. It then concatenates the data from both files into a single DataFrame 'df', stacking them vertically. The 'head()' function is used to display the first few rows of the combined DataFrame.
"""

train = pd.read_csv('data/train.csv', parse_dates=['date'])
test = pd.read_csv('data/test.csv', parse_dates=['date'])
df = pd.concat([train, test], sort=False)
df.head()

"""The code prints the dimensions (number of rows and columns) of the 'train' and 'test' DataFrames, showing the size of each dataset.





"""

print("Train setinin boyutu:",train.shape)
print("Test setinin boyutu:",test.shape)

df.shape

"""The code calculates the quantiles (percentiles) of the data in the DataFrame 'df' for the specified quantile levels [0, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]. It transposes the resulting DataFrame to display the quantiles for each column as rows.





"""

df.quantile([0, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]).T

df["date"].min()

df["date"].max()

"""The code calculates descriptive statistics for the 'sales' column in the DataFrame 'df', including mean, standard deviation, minimum, maximum, and percentiles at the specified quantile levels [0.10, 0.30, 0.50, 0.70, 0.80, 0.90, 0.95, 0.99].





"""

df["sales"].describe([0.10, 0.30, 0.50, 0.70, 0.80, 0.90, 0.95, 0.99])

df["store"].nunique()

df["item"].nunique()

"""The code groups the DataFrame 'df' by the "store" column and then calculates the number of unique items associated with each store in the dataset.





"""

df.groupby(["store"])["item"].nunique()

"""The code groups the DataFrame 'df' by both the "store" and "item" columns, and then aggregates the "sales" column for each group, calculating the sum, mean, median, and standard deviation of sales for each combination of store and item in the dataset.





"""

df.groupby(["store", "item"]).agg({"sales": ["sum", "mean", "median", "std"]})

"""#Feature Engineering

The code extracts various date-related features from the "date" column of the DataFrame 'df', such as month, day of the month, day of the year, week of the year, day of the week, and year. It also creates new binary features indicating whether the date is a weekend, month start, or month end.
"""

df['month'] = df.date.dt.month
df['day_of_month'] = df.date.dt.day
df['day_of_year'] = df.date.dt.dayofyear
df['week_of_year'] = df.date.dt.weekofyear
df['day_of_week'] = df.date.dt.dayofweek
df['year'] = df.date.dt.year
df["is_wknd"] = df.date.dt.weekday // 4
df['is_month_start'] = df.date.dt.is_month_start.astype(int)
df['is_month_end'] = df.date.dt.is_month_end.astype(int)

df.head()

"""The code groups the DataFrame 'df' by the "store", "item", and "month" columns, and then aggregates the "sales" column for each combination of store, item, and month, calculating the sum, mean, median, and standard deviation of sales for each group.





"""

df.groupby(["store", "item", "month"]).agg({"sales": ["sum", "mean", "median", "std"]})

"""#Random Noise (Gürültü

The code defines a function 'random_noise' that takes a DataFrame as input and returns an array of random noise generated from a normal distribution with a scale of 1.6 and the same length as the input DataFrame.
"""

def random_noise(dataframe):
    return np.random.normal(scale=1.6, size=(len(dataframe),))

"""#Lag/Shifted Features (Gecikmeler)

The code sorts the DataFrame 'df' in place based on multiple columns, first by 'store', then by 'item', and finally by 'date' in ascending order. The 'head()' function is then used to display the first few rows of the sorted DataFrame.
"""

df.sort_values(by=['store', 'item', 'date'], axis=0, inplace=True)
df.head()

"""The code defines a function 'lag_features' that creates lagged features for the 'sales' column in the DataFrame 'df' by shifting the values by different time intervals specified in 'lags'. The function adds random noise to the shifted values and returns the updated DataFrame. The 'lag_features' function is then called with 'df' and a list of lag intervals to create the lagged features for the specified lags.





"""

def lag_features(dataframe, lags):
    for lag in lags:
        dataframe['sales_lag_' + str(lag)] = dataframe.groupby(["store", "item"])['sales'].transform(
            lambda x: x.shift(lag)) + random_noise(dataframe)
    return dataframe

df = lag_features(df, [91, 98, 105, 112, 119, 126, 182, 364, 546, 728])

"""#Rolling Mean Features (Hareketli Ortalamalar)

The code defines a function 'roll_mean_features' that calculates rolling mean features for the 'sales' column in the DataFrame 'df' using different rolling window sizes specified in 'windows'. The function applies the triangular rolling window with a minimum of 10 periods and adds random noise to the calculated rolling means. The updated DataFrame is then returned. The 'roll_mean_features' function is called with 'df' and a list of rolling window sizes to create the rolling mean features for the specified windows.
"""

def roll_mean_features(dataframe, windows):
    for window in windows:
        dataframe['sales_roll_mean_' + str(window)] = dataframe.groupby(["store", "item"])['sales']. \
                                                          transform(
            lambda x: x.shift(1).rolling(window=window, min_periods=10, win_type="triang").mean()) + random_noise(
            dataframe)
    return dataframe


df = roll_mean_features(df, [365, 546, 730])

"""#Exponentially Weighted Mean Features (Üssel Ağırlıklı Ortalama Featureları)

The code defines a function 'ewm_features' that calculates exponentially weighted moving average (EWMA) features for the 'sales' column in the DataFrame 'df' using different smoothing factors (alphas) and lag intervals specified in 'alphas' and 'lags', respectively. The function applies the EWMA to the lagged 'sales' data within each group defined by 'store' and 'item'. The updated DataFrame is then returned. The 'ewm_features' function is called with lists of alphas and lags to create the EWMA features for the specified combinations of smoothing factors and lag intervals, and the last few rows of the updated DataFrame are displayed using 'tail()'.
"""

def ewm_features(dataframe, alphas, lags):
    for alpha in alphas:
        for lag in lags:
            dataframe['sales_ewm_alpha_' + str(alpha).replace(".", "") + "_lag_" + str(lag)] = \
                dataframe.groupby(["store", "item"])['sales'].transform(lambda x: x.shift(lag).ewm(alpha=alpha).mean())
    return dataframe


alphas = [0.99, 0.95, 0.9, 0.8, 0.7, 0.5]
lags = [91, 98, 105, 112, 180, 270, 365, 546, 728]

df = ewm_features(df, alphas, lags)
df.tail()

"""The code performs one-hot encoding on the 'day_of_week' and 'month' columns of the DataFrame 'df', creating binary columns for each unique value in these columns, effectively converting categorical variables into numerical format.





"""

df = pd.get_dummies(df, columns=['day_of_week', 'month'])

"""The code applies the natural logarithm transformation (logarithm with base e) to the 'sales' column in the DataFrame 'df', using the numpy function 'np.log1p', which handles zero values gracefully by adding 1 before taking the logarithm. This transformation is often used to stabilize the variance and improve the performance of certain models.





"""

df['sales'] = np.log1p(df["sales"].values)

"""#LightGBM Model

The code creates two new DataFrames, 'train' and 'val', by filtering rows from the original DataFrame 'df' based on the dates. 'train' contains data before January 1, 2017, and 'val' contains data between January 1, 2017, and April 1, 2017. The variable 'cols' is defined as a list of column names from 'train' DataFrame, excluding the columns 'date', 'id', 'sales', and 'year'.
"""

train = df.loc[(df["date"] < "2017-01-01"), :]

val = df.loc[(df["date"] >= "2017-01-01") & (df["date"] < "2017-04-01"), :]

cols = [col for col in train.columns if col not in ['date', 'id', "sales", "year"]]

"""The code creates four new variables: 'Y_train' and 'Y_val' are the target variables containing the 'sales' data for the training and validation sets, respectively. 'X_train' and 'X_val' are the feature matrices containing the selected columns (excluding 'date', 'id', 'sales', and 'year') for the training and validation sets, respectively. The final line displays the shapes of these arrays, indicating the number of rows and columns in each set.





"""

Y_train = train['sales']

X_train = train[cols]

Y_val = val['sales']

X_val = val[cols]

Y_train.shape, X_train.shape, Y_val.shape, X_val.shape

"""#Custom Cost Function

The code defines two functions: 'smape' calculates the Symmetric Mean Absolute Percentage Error (SMAPE) for two arrays of predictions and true target values, while 'lgbm_smape' computes SMAPE for LightGBM predictions by converting them back from log-scale using 'np.expm1' and comparing with the original labels.
"""

def smape(preds, target):
    n = len(preds)
    masked_arr = ~((preds == 0) & (target == 0))
    preds, target = preds[masked_arr], target[masked_arr]
    num = np.abs(preds - target)
    denom = np.abs(preds) + np.abs(target)
    smape_val = (200 * np.sum(num / denom)) / n
    return smape_val


def lgbm_smape(preds, train_data):
    labels = train_data.get_label()
    smape_val = smape(np.expm1(preds), np.expm1(labels))
    return 'SMAPE', smape_val, False

"""The code defines a dictionary 'lgb_params' containing various parameters for the LightGBM model, including the evaluation metric (Mean Absolute Error - 'mae'), number of leaves, learning rate, feature fraction, maximum depth, verbosity, number of boosting rounds, early stopping rounds, and the number of threads to use (-1 indicates using all available threads). These parameters will be used to configure the LightGBM model for training and evaluation.





"""

# LightGBM parameters
lgb_params = {'metric': {'mae'},
              'num_leaves': 10,
              'learning_rate': 0.02,
              'feature_fraction': 0.8,
              'max_depth': 5,
              'verbose': 0,
              'num_boost_round': 2000,
              'early_stopping_rounds': 200,
              'nthread': -1}

"""The code sets up the LightGBM datasets for training and validation ('lgbtrain' and 'lgbval') with specified features and labels. It then trains the LightGBM model using 'lgb_params' with early stopping based on the validation set, and evaluates the model's performance using SMAPE on the validation set, which is then calculated on the predicted target values ('y_pred_val') and the true target values ('Y_val').





"""

lgbtrain = lgb.Dataset(data=X_train, label=Y_train, feature_name=cols)
lgbval = lgb.Dataset(data=X_val, label=Y_val, reference=lgbtrain, feature_name=cols)

model = lgb.train(lgb_params, lgbtrain,
                  valid_sets=[lgbtrain, lgbval],
                  num_boost_round=lgb_params['num_boost_round'],
                  early_stopping_rounds=lgb_params['early_stopping_rounds'],
                  feval=lgbm_smape,
                  verbose_eval=100)

y_pred_val = model.predict(X_val, num_iteration=model.best_iteration)

smape(np.expm1(y_pred_val), np.expm1(Y_val))

"""The code separates the original DataFrame 'df' into the training set and the test set based on the presence of NaN values in the 'sales' column. It creates 'X_train' and 'X_test' as the feature matrices and 'Y_train' as the target variable containing non-NaN sales data for training.





"""

#Final Model

train = df.loc[~df.sales.isna()]
Y_train = train['sales']
X_train = train[cols]

test = df.loc[df.sales.isna()]
X_test = test[cols]

"""The code sets up LightGBM parameters in the 'lgb_params' dictionary and initializes the LightGBM dataset 'lgbtrain_all' using the entire training data. Then, it trains the LightGBM model on the full training data with 'lgb_params', using the optimal number of boosting rounds obtained from the earlier trained model ('model.best_iteration'). The model is then used to make predictions on the test set, and the results are stored in 'test_preds'.





"""

lgb_params = {'metric': {'mae'},
              'num_leaves': 10,
              'learning_rate': 0.02,
              'feature_fraction': 0.8,
              'max_depth': 5,
              'verbose': 0,
              'nthread': -1,
              "num_boost_round": model.best_iteration}

# LightGBM dataset
lgbtrain_all = lgb.Dataset(data=X_train, label=Y_train, feature_name=cols)

model = lgb.train(lgb_params, lgbtrain_all, num_boost_round=model.best_iteration)
test_preds = model.predict(X_test, num_iteration=model.best_iteration)

"""The code creates a DataFrame 'forecast' containing the predicted sales for each 'date', 'store', and 'item' in the test set based on the model's predictions ('test_preds'). Then, it filters the data for 'store' 1 and 'item' 1 from 'forecast', sets the 'date' column as the index, and plots the sales forecast for this specific store and item over time using Matplotlib, with the line color set to green and the specified figure size.





"""

forecast = pd.DataFrame({"date":test["date"],
                        "store":test["store"],
                        "item":test["item"],
                        "sales":test_preds
                        })

forecast[(forecast.store == 1) & (forecast.item == 1)].set_index("date").sales.plot(color = "green",
                                                                                    figsize = (20,9),
                                                                                    legend=True, label = "Store 1 Item 1 Forecast");

"""The code first filters the 'train' DataFrame for 'store' 1 and 'item' 17, sets the 'date' column as the index, and plots the historical sales data for this specific store and item. Then, it does the same for the 'forecast' DataFrame, plotting the sales forecast for the same store and item. Both plots are displayed on the same graph, with different colors to distinguish between historical sales and sales forecast.





"""

train[(train.store == 1) & (train.item == 17)].set_index("date").sales.plot(figsize = (20,9),legend=True, label = "Store 1 Item 17 Sales")
forecast[(forecast.store == 1) & (forecast.item == 17)].set_index("date").sales.plot(legend=True, label = "Store 1 Item 17 Forecast");

df.shape