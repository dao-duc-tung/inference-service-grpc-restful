FROM python:3.8-slim

ARG GRPC_PORT=8000
ARG REST_PORT=5000

RUN python -m pip install --upgrade pip

RUN mkdir /service
WORKDIR /service

COPY src/requirements.txt /service/src/requirements.txt
RUN python -m pip install -r /service/src/requirements.txt

COPY protobufs/ /service/protobufs/
COPY ./build_protobufs.sh /service/build_protobufs.sh
RUN bash build_protobufs.sh

COPY src/ /service/src/

EXPOSE ${GRPC_PORT}
EXPOSE ${REST_PORT}

WORKDIR /service/src
# ENTRYPOINT ["python", "service_ctrl.py"]
