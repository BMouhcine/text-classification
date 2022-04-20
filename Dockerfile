FROM python:3.9.1

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt && pip install -U pyopenssl
COPY . /app

EXPOSE 5001

CMD [ "python", "./text_classifier.py" ]
