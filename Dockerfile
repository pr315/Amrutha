FROM python:latest

COPY ./App/ ./app

RUN pip3 install -r ./app/requirements.txt

EXPOSE 8080
ENV FLASK_APP=./app/app.py
CMD ["flask", "run", "--host", "prajvalwebapp.eu-west-1.elasticbeanstalk.com"]

