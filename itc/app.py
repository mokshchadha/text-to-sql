import streamlit as st
import os
import pandas as pd
from openai import OpenAI
import psycopg2
from psycopg2 import Error
from streamlit_ace import st_ace
from dotenv import load_dotenv
import math
from typing import Dict, Any, Tuple, Optional

# Database configuration
DB_CONFIG = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost',
    'port': '5454'
}

# System prompt for SQL generation
META_PROMPT = '''
You are an expert in converting English questions to SQL queries, working for source.one
And you have the access to tracker  related information for the company ITC you only generate SELECT query do not generate DELETE, ALTER, DROP or TRUNCATE queries
The Postgres database has a table named tracker_responses with the following structure:
CREATE TABLE IF NOT EXISTS tracker_responses (
    s_no SERIAL PRIMARY KEY,
    submitted_time TIMESTAMP,
    tl TEXT,
    ds TEXT,
    outlet_name TEXT,
    soh INTEGER,
    number_of_packets INTEGER
);

Make sure you only return executable sql and no extra information 
The SQL code should not have ``` in the beginning or end and should not include the word 'sql' in the output.
'''

class DatabaseConnection:
    @staticmethod
    def get_connection():
        try:
            return psycopg2.connect(**DB_CONFIG)
        except Error as e:
            st.error(f"Error connecting to PostgreSQL database: {e}")
            raise

    @staticmethod
    def read_sql_query(sql: str) -> pd.DataFrame:
        with DatabaseConnection.get_connection() as conn:
            return pd.read_sql_query(sql, conn)

class OpenAIClient:
    def __init__(self):
        load_dotenv(override=True)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_sql_query(self, question: str) -> str:
        messages = [
            {"role": "system", "content": META_PROMPT},
            {"role": "user", "content": question}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return self.sanitize_sql(response.choices[0].message.content)

    @staticmethod
    def sanitize_sql(sql_response: str) -> str:
        return sql_response.replace("```sql", "").replace("```", "").strip()

class DataPaginator:
    @staticmethod
    def paginate_dataframe(df: pd.DataFrame, page_number: int, rows_per_page: int) -> Tuple[pd.DataFrame, int]:
        total_pages = math.ceil(len(df) / rows_per_page)
        start_idx = (page_number - 1) * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(df))
        return df.iloc[start_idx:end_idx], total_pages

class StreamlitApp:
    def __init__(self):
        self.init_session_state()
        self.openai_client = OpenAIClient()
        
    @staticmethod
    def init_session_state():
        default_states = {
            'current_sql': "",
            'current_results': None,
            'question': "",
            'error_message': None,
            'is_first_generation': True,
            'page_number': 1,
            'rows_per_page': 50,
            'total_rows': 0,
            'editor_key': 0
        }
        for key, value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def setup_page(self):
        st.set_page_config(page_title="Tracker-GPT")
        st.header("Get ITC tracker information")
        self.show_preview = st.toggle("Enable Preview", value=True)
        self.question = st.text_input("Input: ", key="input")

    def handle_question_change(self):
        if self.question != st.session_state.question:
            st.session_state.current_sql = ""
            st.session_state.current_results = None
            st.session_state.is_first_generation = True
            st.session_state.error_message = None
            st.session_state.question = self.question
            st.session_state.page_number = 1

    def generate_sql(self):
        if st.button("Generate SQL"):
            try:
                generated_sql = self.openai_client.get_sql_query(self.question)
                st.session_state.current_sql = generated_sql
                st.session_state.error_message = None
                st.session_state.editor_key += 1

                if st.session_state.is_first_generation:
                    self.execute_sql(generated_sql)
                    st.session_state.is_first_generation = False
            except Exception as e:
                st.session_state.error_message = f"Error generating SQL: {str(e)}"

    def display_sql_editor(self):
        if st.session_state.current_sql:
            st.subheader("Generated SQL Query:")
            
            col1, col2 = st.columns([6, 1])
            with col1:
                edited_sql = st_ace(
                    value=st.session_state.current_sql,
                    language="sql",
                    theme="sqlserver",
                    key=f"sql_editor_{st.session_state.editor_key}",
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
                if st.button("Run SQL"):
                    self.execute_sql(edited_sql)

    def execute_sql(self, sql: str):
        try:
            df = DatabaseConnection.read_sql_query(sql)
            st.session_state.current_results = df
            st.session_state.error_message = None
        except Exception as e:
            st.session_state.error_message = f"Error executing SQL: {str(e)}"

    def display_results(self):
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
                
                if self.show_preview and total_rows > 0:
                    self.handle_pagination(total_rows)

    def handle_pagination(self, total_rows: int):
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            st.session_state.rows_per_page = st.selectbox(
                "Rows per page:",
                options=[10, 20, 50, 100],
                index=2
            )
        
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
        
        paginated_df, _ = DataPaginator.paginate_dataframe(
            st.session_state.current_results,
            st.session_state.page_number,
            st.session_state.rows_per_page
        )
        
        st.table(paginated_df)
        self.display_navigation_buttons(total_pages)

    def display_navigation_buttons(self, total_pages: int):
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

    def display_errors(self):
        if st.session_state.error_message:
            st.error(st.session_state.error_message)

    def run(self):
        self.setup_page()
        self.handle_question_change()
        self.generate_sql()
        self.display_sql_editor()
        self.display_results()
        self.display_errors()

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()