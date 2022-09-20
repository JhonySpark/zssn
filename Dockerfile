FROM python:3.6

EXPOSE 5000
WORKDIR /app

COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
CMD python main.py