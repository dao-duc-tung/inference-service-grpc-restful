import logging

import flask
from markupsafe import escape
from utils import AppConst
from utils import RestApiDefinition

from .service_ctrl import ServiceCtrl

logger = logging.getLogger(AppConst.APP_NAME)

# Global vars
flask_app = flask.Flask(__name__)


@flask_app.route(f"/{RestApiDefinition.PING}", methods=["GET"])
def ping():
    logger.info(f"flask_app.ping")
    health = ServiceCtrl.db_mgt.is_connected
    message = "ready" if health else "not ready"
    status = 200
    return flask.Response(
        response=f"{message}!\n", status=status, mimetype="application/json"
    )


def format_invocation_response_success(
    model_input_dict: dict, model_output_dict: dict
) -> dict:
    response_dict = {
        "model_input": model_input_dict,
        "model_output": model_output_dict,
    }
    return response_dict


def format_invocation_response_not_found(model_input_id: str) -> dict:
    response_dict = {"message": f"Input id={model_input_id} not found."}
    return response_dict


def format_invocation_response_exception(ex: Exception) -> dict:
    response_dict = {"message": f"{str(ex)}"}
    return response_dict


def decor_response(response_dict: dict, status_code: int) -> flask.Response:
    response = flask.make_response(flask.jsonify(response_dict), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@flask_app.route(
    f"/{RestApiDefinition.GET_INVOCATION_INFO}/<input_id>", methods=["GET"]
)
def get_invocation_info(input_id):
    try:
        logger.info(f"flask_app.get_invocation_info: input_id={input_id}")
        model_input_id = str(escape(input_id))
        model_input_dict, model_output_dict = ServiceCtrl.get_invocation_info(
            model_input_id
        )

        if model_input_dict != None and model_output_dict != None:
            response_dict = format_invocation_response_success(
                model_input_dict, model_output_dict
            )
            response = decor_response(response_dict, 200)
        else:
            response_dict = format_invocation_response_not_found(model_input_id)
            response = decor_response(response_dict, 404)
    except Exception as ex:
        logger.error(f"flask_app.get_invocation_info: {ex}")
        response_dict = format_invocation_response_exception(ex)
        response = decor_response(response_dict, 500)

    return response
