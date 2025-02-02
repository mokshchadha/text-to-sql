#!/bin/bash

# Install requirements
pip install -r requirements.txt 

# Create .streamlit directory if it doesn't exist
mkdir -p .streamlit

touch .streamlit/secrets.toml

# Create or update config.toml with memory settings
cat > .streamlit/config.toml << EOL
[server]
maxUploadSize = 1000
maxMessageSize = 1000
port = 8501
address = "0.0.0.0"
enableXsrfProtection = true
enableCORS = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
EOL

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

# Clear system cache
echo "Clearing system cache..."
sync
echo 3 > /proc/sys/vm/drop_caches

# Set environment variables for Python memory management
export PYTHONUNBUFFERED=1
export PYTHONUTF8=1
export MALLOC_TRIM_THRESHOLD_=100000

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Clear environment variables
unset $(env | grep '^STREAMLIT_' | cut -d= -f1)
# Then load new ones from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Clear Streamlit cache
streamlit cache clear

echo "Starting Streamlit application with nohup..."

# Start Streamlit with nohup and memory optimizations
nohup streamlit run mariadb_app.py \
    --server.maxUploadSize=1000 \
    --server.maxMessageSize=1000 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=true \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    > streamlit.log 2>&1 &

# Get the new process ID
NEW_PID=$!
echo "Streamlit started with PID: $NEW_PID"

# Set resource limits for the process
if [ ! -z "$NEW_PID" ]; then
    echo "Setting resource limits for PID: $NEW_PID"
    # Set memory limit to 4GB (4194304 KB)
    ulimit -v 4194304
    # Set maximum number of open files
    ulimit -n 4096
fi

# Monitor initial memory usage
echo "Initial memory usage:"
ps -o pid,ppid,%cpu,%mem,cmd -p $NEW_PID

# Create a PID file for future reference
echo $NEW_PID > streamlit.pid

echo "Deployment completed successfully!"
echo "You can find the application logs in streamlit.log"
echo "To stop the application later, use: kill -9 \$(cat streamlit.pid)"