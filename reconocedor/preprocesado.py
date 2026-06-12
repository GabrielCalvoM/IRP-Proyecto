import cv2

def resize_img(img: cv2.Mat) -> cv2.Mat:
    height, width = img.shape[:2]
    scale = 640 / max([height, width])

    rescaled_img = cv2.resize(img, None, fx=scale, fy=scale)

    new_height, new_width = rescaled_img.shape[:2]
    v_padding, h_padding = 640 - new_height, 640 - new_width

    top: int = v_padding // 2
    bottom: int = v_padding - top
    left: int = h_padding // 2
    right: int = h_padding - left

    resized_img = cv2.copyMakeBorder(rescaled_img, top, bottom, left, right, cv2.BORDER_CONSTANT)
    resize_info = {"scale": scale, "top": top, "bottom": bottom, "left": left, "right": right}

    return resized_img, resize_info

def normalize(img: cv2.Mat) -> cv2.Mat:
    normalized_img, resize_info = resize_img(img)

    return normalized_img, resize_info
