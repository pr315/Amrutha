FROM python:latest

COPY ./App/ ./app

RUN pip3 install -r ./app/requirements.txt

EXPOSE 80
ENV FLASK_APP=./app/app.py
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
