FROM python:3.8.3-slim

RUN mkdir -p /api-item

WORKDIR /api-item

RUN pip install --upgrade pip
COPY ./requirements.txt /api-item/requirements.txt
RUN pip3 install -r /api-item/requirements.txt

COPY . /api-item/

EXPOSE 5001

WORKDIR /api-item/sources

ENTRYPOINT ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]