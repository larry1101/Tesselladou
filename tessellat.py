import random

import svgwrite
from svgwrite.container import Defs
from svgwrite.gradients import LinearGradient
from svgwrite.shapes import Polygon

fosu = ['#F0FFFD', '#97FBE7', '#53F0C9', '#33BD9B', '#2BA473', '#41D6BF', '#39CDDD',
        '#C1FDDE', '#42FF80', '#30C965', '#26C168', '#31D9B3',
        ]
shinnsha = ['#FF0202', '#FF3C3C', '#F2655E', '#FA8B8B', '#F9B0AC', '#FCDCDA',
            '#FB0F26', '#FD3145', '#FC495B', '#FD6C7B', '#F84040', '#FF9EA6',
            '#AD0310', '#CF0312', '#B41612']
anntaku = ['#C0C0C0', '#C8CBDE', '#DBE3E2', '#D1D7CC', '#5E6377',
           '#DDDDDD', '#C9CDE0', '#CBD3D2', '#C1C7BC', '#7E8397',
           '#FFFFFF']
diamond = ['#FF0000', '#FBFB3C', '#13EC18', '#0E02FE', '#6803C2',
           '#DDDDDD', '#C9CDE0', '#CBD3D2', '#C1C7BC', '#7E8397',
           '#FFFFFF']

tiger = ['#F1DD25', '#F5E86B', '#F9EF9B', '#FDF9D2', '#F4E451',
         '#F2B026', '#F3BA43', '#F4C560', '#F7CF7D', '#FBB779',
         '#C05F05', '#C59A05', '#AE561C', '#DC6C07', '#B32B09']

sakura = ['#F86381', '#FD6A88', '#FC6382', '#FD718C', '#FD869D',
         '#FD97AB', '#FEB1C0', '#FEDEE4', '#FEDEDE', '#FEC9C9',
         '#F73E63', '#D2022C', '#CB032C', '#F85C6C', '#FCCCD1']

colors = {'fosu': fosu, 'shinnsha': shinnsha, 'anntaku': anntaku, 'diamond': diamond,'tiger':tiger,'sakura':sakura}

using_color = 'fosu'

dwg = svgwrite.Drawing('%s.svg' % using_color)

patternize = True
pattern_labels_cnt = 2
pattern_file_name = '%s.bmp'%using_color
# pattern_file_name = 'doudou.bmp'
if patternize:
    from skimage import io

    img = io.imread(pattern_file_name)

    width = img.shape[1]
    height = img.shape[0]
    step_min = 11
    step_max = 23
    triangle_leftest = 20
else:
    width = 1000
    height = 600
    step_min = 17
    step_max = 43
    triangle_leftest = 13
uni_left = True
have_gradient = False
gradient_cnt = 3
center_y_rand = True

if patternize:
    import math


    def get_rgb(rgb_str):
        return int(rgb_str[1:3], 16), int(rgb_str[3:5], 16), int(rgb_str[5:], 16)


    def hsv2rgb(hsv):
        h = float(hsv[0])
        s = float(hsv[1])
        v = float(hsv[2])
        h60 = h / 60.0

        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return r, g, b


    def rgb2hsv(rgb):
        if isinstance(rgb, tuple):
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
        else:
            raise Exception('Need rgb tuple')
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        else:
            raise Exception('rgb2hsv error')
        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return h, s, v


    def divide_colors():
        for colors_series in colors:
            v_tmp = []
            for color in colors[colors_series]:
                v_tmp.append(rgb2hsv(get_rgb(color))[2])
            v_max = max(v_tmp)
            v_min = min(v_tmp)
            v_d = (v_max - v_min) / pattern_labels_cnt
            color_series_tmp = {}
            for label in range(pattern_labels_cnt):
                color_series_tmp[label] = []
            for v_index in range(len(v_tmp)):
                try:
                    color_series_tmp[int((v_tmp[v_index] - v_min) / v_d)].append(colors[colors_series][v_index])
                except KeyError:
                    color_series_tmp[int((v_tmp[v_index] - v_min) / v_d) - 1].append(colors[colors_series][v_index])
            colors[colors_series] = color_series_tmp


    divide_colors()


def get_color(points):
    if patternize:
        x_sum = 0
        y_sum = 0
        for point in points:
            x_sum += point[0]
            y_sum += point[1]
        x_avg = int(x_sum / len(points))
        y_avg = int(y_sum / len(points))

        img_col_ref = img[y_avg][x_avg]
        hsv = rgb2hsv((img_col_ref[0], img_col_ref[1], img_col_ref[2]))
        label = int(hsv[2] / (1 / pattern_labels_cnt))
        try:
            return random.sample(colors[using_color][label], 1)[0]
        except KeyError:
            return random.sample(colors[using_color][label - 1], 1)[0]

    else:
        return random.sample(colors[using_color], 1)[0]


if have_gradient:
    defs = Defs(id='gradients')
    colors_gradient = []
    gradient_direction = [(1, 1), (0, 1), (1, 0)]
    for gradient_index in range(gradient_cnt):
        l_g = LinearGradient((0, 0), random.choice(gradient_direction), id='gradient_%d' % gradient_index)
        l_g.add_colors(random.sample(colors[using_color], 2))
        defs.add(l_g)
        colors_gradient.append('url(#gradient_%d)' % gradient_index)

    colors[using_color] += colors_gradient

    dwg.add(defs)

# start
x_p0 = []
for i in range(triangle_leftest + 1):
    x_p0.append(0)
if uni_left:
    y_p0 = []
    for i in range(triangle_leftest + 1):
        y_p0.append(int(height / triangle_leftest * i))
else:
    y_p0 = random.sample(range(1, height), triangle_leftest - 1)
    y_p0.sort()
    y_p0.insert(0, 0)
    y_p0.append(height)
p0 = list(zip(x_p0, y_p0))

while True:

    x_p0_max = max(x_p0)
    if width - x_p0_max > step_max:
        x_p2 = []
        for i in range(triangle_leftest):
            x_p2.append(random.randint(step_min, step_max))
        for i in range(len(x_p2)):
            x_p2[i] += x_p0_max
        y_p2 = []
        for i in range(1, len(y_p0)):
            if center_y_rand:
                d = y_p0[i] - y_p0[i - 1]
                y_p2.append(random.randint(y_p0[i - 1] + int(0.45 * d), y_p0[i - 1] + int(0.55 * d)))
            else:
                y_p2.append(random.randint(y_p0[i - 1], y_p0[i] - 1))
        p2 = list(zip(x_p2, y_p2))

        for i in range(len(p2)):
            dwg.add(Polygon([p0[i], p2[i], p0[i + 1]], fill=get_color([p0[i], p2[i], p0[i + 1]])))
        for i in range(len(p2) - 1):
            dwg.add(Polygon([p2[i], p0[i + 1], p2[i + 1]], fill=get_color([p2[i], p0[i + 1], p2[i + 1]])))

        x_p2_max = max(x_p2)

        if width - x_p2_max > step_max:

            x_p1 = []
            for i in range(triangle_leftest + 1):
                x_p1.append(random.randint(step_min, step_max))

            for i in range(len(x_p1)):
                x_p1[i] += x_p2_max
            y_p1 = []
            for i in range(1, len(y_p2)):
                if center_y_rand:
                    d = y_p2[i] - y_p2[i - 1]
                    y_p1.append(random.randint(y_p2[i - 1] + int(0.45 * d), y_p2[i - 1] + int(0.55 * d)))
                else:
                    y_p1.append(random.randint(y_p2[i - 1], y_p2[i] - 1))
            y_p1.insert(0, 0)
            y_p1.append(height)
            p1 = list(zip(x_p1, y_p1))

            for i in range(len(p2)):
                dwg.add(Polygon([p1[i], p2[i], p1[i + 1]], fill=get_color([p1[i], p2[i], p1[i + 1]])))
            for i in range(len(p2) - 1):
                dwg.add(Polygon([p2[i], p1[i + 1], p2[i + 1]], fill=get_color([p2[i], p1[i + 1], p2[i + 1]])))

            dwg.add(Polygon([p0[0], p1[0], p2[0]], fill=get_color([p0[0], p1[0], p2[0]])))
            dwg.add(Polygon([p0[-1], p1[-1], p2[-1]], fill=get_color([p0[-1], p1[-1], p2[-1]])))
        else:
            x_p1 = []
            for i in range(triangle_leftest + 1):
                x_p1.append(width)
            y_p1 = []
            for i in range(1, len(y_p2)):
                if center_y_rand:
                    d = y_p2[i] - y_p2[i - 1]
                    y_p1.append(random.randint(y_p2[i - 1] + int(0.45 * d), y_p2[i - 1] + int(0.55 * d)))
                else:
                    y_p1.append(random.randint(y_p2[i - 1], y_p2[i] - 1))
            y_p1.insert(0, 0)
            y_p1.append(height)
            p1 = list(zip(x_p1, y_p1))

            for i in range(len(p2)):
                dwg.add(Polygon([p1[i], p2[i], p1[i + 1]], fill=get_color([p1[i], p2[i], p1[i + 1]])))
            for i in range(len(p2) - 1):
                dwg.add(Polygon([p2[i], p1[i + 1], p2[i + 1]], fill=get_color([p2[i], p1[i + 1], p2[i + 1]])))

            dwg.add(Polygon([p0[0], p1[0], p2[0]], fill=get_color([p0[0], p1[0], p2[0]])))
            dwg.add(Polygon([p0[-1], p1[-1], p2[-1]], fill=get_color([p0[-1], p1[-1], p2[-1]])))

            break
    else:
        x_p2 = []
        for i in range(triangle_leftest):
            x_p2.append(width)
        y_p2 = []
        for i in range(1, len(y_p0)):
            if center_y_rand:
                d = y_p0[i] - y_p0[i - 1]
                y_p2.append(random.randint(y_p0[i - 1] + int(0.45 * d), y_p0[i - 1] + int(0.55 * d)))
            else:
                y_p2.append(random.randint(y_p0[i - 1], y_p0[i] - 1))

        p2 = list(zip(x_p2, y_p2))

        for i in range(len(p2)):
            dwg.add(Polygon([p0[i], p2[i], p0[i + 1]], fill=get_color([p0[i], p2[i], p0[i + 1]])))
        for i in range(len(p2) - 1):
            dwg.add(Polygon([p2[i], p0[i + 1], p2[i + 1]], fill=get_color([p2[i], p0[i + 1], p2[i + 1]])))

        dwg.add(Polygon([p0[0], (width, 0), p2[0]], fill=get_color([p0[0], (width, 0), p2[0]])))
        dwg.add(Polygon([p0[-1], (width, height), p2[-1]], fill=get_color([p0[-1], (width, height), p2[-1]])))

        break

    x_p0 = x_p1.copy()
    y_p0 = y_p1.copy()
    p0 = list(zip(x_p0, y_p0))

dwg.save()
