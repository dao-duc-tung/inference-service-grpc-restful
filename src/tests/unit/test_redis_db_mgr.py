import pytest
from data_module import RedisDatabaseMgr
from protobufs.model_pb2 import (
    ModelInput,
    ModelInputMetadata,
    ModelOutput,
    ModelOutputMetadata,
)


def connect_db():
    db = RedisDatabaseMgr()
    db.connect()
    return db


def init_model_input(id, content, metadata) -> ModelInput:
    key, value = metadata
    model_input_metadata_list = [ModelInputMetadata(key=key, value=value)]
    model_input = ModelInput(id=id, content=content, metadata=model_input_metadata_list)
    return model_input


def init_model_output(id, metadata) -> ModelOutput:
    key, value = metadata
    model_output_metadata_list = [ModelOutputMetadata(key=key, value=value)]
    model_output = ModelOutput(id=id, metadata=model_output_metadata_list)
    return model_output


def test_RedisDatabaseMgr_connect():
    db = RedisDatabaseMgr()
    res = db.connect()
    assert res == True


def test_RedisDatabaseMgr_close():
    db = connect_db()
    res = db.close()
    assert res == True


@pytest.mark.parametrize("id", [100, 200])
@pytest.mark.parametrize("content", ["0.1,0.2", "0.3,0.4"])
@pytest.mark.parametrize("metadata", [("type", "list"), ("size", "2,1")])
def test_RedisDatabaseMgr_save_model_input(id, content, metadata):
    db = connect_db()
    db.flush_all()
    model_input = init_model_input(id, content, metadata)
    db.save_model_input(model_input)


@pytest.mark.parametrize("input_id", [100, 200])
@pytest.mark.parametrize("input_content", ["0.1,0.2", "0.3,0.4"])
@pytest.mark.parametrize("input_metadata", [("type", "list"), ("size", "2,1")])
@pytest.mark.parametrize("output_id", [300, 400])
@pytest.mark.parametrize("output_metadata", [("accuracy", "0.9"), ("f1", "0.8")])
def test_RedisDatabaseMgr_save_model_output(
    input_id, input_content, input_metadata, output_id, output_metadata
):
    db = connect_db()
    db.flush_all()
    model_input = init_model_input(input_id, input_content, input_metadata)
    model_output = init_model_output(output_id, output_metadata)
    db.save_model_output(model_input, model_output)


@pytest.mark.parametrize("id", [100, 200])
@pytest.mark.parametrize("content", ["0.1,0.2", "0.3,0.4"])
@pytest.mark.parametrize("metadata", [("type", "list"), ("size", "2,1")])
def test_RedisDatabaseMgr_retrieve_model_input_key_exists(id, content, metadata):
    db = connect_db()
    db.flush_all()
    model_input = init_model_input(id, content, metadata)
    db.save_model_input(model_input)

    key, value = metadata
    model_input_dict = db.retrieve_model_input(model_input_id=id)
    assert model_input_dict["id"] == id
    assert model_input_dict["content"] == content
    assert model_input_dict["metadata"][0]["key"] == key
    assert model_input_dict["metadata"][0]["value"] == value


@pytest.mark.parametrize("input_id", [100, 200])
@pytest.mark.parametrize("input_content", ["0.1,0.2", "0.3,0.4"])
@pytest.mark.parametrize("input_metadata", [("type", "list"), ("size", "2,1")])
@pytest.mark.parametrize("output_id", [300, 400])
@pytest.mark.parametrize("output_metadata", [("accuracy", "0.9"), ("f1", "0.8")])
def test_RedisDatabaseMgr_retrieve_model_output_key_exists(
    input_id, input_content, input_metadata, output_id, output_metadata
):
    db = connect_db()
    db.flush_all()
    model_input = init_model_input(input_id, input_content, input_metadata)
    model_output = init_model_output(output_id, output_metadata)
    db.save_model_output(model_input, model_output)

    out_key, out_value = output_metadata
    model_output_dict = db.retrieve_model_output(model_input_id=input_id)
    assert model_output_dict["id"] == output_id
    assert model_output_dict["metadata"][0]["key"] == out_key
    assert model_output_dict["metadata"][0]["value"] == out_value


@pytest.mark.parametrize("id", [100, 200])
def test_RedisDatabaseMgr_retrieve_model_input_key_doesnt_exist(id):
    db = connect_db()
    db.flush_all()

    model_input_dict = db.retrieve_model_input(model_input_id=id)
    assert model_input_dict == None


@pytest.mark.parametrize("input_id", [100, 200])
def test_RedisDatabaseMgr_retrieve_model_output_key_doesnt_exist(input_id):
    db = connect_db()
    db.flush_all()

    model_output_dict = db.retrieve_model_output(model_input_id=input_id)
    assert model_output_dict == None
