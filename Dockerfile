FROM python:3.11

WORKDIR /app

COPY .chainlit /app/.chainlit

COPY public /app/public

ENV CHAINLIT_AUTH_SECRET ""
ENV PG_CONNECTION_STRING ""
COPY app.py /app/app.py

COPY chainlit.md /app/chainlit.md

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["chainlit", "run","app.py"]