import cv2
from preprocesado import normalize
from detector import *

def main():
    img = cv2.imread("tests/I-80_Eastshore_Fwy.jpg")
    normalized_img, resize_info = normalize(img)
    result = identify_img(normalized_img)
    result = filter_classes(result)
    new_img = set_boxes(img, result, resize_info)

    cv2.imwrite("./testboxes.png", new_img)

    print(len(result.boxes))

if __name__ == "__main__":
    main()
