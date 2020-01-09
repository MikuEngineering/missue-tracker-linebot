FROM python:3.6

WORKDIR /usr/src/app

ARG LINE_BOT_PORT=8000
ARG LINE_BOT_DB_HOST=database
ARG LINE_BOT_DB_USERNAME=miku
ARG LINE_BOT_DB_PASSWORD=mtpassword
ARG LINE_BOT_DB_DATABASE=missue_tracker_linebot

COPY . .

RUN pip install poetry

RUN poetry install

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
RUN chmod +x /wait

ENV LINE_BOT_PORT=$LINE_BOT_PORT \
    LINE_BOT_DB_HOST=$LINE_BOT_DB_HOST \
    LINE_BOT_DB_USERNAME=$LINE_BOT_DB_USERNAME \
    LINE_BOT_DB_PASSWORD=$LINE_BOT_DB_PASSWORD \
    LINE_BOT_DB_DATABASE=$LINE_BOT_DB_DATABASE

EXPOSE $LINE_BOT_PORT

CMD /wait && poetry run gunicorn -b 0.0.0.0:$LINE_BOT_PORT -w 4 app:app
