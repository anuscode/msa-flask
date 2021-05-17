FROM python:3.8.3-slim

RUN mkdir -p /api-alarm

WORKDIR /api-alarm

RUN pip install --upgrade pip
COPY ./requirements.txt /api-alarm/requirements.txt
RUN pip3 install -r /api-alarm/requirements.txt

COPY . /api-alarm/

EXPOSE 6001

WORKDIR /api-alarm/sources

ENTRYPOINT ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]