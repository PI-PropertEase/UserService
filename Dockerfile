FROM python:3.11.9-bookworm

COPY . /app
WORKDIR /app

RUN apt-get -y update \
  && apt-get -y install libpq-dev python3-dev \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* \
  && pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "UserService.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]