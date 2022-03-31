from typing import Tuple

import flask
from markupsafe import escape

from data_module import IDatabaseMgt, InMemoryDatabaseMgt
from model_module import (IModelMgt, IModelSource, ModelInput, ModelOutput,
                          S3ModelSource, TensorFlowModelMgt)

# GLOBAL VARS
model_mgt = TensorFlowModelMgt()
db_mgt = InMemoryDatabaseMgt()
S3_URL = "S3_URL"
s3_model_src = S3ModelSource(S3_URL)
app = flask.Flask(__name__)


class ServiceCtrl:
    model_mgt: IModelMgt = None
    db_mgt: IDatabaseMgt = None
    initialized: bool = False

    @classmethod
    def initialize(cls, model_mgt: IModelMgt, db_mgt: IDatabaseMgt):
        cls.model_mgt = model_mgt
        cls.db_mgt = db_mgt
        cls.db_mgt.connect()

    @classmethod
    def load_model(cls, model_source: IModelSource, *args, **kwargs):
        cls.model_mgt.load_model(model_source)

    @classmethod
    def invoke_model(cls, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        model_output = cls.model_mgt.invoke(model_input)
        cls.db_mgt.save_model_input(model_input)
        cls.db_mgt.save_model_output(model_input, model_output)

    @classmethod
    def get_invocation_info(cls, model_input_id: str, *args, **kwargs) -> Tuple[ModelInput, ModelOutput]:
        model_input = cls.db_mgt.retrieve_model_input(model_input_id)
        model_output = cls.db_mgt.retrieve_model_output(model_input_id)
        return model_input, model_output


@app.route("/ping", methods=["GET"])
def ping():
    if not ServiceCtrl.initialized:
        ServiceCtrl.initialize(model_mgt, db_mgt)
        ServiceCtrl.load_model(s3_model_src)

    health = ServiceCtrl.db_mgt.is_connected and ServiceCtrl.model_mgt.is_model_loaded
    status = 200 if health else 404
    return flask.Response(response="Welcome!\n", status=status, mimetype="application/json")


@app.route("/get-invocation-info/<input_id>", methods=["GET"])
def get_invocation_info(input_id):
    try:
        model_input_id = escape(input_id)
        model_input, model_output = ServiceCtrl.get_invocation_info(model_input_id)
        input_dict = model_input.to_dict()
        output_dict = model_output.to_dict()
        response_dict = {
            "input": input_dict,
            "output": output_dict,
        }

        response = flask.make_response(flask.jsonify(response_dict), 200)
    except Exception as ex:
        response_dict = {"error": str(ex)}
        response = flask.make_response(flask.jsonify(response_dict), 500)

    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")
