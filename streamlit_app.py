import streamlit as st
import pandas as pd
import requests

AWS_FRUIT_MACROS="https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
URL_FRUITYVICE="https://fruityvice.com/api/fruit/"


my_fruit_list = pd.read_csv(AWS_FRUIT_MACROS)
my_fruit_list = my_fruit_list.set_index('Fruit')

st.title("Nice New App for the restaurant")

st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = st.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")
fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)
fruityvice_response = requests.get(URL_FRUITYVICE+fruit_choice)

# normalize json and print it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)

