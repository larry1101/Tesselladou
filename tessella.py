import random
import svgwrite
from svgwrite.container import Defs
from svgwrite.gradients import LinearGradient
from svgwrite.shapes import Polygon

fasi = ['#34F3CD', '#34F3DD', '#5BF993', '#10D5C2', '#09DF69', '#11D06C', '#1CB79F',
        '#34F3C2', '#34F3D5', '#5BFE83', '#20D5C2', '#0FDF69', '#13E07C', '#1FBFAB',
        '#F0FFFC', '#14CD59']
shinsha = ['#FE8585', '#FA5A66', '#ED2C2D', '#AD1D1D', '#F83030', '#FF8E9C',
           '#FE8575', '#FA5A66', '#ED3C2D', '#AD1F14', '#F84040', '#FF9EA6',
           '#FEF5F8']
antaku = ['#C0C0C0', '#C8CBDE', '#DBE3E2', '#D1D7CC', '#5E6377',
          '#DDDDDD', '#C9CDE0', '#CBD3D2', '#C1C7BC', '#7E8397',
          '#FFFFFF']
diamond = ['#FF0000', '#FBFB3C', '#13EC18', '#0E02FE','#6803C2',
          '#DDDDDD', '#C9CDE0', '#CBD3D2', '#C1C7BC', '#7E8397',
          '#FFFFFF']

colors = {'fasi': fasi, 'shinsha': shinsha, 'antaku': antaku, 'diamond': diamond}

using_color = 'diamond'

dwg = svgwrite.Drawing('%s.svg' % using_color)

width = 1000
height = 600
step_min = 17
step_max = 43
triangle_leftest = 13
uni_left = True
have_gradient = True
gradient_cnt = 3


def get_color():
    return random.sample(colors[using_color], 1)[0]


if have_gradient:
    defs = Defs(id='gradients')
    colors_gradient=[]
    gradient_direction=[(1,1),(0,1),(1,0)]
    for gradient_index in range(gradient_cnt):
        l_g = LinearGradient((0, 0), random.choice(gradient_direction),id='gradient_%d'%gradient_index)
        l_g.add_colors(random.sample(colors[using_color], 2))
        defs.add(l_g)
        colors_gradient.append('url(#gradient_%d)'%gradient_index)

    colors[using_color]+=colors_gradient

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
            y_p2.append(random.randint(y_p0[i - 1], y_p0[i] - 1))
        p2 = list(zip(x_p2, y_p2))

        for i in range(len(p2)):
            dwg.add(Polygon([p0[i], p2[i], p0[i + 1]], fill=get_color()))
        for i in range(len(p2) - 1):
            dwg.add(Polygon([p2[i], p0[i + 1], p2[i + 1]], fill=get_color()))

        x_p2_max = max(x_p2)

        if width - x_p2_max > step_max:

            x_p1 = []
            for i in range(triangle_leftest + 1):
                x_p1.append(random.randint(step_min, step_max))

            for i in range(len(x_p1)):
                x_p1[i] += x_p2_max
            y_p1 = []
            for i in range(1, len(y_p2)):
                y_p1.append(random.randint(y_p2[i - 1], y_p2[i] - 1))
            y_p1.insert(0, 0)
            y_p1.append(height)
            p1 = list(zip(x_p1, y_p1))

            for i in range(len(p2)):
                dwg.add(Polygon([p1[i], p2[i], p1[i + 1]], fill=get_color()))
            for i in range(len(p2) - 1):
                dwg.add(Polygon([p2[i], p1[i + 1], p2[i + 1]], fill=get_color()))

            dwg.add(Polygon([p0[0], p1[0], p2[0]], fill=get_color()))
            dwg.add(Polygon([p0[-1], p1[-1], p2[-1]], fill=get_color()))
        else:
            x_p1 = []
            for i in range(triangle_leftest + 1):
                x_p1.append(width)
            y_p1 = []
            for i in range(1, len(y_p2)):
                y_p1.append(random.randint(y_p2[i - 1], y_p2[i] - 1))
            y_p1.insert(0, 0)
            y_p1.append(height)
            p1 = list(zip(x_p1, y_p1))

            for i in range(len(p2)):
                dwg.add(Polygon([p1[i], p2[i], p1[i + 1]], fill=get_color()))
            for i in range(len(p2) - 1):
                dwg.add(Polygon([p2[i], p1[i + 1], p2[i + 1]], fill=get_color()))

            dwg.add(Polygon([p0[0], p1[0], p2[0]], fill=get_color()))
            dwg.add(Polygon([p0[-1], p1[-1], p2[-1]], fill=get_color()))

            break
    else:
        x_p2 = []
        for i in range(triangle_leftest):
            x_p2.append(width)
        y_p2 = []
        for i in range(1, len(y_p0)):
            y_p2.append(random.randint(y_p0[i - 1], y_p0[i] - 1))

        p2 = list(zip(x_p2, y_p2))

        for i in range(len(p2)):
            dwg.add(Polygon([p0[i], p2[i], p0[i + 1]], fill=get_color()))
        for i in range(len(p2) - 1):
            dwg.add(Polygon([p2[i], p0[i + 1], p2[i + 1]], fill=get_color()))

        dwg.add(Polygon([p0[0], (width, 0), p2[0]], fill=get_color()))
        dwg.add(Polygon([p0[-1], (width, height), p2[-1]], fill=get_color()))

        break

    x_p0 = x_p1.copy()
    y_p0 = y_p1.copy()
    p0 = list(zip(x_p0, y_p0))

dwg.save()
