import argparse

from apis import ServiceCtrl, flask_app, serve_InvocationService
from data_module import RedisDatabaseMgr
from model_module import MockModelMgr, S3ModelSource

# Global vars
GRPC_PORT = 8000
REST_PORT = 5000
MODEL_S3_URL = "S3_URL"
model_mgt = MockModelMgr()
db_mgt = RedisDatabaseMgr()
s3_model_src = S3ModelSource(MODEL_S3_URL)


# Init ServiceCtrl
if not ServiceCtrl.initialize(model_mgt, db_mgt):
    exit()

if not ServiceCtrl.load_model(s3_model_src):
    exit()


def run_service(grpc_port, rest_port):
    serve_InvocationService(grpc_port, wait=False)
    # Must use 0.0.0.0 for docker
    flask_app.run(host="0.0.0.0", port=rest_port)


if __name__ == "__main__":
    # Use ArgumentParser with Docker ENTRYPOINT
    # https://stackoverflow.com/a/67868029
    parser = argparse.ArgumentParser()
    parser.add_argument("--grpc-port", type=str, required=False, default=GRPC_PORT)
    parser.add_argument("--rest-port", type=str, required=False, default=REST_PORT)
    args = vars(parser.parse_args())
    print(args)

    grpc_port = args["grpc_port"]
    rest_port = args["rest_port"]
    run_service(grpc_port, rest_port)
