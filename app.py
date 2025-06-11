import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
from utils.insights import spending_insights

with open('model/predictor.pkl', 'rb') as f:
    model = pickle.load(f)


try:
    df = pd.read_csv('expense_data.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  
except:
    df = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
    st.warning("No expense data found. Please add your first expense.")


st.set_page_config(page_title="Smart Expense Manager", layout="centered")
st.title("💰 Smart Expense Manager with AI")
st.markdown("Track, Visualize, and Predict your expenses intelligently!")


st.header("➕ Add New Expense")
with st.form("expense_form"):
    date = st.date_input("Date")
    amount = st.number_input("Amount (₹)", min_value=1.0)
    category = st.selectbox("Category", ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Other"])
    description = st.text_input("Description")
    submit = st.form_submit_button("Add Expense")

if submit:
    new_data = pd.DataFrame([[date, amount, category, description]],
                            columns=["Date", "Amount", "Category", "Description"])
    new_data['Date'] = pd.to_datetime(new_data['Date']) 
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("expense_data.csv", index=False)
    st.success("✅ Expense added!")



st.subheader("📄 Recent Expenses")
st.dataframe(df.tail(5))


st.subheader("📊 Spending Distribution")
if not df.empty:
    chart_df = df.groupby("Category")["Amount"].sum().reset_index()
    fig = px.pie(chart_df, names='Category', values='Amount', title='Expenses by Category')
    st.plotly_chart(fig)


st.subheader("💡 AI Suggestions")
for tip in spending_insights(df):
    st.info(tip)


st.subheader("🔮 Predicted Spending (Tomorrow)")
if not df.empty:
    df['Day'] = df['Date'].dt.day
    next_day = df['Day'].max() + 1
    prediction = model.predict([[next_day]])
    st.success(f"Predicted expense for day {next_day}: ₹{prediction[0]:.2f}")


st.subheader("⬇️ Download All Expenses")
st.download_button("Download CSV", df.to_csv(index=False), file_name="expenses.csv", mime="text/csv")
