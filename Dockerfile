FROM python:3.8

RUN pip install Flask==2.0.2
RUN pip install flask-mysql==1.5.2
RUN pip install PyMySQL==0.10.0


WORKDIR /dfs-co2emission
COPY . /dfs-co2emission

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0"]