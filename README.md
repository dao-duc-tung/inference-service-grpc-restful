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
  - The system contains only 1 model

### Non-functional requirements

- Adaptability
  - Load model from S3 URL, filesystem
  - Support model formats: TensorFlow, PyTorch, MXNet, ONNX, custom Python script, etc
  - Flexible to change the database technology
- Reliability: Service is resilient, handle errors
- Testability: Write unit tests, integration tests

## High-level design

### API design

- invokeModel(input)
- getInvocationInfo(input_id) -> (input, output)

### Architecture overview

> invokeModel() --> Main service --> database

> getInvocationInfo() <--> Main service <--> database

> S3 URL --> Main service

- Main service contains

  - Model Manager
  - Database Manager

- Model Manager responsibilities

  - Load model at start given
  - Run model inference when invokeModel() API is called

- Database Manager responsibilities

  - Save model input and model output to database
  - Retrieve model input and model output when getInvocationInfo() API is called

## Detailed implementation
