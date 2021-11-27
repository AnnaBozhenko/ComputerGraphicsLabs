from matplotlib import pyplot as plt
import re


# alternative way to regex to get int numbers from the given string
def dot_coords(str_with_coords):
    """function to extract int numbers from the given 'str_with_coords' string,
    it's supposed that string contains only two numbers separated by ' '
    and the last character can be either '\n' or nothing at all.
    function returns list with two int numbers"""
    coords = []
    numb = ''
    for i in range(len(str_with_coords)):
        if '0' <= str_with_coords[i] <= '9':
            numb += str_with_coords[i]
            if i + 1 == len(str_with_coords):
                coords += [int(numb)]
        elif (str_with_coords[i] == ' ' or str_with_coords[i] == '\n') and numb != '':
            coords += [int(numb)]
            numb = ''
        else:
            numb = ''
    if coords:
        return coords
    else:
        return None


def coordinates(file_name):
    """get dots' coordinates from given file
    returns list of x- and y- values"""
    x_arr = []
    y_arr = []
    regexp = "\d+"
    with open(file_name) as f:
        for line in f:
            # temp = dot_coords(line)
            # x_arr += [temp[0]]
            # x_arr += [temp[1]]
            temp = re.findall(regexp, line)
            x_arr += [int(temp[0])]
            y_arr += [int(temp[1])]
    return [x_arr, y_arr]


def draw_save_image(file_name):
    """draw and save a picture from the given dataset of dots'
    coordinates placed int the file"""
    x_arr, y_arr = coordinates(file_name)
    fig, ax = plt.subplots(figsize=(9.6, 5.4))
    ax.scatter(x_arr, y_arr, color='black')
    ax.axis('off')
    plt.savefig('image.png')


# starting point
f_name = 'DS1.txt'
draw_save_image(f_name)
