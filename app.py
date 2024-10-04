from dotenv import load_dotenv
load_dotenv()
from prompt import prompts

import streamlit as st
import os 
import psycopg2
import pandas as pd
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt4_response(question, prompts):
    messages = [
        {"role": "system", "content": prompts[0]},
        {"role": "user", "content": question}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content

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
    response = get_gpt4_response(question, prompts)
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