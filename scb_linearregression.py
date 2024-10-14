# -*- coding: utf-8 -*-
"""SCB_LinearRegression

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_Vpy2alCyZvx8AtvBGOB3ISv4m4GS57o

# Project description

Predicting explained variance score. Data gathered is number of companies with 100 percent ownership by region and year

Statistics used:

https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__OE__OE0108/KomFtgK100/table/tableViewLayout1/

Python module for SCB api usage:

https://github.com/kirajcg/pyscbwrapper/blob/master/pyscbwrapper.ipynb

# Importing requirements
"""

import json
# from urllib import request, response
import requests
import pandas as pd

from sklearn.metrics import accuracy_score
from sklearn.metrics import explained_variance_score

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn import linear_model

"""# Data gathering and formatting

# Request
"""

api_url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/OE/OE0108/KomFtgK100"

user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64"
headers = {
    'Content-Type' : 'application/json',
    "User-Agent" : user_agent,

    }


payload = {
  "query": [
    {
      "code": "ContentsCode",
      "selection": {
        "filter": "item",
        "values": [
          "00000190"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}


json_data = json.dumps(payload)

"""# Data

**Request**
"""

api_call = requests.post(url=api_url, data=json_data, headers=headers)

if api_call.status_code != 200:
  print("Status code:", api_call.status_code)
  print("Reason:", api_call.reason)
  print("Response headers:", api_call.headers)
else:
  print("Status code:", api_call.status_code)
  print("Request successful")
  print("Response headers:", api_call.headers)

json_response = api_call.json()

data_only = json_response.get('data', [])

df = pd.DataFrame(data_only)

df[['region', 'year']] = pd.DataFrame(df['key'].tolist(), index=df.index)

df['year'] = df['year'].str[:4]

df['value'] = df['values'].apply(lambda x: x[0] if isinstance(x, list) else x)

df_pivot = df.pivot(index='region', columns='year', values='value')

df_pivot.to_csv('pivoted_region_years_values.csv')

print("Pivoted data with values saved to pivoted_region_years_values.csv")

df2 = pd.read_csv("pivoted_region_years_values.csv", index_col=False)

# df2.head(20)

"""# Plot raw data

# Predictions
"""

X = df2.drop(columns=["2016", 'region'], axis=1)
y = df2["2016"]


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.3, random_state=45)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# svm = SVC()
linear = linear_model.LinearRegression()

linear.fit(X_train, y_train)

y_pred = linear.predict(X_test)

accuracy = explained_variance_score(y_test, y_pred)

print("Accuracy:", accuracy)

"""**Accuracy with SVM:** 0.5-0.58

**Explained variance score with Linear regression:** 0.99
"""