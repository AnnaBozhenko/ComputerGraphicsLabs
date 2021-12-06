from math import cos, sin, radians
import numpy as np
import re
import matplotlib.pyplot as plt


def form_matrice(point, angle):
    """point - list with two numbers, coordinates of a point in Cartesian system;
    angle - number;
    returns numpy array 3x3"""
    return np.array([[cos(angle), sin(angle), 0],
                     [-sin(angle), cos(angle), 0],
                     [point[0] * (1 - cos(angle)) + point[1] * sin(angle),
                      point[1] * (1 - cos(angle)) - point[0] * sin(angle),
                      1]
                     ])


def affine_transformation(points_arr, center_point, angle):
    """points_arr - list of lists, where lists are points' coordinates in Cartesian system;
    center_point - list with two numbers - x and y coordinates of a point in Cartesian;
    angle - a number;
    returns list of lists, which have two numbers - coordinates of a point in a transformed Cartesian."""
    for i in range(len(points_arr)):
        point = np.array(points_arr[i] + [1])
        matrice = form_matrice(center_point, angle)
        point = np.matmul(point, matrice)
        points_arr[i] = point
    return np.array(points_arr)


def coordinates(file_name):
    """file_name - string, which represent name of file,
    returns points' coordinates (in 2D) from given file
    returns list of x- and y- values according to Cartesian system"""
    points_arr = []
    regexp = r"\d+"
    with open(file_name) as f:
        for line in f:
            temp = re.findall(regexp, line)
            points_arr += [[int(temp[0]), int(temp[1])]]
    return points_arr


def max_i(points_arr, ind):
    """points_arr - list of lists (length of lists are equal and is greater than ind),
    returns index of list in points_arr, that has the greatest value by ind's index"""
    max_i_coord = 0
    for i in range(len(points_arr)):
        if points_arr[ind] > max_i_coord:
            max_i_coord = points_arr[ind]
    return max_i_coord


def save_and_show(points_arr, file_to_save_as, width_in_pixels, height_in_pixels):
    """points_arr - list of lists, where lists are points' coordinates in Cartesian system;
    file_to_save_as - string; width_in_pixels, height_in_pixels - numbers"""
    x_coords = points_arr[:, 0]
    y_coords = points_arr[:, 1]
    dpi = 100
    width_in_pixels /= dpi
    height_in_pixels /= dpi
    fig, (ax) = plt.subplots(figsize=(width_in_pixels, height_in_pixels), dpi=100)
    ax.scatter(x_coords, y_coords, color="blue")
    ax.axis('off')
    plt.savefig(file_to_save_as)
    plt.show()
    plt.close()


# Driver code
file_n = "DS1.txt"
points = coordinates(file_n)
angle_in_rad = radians(10 * (1 + 1))
center = [480, 480]
points = affine_transformation(points, center, angle_in_rad)
save_and_show(points, "affine_transform.png", 960, 960)
