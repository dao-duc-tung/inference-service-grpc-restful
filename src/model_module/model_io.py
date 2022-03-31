from protobufs.model_pb2 import ModelInput, ModelOutput


class ModelIo:
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
