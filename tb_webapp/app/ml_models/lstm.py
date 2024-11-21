import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

model = load_model('app/ml_models/lstm_model.keras')

df = pd.read_csv('app/ml_models/diagnosed_final.csv', parse_dates=['DATE'], index_col='DATE')
# Assuming the dataset has a column 'cases' which contains the tuberculosis case counts
data = df['DIAGNOSED'].values

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data.reshape(-1, 1))

# Number of future steps to predict (5 years = 60 months)
future_steps = 60

time_steps = 10 
# Get the last 'time_steps' data points from the dataset
last_sequence = data_scaled[-time_steps:]  # Last sequence for prediction

# Reshape the sequence to [1, timesteps, features]
current_input = last_sequence.reshape(1, time_steps, 1)

# Placeholder for future predictions
future_predictions = []

for _ in range(future_steps):
    # Predict the next value
    predicted_scaled = model.predict(current_input, verbose=0)
    
    # Save the prediction (inverse transform later)
    future_predictions.append(predicted_scaled[0, 0])
    
    # Update the input sequence: remove the oldest value, add the predicted value
    current_input = np.append(current_input[:, 1:, :], [[[predicted_scaled[0,0]]]], axis=1)

# Inverse transform the predictions to the original scale
future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

# Create a timeline for the predictions
import pandas as pd

df['DATE'] = df.index

last_date = pd.to_datetime(df['DATE'].iloc[-1])  # Last date in the dataset
future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, future_steps + 1)]

# Create a DataFrame for the future predictions
future_df = pd.DataFrame({'DATE': future_dates, 'DIAGNOSED': future_predictions.flatten()})


df.reset_index(drop=True, inplace=True)
future_df.reset_index(drop=True, inplace=True)

result = pd.merge(df, future_df, left_on=['DATE', 'DIAGNOSED'], right_on=['DATE', 'DIAGNOSED'], how='outer')
result.index = result['DATE']