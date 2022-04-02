import logging
from functools import wraps

from protobufs.model_pb2 import ModelInput, ModelOutput

from utils import AppConst

from .i_model_mgr import IModelMgr
from .i_model_source import IModelSource
from .tensorflow_model_mgr import TensorFlowModelMgr

logger = logging.getLogger(AppConst.APP_NAME)


class ModelFramework:
    TENSORFLOW = "TENSORFLOW"
    PYTORCH = "PYTORCH"


class ModelMgr(IModelMgr):
    """
    ModelMgr manages 1 model only.
    ModelMgr can be extended to manage multiple models in different frameworks.
    """

    def _check_model_mgr(func, default_return=None):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._model_mgr != None:
                return func(self, *args, **kwargs)
            else:
                return default_return

        return wrapper

    @property
    def is_model_loaded(self) -> bool:
        if self._model_mgr != None:
            return self._model_mgr.is_model_loaded
        return False

    def __init__(self, framework: str) -> None:
        if framework == ModelFramework.TENSORFLOW:
            self._model_mgr = TensorFlowModelMgr()
        else:
            logger.error(f"Framework {framework} is not supported.")

    @_check_model_mgr
    def get_model(self):
        return self._model_mgr.get_model()

    @_check_model_mgr
    def load_model(self, model_source: IModelSource, *args, **kwargs):
        return self._model_mgr.load_model(model_source)

    @_check_model_mgr
    def invoke(self, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        return self._model_mgr.invoke(model_input)
