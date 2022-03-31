# aaqua-sys

## Requirements

### Functional requirements

- API 1 - gRPC-based API

  - input: model input with id, content, and metadata
  - process: run model inference on given input, save model outputs to database
  - output: none

- API 2 - RESTful-based API

  - input: input id
  - process: retrieve model input by input id, retrieve corresponding model outputs
  - output: content, model output

- Model is loaded at runtime when starting app given an S3 URL

### Non-functional requirements

- Adaptability
  - Load model from S3 URL, filesystem
  - Support model formats: TensorFlow, PyTorch, MXNet, ONNX, custom Python script, etc
  - Flexible to change the database technology
- Reliability: Service is resilient, handle errors
- Testability: Write unit tests, integration tests
