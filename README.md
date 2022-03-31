# aaqua-sys

## Quick start

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

## High-level design

### API design

- runModel(input)
- getModelOutput(input_id) -> (input, output)

### Architecture overview

> runModel() --> Model Module --> database

> getModelOutput() <--> Data Module <--> database

> S3 URL --> Model Module

- Model Module responsibilities

  - Load model at start given
  - Run model inference when runModel() API is called

- Data Module responsibilities

  - Save model input and model output to database
  - Retrieve model input and model output when getModelOutput() API is called

## Detailed implementation
