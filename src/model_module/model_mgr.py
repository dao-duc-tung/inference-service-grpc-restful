from protobufs.model_pb2 import ModelInput, ModelOutput, ModelOutputMetadata


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


class MockModelMgr(IModelMgr):
    @property
    def is_model_loaded(self) -> bool:
        return True

    def load_model(self, model_source: S3ModelSource, *args, **kwargs):
        print(f"Load model from {model_source}")

    def invoke(self, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        print(f"Invoke model for input {model_input}")
        model_output_metadata_list = [ModelOutputMetadata(key="accuracy", value="0.9")]
        model_output = ModelOutput(id=1, metadata=model_output_metadata_list)
        return model_output
