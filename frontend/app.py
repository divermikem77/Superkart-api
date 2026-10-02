import streamlit as st
import pandas as pd
import requests

# "backend" is the service name in docker-compose.yml
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Forecasting App")
st.write("Predicts sales for a given product in a specific store.")

Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area (fraction, e.g. 0.027)",
                                         min_value=0.0, max_value=1.0, value=0.027, format="%.3f")
Product_MRP = st.number_input("Maximum Retail Price (USD)", min_value=0.0, value=150.0)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
Store_Age_Years = st.slider("Store Age (years)", min_value=0, max_value=50, value=10)
Product_Type_Category = st.selectbox("Product Type Category", ["Non Perishables", "Perishables"])
Product_Id_char = st.selectbox("Product Id prefix", ["FD", "DR", "NC"])

input_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category,
    "Product_Id_char": Product_Id_char,
}

if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data)
    if response.status_code == 200:
        sales = response.json()["Predicted_Sales"]
        st.success(f"Predicted Sales: **${sales:,.2f}**")
    else:
        st.error(f"Error in API request: {response.text}")

st.subheader("Batch Prediction")
file = st.file_uploader("Upload CSV file", type=["csv"])
if file is not None and st.button("Predict for Batch", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": file})
    if response.status_code == 200:
        st.header("Batch Prediction Results")
        st.write(response.json())
    else:
        st.error(f"Error in API request: {response.text}")
