from protobufs.model_pb2 import ModelInput, ModelOutput

from .i_model_source import IModelSource


class IModelMgr:
    @property
    def is_model_loaded(self) -> bool:
        raise NotImplementedError()

    def get_model(self, *args, **kwargs):
        raise NotImplementedError()

    def load_model(self, model_source: IModelSource, *args, **kwargs):
        raise NotImplementedError()

    def invoke(self, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        raise NotImplementedError()
