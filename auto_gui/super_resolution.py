from cv2 import dnn_superres

from auto_gui import error

# https://github.com/opencv/opencv_contrib/tree/master/modules/dnn_superres
DEFAULT_MODEL = {
    "fsrcnn": "auto_gui/model/FSRCNN_x2.pb"
}

class SuperResolution(object):
    def __init__(self, **data):
        self.img = data.get("img")
        self.sr = dnn_superres.DnnSuperResImpl_create()
        self.model = data.get("model", "fsrcnn")

        self.read_model()

    def read_model(self):
        model_path = DEFAULT_MODEL.get(self.model)
        if model_path == None:
            raise Exception(error.SR_MODEL_NOT_FOUND)

        self.sr.readModel(model_path)

    def scale(self, ratio=2):
        self.sr.setModel(self.model, ratio)
        return self.sr.upsample(self.img)
