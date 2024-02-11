import cv2
from ClassimageProcessingModule import ImageProcessingModule



if __name__ == "__main__":
    module = ImageProcessingModule()
    image = cv2.imread("street_lamp.jpg")
    pipeline = [("resize", (640, 640)), ("adjust_brightness", 3.), ("binarize", 150), ("invert",)]
    def callback(result):
        print(f'[INFO]... processing completed successfully')
        # Тут можно обработать результат

    module.process_image_async(image, pipeline, callback)
    # продолжаем работать, так как основной поток не блокирован