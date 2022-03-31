from concurrent import futures
from signal import SIGTERM, signal
from typing import Tuple

import flask
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from markupsafe import escape

import protobufs.invocation_pb2_grpc as invocation_pb2_grpc
from data_module import IDatabaseMgr, InMemoryDatabaseMgr
from model_module import (IModelMgr, IModelSource, ModelIo, S3ModelSource,
                          TensorFlowModelMgr)
from protobufs.invocation_pb2 import InvocationResponse
from protobufs.model_pb2 import ModelInput, ModelOutput

# GLOBAL VARS
GRPC_PORT = 8000
GRPC_WORKERS = 10
GRPC_STOP_WAIT_TIME = 30 # seconds
REST_PORT = 5000
MODEL_S3_URL = "S3_URL"

model_mgt = TensorFlowModelMgr()
db_mgt = InMemoryDatabaseMgr()
s3_model_src = S3ModelSource(MODEL_S3_URL)
app = flask.Flask(__name__)


class ServiceCtrl:
    model_mgt: IModelMgr = None
    db_mgt: IDatabaseMgr = None
    initialized: bool = False

    @classmethod
    def initialize(cls, model_mgt: IModelMgr, db_mgt: IDatabaseMgr) -> bool:
        try:
            print(f"ServiceCtrl.initialize")
            cls.model_mgt = model_mgt
            cls.db_mgt = db_mgt
            cls.db_mgt.connect()
            print(f"ServiceCtrl.initialize done")
            return True
        except Exception as ex:
            print(f"ServiceCtrl.initialize failed: Exception={ex}")
            return False

    @classmethod
    def load_model(cls, model_source: IModelSource, *args, **kwargs) -> bool:
        try:
            print(f"ServiceCtrl.load_model")
            cls.model_mgt.load_model(model_source)
            print(f"ServiceCtrl.load_model done")
            return True
        except Exception as ex:
            print(f"ServiceCtrl.load_model failed: Exception={ex}")
            return False

    @classmethod
    def invoke_model(cls, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        try:
            print(f"ServiceCtrl.invoke_model")
            model_output = cls.model_mgt.invoke(model_input)
            cls.db_mgt.save_model_input(model_input)
            cls.db_mgt.save_model_output(model_input, model_output)
            print(f"ServiceCtrl.invoke_model done")
            return True
        except Exception as ex:
            print(f"ServiceCtrl.invoke_model failed: Exception={ex}")
            return False

    @classmethod
    def get_invocation_info(cls, model_input_id: str, *args, **kwargs) -> Tuple[ModelInput, ModelOutput]:
        try:
            print(f"ServiceCtrl.get_invocation_info")
            model_input = cls.db_mgt.retrieve_model_input(model_input_id)
            model_output = cls.db_mgt.retrieve_model_output(model_input_id)
            print(f"ServiceCtrl.get_invocation_info done")
            return model_input, model_output
        except Exception as ex:
            print(f"ServiceCtrl.get_invocation_info failed: Exception={ex}")
            return None

# Init ServiceCtrl
if not ServiceCtrl.initialize(model_mgt, db_mgt):
    exit()

if not ServiceCtrl.load_model(s3_model_src):
    exit()

# gRPC API Definition

class InvocationServiceStatus:
    OK = "OK"
    ERROR = "ERROR"


class InvocationService(invocation_pb2_grpc.InvocationServicer):
    def Invoke(self, request, context):
        try:
            print(f"InvocationService.Invoke: request={request}")
            model_input = request.model_input
            print(f"InvocationService.Invoke: model_input={model_input}")
            ServiceCtrl.invoke_model(model_input)
            return InvocationResponse(status=InvocationServiceStatus.OK)
        except Exception as ex:
            print(f"InvocationService.Invoke: Exception={ex}")
            return InvocationResponse(
                status=InvocationServiceStatus.ERROR,
                message=str(ex),
            )

def serve_InvocationService():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=GRPC_WORKERS),
        interceptors=interceptors,
    )
    invocation_pb2_grpc.add_InvocationServicer_to_server(InvocationService(), server)
    server.add_insecure_port(f"[::]:{GRPC_PORT}")

    server.start()
    print("InvocationService started")

    def handle_sigterm(*_):
        print("Received shutdown signal")
        # ASYNC stop func: refuse new requests
        all_rpcs_done_event = server.stop(GRPC_STOP_WAIT_TIME)
        # real wait
        all_rpcs_done_event.wait(GRPC_STOP_WAIT_TIME)
        print("Shutdown gracefully")

    signal(SIGTERM, handle_sigterm)
    # server.wait_for_termination()

# RESTful API Definition
@app.route("/", methods=["GET"])
def ping():
    health = ServiceCtrl.db_mgt.is_connected and ServiceCtrl.model_mgt.is_model_loaded
    status = 200 if health else 404
    return flask.Response(response="Welcome!\n", status=status, mimetype="application/json")


@app.route("/get-invocation-info/<input_id>", methods=["GET"])
def get_invocation_info(input_id):
    try:
        print(f"get_invocation_info: input_id={input_id}")
        model_input_id = escape(input_id)
        model_input, model_output = ServiceCtrl.get_invocation_info(model_input_id)
        input_dict = ModelIo.model_input_to_dict(model_input)
        output_dict = ModelIo.model_output_to_dict(model_output)
        response_dict = {
            "input": input_dict,
            "output": output_dict,
        }
        print(f"get_invocation_info: response_dict={response_dict}")

        response = flask.make_response(flask.jsonify(response_dict), 200)
    except Exception as ex:
        print(f"get_invocation_info: Exception={ex}")
        response_dict = {"error": str(ex)}
        response = flask.make_response(flask.jsonify(response_dict), 500)

    response.headers["Content-Type"] = "application/json"
    print(f"get_invocation_info: response={response}")
    return response

def run_service():
    serve_InvocationService()
    app.run(host="localhost", port=REST_PORT)


if __name__ == "__main__":
    run_service()
