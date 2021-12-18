FROM python:3.9

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]