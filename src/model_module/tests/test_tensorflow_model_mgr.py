import pytest
from model_module.path_model_source import PathModelSource

from model_module.tensorflow_model_mgr import TensorFlowModelMgr
from model_module.utils import ImgUtils
from protobufs.model_pb2 import ModelInput


def init_mgr(model_local_path):
    model_source = PathModelSource(f"file://{model_local_path}")
    tf_model_mgr = TensorFlowModelMgr()
    tf_model_mgr.load_model(model_source)
    return tf_model_mgr


@pytest.mark.slow
@pytest.mark.parametrize("model_local_path", ["../models/tf_face_det/"])
def test_TensorFlowModelMgr_load_model(model_local_path):
    tf_model_mgr = init_mgr(model_local_path)
    assert tf_model_mgr.model != None


@pytest.mark.slow
@pytest.mark.parametrize("model_local_path", ["../models/tf_face_det/"])
@pytest.mark.parametrize("img_path", ["../images/lenna.png"])
def test_TensorFlowModelMgr_invoke(model_local_path, img_path):
    base64_str = ImgUtils.img_path_to_base64_str(img_path)
    input_id = 1
    model_input = ModelInput(id=input_id, content=base64_str, metadata=[])

    tf_model_mgr = init_mgr(model_local_path)
    model_output = tf_model_mgr.invoke(model_input)
    assert model_output.id == input_id
    assert len(model_output.metadata) == 1
