FROM python:3.8-slim

RUN mkdir /service
WORKDIR /service

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN python -m pip install --upgrade pip

COPY src/requirements.txt /service/src/requirements.txt
RUN python -m pip install -r /service/src/requirements.txt

# COPY models/ /service/models/
COPY images/ /service/images/
COPY protobufs/ /service/protobufs/
COPY ./build_protobufs.sh /service/build_protobufs.sh
RUN bash build_protobufs.sh

COPY src/ /service/src/

WORKDIR /service/src
# ENTRYPOINT ["python", "main.py"]
