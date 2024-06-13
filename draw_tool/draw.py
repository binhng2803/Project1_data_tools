import numpy as np
import cv2

def quadratic_bezier(p0, p1, p2, t):
    return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2

def curved_line(p0, p1, p2, num_points=100):
    points = []
    for t in np.linspace(0, 1, num_points):
        point = quadratic_bezier(p0, p1, p2, t)
        points.append(point)
    return np.array(points, dtype=np.int32)

def draw_curved_line(image, p0, p1, p2):
    curve_points = curved_line(p0, p1, p2)
    cv2.polylines(image, [curve_points], isClosed=False, 
                  color=(2555, 255, 255), thickness=0)
    return image

def draw_straight_line(image, start_point, end_point):
    color = (0, 255, 0)  
    cv2.line(image, start_point, end_point, color, 1)
    return image

if __name__=='__main__':
    # Create a blank image
    # image = np.zeros((400, 400, 3), dtype=np.uint8)
    image = cv2.imread('data\\org_images2\\efea1d4de26fcd1a656f01fb1cb507e1.jpg')
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # data\org_images2\efea1d4de26fcd1a656f01fb1cb507e1.jpg
    # Define the control points
    p0 = np.array([50, 50])
    p1 = np.array([200, 100])
    p2 = np.array([350, 350])

    # Draw the curve
    image = draw_curved_line(image, p0, p1, p2)
    image = draw_straight_line(image, p0, p1)
    image = draw_straight_line(image, p1, p2)

    # Display the image
    cv2.imshow('Quadratic Bezier Curve', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()