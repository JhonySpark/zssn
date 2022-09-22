FROM python:3.6

EXPOSE 5000
WORKDIR /app

COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
CMD ENV=prod flask run --host 0.0.0.0 --port 5000 

