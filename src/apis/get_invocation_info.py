import logging

import flask
from markupsafe import escape
from utils import AppConst

from .service_ctrl import ServiceCtrl

logger = logging.getLogger(AppConst.APP_NAME)

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
        logger.info(f"get_invocation_info: input_id={input_id}")
        model_input_id = str(escape(input_id))
        model_input_dict, model_output_dict = ServiceCtrl.get_invocation_info(
            model_input_id
        )

        if model_input_dict != None and model_output_dict != None:
            response_dict = {
                "model_input": model_input_dict,
                "model_output": model_output_dict,
            }
            logger.info(f"get_invocation_info: response_dict={response_dict}")
        else:
            response_dict = {"message": f"Input id={model_input_id} not found."}

        response = flask.make_response(flask.jsonify(response_dict), 200)
    except Exception as ex:
        logger.error(f"get_invocation_info: Exception={ex}")
        response_dict = {"message": str(ex)}
        response = flask.make_response(flask.jsonify(response_dict), 500)

    response.headers["Content-Type"] = "application/json"
    return response
