import cv2
import os

list_name = os.listdir(r"images")
for name in list_name:
    path = "images"
    image_name = path + "\\" + name
    img = cv2.imread(image_name)
    img = cv2.resize(img, (500, 500))
    cv2.imshow('slide show', img)
    cv2.waitKey(3000)
cv2.destroyAllWindows()