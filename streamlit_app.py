# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


st.title("Example Streamlit App :balloon:")


name_on_order = st.text_input("Movie title")
st.write("The current movie title is", name_on_order)

# Get the current credentials
cns = st.connection("snowflake")
session = cns.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


data = st.multiselect('data',my_dataframe,max_selections=5)

st.write(data)
if(data):
    str = ''
    for i in data:
    	str+=i+' '
      st.subheader(i + 'Nutrition Information')
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+i)
	fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    # st.text(fruityvice_response.json())
    st.write(str)
    insert_query = """ insert into smoothies.public.orders(INGREDIENTS,
	NAME_ON_ORDER) values('"""+str+"""','"""+name_on_order+"""')"""
    st.write(insert_query)
    session.sql(insert_query).collect()
    st.success('Your Smoothie is ordered! '+name_on_order, icon="✅")
