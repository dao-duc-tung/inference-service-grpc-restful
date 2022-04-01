import pytest

from model_module.utils import ImgUtils

TRIM_LEN = 10


@pytest.mark.parametrize("param", [("../images/lenna.png", b"iVBORw0KGg")])
def test_ImgUtils_img_path_to_base64_str(param):
    img_path, result = param
    output = ImgUtils.img_path_to_base64_str(img_path)
    output = output[:TRIM_LEN]
    assert output == result


@pytest.mark.parametrize("param", [(b"\x89PNG\r\n\x1a\n\x00\x00", b"iVBORw0KGgoAAA==")])
def test_ImgUtils_bytes_str_to_base64_str(param):
    byte_str, result = param
    output = ImgUtils.bytes_str_to_base64_str(byte_str)
    assert output == result


@pytest.mark.parametrize("param", [(b"iVBORw0KGgoAAA==", b"\x89PNG\r\n\x1a\n\x00\x00")])
def test_ImgUtils_base64_str_to_bytes_io(param):
    base64_str, result = param
    output = ImgUtils.base64_str_to_bytes_io(base64_str)
    output = output.read()
    assert output == result
