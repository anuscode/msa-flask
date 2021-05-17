FROM python:3.8.3-slim

RUN mkdir -p /api-user

WORKDIR /api-user

RUN pip install --upgrade pip
COPY ./requirements.txt /api-user/requirements.txt
RUN pip3 install -r /api-user/requirements.txt

COPY . /api-user/

EXPOSE 7001

WORKDIR /api-user/sources

ENTRYPOINT ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]