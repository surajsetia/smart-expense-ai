import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle


df = pd.read_csv('expense_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Day'] = df['Date'].dt.day


daily_expense = df.groupby('Day')['Amount'].sum().reset_index()

X = daily_expense[['Day']]
y = daily_expense['Amount']


model = LinearRegression()
model.fit(X, y)


with open('model/predictor.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved.")
