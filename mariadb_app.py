from mariadb_prompt import prompts
import streamlit as st
import os
import pandas as pd
from openai import OpenAI
import mysql.connector 
from streamlit_ace import st_ace
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt4_response(question, prompts):
    messages = [
        {"role": "system", "content": prompts[0]},
        {"role": "user", "content": question}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content

def read_sql_query(sql):
    conn = mysql.connector.connect(
        database = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password= os.getenv('DB_PASSWORD'),
        host= os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        charset='utf8mb4', 
        collation='utf8mb4_general_ci'
    )
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

if 'current_sql' not in st.session_state:
    st.session_state.current_sql = ""
if 'current_results' not in st.session_state:
    st.session_state.current_results = None
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'error_message' not in st.session_state:
    st.session_state.error_message = None
if 'is_first_generation' not in st.session_state:
    st.session_state.is_first_generation = True


st.set_page_config(page_title="Source-GPT")
st.header("Get Source.one Orders Info")

show_preview = st.toggle("Enable Preview", value=True)

question = st.text_input("Input: ", key="input", value=st.session_state.question)

if st.button("Generate SQL"):
    try:
        st.session_state.question = question
        generated_sql = get_gpt4_response(question, prompts)
        st.session_state.current_sql = generated_sql
        st.session_state.error_message = None
        
        if st.session_state.is_first_generation:
            try:
                df = read_sql_query(generated_sql)
                st.session_state.current_results = df
                st.session_state.is_first_generation = False
            except Exception as e:
                st.session_state.error_message = f"Error executing SQL: {str(e)}"
    except Exception as e:
        st.session_state.error_message = f"Error generating SQL: {str(e)}"

if st.session_state.current_sql:
    st.subheader("Generated SQL Query:")
    
    col1, col2 = st.columns([6, 1])
    with col1:
        edited_sql = st_ace(
            value=st.session_state.current_sql,
            language="sql",
            theme="sqlserver",
            key="sql_editor",
            height=100,
            auto_update=True,
            wrap=True,
            show_gutter=True,
            show_print_margin=True,
            annotations=None,
            min_lines=3,
            keybinding="vscode",
            tab_size=4
        )
    with col2:
        execute_sql = st.button("Run SQL")

    if execute_sql:
        try:
            df = read_sql_query(edited_sql)
            st.session_state.current_results = df
            st.session_state.error_message = None
        except Exception as e:
            st.session_state.error_message = f"Error executing SQL: {str(e)}"

if st.session_state.current_results is not None:
    st.subheader("Query Results:")
    
    results_container = st.container()
    with results_container:
        st.write(f"Number of rows returned: {len(st.session_state.current_results)}")
        
        csv = st.session_state.current_results.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
        )
        
        if show_preview:
            st.table(st.session_state.current_results)

if st.session_state.error_message:
    st.error(st.session_state.error_message)

if question != st.session_state.question:
    st.session_state.is_first_generation = True