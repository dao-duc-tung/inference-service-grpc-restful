from model_module.model_io import ModelInput, ModelOutput


class IModelSource:
    pass


class S3ModelSource(IModelSource):
    def __init__(self, s3_url: str) -> None:
        self.s3_url = s3_url

    def __str__(self) -> str:
        s = f"s3_url={self.s3_url}"
        return s


class IModelMgr:
    @property
    def is_model_loaded(self) -> bool:
        raise NotImplementedError()

    def load_model(self, model_source: IModelSource, *args, **kwargs):
        raise NotImplementedError()

    def invoke(self, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        raise NotImplementedError()


class TensorFlowModelMgr(IModelMgr):
    @property
    def is_model_loaded(self) -> bool:
        return True

    def load_model(self, model_source: S3ModelSource, *args, **kwargs):
        print(f"Load model from {model_source}")

    def invoke(self, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        print(f"Invoke model for input {model_input}")
