from model_module.model_utils import ModelInput, ModelOutput

from .i_database_mgr import IDatabaseMgr


class InMemoryDatabaseMgr(IDatabaseMgr):
    @property
    def is_connected(self) -> bool:
        return True

    def __init__(self) -> None:
        self._model_input_dict = {}
        self._model_output_dict = {}

    def connect(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        pass

    def save_model_input(self, model_input: ModelInput, *args, **kwargs):
        self._model_input_dict[str(model_input.id)] = model_input

    def save_model_output(
        self, model_input: ModelInput, model_output: ModelOutput, *args, **kwargs
    ):
        self._model_output_dict[str(model_input.id)] = model_output

    def retrieve_model_input(self, model_input_id: str, *args, **kwargs):
        if model_input_id in self._model_input_dict:
            return self._model_input_dict[model_input_id]
        return None

    def retrieve_model_output(self, model_input_id: str, *args, **kwargs):
        if model_input_id in self._model_output_dict:
            return self._model_output_dict[model_input_id]
        return None
