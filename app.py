import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data_rostat.csv", skiprows=2, encoding="cp1251")

data.columns = ["Region", "Code", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]

columns_to_plot = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

st.title("Отображение данных из data_rostat.csv")

st.dataframe(data)

st.line_chart(data[columns_to_plot])
