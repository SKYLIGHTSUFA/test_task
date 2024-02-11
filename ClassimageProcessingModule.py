import cv2
import threading


class ImageProcessingModule:
    def __init__(self):
        self.lock = threading.Lock()

    def resize(self, image, size):
        resized_image = cv2.resize(image, size)
        return resized_image

    def brightness(self, image, cliplimit): # работаем с освещенностью изображения. Особенно важно для сумерек на дорогах
        clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(16, 16))
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l2 = clahe.apply(l)
        lab = cv2.merge((l2, a, b))
        adjusted_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        cv2.imwrite('out.png', adjusted_image)
        return adjusted_image

    def binarize(self, image, threshold):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
        return binary_image

    def invert(self, image):
        invert_image = cv2.bitwise_not(image)
        return invert_image

    def process_image(self, image, pipeline):
        processed_image = image.copy()
        for operation in pipeline:
            if operation[0] == "resize":
                size = operation[1]
                processed_image = self.resize(processed_image, size)
            elif operation[0] == "brightness":
                processed_image = self.brightness(processed_image, operation[1])
            elif operation[0] == "binarize":
                threshold = operation[1]
                processed_image = self.binarize(processed_image, threshold)
            elif operation[0] == "invert":
                processed_image = self.invert(processed_image)

        return processed_image

    def process_image_async(self, image, pipeline, callback):
        def process():
            processed_image = self.process_image(image, pipeline)
            callback(processed_image)

        thread = threading.Thread(target=process)
        thread.start()
