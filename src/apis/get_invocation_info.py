import flask
from markupsafe import escape
from model_module import ModelIo
from protobufs.model_pb2 import ModelInput, ModelOutput

from .service_ctrl import ServiceCtrl

# Global vars
flask_app = flask.Flask(__name__)


@flask_app.route("/", methods=["GET"])
def ping():
    health = ServiceCtrl.db_mgt.is_connected and ServiceCtrl.model_mgt.is_model_loaded
    status = 200 if health else 404
    return flask.Response(
        response="Welcome!\n", status=status, mimetype="application/json"
    )


@flask_app.route("/get-invocation-info/<input_id>", methods=["GET"])
def get_invocation_info(input_id):
    try:
        print(f"get_invocation_info: input_id={input_id}")
        model_input_id = str(escape(input_id))
        model_input, model_output = ServiceCtrl.get_invocation_info(model_input_id)

        if type(model_input) == ModelInput:
            input_dict = ModelIo.model_input_to_dict(model_input)
            output_dict = {}
            if type(model_output) == ModelOutput:
                output_dict = ModelIo.model_output_to_dict(model_output)
            response_dict = {
                "model_input": input_dict,
                "model_output": output_dict,
            }
            print(f"get_invocation_info: response_dict={response_dict}")
        else:
            response_dict = {"message": f"Input id={model_input_id} not found."}

        response = flask.make_response(flask.jsonify(response_dict), 200)
    except Exception as ex:
        print(f"get_invocation_info: Exception={ex}")
        response_dict = {"message": str(ex)}
        response = flask.make_response(flask.jsonify(response_dict), 500)

    response.headers["Content-Type"] = "application/json"
    return response
