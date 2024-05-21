# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark import Session

# Write directly to the app
st.title("Example Streamlit App :balloon:")

name_on_order = st.text_input("Movie title")
st.write("The current movie title is", name_on_order)

# Snowflake connection parameters
connection_parameters = {
    "account": "IPTPOUW.YQ86930",
    "user": "PRAVEEN",
    "password": "Qwert12345@",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC",
    "client_session_keep_alive": True
}

try:
    # Create a Snowflake session
    session = Session.builder.configs(connection_parameters).create()

    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

    data = st.multiselect('data', my_dataframe.collect(), max_selections=5)
    st.write(data)
    if data:
        ingredients_str = ' '.join(data)
        st.write(ingredients_str)
        insert_query = f"""
        INSERT INTO smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER) 
        VALUES ('{ingredients_str}', '{name_on_order}')
        """
        st.write(insert_query)
        session.sql(insert_query).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")

except Exception as e:
    st.error(f"Error connecting to Snowflake: {e}")
