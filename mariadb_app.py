from mariadb_prompt import prompts
import streamlit as st
import os
import pandas as pd
from openai import OpenAI
import mysql.connector 

# Initialize OpenAI client
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
        database='mydb', 
        user='myuser',
        password='mypassword',
        host='localhost',
        port='5454',
        charset='utf8mb4', 
        collation='utf8mb4_general_ci'
    )
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

# Streamlit App
st.set_page_config(page_title="GPT - Source.one")
st.header("Get Source.one Orders Info")

# Add preview toggle
show_preview = st.toggle("Enable Preview", value=True)

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gpt4_response(question, prompts)
    st.subheader("Generated SQL Query:")
    
    # Make SQL query editable and add execute button
    col1, col2 = st.columns([6, 1])
    with col1:
        edited_sql = st.text_area("Edit SQL if needed:", value=response, height=100, key="sql_editor")
    with col2:
        execute_sql = st.button("Execute SQL", key="execute_sql")

    try:
        # Execute SQL when either the main submit button is pressed or execute_sql button is pressed
        if submit or execute_sql:
            print("question: ", question)
            df = read_sql_query(edited_sql)  # Use the edited SQL instead of the original response

            # Create a container for download button and row count
            result_header = st.container()
            with result_header:
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

            # Only show preview if enabled
            if show_preview:
                st.subheader("Query Results:")
                # Display the results in a SQL-like table format
                st.table(df)
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")