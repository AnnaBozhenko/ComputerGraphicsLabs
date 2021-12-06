import re
from math import atan, pi
from matplotlib import pyplot as plt


def orientation(p_1, p_2, p_3):
    """p_1, p_2, p_3 - numbers, there is a movement p_1-p_2-p_3,
    if the movement represents clockwise orientation - 1 is returned,
    if counterclockwise orientation - 2 is returned,
    else (p_1, p_2 and p_3 lie on the same line) - 0 is returned"""
    # driver formula
    # (y2 - y1)*(x3 - x2) - (y3 - y2)*(x2 - x1)

    orient = (p_2[1] - p_1[1]) * (p_3[0] - p_2[0]) - (p_3[1] - p_2[1]) * (
            p_2[0] - p_1[0])
    if orient > 0:
        return 1
    elif orient < 0:
        return 2
    else:
        return 0


def the_lowest_point_index(points_arr):
    """returns index of the point with the least y-coordinate, if there are several such points,
    returns index of the point with the greatest x-coordinate"""
    if len(points_arr) == 0:
        return None
    # set starting value - the first element
    lowest_ind = 0
    for i in range(len(points_arr)):
        if points_arr[i][1] < points_arr[lowest_ind][1]:
            lowest_ind = i
        elif points_arr[i][1] == points_arr[lowest_ind][1]:
            if points_arr[i][0] > points_arr[lowest_ind][0]:
                lowest_ind = i
    return lowest_ind


def polar_point(point_coords):
    """point_coords - list with two numbers [x, y] - coordinates of a point in Cartesian system,
    the function counts point coordinates in polar system - [squared_length, angle], where len is squared length,
    returns list with two numbers"""
    squared_length = point_coords[0]**2 + point_coords[1]**2
    # x == 0 and y > 0
    if point_coords[0] == 0 and point_coords[1] > 0:
        return [squared_length, pi / 2]
    # x == 0 and y < 0
    elif point_coords[0] == 0 and point_coords[1] < 0:
        return [squared_length, -(pi / 2)]
    # x == 0 and y == 0
    elif point_coords[0] == 0 and point_coords[1] == 0:
        return [squared_length, 0]

    arctg = atan(point_coords[1] / point_coords[0])
    # x > 0
    if point_coords[0] > 0:
        return [squared_length, arctg]
    # x < 0 and y >= 0
    elif point_coords[0] < 0 and point_coords[1] >= 0:
        return [squared_length, arctg + pi]
    # x < 0 and y < 0
    elif point_coords[0] < 0 and point_coords[1] < 0:
        return [squared_length, arctg - pi]


def sort_polar(points_arr):
    """points_arr - list with points' coordinates, represented in lists with two numbers - [x, y],
    where x - x coordinate and y - y coordinate in Cartesian system,
    returns sorted list of points_arr according to polar angle, where pole is found the least and
    rightest point in array"""
    lowest_i = the_lowest_point_index(points_arr)
    lowest_point = points_arr[lowest_i]
    points_arr[lowest_i] = points_arr[0]
    points_arr[0] = lowest_point

    for i in range(1, len(points_arr)):
        # set point coordinates according to the polar - points_arr[0]
        point = [
            points_arr[i][0] - points_arr[0][0],
            points_arr[i][1] - points_arr[0][1]
        ]
        min_polar_point_ind = i
        min_polar_point = polar_point(point)
        for j in range(i + 1, len(points_arr)):
            point = [
                points_arr[j][0] - points_arr[0][0],
                points_arr[j][1] - points_arr[0][1]
            ]
            polar_point_coords = polar_point(point)
            if polar_point_coords[1] < min_polar_point[1]:
                min_polar_point = polar_point_coords
                min_polar_point_ind = j
            elif polar_point_coords[1] == min_polar_point[1]:
                if polar_point_coords[0] < min_polar_point[0]:
                    min_polar_point = polar_point_coords
                    min_polar_point_ind = j
        # swap current point with i-index with found polar point
        temp_i = min_polar_point_ind
        temp = points_arr[temp_i]
        points_arr[temp_i] = points_arr[i]
        points_arr[i] = temp
    return points_arr


def convex_hull_graham(points_arr):
    """points_arr - list with points' coordinates, represented in lists with two numbers - [x, y],
    where x - x coordinate and y - y coordinate in Cartesian system,
    returns list of indices of points which form convex_hull, the points' indices are placed
    sequentially in the list according to their polar angle, where pole is the least and
    rightest point in points_array"""
    points_arr = sort_polar(points_arr)
    if points_arr is None:
        return None
    elif len(points_arr) < 4:
        return points_arr
    # indices of points_arr, where point under particular index forms convex hull
    # include index of the first point as it certainly is one of the convex hull's point
    points_arr_indices_of_hull = [0]
    p_1_ind = 0
    p_2_ind = 1
    p_3_ind = 2
    while True:
        if orientation(points_arr[p_1_ind], points_arr[p_2_ind],
                       points_arr[p_3_ind]) == 2:
            points_arr_indices_of_hull.append(p_2_ind)
            p_1_ind = p_2_ind
            p_2_ind = p_3_ind
            if p_2_ind == 0:
                break
            p_3_ind = (p_3_ind + 1) % len(points_arr)
        else:
            points_arr_indices_of_hull.pop()
            p_2_ind = p_1_ind
            while points_arr[p_1_ind] != points_arr[points_arr_indices_of_hull[-1]]:
                p_1_ind -= 1
    return points_arr_indices_of_hull


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


def write_points_to_file(name_of_file, points_arr, points_indices_array):
    """name_of_file - string, which represents name of file; points_arr - list of lists,
    where lists are points' coordinates in Cartesian system; points_indices_array - list of numbers,
    which are particular indices in points_arr list,
    returns nothing"""
    with open(name_of_file, "w") as f:
        for ind in points_indices_array:
            f.write(str(points_arr[ind][0]) + " " + str(points_arr[ind][1]) + "\n")


def max_i(points_arr, ind):
    """points_arr - list of lists (length of lists are equal and is greater than ind),
    returns index of list in points_arr, that has the greatest value by ind's index"""
    max_i_coord = 0
    for i in range(len(points_arr)):
        if points_arr[ind] > max_i_coord:
            max_i_coord = points_arr[ind]
    return max_i_coord


def save_only_hull(points_arr, points_indices_arr, name_of_file_to_create, width_in_pixels, heigth_in_pixels):
    """points_arr - list of lists, where lists are points' coordinates in Cartesian system;
    points_indices_array - list of numbers, which are particular indices in points_arr list,
    name_of_file_to_create - string; width_in_pixels, heigth_in_pixels - numbers"""
    x_coords = [points_arr[i][0] for i in points_indices_arr] + [points_arr[points_indices_arr[0]][0]]
    y_coords = [points_arr[i][1] for i in points_indices_arr] + [points_arr[points_indices_arr[0]][1]]
    dpi = 100
    width_in_pixels /= dpi
    heigth_in_pixels /= dpi
    plt.figure(figsize=(width_in_pixels, heigth_in_pixels), dpi=100)
    plt.plot(x_coords, y_coords, color="blue")
    plt.axis('off')
    plt.savefig(name_of_file_to_create)
    plt.show()
    plt.close()


def save_hull_and_inner(points_arr, points_indices_arr, name_of_file_to_create, width_in_pixels, heigth_in_pixels):
    """points_arr - list of lists, where lists are points' coordinates in Cartesian system;
    points_indices_array - list of numbers, which are particular indices in points_arr list,
    name_of_file_to_create - string; width_in_pixels, heigth_in_pixels - numbers"""
    hull_points_x = []
    hull_points_y = []
    inner_points_x = []
    inner_points_y = []
    for i in range(len(points_arr)):
        if i in points_indices_arr:
            hull_points_x += [points_arr[i][0]]
            hull_points_y += [points_arr[i][1]]
        else:
            inner_points_x += [points_arr[i][0]]
            inner_points_y += [points_arr[i][1]]
    hull_points_x += [points_arr[points_indices_arr[0]][0]]
    hull_points_y += [points_arr[points_indices_arr[0]][1]]
    dpi = 100
    width_in_pixels /= dpi
    heigth_in_pixels /= dpi
    plt.figure(figsize=(width_in_pixels, heigth_in_pixels), dpi=100)
    # draw the convex_hull figure
    plt.plot(hull_points_x, hull_points_y, color="black")
    plt.scatter(inner_points_x, inner_points_y, color="blue")
    plt.axis('off')
    plt.savefig(name_of_file_to_create)
    plt.show()
    plt.close()


# Driver point
file = "DS1.txt"
points = coordinates(file)
points_indices = convex_hull_graham(points)
write_points_to_file("convex_hull_points.txt", points, points_indices)
save_only_hull(points, points_indices, "convex_hull.png", 960, 540)
save_hull_and_inner(points, points_indices, "convex_hull_inner.png", 960, 540)
