import logging
from typing import Tuple

from data_module import IDatabaseMgr
from model_module import IModelMgr, IModelSource
from protobufs.model_pb2 import ModelInput, ModelOutput
from utils import AppConst

logger = logging.getLogger(AppConst.APP_NAME)


class ServiceCtrl:
    model_mgt: IModelMgr = None
    db_mgt: IDatabaseMgr = None
    initialized: bool = False

    @classmethod
    def initialize(cls, model_mgt: IModelMgr, db_mgt: IDatabaseMgr) -> bool:
        try:
            logger.info(f"ServiceCtrl.initialize")
            cls.model_mgt = model_mgt
            cls.db_mgt = db_mgt
            cls.db_mgt.connect()
            logger.info(f"ServiceCtrl.initialize done")
            return True
        except Exception as ex:
            logger.error(f"ServiceCtrl.initialize failed: Exception={ex}")
            return False

    @classmethod
    def load_model(cls, model_source: IModelSource, *args, **kwargs) -> bool:
        try:
            logger.info(f"ServiceCtrl.load_model")
            cls.model_mgt.load_model(model_source)
            logger.info(f"ServiceCtrl.load_model done")
            return True
        except Exception as ex:
            logger.error(f"ServiceCtrl.load_model failed: Exception={ex}")
            return False

    @classmethod
    def invoke_model(cls, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        try:
            logger.info(f"ServiceCtrl.invoke_model")
            model_output = cls.model_mgt.invoke(model_input)
            cls.db_mgt.save_model_input(model_input)
            cls.db_mgt.save_model_output(model_input, model_output)
            logger.info(f"ServiceCtrl.invoke_model done")
            return True
        except Exception as ex:
            logger.error(f"ServiceCtrl.invoke_model failed: Exception={ex}")
            return False

    @classmethod
    def get_invocation_info(
        cls, model_input_id: str, *args, **kwargs
    ) -> Tuple[ModelInput, ModelOutput]:
        try:
            logger.info(f"ServiceCtrl.get_invocation_info")
            model_input = cls.db_mgt.retrieve_model_input(model_input_id)
            model_output = cls.db_mgt.retrieve_model_output(model_input_id)
            logger.info(f"ServiceCtrl.get_invocation_info done")
            return model_input, model_output
        except Exception as ex:
            logger.error(f"ServiceCtrl.get_invocation_info failed: Exception={ex}")
            return (None, None)
