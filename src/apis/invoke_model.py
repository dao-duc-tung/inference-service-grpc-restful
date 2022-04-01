import logging
from concurrent import futures
from signal import SIGTERM, signal

import grpc
import protobufs.invocation_pb2_grpc as invocation_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from protobufs.invocation_pb2 import InvocationResponse
from utils import AppConst

from .service_ctrl import ServiceCtrl

logger = logging.getLogger(AppConst.APP_NAME)

# Global vars
GRPC_WORKERS = 4
GRPC_STOP_WAIT_TIME = 5  # seconds


class InvocationServiceStatus:
    OK = "OK"
    ERROR = "ERROR"


class InvocationService(invocation_pb2_grpc.InvocationServicer):
    def Invoke(self, request, context):
        try:
            logger.info(f"InvocationService.Invoke: request={str(request)[:50]}")
            model_input = request.model_input
            logger.info(f"InvocationService.Invoke: model_input.id={model_input.id}")
            if ServiceCtrl.invoke_model(model_input):
                return InvocationResponse(status=InvocationServiceStatus.OK)
            else:
                return InvocationResponse(status=InvocationServiceStatus.ERROR)
        except Exception as ex:
            logger.error(f"InvocationService.Invoke: {ex}")
            return InvocationResponse(
                status=InvocationServiceStatus.ERROR,
                message=str(ex),
            )


def serve_InvocationService(grpc_port, wait: bool = False):
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=GRPC_WORKERS),
        interceptors=interceptors,
    )
    invocation_pb2_grpc.add_InvocationServicer_to_server(InvocationService(), server)
    server.add_insecure_port(f"[::]:{grpc_port}")

    server.start()
    logger.info("InvocationService started")

    def handle_sigterm(*_):
        logger.info("Received shutdown signal")
        # ASYNC stop func: refuse new requests
        all_rpcs_done_event = server.stop(GRPC_STOP_WAIT_TIME)
        # real wait
        all_rpcs_done_event.wait(GRPC_STOP_WAIT_TIME)
        logger.info("Shutdown gracefully")

    signal(SIGTERM, handle_sigterm)
    if wait:
        server.wait_for_termination()
