import streamlit as st
import pandas as pd
import numpy as np
st.scatter_chart(df[['Cost', 'Sales']])

# Load Data
df = pd.read_csv("Nassau Candy Distributor (1).csv")

# Data Cleaning
df = df[df['Sales'] > 0]
df = df[df['Gross Profit'].notna()]
df['Units'] = df['Units'].replace(0, np.nan)

# KPIs
df['Gross Margin'] = df['Gross Profit'] / df['Sales']
df['Profit per Unit'] = df['Gross Profit'] / df['Units']

# Sidebar Filters
st.sidebar.title("Filters")
division = st.sidebar.multiselect("Select Division", df['Division'].unique())
date_range = st.sidebar.date_input("Select Date Range", [])

margin_threshold = st.sidebar.slider("Margin Threshold", 0.0, 1.0, 0.2)

if division:
    df = df[df['Division'].isin(division)]

# Title
st.title("Nassau Candy Profitability Dashboard")

# -------------------------------
# Product Profitability Overview
# -------------------------------
st.header("Product Profitability")

product_profit = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Gross Profit': 'sum',
    'Gross Margin': 'mean'
}).reset_index()

top_products = product_profit.sort_values(by='Gross Profit', ascending=False).head(10)

st.subheader("Top 10 Products by Profit")
st.dataframe(top_products)

# -------------------------------
# Division Performance
# -------------------------------
st.header("Division Performance")

division_perf = df.groupby('Division').agg({
    'Sales': 'sum',
    'Gross Profit': 'sum',
    'Gross Margin': 'mean'
}).reset_index()

st.bar_chart(division_perf.set_index('Division')[['Sales', 'Gross Profit']])

# -------------------------------
# Cost vs Sales Scatter
# -------------------------------
st.header("Cost vs Sales Analysis")

fig, ax = plt.subplots()
ax.scatter(df['Cost'], df['Sales'])
ax.set_xlabel("Cost")
ax.set_ylabel("Sales")
st.pyplot(fig)

# -------------------------------
# Pareto Analysis
# -------------------------------
st.header("Profit Concentration (Pareto)")

pareto = product_profit.sort_values(by='Gross Profit', ascending=False)
pareto['Cumulative %'] = pareto['Gross Profit'].cumsum() / pareto['Gross Profit'].sum()

st.line_chart(pareto['Cumulative %'])

# -------------------------------
# Margin Risk Products
# -------------------------------
st.header("Low Margin Risk Products")

risk_products = df[df['Gross Margin'] < margin_threshold]

st.dataframe(risk_products[['Product Name', 'Sales', 'Gross Margin']])
