
import cv2
import numpy as np  
import os


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append((x, y))


def point_reader(image_path):

    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"No file found at {image_path}")

    img = cv2.imread(image_path)
    if img is None:
        raise IOError(f"Could not open image at {image_path}")

    points = []

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', click_event, points)

    while True:
        cv2.imshow('Image', img)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    return np.array(points)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('Lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def vanishing_point(image_path):
    points = point_reader(image_path)
    
    if len(points) != 4:
        raise ValueError("Exactly four points are required to define two lines.")

    line1 = (points[0], points[1])
    line2 = (points[2], points[3])

    vp_x, vp_y = line_intersection(line1, line2)

    img = cv2.imread(image_path)
    cv2.line(img, line1[0], line1[1], (255, 0, 0), 2)
    cv2.line(img, line2[0], line2[1], (255, 0, 0), 2)
    cv2.circle(img, (int(vp_x), int(vp_y)), 5, (0, 255, 0), -1)

    cv2.imwrite('image_with_vanishing_point.jpg', img)
    cv2.imshow('Vanishing Point', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    
    # # Task 0
    # home_directory = os.path.expanduser('~')
    # downloads_path = os.path.join(home_directory, 'Downloads')
    # image_filename = '1.jpeg'
    # image_path = os.path.join(downloads_path, image_filename)
    # points_array = point_reader(image_path)
    # print(points_array)

    # # Task 1
    # image_filename = 'spot.jpg'
    # image_path = os.path.join(downloads_path, image_filename)
    # vanishing_point(image_path)

    # Task 3
    # image_filename = 'img1_gray.jpg'
    # image_path = '/Users/fj/Downloads/img1_gray.jpg'
    # point1_array = point_reader(image_path)
    # print(point1_array)
    
    # image_filename = 'img2_gray.jpg'
    # image_path = '/Users/fj/Downloads/img2_gray.jpg'
    # point2_array = point_reader(image_path)
    # print(point2_array)

    # Last Task
    # image_filename = 'Last.jpeg'
    # image_path = '/Users/fj/Downloads/Last.jpeg'
    # point20_array = point_reader(image_path)
    # print(point20_array)

main()