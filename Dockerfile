FROM python:3.8-slim

RUN python -m pip install --upgrade pip

RUN mkdir /service
WORKDIR /service

COPY src/requirements.txt /service/src/requirements.txt
RUN python -m pip install -r /service/src/requirements.txt

COPY protobufs/ /service/protobufs/
COPY ./build_protobufs.sh /service/build_protobufs.sh
RUN bash build_protobufs.sh

COPY src/ /service/src/

WORKDIR /service/src
# ENTRYPOINT ["python", "main.py"]
