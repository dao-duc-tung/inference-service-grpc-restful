class IModelSource:
    def get_raw_path(self) -> str:
        raise NotImplementedError()
