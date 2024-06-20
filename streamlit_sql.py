import streamlit as st
import pandas as pd
from streamlit_modal import Modal
from sqldemo import *
#------------------------------------------

conn, cursor = db_connection('visual_interface_chat\sakila_master.db')

modal = Modal('Database schema', key="image_modal", max_width=700)


def main():
        

    st.title("Chat")

    with st.sidebar:
        st.image(r'data/00. Marca DATAI_red.png')
        st.image(r'data/Logo-BBVA_edited-removebg-preview.png')

        st.title('ChatGPT SQL-Lite Master')


        if st.button("Show Database Schema"):
            modal.open()

        # Check if the modal is open and display the content inside it
        if modal.is_open():
            with modal.container():
                st.image(r'visual_interface_chat\data\sakila_db_schema.png', caption='Database schema')


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        if message["role"]=="user":

            with st.chat_message(message["role"], avatar="🤵‍♂️"):

                st.markdown(message["content"])

        else:

            with st.chat_message(message["role"], avatar="🤖"):

                st.markdown(message["content"][0])

                try:
                    st.dataframe(pd.DataFrame(message["content"][1], columns=message["content"][2]))
                except Exception as e:
                    st.markdown(f':red[{e}]')



    if prompt := st.chat_input("Introduzca su duda..."):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="🤵‍♂️"):

            st.markdown(prompt)


        with st.chat_message("assistant", avatar="🤖"):


            for i in range(5):
                query = answer_query(prompt)
                is_query = check_query_message(query)
                answer = answer_table(cursor, is_query)

                st.markdown(is_query)

                try:
                    column_names = [description[0] for description in cursor.description]        
                    st.dataframe(pd.DataFrame(answer, columns=column_names))
                    break
                except Exception as e:
                    column_names=[]
                    st.markdown(f'Fixing error {i} :red[{e}]')
    
        st.session_state.messages.append({"role": "assistant", "content": [is_query, answer, column_names]})




if __name__ == '__main__':

    main()