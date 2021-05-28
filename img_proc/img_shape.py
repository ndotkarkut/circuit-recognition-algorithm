import cv2 as cv2
import numpy as np

image = '../test_pictures/textbook/circuit6.png'
image = '../test_pictures/handwritten/0524_brandnew.jpg'
image = '../test_pictures/textbook/tough_circuit.png'
image = '../test_pictures/handwritten/3_loop_circuit_i.jpg'
image = '../test_pictures/handwritten/3_loop_new.jpg'

img = cv2.imread(image)
print(img.shape)
resized_img = cv2.resize(img, (int(img.shape[1] * 0.2), int(img.shape[0] * 0.2)), cv2.INTER_AREA)
loop_detection_img = img.copy()
img_x, img_y, img_z = img.shape

print(resized_img.shape)

cv2.imwrite('../test_pictures/handwritten/3_loop_new_r.jpg', resized_img)
# cv2.imwrite('../test_pictures/textbook/0524_tough.png', resized_img)
