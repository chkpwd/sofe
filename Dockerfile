FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
  git

ENV PYTHONUNBUFFERED=1

ENV ADDRESS=0.0.0.0
ENV PORT=7979

ENV DEBUG=false

WORKDIR /src

COPY requirements.txt /src

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /src/app

COPY constants/*.py /src/constants/
COPY app/*.py /src/app/
COPY main.py /src

EXPOSE 7979

CMD [ "/usr/local/bin/python", "/src/main.py" ]
