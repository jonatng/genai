# This sets up the container with Python 3.10 installed.
FROM python:3.10-slim

# Install git so that we can cloen the app code from a remote repo
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone your code that lives in a remote repo to WORKDIR
RUN git clone https://github.com/jonatng/genai.git

# This copies everything in your current directory to the /app directory in the container.
COPY . /genai

# This sets the /app directory as the working directory for any RUN, CMD, ENTRYPOINT, or COPY instructions that follow.
WORKDIR /genai

# This runs pip install for all the packages listed in your requirements.txt file.
RUN pip3 install -r requirements.txt

# This tells Docker to listen on port 8501 at runtime. Port 8501 is Streamlit's default port for HTTP.
EXPOSE 8501

# This command creates a .streamlit directory in the home directory of the container.
RUN mkdir ~/.genai

#The HEALTHCHECK instruction tells Docker how to test a container to check that it is still working. Your container needs to listen to Streamlit’s (default) port 8501:
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# This sets the default command for the container to run the app with Streamlit.
ENTRYPOINT ["genai", "run", 'app.py', '--server.port=8501', '--server.address=0.0.0.0']

# This command tells Streamlit to run your app.py script when the container starts.
CMD ["app.py"]