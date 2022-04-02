import logging
import time

import cv2
import numpy as np
from PIL import Image
from protobufs.model_pb2 import ModelInput, ModelOutput, ModelOutputMetadata

from model_module.path_model_source import PathModelSource
from model_module.utils import FileUtils, ImgUtils
from utils import AppConst

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
        return self._model != None

    def get_model(self):
        return self._model

    def load_model(self, model_source: PathModelSource, *args, **kwargs):
        try:
            logger.info(f"TensorFlowModelMgr.load_model: model_source={model_source}")
            if model_source.path_type == PathModelSource.LOCALFILE:
                self._model = self._load_model_from_local(model_source.get_raw_path())
            elif model_source.path_type == PathModelSource.URL:
                self._model = self._load_model_from_url(model_source.path)
            else:
                raise NotImplementedError()
            logger.info(f"TensorFlowModelMgr.load_model done")
        except Exception as ex:
            logger.error(f"TensorFlowModelMgr.load_model: {ex}")

    def invoke(self, model_input: ModelInput, *args, **kwargs) -> ModelOutput:
        try:
            logger.info(f"TensorFlowModelMgr.invoke model_input.id={model_input.id}")

            if not self.is_model_loaded:
                raise Exception(f"TensorFlowModelMgr.invoke: Model is not loaded.")

            img_pil = self._base64_to_pil_image(model_input.content)
            orig_img = np.array(img_pil)

            inp = self._prepare_input(orig_img)
            preds = self._predict(inp)
            out = self._prepare_output(preds, orig_img, model_input)
            logger.info(f"TensorFlowModelMgr.invoke done")
            return out
        except Exception as ex:
            logger.error(f"TensorFlowModelMgr.invoke: {ex}")

    def _load_model_from_url(self, url: str):
        """
        Supports zip file only
        """
        current_time = int(time.time())
        out_file = f"{AppConst.TMP_DIR}/tf_model_{current_time}.zip"
        FileUtils.download_object(url, out_file)

        out_dir = f"{AppConst.TMP_DIR}/tf_model_{current_time}"
        FileUtils.extract_zip(out_file, out_dir)

        model = self._load_model_from_local(out_dir)
        return model

    def _load_model_from_local(self, local_path: str):
        import tensorflow as tf

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
