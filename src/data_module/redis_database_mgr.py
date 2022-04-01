import json
import os

import redis
from model_module.model_utils import ModelInput, ModelOutput, ModelUtils

from .i_database_mgr import IDatabaseMgr

DB_HOST_NAME = os.getenv("DB_HOST_NAME", "aaqua_db")
DB_PORT = os.getenv("DB_PORT", 6379)
import logging

from utils import AppConst

logger = logging.getLogger(AppConst.APP_NAME)


class RedisDatabaseMgr(IDatabaseMgr):
    MODEL_INPUT_DB_IDX = 0
    MODEL_OUTPUT_DB_IDX = 1

    @property
    def is_connected(self) -> bool:
        return True

    def __init__(self) -> None:
        self._model_input_conn = None
        self._model_output_conn = None

    def connect(self, *args, **kwargs) -> bool:
        try:
            self._model_input_conn = redis.Redis(
                host=DB_HOST_NAME, port=DB_PORT, db=RedisDatabaseMgr.MODEL_INPUT_DB_IDX
            )
            self._model_output_conn = redis.Redis(
                host=DB_HOST_NAME, port=DB_PORT, db=RedisDatabaseMgr.MODEL_OUTPUT_DB_IDX
            )
            return True
        except Exception as ex:
            logger.error(f"RedisDatabaseMgr.connect: {ex}")
            return False

    def close(self, *args, **kwargs):
        try:
            self._model_input_conn.close()
            self._model_output_conn.close()
            return True
        except Exception as ex:
            logger.error(f"RedisDatabaseMgr.close: {ex}")
            return False

    def flush_all(self, *args, **kwargs) -> bool:
        try:
            self._model_input_conn.flushdb()
            self._model_output_conn.flushdb()
            return True
        except Exception as ex:
            logger.error(f"RedisDatabaseMgr.flush_all: {ex}")
            return False

    def save_model_input(self, model_input: ModelInput, *args, **kwargs):
        key = str(model_input.id)
        value = json.dumps(ModelUtils.model_input_to_dict(model_input))
        self._model_input_conn.set(key, value)
        self._model_input_conn.save()

    def save_model_output(
        self, model_input: ModelInput, model_output: ModelOutput, *args, **kwargs
    ):
        key = str(model_input.id)
        value = json.dumps(ModelUtils.model_output_to_dict(model_output))
        self._model_output_conn.set(key, value)
        self._model_output_conn.save()

    def retrieve_model_input(self, model_input_id: str, *args, **kwargs) -> dict:
        key = model_input_id
        model_input_dict_str = self._model_input_conn.get(key)
        if model_input_dict_str == None:
            return None

        model_input_dict = json.loads(model_input_dict_str)
        return model_input_dict

    def retrieve_model_output(self, model_input_id: str, *args, **kwargs) -> dict:
        key = model_input_id
        model_output_dict_str = self._model_output_conn.get(key)
        if model_output_dict_str == None:
            return None

        model_output_dict = json.loads(model_output_dict_str)
        return model_output_dict
