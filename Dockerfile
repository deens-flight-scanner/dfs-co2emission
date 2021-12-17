FROM python:3.9

RUN pip install --upgrade pip

WORKDIR /dfs-co2emission
COPY . /dfs-co2emission

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0"]