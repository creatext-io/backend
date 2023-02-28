FROM python:3.9-slim
RUN apt-get update
RUN apt-get -y install --no-install-recommends gcc && apt-get -y --no-install-recommends install g++ && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -U setuptools
RUN pip install Cmake
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["uvicorn","src.app.main:app","--proxy-headers","--host", "0.0.0.0","--port","8000"] 