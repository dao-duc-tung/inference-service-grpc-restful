import base64
import io
from protobufs.model_pb2 import ModelInput, ModelOutput


class ModelUtils:
    @staticmethod
    def model_input_to_dict(model_input: ModelInput) -> dict:
        temp_metadata = []
        metadata = model_input.metadata
        for item in metadata:
            temp_metadata.append(
                {
                    "key": item.key,
                    "value": item.value,
                }
            )

        d = {
            "id": model_input.id,
            "content": model_input.content,
            "metadata": temp_metadata,
        }

        return d

    @staticmethod
    def model_output_to_dict(model_output: ModelOutput) -> dict:
        temp_metadata = []
        metadata = model_output.metadata
        for item in metadata:
            temp_metadata.append(
                {
                    "key": item.key,
                    "value": item.value,
                }
            )

        d = {
            "id": model_output.id,
            "metadata": temp_metadata,
        }

        return d


class ImgUtils:
    @staticmethod
    def img_path_to_base64_str(img_path: str) -> str:
        msg = ""
        with open(img_path, "rb") as f:
            msg = ImgUtils.bytes_str_to_base64_str(f.read())
        return msg

    @staticmethod
    def bytes_str_to_base64_str(img_bytes: str) -> str:
        msg = base64.b64encode(img_bytes)
        return msg

    @staticmethod
    def base64_str_to_bytes_io(base64_str: str) -> io.BytesIO:
        msg = base64.b64decode(base64_str)
        buf = io.BytesIO(msg)
        return buf
