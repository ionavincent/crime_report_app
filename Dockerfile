FROM python:2.7.14-alpine3.7

EXPOSE 8080

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/.

ENV PYTHONPATH /app

CMD [ "python", "app.py" ]
