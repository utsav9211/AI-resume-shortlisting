FROM python:3.10-slim
WORKDIR /app

# copy files
COPY . /app

# install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# expose port
EXPOSE 8501

# default command
CMD ["streamlit","run","streamlit_app.py","--server.port=8501","--server.address=0.0.0.0"]
