import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv('data/modified_logs_OMBA-Strategy Execution-2023_20230815-1405.csv')
df = df.sort_values('Time')
# Retain only the necessary columns
df = df[['Time', 'User full name']]
# Convert the 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%d/%m/%y, %H:%M')
# Group by date and count accesses per user per day
daily_counts = df.groupby('Time').size()

# Use Auto ARIMA to determine p, d, q
stepwise_model = auto_arima(daily_counts, trace=True, suppress_warnings=True,
                            seasonal=False, stepwise=True)
print(stepwise_model.summary())

# Best order for ARIMA
best_order = stepwise_model.order
print(f"Best values for (p, d, q): {best_order}")

# ARIMA model with best values
model = ARIMA(daily_counts, order=best_order)
model_fit = model.fit(disp=0)
print(model_fit.summary())

# Forecast
forecast = model_fit.forecast(steps=10)[0]
print(forecast)
