FROM python:3.9-alpine

RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev libffi-dev openssl-dev python3-dev rust cargo
RUN python -m pip install virtualenv poetry

EXPOSE 8080
COPY . /booking
WORKDIR /booking
RUN poetry config virtualenvs.create false && poetry install
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["python", "booking/main.py", "--host", "0.0.0.0", "--port", "8080"]
