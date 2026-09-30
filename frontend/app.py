import streamlit as st
import pandas as pd
import requests


# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Streamlit UI for Superkart Sales Prediction
st.title("SuperKart Sales Forecasting App")
st.write("This app predicts the value of monthly sales for a given product in a specific store.")
#st.write("Move the sliders below to adjust values and get a prediction.")

# Instructions
st.markdown("🔍 Enter product and store data to forecast monthly product sales, in USD.\n")


# Collect user inputs
Product_Weight = st.number_input("Product Weight (oz)", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area (linear in.)", min_value=0.0, value=100.0)
Product_MRP = st.number_input("Maximum Retail Price (USD)", min_value=0.0, value=150.0)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])

# zzz change store age/year stuff:
Store_Age_Years = st.slider("Store Age (years)", min_value=0, max_value=50, value=10)

# zzz fix this below with reduced 2 choices now
Product_Type_Category = st.selectbox("Product Type Category", ["Non Perishables", "Perishables"])

# Create input DataFrame
input_data = {
    "Product_Weight": str(Product_Weight),
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": str(Product_Allocated_Area),
    "Product_MRP": str(Product_MRP),
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Store_Age_Years": str(Store_Age_Years),
    "Product_Type_Category": Product_Type_Category
}


if st.button("Predict", type='primary'):
    # Replace with your deployed backend URL
    response = requests.post(
        # zzz replace this below, may be tough to figure out:
        # "https://{BACKEND_URL}/v1/house",
        f"{BACKEND_URL}/v1/house",
        json=input_data
    )

    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Predicted_Sales"]
        st.success(f"🏡 Predicted Monthly Sales Value: **${predicted_sales * 1000:.2f}**")
    else:
        st.error("Error in API request, verify input values")


# Batch Prediction
st.subheader("Batch Prediction")

# look at batch csv upload stuff here:
file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    if st.button("Predict for Batch", type='primary'):
        response = requests.post(
            # "https://{BACKEND_URL}/v1/housebatch",
            f"{BACKEND_URL}/v1/housebatch",
            files={"file": file}
        )

        if response.status_code == 200:
            result = response.json()
            st.header("Batch Prediction Results")
            st.write(result)
        else:
            st.error("Error in API request")
