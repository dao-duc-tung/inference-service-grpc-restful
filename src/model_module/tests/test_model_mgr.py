import pytest
from model_module import ImgUtils, ModelFramework, ModelMgr, PathModelSource
from protobufs.model_pb2 import ModelInput

model_paths = [
    # "file://../models/tf_face_det/",
    "https://tungdao-public.s3.ap-southeast-1.amazonaws.com/tf_face_det.zip",
]
model_framework = ModelFramework.TENSORFLOW


def init_mgr(model_path):
    model_source = PathModelSource(model_path)
    model_mgr = ModelMgr(model_framework)
    model_mgr.load_model(model_source)
    return model_mgr


@pytest.mark.slow
@pytest.mark.parametrize("model_path", model_paths)
def test_ModelMgr_load_model(model_path):
    model_mgr = init_mgr(model_path)
    assert model_mgr.get_model() != None


@pytest.mark.slow
@pytest.mark.parametrize("model_path", model_paths)
@pytest.mark.parametrize("img_path", ["../images/lenna.png"])
def test_ModelMgr_invoke(model_path, img_path):
    base64_str = ImgUtils.img_path_to_base64_str(img_path)
    input_id = 1
    model_input = ModelInput(id=input_id, content=base64_str, metadata=[])

    model_mgr = init_mgr(model_path)
    model_output = model_mgr.invoke(model_input)
    assert model_output.id == input_id
    assert len(model_output.metadata) == 1
