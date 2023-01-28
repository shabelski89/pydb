FROM python:3.6

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev
RUN apt-get install -y python3-venv

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -m pip install --upgrade build
RUN python -m build

RUN pip install "$(ls ./dist/*.whl)"
