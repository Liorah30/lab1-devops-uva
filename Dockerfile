FROM python:3.8-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENV MONGO_URI=mongodb://localhost:27017
ENV DB_NAME=student_db

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]