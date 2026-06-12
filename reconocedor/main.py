import cv2
import os
from preprocesado import normalize
from detector import *

def test_dir(filedir: str = "tests"):
    for archivo in os.listdir(filedir):
        if archivo.endswith(('.jpg', '.jpeg', '.png')):            
            test_file(filedir, archivo)

def test_file(filedir: str = "tests", filename: str = "test1.png"):
    ruta = os.path.join(filedir, filename)

    img = cv2.imread(ruta)
    normalized_img, resize_info = normalize(img)
    result = identify_img(normalized_img, filter_threshold=0.25)
    
    new_img = set_boxes(img, result, resize_info)

    ruta_box = os.path.join("boxes", filename)
    cv2.imwrite(ruta_box, new_img)

def main():
    test_dir()

if __name__ == "__main__":
    main()
