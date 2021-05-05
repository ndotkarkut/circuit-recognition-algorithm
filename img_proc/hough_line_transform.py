import cv2
import numpy as np
import json
import imutils

# open image of circuit
img = cv2.imread('../circuit3.png')
img_x, img_y, img_z = img.shape
print('shape', img.shape)

# use processed object detections to draw circles on circuit
with open('../results.json', 'r') as f:
    json_output = json.load(f)[0]
    detections = json_output['objects']
    for component in detections:
        x = component['relative_coordinates']['center_x']
        y = component['relative_coordinates']['center_y']
        width = component['relative_coordinates']['width']
        height = component['relative_coordinates']['height']
        print(x, y, width, height)

        # multiply by image dimensions to get absolute positions
        ctr_x = int(round(x * img_x))
        # ctr_x = int(round(0.9 * ctr_x))
        ctr_x = int(round(ctr_x))
        ctr_y = int(round(y * img_y))
        if height < width:
            radius = int(round((height * img_x / 2)))
        else:
            radius = int(round((width * img_x / 2)))
        print(ctr_x, ctr_y, radius)
        print('______')

        # place circle on image
        cv2.circle(img, (ctr_x, ctr_y), radius, (255, 0, 0), -1)

        # place line on image
        if height > width:
            ind_1 = (int(ctr_x), int(ctr_y - height * img_y / 2))
            ind_2 = (int(ctr_x), int(ctr_y + height * img_y / 2))
        else:
            ind_1 = (int(ctr_x - width * img_x / 2), int(ctr_y))
            ind_2 = (int(ctr_x + width * img_x / 2), int(ctr_y))
            

        cv2.line(img, ind_1, ind_2, (0, 255, 255), 5)


# find lines of the wires on the circuit
img = cv2.GaussianBlur(img, (9, 9), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 75, 100)


# img = cv2.GaussianBlur(img, (9, 9), 0)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
# edges = cv2.Canny(gray, 75, 100)

# unp_lines = cv2.HoughLines(edges, 1, np.pi/180, 75)
# print(unp_lines)
# print(len(unp_lines))

lines = cv2.HoughLinesP(edges, 1, np.pi/180, 75,
                        minLineLength=5, maxLineGap=45)
# print(lines)
print(len(lines))

lines = cv2.HoughLinesP(edges, 1, np.pi/180, 75,
                        minLineLength=5, maxLineGap=45)
print(lines)
print(len(lines))

for line in lines:
    x1, y1, x2, y2 = line[0]

    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
    
    
for alpha in range(0,90):
    diff_x = ind_2[0] - ind_1[0]
    diff_y = ind_2[1] - ind_2[1]
    
    x_prime = diff_x * np.cos(alpha) - diff_y * np.sin(alpha)
    y_prime = diff_x * np.sin(alpha) - diff_y * np.cos(alpha)
    
    # new_coords = 


cv2.imshow('Edges', edges)
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
