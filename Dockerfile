FROM python:3.11.7 AS base


RUN mkdir /usr/src/app

ENV PYTHONPATH /usr/src/app
ENV SETTINGS_PATH /usr/src/app/resources/config.ini

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

FROM base AS deploy

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS run_tests

CMD ["pytest", "-v", "--cov", "tests"]
