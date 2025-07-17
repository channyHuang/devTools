import cv2
import numpy as np

class DrawImageMask():
    def __init__(self, image_name = '/home/channy/Downloads/dataset_train/class1_1/test/bad/1_12_1_31_1.jpg'):
        self.drawing = False
        self.thickness = 3  

        self.run(image_name)

    def onmouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                cv2.circle(self.img, (x, y), self.thickness, [255, 0, 0], -1)
                cv2.circle(self.output, (x, y), self.thickness, [255, 255, 255], -1)
            else:
                self.show = np.zeros(self.img.shape[:2], np.uint8) 
                cv2.putText(self.show, '{}.{}'.format(x, y), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            
    def run(self, image_name = './input.jpg'):
        out_name = image_name[:-4] + '.png'
        self.img = cv2.imread(image_name)
        self.show = np.zeros(self.img.shape[:2], np.uint8) 
        self.img2 = self.img.copy()
        self.output = np.zeros(self.img.shape[:2], np.uint8) 
        
        cv2.namedWindow('output')
        cv2.namedWindow('input')
        cv2.setMouseCallback('input', self.onmouse)
        cv2.moveWindow('input', self.img.shape[1]+10,90)


        while True:
            cv2.imshow('output', self.output)
            cv2.imshow('input', self.img)
            cv2.imshow('show', self.show)
            k = cv2.waitKey(1)
            if k == ord('r'):
                self.img = self.img2.copy()
                self.output = np.zeros(self.img.shape[:2], np.uint8) 
            elif k == ord('s'):
                cv2.imwrite(out_name, self.output)
            elif k == ord('5'):
                self.thickness = 5
            elif k == ord('7'):
                self.thickness = 7
            elif k == ord('8'):
                self.thickness = 10
            elif k == ord('9'):
                self.thickness = 20
            elif k == ord('q'):
                break

class DrawImageRepair():
    def __init__(self, image_name = '/home/channy/Downloads/dataset_train/class4_4_val/test/bad/1_31_2_29_7.jpg'):
        self.stx = 0
        self.sty = 0
        self.endx = 100
        self.endy = 100
        self.drawing = False
        self.run(image_name)

    def onmouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.stx = x
            self.sty = y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.img = self.img2.copy()
                cv2.rectangle(self.img, (self.stx, self.sty), (x, y), (255, 0, 0), 3)
            else:
                self.show = np.zeros(self.img.shape[:2], np.uint8) 
                cv2.putText(self.show, '{}.{}'.format(x, y), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.endx = x
            self.endy = y

    def run(self, image_name):
        out_name = image_name[:-4] + '_repair.jpg'
        self.img = cv2.imread(image_name)
        self.img2 = self.img.copy()
        self.output = np.zeros(self.img.shape[:2], np.uint8) 
        
        cv2.namedWindow('output')
        cv2.namedWindow('input')
        cv2.setMouseCallback('input', self.onmouse)
        cv2.moveWindow('input', self.img.shape[1]+10,90)


        while True:
            cv2.imshow('output', self.output)
            cv2.imshow('input', self.img)
            k = cv2.waitKey(1)
            if k == ord('r'):
                self.img = self.img2.copy()
                self.output = np.zeros(self.img.shape[:2], np.uint8) 
            elif k == ord('s'):
                cv2.imwrite(out_name, self.output)
            elif k == ord('p'):
                mask = np.zeros(self.img.shape[:2], np.uint8)
                img = self.img2.copy()
                cv2.rectangle(mask, (self.stx, self.sty), (self.endx, self.endy), (255, 255, 255), -1)
                # inpaint = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
                inpaint = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
                self.output = inpaint.copy()
            elif k == ord('q'):
                break
        

if __name__ == '__main__':
    app = DrawImageMask('/home/channy/Downloads/dataset_train/class2_8/test/bad/2_29_3_8_40.jpg')
    # app = DrawImageRepair('/home/channy/Downloads/dataset_train/class4_4_val/test/bad/1_12_1_31_34.jpg')