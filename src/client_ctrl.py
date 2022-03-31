import grpc
from protobufs.model_pb2 import ModelInput, ModelInputMetadata
from protobufs.invocation_pb2 import InvocationRequest
from protobufs.invocation_pb2_grpc import InvocationStub

channel = grpc.insecure_channel("localhost:8000")
client = InvocationStub(channel)

model_input_metadata_list = [ModelInputMetadata(key="type", value="list")]
model_input = ModelInput(id=1, content="0.1,0.2", metadata=model_input_metadata_list)
request = InvocationRequest(model_input=model_input)
response = client.Invoke(request)
print(response)
