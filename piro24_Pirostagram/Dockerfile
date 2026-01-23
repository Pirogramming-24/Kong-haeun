FROM python:3.12.7

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD python manage.py makemigrations --noinput &&\
	python manage.py migrate --noinput &&\
    python manage.py runserver 0.0.0.0:8000

EXPOSE 8000