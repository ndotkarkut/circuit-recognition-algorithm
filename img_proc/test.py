import cv2
import numpy as np
import json
import imutils
from shapedetector import ShapeDetector

def parse_predictions():
    detections = []
    with open('../predictions.txt', 'r') as f:
        for line in f.readlines():
            # parse the file's text into an array
            if 'left_x' in line:
                parsed_line = line.split(' ')
                while '' in parsed_line:
                    parsed_line.remove('')
            
                # take the raw array and place into dict 
                detection_dict = {}
                for el in parsed_line:
                    if 'left_x' in el:
                        detection_dict['left_x'] = parsed_line[parsed_line.index(el)+1]
                    elif 'top_y' in el:
                        detection_dict['top_y'] = parsed_line[parsed_line.index(el)+1] 
                    elif 'width' in el:
                        detection_dict['width'] = parsed_line[parsed_line.index(el)+1]
                    elif 'height' in el:
                        detection_dict['height'] = parsed_line[parsed_line.index(el)+1].rstrip(')\n')

                detections.append(detection_dict)
                
    return detections 

def find_intersection(line1, line2):
    # line1[0] = x1
    # line1[1] = y1
    # line1[2] = x2
    # line1[3] = y2
    
    xdiff = (line1[0] - line1[2], line2[0] - line2[2])
    ydiff = (line1[1] - line1[3], line2[1] - line2[3])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    line_1 = ((line1[0], line1[1]), (line1[2], line1[3]))
    line_2 = ((line2[0], line2[1]), (line2[2], line2[3]))

    d = (det(*line_1), det(*line_2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def find_intersection_neighbors(intersection_info):
    # neighbor info = {node_number: (x,y), [...neighbors]; }
    neighbor_info = {}
    i = 0
    for info in intersection_info:
        # print('current_node is: ', info[0])
        node_coords = info[0] # x,y
        hori_line = info[1] # x1,y1,x2,y2
        vert_line = info[2] # x1,y1,x2,y2
        # print(hori_line, vert_line)
        
        is_on_hori_line = []
        for other_info in intersection_info:
            other_node = other_info[0] # x,y
            
            # check if this other node is on horizontal line 
            if (other_node[1] >= hori_line[1] and other_node[1] <= hori_line[3]) or (other_node[1] <= hori_line[1] and other_node[1] >= hori_line[3]):
                is_on_hori_line.append(other_node)
                
        
        # check if nodes in is_on_hori_line are neighbors to current node
        hori_neighbors = []
        right_neighbor = None
        left_neighbor = None 
        for node in is_on_hori_line: 
            x, y = node_coords
            
            if node[0] == x and node[1] == y:
                pass 
            else:                 
                if node[0] <= x:
                    if left_neighbor == None:
                        left_neighbor = node 
                    else: 
                        if abs(node[0] - x) < abs(left_neighbor[0] - x):
                            left_neighbor = node 
                elif node[0] >= x:
                    if right_neighbor == None:
                        right_neighbor = node 
                    else: 
                        if abs(node[0] - x) < abs(right_neighbor[0] - x):
                            right_neighbor = node 
                            
                            
        # print(right_neighbor, left_neighbor)
        if right_neighbor:
            hori_neighbors.append(right_neighbor)
        if left_neighbor:
            hori_neighbors.append(left_neighbor)
        # if right_neighbor != None:
        #     cv2.circle(loop_detection_img, (int(right_neighbor[0]), int(right_neighbor[1])), 5, (0,0,255), -1)
        # if left_neighbor != None:
        #     cv2.circle(loop_detection_img, (int(left_neighbor[0]), int(left_neighbor[1])), 5, (0,0,255), -1)
        # cv2.circle(loop_detection_img, (int(node_coords[0]), int(node_coords[1])), 5, (0,255,0), -1)
                
        # find out what nodes lay on vertical line and are neighbors vertically
        is_on_vert_line = []
        for other_info in intersection_info:
            other_node = other_info[0] # x,y
            
            # check if this other node is on vertical line 
            if (other_node[0] >= vert_line[0] and other_node[0] <= vert_line[2]) or (other_node[0] <= vert_line[0] and other_node[0] >= vert_line[2]):
                is_on_vert_line.append(other_node)
                
        
        # check if nodes in is_on_vert_line are neighbors to current node
        vert_neighbors = []
        up_neighbor = None
        down_neighbor = None 
        for node in is_on_vert_line: 
            x, y = node_coords
            
            if node[0] == x and node[1] == y:
                pass 
            else:                 
                if node[1] <= y:
                    if down_neighbor == None:
                        down_neighbor = node 
                    else: 
                        if abs(node[1] - y) < abs(down_neighbor[1] - y):
                            down_neighbor = node 
                elif node[1] >= y:
                    if up_neighbor == None:
                        up_neighbor = node 
                    else: 
                        if abs(node[1] - y) < abs(up_neighbor[1] - y):
                            up_neighbor = node 
                            
        # print(up_neighbor, down_neighbor)
        if up_neighbor:
            vert_neighbors.append(up_neighbor)
        if down_neighbor:
            vert_neighbors.append(down_neighbor)
        # if up_neighbor != None:
        #     cv2.circle(loop_detection_img, (int(up_neighbor[0]), int(up_neighbor[1])), 5, (0,0,255), -1)
        # if down_neighbor != None:
        #     cv2.circle(loop_detection_img, (int(down_neighbor[0]), int(down_neighbor[1])), 5, (0,0,255), -1)                           
               
         
        neighbor_info[i] = node_coords, hori_neighbors, vert_neighbors
        
        i += 1
        
        ### END OF FOR LOOP ### 

    return neighbor_info
     
def get_key(dictionary, val):
    ''' used to find the node number based on the location of the node '''
    for key, value in dictionary.items():
        if val == value[0]: 
            return key   
        
def find_neighbors(neighbor_dict):
    ''' return a list of the vertical and horizontal neighbors in 
        just one array together
    '''
    
    neighbor_array = []
    
    for neighbor in neighbor_dict[1]:
        neighbor_array.append(neighbor)
        
    for neighbor in neighbor_dict[2]:
        neighbor_array.append(neighbor)
        
    return neighbor_array
      
def node_enumeration(neighbor_info, cmp_locations, resistor_dimensions):
    # print(cmp_locations)
    # print('neighbor info: ', neighbor_info) 
    nodes = {}
    cmp_nodes = []
    for i in list(neighbor_info.keys()):
        nodes[i] = None 
    # print(nodes)
    
    i = 0
    for node in neighbor_info:
        node_x = neighbor_info[node][0][0]
        node_y = neighbor_info[node][0][1]
        
        coords = (int(neighbor_info[node][0][0]), int(neighbor_info[node][0][1]))
        cv2.circle(loop_detection_img, coords, 5, (0, 255, 0), -1)
        
        # print(neighbor_info[node][0])
        
        # first node we check is considered as Node 0
        if i == 0:
            nodes[i] = 0
        
        # make dict of neighbors only
        neighbors = find_neighbors(neighbor_info[i])
        # del neighbors[i]
        # print(neighbors)
        # i += 1
        # continue

        for neighbor in neighbors:
            print(neighbor)
            neighbor_x = neighbor[0]
            neighbor_y = neighbor[1]
            cmp_exists = False
            
            for cmp_loc in cmp_locations:
                # print(cmp_loc)
                # find center of component 
                # cmp_ctr = ()
                
                cmp_x = np.arange(cmp_loc[0], cmp_loc[0] + cmp_loc[2])
                cmp_y = np.arange(cmp_loc[1], cmp_loc[1] + cmp_loc[3])
                # print(cmp_x, cmp_y)
                
                if node_x > neighbor_x:
                    x_result = np.where(np.logical_and(cmp_x >= neighbor_x, cmp_x <= node_x))
                else:
                    x_result = np.where(np.logical_and(cmp_x >= node_x, cmp_x <= neighbor_x))

                if node_y > neighbor_y:
                    y_result = np.where(np.logical_and(cmp_y >= neighbor_y, cmp_y <= node_y))
                else:
                    y_result = np.where(np.logical_and(cmp_y >= node_y, cmp_y <= neighbor_y))

                # print(np.any(x_result), np.any(y_result))
                
                if np.any(x_result) and np.any(y_result):
                    if cmp_loc in resistor_dimensions:
                        cmp_nodes.append((get_key(neighbor_info, neighbor_info[node][0]), get_key(neighbor_info, neighbor)))
                    
                    cmp_exists = True 
                    coords = (int(neighbor[0]), int(neighbor[1]))
                    cv2.circle(loop_detection_img, coords, 5, (0, 0, 255), -1)

                # break
                # x_result = np.where(np.logical_and(cmp_x > node[0][0], cmp_x < neighbor[0][0]))
                
            # assign the node a value of 1 more than current node if 
            # component exists between nodes    
            if cmp_exists:
                neighbor_node_num = get_key(neighbor_info, neighbor)
                if nodes[neighbor_node_num] == None:
                    nodes[neighbor_node_num] = nodes[i] + 1
            else:
                neighbor_node_num = get_key(neighbor_info, neighbor)
                if nodes[neighbor_node_num] == None:
                    nodes[neighbor_node_num] = nodes[i]
                else:
                    nodes[neighbor_node_num] = nodes[i]
                    
        # if i == 3:
            # break
    
        i += 1
         
    # get rid of duplicate node pairings for resistor nodes        
    resistor_nodes = clean_res_nodes(cmp_nodes)
    
    # convert the numbers in resistor nodes to the node numbers 
    # we assigned based on the circuit configuration
    # used to tell if it is series or parallel circuit
    final_res_node_nums, final_res_node_str = apply_num_to_node(resistor_nodes, nodes)
                
    print(cmp_nodes)        
    print(nodes)
    print(final_res_node_nums)
    
    parallel_amount, series_amount = count_parallel_and_series(final_res_node_str)
    
    print(parallel_amount, series_amount)
    
    return (parallel_amount, series_amount)

def count_parallel_and_series(final_node_vals):
    '''
    function for finding out how many series resistors and 
    how many parallel resistors are found in each circuit
    '''
    print(final_node_vals)
    occurence_dict = {}
    # dict for holding # of occurences of each instance
    for node_val in final_node_vals:
        # count num of instances
        count = final_node_vals.count(node_val)
        
        if node_val not in occurence_dict:
            occurence_dict[node_val] = 1
        else:
            occurence_dict[node_val] += 1
                
    print(occurence_dict)
            
    # length of dictionary decides how many resistors in series there are
    # non-one values for keys means there are resistors in parallel
    
    num_of_series = len(occurence_dict)
    num_of_parallel = [value for key, value in occurence_dict.items()]
    
    return num_of_parallel, num_of_series
            
def apply_num_to_node(resistor_nodes, node_numbers):
    ''' change the default intersection numbers into circuit nodes
    so we can tell if they are series or parallel resistors
    '''
    final_node_numbers = []
    final_node_strings = []
    for res_node in resistor_nodes:
        # node_0 is node on one side of the component
        # node_1 is node on other side of the component
        node_0 = res_node[0]
        node_1 = res_node[1] 
        # we then re-assign whatever these values are to the new values
        # i.e. (0,4) => (0,1) ; (3,7) => (0,1)
        new_node_0 = node_numbers[node_0]
        new_node_1 = node_numbers[node_1]
        
        final_node_numbers.append((new_node_0, new_node_1))
        final_node_strings.append((str(new_node_0) + '_' + str(new_node_1)))
        
    return final_node_numbers, final_node_strings   
    
def clean_res_nodes(node_arr):
    '''
    get rid of duplicate nodes in our array that tracks which lines 
    have resistors/components in between them
    ''' 
    clean_array = []
    for node_a in node_arr:
        for node_b in node_arr:
            if node_a != node_b:
                if len(set(node_a) & set(node_b)) != 2 and sorted(node_a) not in clean_array:
                    clean_array.append(sorted(node_a))

    # return the array elements back in tuple form
    return_array = []
    for arr in clean_array:
        return_array.append(tuple(arr))
    print(return_array)
    return return_array

# images = ['../circuit4.png', '../predictions.jpg']
images = ['../circuit4.png']

i = 0
for image in images:
    i += 1
    # open image of circuit
    img = cv2.imread(image)
    loop_detection_img = img.copy()
    img_x, img_y, img_z = img.shape
    # print('shape', img.shape)

    detections = parse_predictions()
    
    cmp_dims = []
    res_dims = []
    # manually adding the battery for node quantifying
    cmp_dims.append((57-10, 84-20, 20, 42))
    
    for component in detections:
        left_x = int(component['left_x'])
        top_y = int(component['top_y'])
        width = int(component['width'])
        height = int(component['height'])
        # print(left_x, top_y, width, height)
        #TODO: make a way to distinguish between resistors and batteries
        res_dims.append((left_x, top_y, width, height))
        cmp_dims.append((left_x, top_y, width, height))
        
        top_left = (left_x, top_y)
        bot_right = (left_x + width, top_y + height)
        
        cv2.rectangle(img, top_left, bot_right, (0,0,0), -1)
        cv2.rectangle(loop_detection_img, top_left, bot_right, (255,255,255), -1)
        
        # replace the detected components with lines to create loops 
        if width > height:
            cv2.line(loop_detection_img, (left_x, top_y + int(height / 2)), (left_x + width, top_y + int(height / 2)), (0,0,0), 2)
        elif height > width:
            cv2.line(loop_detection_img, (left_x + int(width / 2), top_y), (left_x + int(width / 2), top_y + height), (0,0,0), 2)
        
        loop_det_img_copy = loop_detection_img.copy()
        cv2.imshow('loop_det', loop_det_img_copy)
        # find lines of the wires on the circuits using HoughLinesP
        # first blur the image for smoother lines 
        loop_det_img_copy = cv2.GaussianBlur(loop_det_img_copy, (3,3), 0)
        # convert to gray scale to make easier
        gray_img = cv2.cvtColor(loop_det_img_copy, cv2.COLOR_BGR2GRAY)
        # create an edge detection image
        edges = cv2.Canny(gray_img, 75, 100)
        # create a threshold image
        thresh = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)[1]
        # edges of threshold image lol
        thresh_edges = cv2.Canny(thresh, 75, 100)
        
        cv2.imshow('gray', gray_img)
        cv2.imshow('thresh', thresh)
        cv2.imshow('thresh_edges', thresh_edges)

        # END OF FOR-LOOP

    # generate the lines using Houghlines
    lines = cv2.HoughLinesP(thresh_edges.copy(), 1, np.pi/180, 75,
                    minLineLength=5, maxLineGap=45)
    
    # print(len(lines))
    horizontal_lines = []
    vertical_lines = []
    # add lines to image
    for line in lines:
        x1, y1, x2, y2 = line[0]
        
        # check if line is vertical or horizontal
        # x distance > y distance = horizontal line
        # y distance > x distance = vertical line
        if abs(x2 - x1) > abs(y2 - y1):
            cv2.line(loop_det_img_copy, (x1, y1), (x2, y2), (0, 255, 0), 1)
            horizontal_lines.append(line[0])
        else:
            cv2.line(loop_det_img_copy, (x1, y1), (x2, y2), (0, 0, 255), 1)
            vertical_lines.append(line[0])
    
    cv2.imshow('loop_det', loop_det_img_copy)

    intersect_coords = []
    intersect_info = []
    # find intersections 
    
    for horizontal_line in horizontal_lines:
        for vertical_line in vertical_lines:
            intersect_coords.append(find_intersection(horizontal_line, vertical_line))
            intersect_info.append([find_intersection(horizontal_line, vertical_line), horizontal_line, vertical_line])
    
    # print(intersect_coords)
    # print(intersect_info)
    
    # add circles onto the image for the intersection points 
    for coords in intersect_coords:
        coords = (int(coords[0]), int(coords[1]))
        cv2.circle(loop_detection_img, coords, 5, (255, 0, 0), -1)
    
    # finding nearest points to neighbor
    neighbor_info = find_intersection_neighbors(intersect_info)
    
    
    # FIND OUT SERIES AND PARALLEL AMOUNT
    parallel_amt, series_amt = node_enumeration(neighbor_info, cmp_dims, res_dims)
        
    
    # PRINT RESULT TO SCREEN
    if len(parallel_amt) != 0:
        for amount in parallel_amt:
            print(f'THERE IS 1 SERIES OF {amount} RESISTORS IN PARALLEL')
            print(f'{series_amt} SERIES IN TOTAL')
    else:
        print(f'NO PARALLEL COMPONENTS, JUST {series_amt} COMPONENTS IN SERIES')    
        
    cv2.imshow(f'loop detection img {i}', loop_detection_img)
    # cv2.imshow(f'Image {i}', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
