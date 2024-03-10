FROM python:3.10-slim-buster

LABEL maintainer="Mauricio Moreira Soares <phydev@protonmail.ch>"

RUN mkdir /app
WORKDIR /app

# Set our app folder as a volume
VOLUME ["/app"]

ENV FAST_APP=app.py
ENV FAST_RUN_HOST=0.0.0.0

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8070

# Run the application:
COPY app/* .

CMD ["python", "main.py"]
