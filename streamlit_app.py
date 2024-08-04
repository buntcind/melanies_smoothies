# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Chose the fruits you want in your custom Smoothie !
    """
)
name_on_order = st.text_input("Name of the smoothie:")
st.write("The name of the Smoothie will be:", name_on_order)


cnx=st.connection("snowflake");
session=cnx.session();
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    "Chose up to 5 ingredients :",
    my_dataframe
)
if ingredients_list:  
    ingredients_string='';
    #st.write("You selected:", ingredients_list)
    #st.text(ingredients_list)
    

    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit + ' '

    #st.text(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    #st.write(my_insert_stmt)

    time_to_insert=st.button('Submit Order')

    if time_to_insert:
             session.sql(my_insert_stmt).collect()
        
st.success('Your Smoothie is ordered!', icon="✅")


import requests

if ingredients_list:  
    ingredients_string='';

    for fruite_chosen in ingredients_list:
        ingredients_string+=fruite_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruite_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruite_chosen,' is ', search_on, '.')
        
        st.subheader(fruite_chosen+ " Nutrition Information")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruite_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
