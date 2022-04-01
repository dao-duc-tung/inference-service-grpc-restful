import logging

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from model_module.utils import ImgUtils
from protobufs.model_pb2 import ModelInput, ModelOutput, ModelOutputMetadata
from utils import AppConst

from model_module.path_model_source import PathModelSource

from .i_model_mgr import IModelMgr

logger = logging.getLogger(AppConst.APP_NAME)


class TensorFlowModelMgr(IModelMgr):
    """
    Ref: https://github.com/jason9075/Ultra-Light-Fast-Generic-Face-Detector_Tensorflow-Model-Converter
    """

    def __init__(self) -> None:
        self._model = None

    @property
    def is_model_loaded(self) -> bool:
        return True

    @property
    def model(self):
        return self._model

    def load_model(self, model_source: PathModelSource, *args, **kwargs):
        logger.info(f"Load model from {model_source}")
        if model_source.path_type == PathModelSource.LOCALFILE:
            self._model = self._load_model_from_local(model_source.get_raw_path())
        elif model_source.path_type == PathModelSource.URL:
            self._model = self._load_model_from_url(model_source.get_raw_path())
        else:
            raise NotImplementedError()

    def invoke(self, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        logger.info(f"Invoke model for input id={model_input.id}")

        img_pil = self._base64_to_pil_image(model_input.content)
        orig_img = np.array(img_pil)

        inp = self._prepare_input(orig_img)
        preds = self._predict(inp)
        out = self._prepare_output(preds, orig_img, model_input)
        return out

    def _load_model_from_url(self, url: str):
        raise NotImplementedError()

    def _load_model_from_local(self, local_path: str):
        model = tf.keras.models.load_model(local_path)
        return model

    def _prepare_output(
        self, preds: np.ndarray, img_np: np.ndarray, model_input: ModelInput
    ) -> ModelOutput:
        bbox_list = []
        h, w, _ = img_np.shape
        for pred in preds:
            start_x = int(pred[-4] * w)
            start_y = int(pred[-3] * h)
            end_x = int(pred[-2] * w)
            end_y = int(pred[-1] * h)
            bbox_val = f"{start_y},{start_x},{end_y},{end_x}"
            bbox = ModelOutputMetadata(key="bbox", value=bbox_val)
            bbox_list.append(bbox)

        model_output = ModelOutput(id=model_input.id, metadata=bbox_list)
        return model_output

    def _predict(self, img_np: np.ndarray) -> np.ndarray:
        pred = self._model.predict(img_np)
        return pred

    def _prepare_input(self, img_np: np.ndarray):
        img_resize = cv2.resize(img_np, (320, 240))
        img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
        img_resize = img_resize - 127.0
        img_resize = img_resize / 128.0
        img_expand = np.expand_dims(img_resize, axis=0)
        return img_expand

    def _base64_to_pil_image(self, base64_str: str):
        buf = ImgUtils.base64_str_to_bytes_io(base64_str)
        img = Image.open(buf)
        return img
