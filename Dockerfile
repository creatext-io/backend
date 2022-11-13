FROM python:3.9-slim
RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get -y install g++
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install -U setuptools
RUN pip install Cmake
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["uvicorn","src.app.main:app","--host", "0.0.0.0","--port","8000"]