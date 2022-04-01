import logging

from protobufs.model_pb2 import ModelInput, ModelOutput, ModelOutputMetadata
from utils import AppConst

from .i_model_mgr import IModelMgr
from .i_model_source import IModelSource

logger = logging.getLogger(AppConst.APP_NAME)


class MockModelMgr(IModelMgr):
    @property
    def is_model_loaded(self) -> bool:
        return True

    def load_model(self, model_source: IModelSource, *args, **kwargs):
        logger.info(f"Load model from {model_source}")

    def invoke(self, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        logger.info(f"Invoke model for model_input.id={model_input.id}")
        model_output_metadata_list = [ModelOutputMetadata(key="accuracy", value="0.9")]
        model_output = ModelOutput(id=1, metadata=model_output_metadata_list)
        return model_output
