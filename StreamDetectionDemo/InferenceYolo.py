import logging
import os
import sys
import numpy as np
import cv2
import torch
from ultralytics import YOLO

sys.path.append(os.path.dirname(__file__))

from Config import *

class BaseInferenceYolo:
    def __init__(self, 
                sModelname = 'models/yolov8n.pt', 
                sConfigName = 'models/yolov8.yaml',
                sAbsPath = os.path.dirname(__file__)):

        self.sAbsPath = sAbsPath
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

        logging.basicConfig(
            level = logging.INFO,
            format= '%(asctime)s [%(levelname)s] %(name)s  - %(message)s',
            filename = __file__ + '.log'
        )

        self.logger = logging.getLogger(__name__)

        try:
            self.sModel = os.path.join(sAbsPath, sModelname)
            self.model = YOLO(self.sModel)
            self.model.to(self.device)
            self.model.eval()
        except:
            self.logger.error('Exception:' + self.__class__.__qualname__ + ' model load failed!')
            self.logger.info(os.path.join(sAbsPath, sModelname))

    def inference(self, inputs, draw = False):
        if self.model is None:
            return None

        input_data = self.preprocess(inputs)

        outputs = self.model.predict(input_data, verbose = False)

        results, classes, boxes, scores = self.postprocess(outputs, draw, inputs)
        return results, classes, boxes, scores

    def preprocess(self, inputs):
        return inputs

    def postprocess(self, outputs, draw = False, image = None):
        boxes = []
        scroes = []
        classes = []
        for result in outputs:
            if result.boxes is not None:
                scores = result.boxes.conf.cpu().tolist()
                classes = result.boxes.cls.cpu().tolist()

                # [[x y x y], [x y x y], ...]
                boxes_data = result.boxes.xyxy.cpu().tolist()

        return inputs, classes, boxes, scores

    def test(self):
        infer = YOLOInference()

        # infer.inference('./data/bus.jpg')
    
        image = cv2.imread('./data/bus.jpg')
        infer.inference(image)

class InferenceYolo(BaseInferenceYolo):
    # @override #python 3.12+
    def preprocess(self, inputs):
        return inputs

    # @override
    def postprocess(self, outputs, draw = False, image = None):
        boxes = []
        scroes = []
        classes = []
        for result in outputs:
            if result.boxes is not None:
                scores = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy().astype(np.int32)
                boxes = result.boxes.xyxy.cpu().numpy()

                keep = scores > CONF_THRES

                boxes, classes, scores = boxes[keep], classes[keep], scores[keep]

        if draw == True:
            self.draw(image, boxes, scores, classes)

        return image, classes, boxes, scores

    @staticmethod
    def draw(image, boxes, scores, classes):
        for box, score, cl in zip(boxes, scores, classes):
            top, left, right, bottom = [int(_b) for _b in box]
            # print("%s @ (%d %d %d %d) %.3f" % (CLASSES[cl], top, left, right, bottom, score))
            cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
            cv2.putText(image, '{0} {1:.2f}'.format(CLASSES[cl], score),
                        (top, left - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
if __name__ == '__main__':
    infer = InferenceYolo('models/yolov8n.pt')

    sImage = os.path.join(os.path.dirname(__file__), 'data/bus.jpg')
    image = cv2.imread(sImage)

    result, classes, boxes, scores = infer.inference(image, True)

    # cv2.imshow('result', result)
    # cv2.waitKey(1000)
    # cv2.imwrite('res.jpg', result)
    # cv2.destroyAllWindows()
