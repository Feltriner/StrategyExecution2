import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('data/modified_logs_OMBA-Strategy Execution-2023_20230815-1405.csv')
df = df.sort_values('Time', ascending=True).reset_index(drop=True)
# Retain only the necessary columns
df = df[['Time', 'User full name']]
# Convert the 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%d/%m/%y, %H:%M')

# Group by date and count accesses per user per day
daily_counts = df.groupby('Time').size()

# Ensure daily_counts uses a datetime index
daily_counts.index = pd.to_datetime(daily_counts.index)

# ARIMA model with derived p, d, and q values
p, d, q = 1, 1, 4  # These are example values. Replace them with the values you've determined.
model = ARIMA(daily_counts, order=(p,d,q))
model_fit = model.fit()

# Make predictions
forecast_steps = 1000
forecast_values = model_fit.forecast(steps=forecast_steps)

# Here we modify the creation of the forecast index
forecast_index = pd.date_range(start=daily_counts.index[-1] + pd.Timedelta(minutes=1), periods=forecast_steps)
forecast_series = pd.Series(forecast_values, index=forecast_index)

# Display results
print(forecast_series)

# Plot the prediction and the original data
plt.figure(figsize=(12, 6))
daily_counts.plot(label="Actual Data")
forecast_series.plot(label="Forecast", color='red', linestyle='--')
plt.legend()
plt.title('ARIMA Forecast')
plt.show()
