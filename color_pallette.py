gamma_table = (0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
               0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
               1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
               2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
               5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
              10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
              17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
              25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
              37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
              51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
              69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
              90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
             115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
             144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
             177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
             215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255)
trunc_gamma_table = (0, 0, 0, 0, 1, 1, 2, 4, 5, 7, 10, 13, 17, 21, 25, 31, 37, 44, 51, 60, 69, 79, 90, 102, 115, 129, 144, 160, 177, 196, 215, 236)

def create_pallette(first_color, second_color, steps, gamma=True):
    pallette = []  # final array of tuples
    slices = []    # tuple of change over steps
    pallette_slice = [] # holding list for each step of the pallette
    t_diff = []
    if len(first_color) == len(second_color) == 3 or 4:
        for each in range(len(first_color)):
            t_diff.append(second_color[each] - first_color[each])
    elif len(first_color) == len(second_color):
        raise ValueError("create_pallette expected tuples of length 3 or 4, got {}".format(len(first_color)))
    else:
        raise ValueError("create_pallette expected tuples both of length 3 or 4, got {} and {}.".format(
                                                                    len(first_color), len(second_color)))

    for each in range(len(t_diff)):
        slices.append(t_diff[each] / steps)

    for each_step in range(steps):
        for each_color in range(0, len(slices)):
            pallette_slice.append(int(first_color[each_color] + (slices[each_color] * each_step)))
        if gamma: pallette.append(gamma_correct(pallette_slice))
        else: pallette.append(pallette_slice)
        pallette_slice = []
    return pallette

def gamma_correct(color):
    output_color = []
    for each in range(0, len(color)):
        output_color.append(gamma_table[color[each]])
    return tuple(output_color)