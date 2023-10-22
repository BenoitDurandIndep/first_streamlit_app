# launch with 
# cd first_streamlit_app
# streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

AWS_FRUIT_MACROS="https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
URL_FRUITYVICE="https://fruityvice.com/api/fruit/"

def get_fuityvice_data(this_fruit_choice):
    fruityvice_response = requests.get(URL_FRUITYVICE+this_fruit_choice)
    return pd.json_normalize(fruityvice_response.json()) 

# using Snowflake
def get_fruit_load_list():   
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('"+new_fruit+"')")
        return "Thanks for adding "+new_fruit

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
try:
    fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        st.error("Please select a fruit to get information.")
    else:
        st.dataframe(get_fuityvice_data(fruit_choice))

except URLError as e:
    st.error()


st.header("VIEW Our Fruit List - Add Your Favorites!")
if st.button("Get Fruit List"):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows=get_fruit_load_list()
    my_cnx.close()
    st.dataframe(my_data_rows,column_config={"0":"Fruits"})


add_my_fruit = st.text_input('What fruit would you like to add?','')
if st.button("Add a Fruit to the List"):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    back_from_function=insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    st.text(back_from_function)
