import svg

def print_something():
    canvas = svg.SVG(
        width=600,
        height=600,
        elements=[
            # print_rect_hatch(40, 400, 400),
            print_rect_hatch_param(40, 500, 500, 4),
            print_rect_hatch_param(20, 400, 400, 2),
            print_curve(200, 200, 80),
            svg.Circle(
                cx=30, cy=30, r=20,
                stroke="red",
                fill="white",
                stroke_width=1,
            ),
        ],
    )
    print(canvas)

def print_rect(length, pos_x, pos_y):
    return  svg.Rect(x=pos_x, y=pos_y, width=length, height=length, stroke="blue", stroke_width=1)

def print_rect_hatch(size, pos_x, pos_y):
    # decide how much line we want in the square - should be an argument
    # divide length by some number to decide on how much lines we want
    # best to select size that is divisible by 4 witouht remaider
    step_size = size//4
    step_1 = step_size
    step_2 = step_size*2
    step_3 = step_size*3
    step_4 = step_size*4
    return  svg.Polyline(
        fill="none",
        stroke="black",
        stroke_width=1,
        points=[
            pos_x+step_1, pos_y,
            pos_x, pos_y+step_1,
            pos_x, pos_y+step_2,
            pos_x+step_2, pos_y,
            pos_x+step_3, pos_y,
            pos_x, pos_y+step_3,
            pos_x, pos_y+step_4,
            pos_x+step_4, pos_y,
            pos_x+step_4, pos_y+step_1,
            pos_x+step_1, pos_y+step_4,
            pos_x+step_2, pos_y+step_4,
            pos_x+step_4, pos_y+step_2,
            pos_x+step_4, pos_y+step_3,
            pos_x+step_3, pos_y+step_4
            ]
        )

# density means into how many parts should the square be divided
def print_rect_hatch_param(size, pos_x, pos_y, density):
    # we can imagine the hatch as a division of two lengths of the rectangle sides
    # into specific number of parts and the lines are the division lines
    # example: size 8 square with density 2 means that line will be every two steps
    # and there will be 8 parts in total which means 7 lines
    step_size = size//density
    number_of_lines = (size * 2 // step_size)
    multiline_points = []
    # generate the steps
    for x in range(number_of_lines+1):
        point_x_0 = min(pos_x+(step_size*x), size + pos_x)
        point_y_0 = max(pos_y+(step_size*x) - size, pos_y)
        point_x_1 = max(pos_x+(step_size*x) - size, pos_x)
        point_y_1 = min(pos_y+(step_size*x), size + pos_y)
        if(x % 2 == 1):
            multiline_points.append(point_x_0) # x
            multiline_points.append(point_y_0) # y
            multiline_points.append(point_x_1) # x
            multiline_points.append(point_y_1) # y
        else:
            multiline_points.append(point_x_1) # x
            multiline_points.append(point_y_1) # y
            multiline_points.append(point_x_0) # x
            multiline_points.append(point_y_0) # y

    return  svg.Polyline(
            fill="none",
            stroke="black",
            stroke_width=1,
            points=multiline_points
            )



def print_curve(start_x, start_y, size):
    return svg.Polyline(
            fill="none",
            stroke="black",
            stroke_width=1,
            points=hilbert_curve(start_x, start_y, size)
            )

# hilbert curve grammar
# up -> right ^ up > up v left
# right -> up > right ^ right < down
# left -> down < left v left > up
# down -> left v down < down ^ right

# sizing
# lets make it so that the basic curve is 1/4 size of the edge
# 2/4 size long and connective parts are 2/4 long
def hilbert_curve(start_x, start_y, size):
    size_part = size//4

    points = []
    points.append(draw_right(start_x+size_part, start_y+3*size_part, size_part))
    points.append(draw_up(start_x+size_part, start_y+size_part, size_part))
    points.append(draw_up(start_x+3*size_part, start_y+size_part, size_part))
    points.append(draw_left(start_x+3*size_part, start_y+3*size_part, size_part))
    return points


# assume start is top left corner
def draw_up(start_x, start_y, size):
    points = []
    points.append(start_x)
    points.append(start_y+size)
    points.append(start_x)
    points.append(start_y)
    points.append(start_x+size)
    points.append(start_y)
    points.append(start_x+size)
    points.append(start_y+size)
    return points

# assume start is top left corner
def draw_right(start_x, start_y, size):
    points = []
    points.append(start_x)
    points.append(start_y+size)
    points.append(start_x+size)
    points.append(start_y+size)
    points.append(start_x+size)
    points.append(start_y)
    points.append(start_x)
    points.append(start_y)
    return points

# assume start is top left corner
def draw_left(start_x, start_y, size):
    points = []
    points.append(start_x+size)
    points.append(start_y)
    points.append(start_x)
    points.append(start_y)
    points.append(start_x)
    points.append(start_y+size)
    points.append(start_x+size)
    points.append(start_y+size)
    return points

# assume start is top left corner
def draw_down(start_x, start_y, size):
    points = []
    points.append(start_x+size)
    points.append(start_y)
    points.append(start_x+size)
    points.append(start_y+size)
    points.append(start_x)
    points.append(start_y+size)
    points.append(start_x)
    points.append(start_y)
    return points