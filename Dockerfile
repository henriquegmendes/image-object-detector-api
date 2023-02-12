FROM python:3.9-slim-buster

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED 1

EXPOSE 8080

CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]