from protobufs.model_pb2 import ModelInput, ModelOutput, ModelOutputMetadata

from .i_model_mgr import IModelMgr
from .i_model_source import IModelSource


class MockModelMgr(IModelMgr):
    @property
    def is_model_loaded(self) -> bool:
        return True

    def load_model(self, model_source: IModelSource, *args, **kwargs):
        print(f"Load model from {model_source}")

    def invoke(self, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        print(f"Invoke model for input {model_input}")
        model_output_metadata_list = [ModelOutputMetadata(key="accuracy", value="0.9")]
        model_output = ModelOutput(id=1, metadata=model_output_metadata_list)
        return model_output
