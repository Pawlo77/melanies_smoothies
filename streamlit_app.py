import requests
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
    """
    Choose fruits you want in your custom smoothie!
    """
)

name_on_order = st. text_input ( 'Name on Smoothie: ')
# st.write('The name on your Smoothie will be:', name_on_order)

# session = get_active_session()
cnx = st. connection ("snowflake")
session = cnx.session()

my_dataframe = session.table(
    "smoothies.public.fruit_options"
    ).select(col("FRUIT_NAME")).order_by(col("FRUIT_NAME"))

ingredients_list = st.multiselect(
    "Choose up to 5 indigrents:",
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = " ".join(ingredients_list) + " "
    # st.text(ingredients_string)

    my_insert_stmt = """
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')
    """
    # st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    for fruit_chosen in ingredients_list:
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        sf_df = st. dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# st.text(smoothiefroot_response).json()
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# display in gui
# st.dataframe(data=my_dataframe, use_container_width=True)

# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Apple", "Peaches"),
# )
# st.write("Your favourite fruit is:", option)
