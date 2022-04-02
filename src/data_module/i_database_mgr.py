from protobufs.model_pb2 import ModelInput, ModelOutput


class IDatabaseMgr:
    @property
    def is_connected(self) -> bool:
        raise NotImplementedError()

    def connect(self, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def close(self, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def flush_all(self, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def save_model_input(self, model_input: ModelInput, *args, **kwargs):
        raise NotImplementedError()

    def save_model_output(
        self, model_input: ModelInput, model_output: ModelOutput, *args, **kwargs
    ):
        raise NotImplementedError()

    def retrieve_model_input(self, model_input_id: str, *args, **kwargs):
        raise NotImplementedError()

    def retrieve_model_output(self, model_input_id: str, *args, **kwargs):
        raise NotImplementedError()

    def delete_model_input(self, model_input_id: str, *args, **kwargs):
        raise NotImplementedError()

    def delete_model_output(self, model_input_id: str, *args, **kwargs):
        raise NotImplementedError()
