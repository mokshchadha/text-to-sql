#!/bin/bash

pip install -r requirements.txt 

# Find and kill any process running on port 8501
echo "Checking for processes on port 8501..."
PORT_PID=$(lsof -ti:8501)

if [ ! -z "$PORT_PID" ]; then
    echo "Found process $PORT_PID running on port 8501. Terminating..."
    kill -9 $PORT_PID
    echo "Process terminated."
else
    echo "No process found running on port 8501."
fi

# Wait a moment to ensure the port is cleared
sleep 2

# Start the Streamlit app
echo "Starting Streamlit application..."

# Replace 'app.py' with your actual streamlit file path
streamlit run mariadb_app.py &

# Get the new process ID
NEW_PID=$!
echo "Streamlit started with PID: $NEW_PID"