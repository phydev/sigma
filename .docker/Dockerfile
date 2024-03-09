FROM python:3.10-slim-buster

LABEL maintainer="Mauricio Moreira Soares <phydev@protonmail.ch>"

RUN mkdir /code
WORKDIR /code

# Set our app folder as a volume
VOLUME ["/code"]


# Check if we really need binutils libproj-dev gdal-bin
#RUN apt-get update && apt-get install -y build-essential libpq-dev libffi-dev libssl-dev libjpeg-dev zlib1g-dev binutils libproj-dev gdal-bin

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV FAST_APP=app.py
ENV FAST_RUN_HOST=0.0.0.0

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8070

# Run the application:
COPY app/* .

CMD ["python", "main.py"]
