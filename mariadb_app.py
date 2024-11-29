from mariadb_prompt import prompts
import streamlit as st
import os
import pandas as pd
from openai import OpenAI
import mysql.connector 
from streamlit_ace import st_ace
from dotenv import load_dotenv
import math
load_dotenv(override=True)

api_key_openai = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key_openai)

def sanitize_sql(sql_response):
    return sql_response.replace("```sql", "").replace("```", "")

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

def paginate_dataframe(df, page_number, rows_per_page):
    """Helper function to paginate a dataframe"""
    total_pages = math.ceil(len(df) / rows_per_page)
    start_idx = (page_number - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, len(df))
    return df.iloc[start_idx:end_idx], total_pages

# Initialize session state variables
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
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
if 'rows_per_page' not in st.session_state:
    st.session_state.rows_per_page = 50
if 'total_rows' not in st.session_state:
    st.session_state.total_rows = 0

# Page configuration
st.set_page_config(page_title="Source-GPT")
st.header("Get Source.one Orders Info")

show_preview = st.toggle("Enable Preview", value=True)

question = st.text_input("Input: ", key="input")

# Reset state when question changes
if question != st.session_state.question:
    st.session_state.current_sql = ""
    st.session_state.current_results = None
    st.session_state.is_first_generation = True
    st.session_state.error_message = None
    st.session_state.question = question
    st.session_state.page_number = 1

# Generate SQL button logic
if st.button("Generate SQL"): 
    try:
        st.session_state.question = question
        sql_response_from_ai = get_gpt4_response(question, prompts)
        generated_sql = sanitize_sql(sql_response_from_ai)
        print(generated_sql)
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

# Display SQL editor
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

    # Execute edited SQL
    if execute_sql:
        try:
            df = read_sql_query(edited_sql)
            st.session_state.current_results = df
            st.session_state.error_message = None
        except Exception as e:
            st.session_state.error_message = f"Error executing SQL: {str(e)}"

# Display results
if st.session_state.current_results is not None:
    st.subheader("Query Results:")
    
    results_container = st.container()
    with results_container:
        total_rows = len(st.session_state.current_results)
        st.write(f"Number of rows returned: {total_rows}")
        
        # Download button
        csv = st.session_state.current_results.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
        )
        
        if show_preview and total_rows > 0:
            # Pagination controls
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                st.session_state.rows_per_page = st.selectbox(
                    "Rows per page:",
                    options=[10, 20, 50, 100],
                    index=2  # Default to 50
                )
            
            # Calculate total pages
            total_pages = math.ceil(total_rows / st.session_state.rows_per_page)
            
            with col2:
                st.session_state.page_number = st.number_input(
                    "Page",
                    min_value=1,
                    max_value=total_pages,
                    value=st.session_state.page_number
                )
            
            with col3:
                st.write(f"Total pages: {total_pages}")
            
            # Paginate the data
            paginated_df, _ = paginate_dataframe(
                st.session_state.current_results,
                st.session_state.page_number,
                st.session_state.rows_per_page
            )
            
            # Display the paginated data
            st.table(paginated_df)
            
            # Navigation buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                if st.button("⏮️ First"):
                    st.session_state.page_number = 1
                    st.rerun()
            
            with col2:
                if st.button("⏪ Previous") and st.session_state.page_number > 1:
                    st.session_state.page_number -= 1
                    st.rerun()
            
            with col3:
                if st.button("⏩ Next") and st.session_state.page_number < total_pages:
                    st.session_state.page_number += 1
                    st.rerun()
            
            with col4:
                if st.button("⏭️ Last"):
                    st.session_state.page_number = total_pages
                    st.rerun()

# Display error messages
if st.session_state.error_message:
    st.error(st.session_state.error_message)

# Reset first generation flag if question changes
if question != st.session_state.question:
    st.session_state.is_first_generation = True