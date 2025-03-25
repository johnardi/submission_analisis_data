import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

from babel.numbers import format_currency
sns.set(style='dark')

file_path = os.path.abspath("./all_data.csv")
all_df = pd.read_csv(file_path)

datetime_columns = ["date"]
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)
    
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["date"].min()
max_date = all_df["date"].max()
    
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://www.logoai.com/oss/icons/2021/10/27/NTs7EMHlHtbJE3B.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date Filter',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.header('Air Quality in Tiantan')

main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]

st.subheader("PM2.5 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["PM2.5"], label="PM2.5")
plt.xlabel("Year")
plt.ylabel("Concentration (µg/m3)")
plt.legend()
st.pyplot(fig)


st.subheader("PM10 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["PM10"], label="PM10")
plt.xlabel("Year")
plt.ylabel("Concentration (µg/m3)")
plt.legend()
st.pyplot(fig)

st.subheader("SO2 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["SO2"], label="SO2")
plt.xlabel("Year")
plt.ylabel("Concentration (µg/m3)")
plt.legend()
st.pyplot(fig)

st.subheader("NO2 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["NO2"], label="NO2")
plt.xlabel("Year")
plt.ylabel("Concentration (µg/m3)")
plt.legend()
st.pyplot(fig)

st.subheader("CO Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["CO"], label="CO")
plt.xlabel("Year")
plt.ylabel("Concentration (µg/m3)")
plt.legend()
st.pyplot(fig)

st.subheader("O3 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["O3"], label="O3")
plt.xlabel("Year")
plt.ylabel("Concentration (µg/m3)")
plt.legend()
st.pyplot(fig)


st.subheader("CO Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["CO"], label="CO")
plt.xlabel("Year")
plt.ylabel("Concentration (µg/m3)")
plt.legend()
st.pyplot(fig)


st.subheader("Temperatur")
groupByYear = main_df.groupby("date").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["TEMP"], label="TEMP")
plt.xlabel("Year")
plt.ylabel("°C")
plt.legend()
st.pyplot(fig)
