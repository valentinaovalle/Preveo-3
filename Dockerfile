# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

RUN pip install --upgrade pip

ENV APP_HOME /app
WORKDIR $APP_HOME


RUN apt-get update \
    && apt-get -y install libpq-dev gcc locales locales-all pkg-config

RUN sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen

ENV LC_ALL es_ES.UTF-8 
ENV LANG es_ES.UTF-8  
ENV LANGUAGE es_ES:es 

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8050
ENV TZ="America/Bogota"


# Setting this ensures print statements and log messages
# promptly appear in Cloud Logging.
ENV PYTHONUNBUFFERED TRUE

# Install dependencies.
RUN pip install streamlit==1.12.2 streamlit-aggrid==0.3.3 pyxlsb==1.0.9 datatable==1.0.0 openpyxl==3.0.10
RUN pip install xlsxwriter==3.0.3 plotly==5.6.0 opencv-python==4.5.5.62 Markdown==3.4.1  keycloak-client

# Copy local code to the container image.
COPY . .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
#CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2 
CMD streamlit run dash.py --server.port $PORT
