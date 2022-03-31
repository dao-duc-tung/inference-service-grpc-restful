
class ModelInput:
    def __init__(self, id: str, content: str, metadata: dict) -> None:
        self.id = id
        self.content = content
        self.metadata = metadata

    def __str__(self) -> str:
        s = f"id={self.id}, content={self.content}, metadata={self.metadata}"
        return s

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
        }
        return d


class ModelOutput:
    def __init__(self, id: str, data: dict) -> None:
        self.id = id
        self.data = data

    def __str__(self) -> str:
        s = f"id={self.id}, data={self.data}"
        return s

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "data": self.data,
        }
