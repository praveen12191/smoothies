# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Example Streamlit App :balloon:")

name_on_order = st.text_input("Movie title")
st.write("The current movie title is", name_on_order)

# Get the current credentials
cns = st.connection("snowflake")
session = cns.session()

# Fetch fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()

# Create a multiselect widget for fruit options
data = st.multiselect('data', [row['FRUIT_NAME'] for row in my_dataframe], max_selections=5)
st.write(data)

if data:
    str = ' '
    for i in data:
        str+= i + ' '
        st.subheader(i + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + i)
        st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(str)
    insert_query = f"""
    INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER) 
    VALUES ('{str}', '{name_on_order}')
    """
    st.write(insert_query)
    session.sql(insert_query).collect()
    st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")
