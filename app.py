from dotenv import load_dotenv
load_dotenv()
from prompt import prompts

import streamlit as st
import os 
import psycopg2
import pandas as pd

import google.generativeai as genai 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompts):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([prompts[0], question])
    return response.text

def read_sql_query(sql):
    conn = psycopg2.connect(
        dbname='mydb',
        user='myuser',
        password='mypassword',
        host='localhost',
        port='5444'
    )
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df



# Streamlit App
st.set_page_config(page_title="Chat with database")
st.header("Get Source.one Orders Info")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompts)
    st.subheader("Generated SQL Query:")
    st.code(response, language="sql")

    try:
        df = read_sql_query(response)
        st.subheader("Query Results:")
        
        # Display the results in a SQL-like table format
        st.table(df)

        # Show the number of rows returned
        st.write(f"Number of rows returned: {len(df)}")

        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")