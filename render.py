import math
import msvcrt
import os

class grid:
    def __init__(self, h:int, w:int, c:str="   "):
        self.h = h
        self.w = w
        self.c = c
        self.content = [[c for _ in range(w)] for _ in range(h)]

    def clear(self):
        self.content = [[self.c for _ in range(self.w)] for _ in range(self.h)]

    def fill(self, c:str=" # "):
        self.content = [[c for _ in range(self.w)] for _ in range(self.h)]

    def set(self, y:int, x:int, c:str=" # "):
        if y < self.h and x < self.w and y >= 0 and x >= 0:
            self.content[y][x] = c

    def get(self, y:int, x:int):
        return self.content[y][x]
        

class matrix_3x3:
    def __init__(self, a:float, b:float, c:float, d:float, e:float, f:float, g:float, h:float, i:float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.i = i

    def multiply(self, other: "matrix_3x3") -> "matrix_3x3":
        result = matrix_3x3(0, 0, 0, 0, 0, 0, 0, 0, 0)
        result.a = self.a*other.a + self.b*other.d + self.c*other.g
        result.b = self.a*other.b + self.b*other.e + self.c*other.h
        result.c = self.a*other.c + self.b*other.f + self.c*other.i
        result.d = self.d*other.a + self.e*other.d + self.f*other.g
        result.e = self.d*other.b + self.e*other.e + self.f*other.h
        result.f = self.d*other.c + self.e*other.f + self.f*other.i
        result.g = self.g*other.a + self.g*other.d + self.g*other.g
        result.h = self.g*other.b + self.g*other.e + self.g*other.h
        result.i = self.g*other.c + self.g*other.f + self.g*other.i
        return result
    
    def multiply_vec(self, other: "vector_3") -> "vector_3":
        result = vector_3(0, 0, 0)
        result.x = self.a*other.x + self.b*other.y + self.c*other.z
        result.y = self.d*other.x + self.e*other.y + self.f*other.z
        result.z = self.g*other.x + self.h*other.y + self.i*other.z
        return result


class vector_3:
    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def add(self, other:"vector_3") -> "vector_3":
        result = vector_3(0, 0, 0)
        result.x = self.x + other.x
        result.y = self.y + other.y
        result.z = self.z + other.z
        return result
    
    def subtract(self, other:"vector_3") -> "vector_3":
        result = vector_3(0, 0, 0)
        result.x = self.x - other.x
        result.y = self.y - other.y
        result.z = self.z - other.z
        return result
    
    def rotate_x(self, angle:float) -> "vector_3":
        rotator = matrix_3x3(1, 0, 0, 
                             0, math.cos(angle), math.sin(angle),
                             0, -math.sin(angle), math.cos(angle))
        result = vector_3(0, 0, 0)
        result = rotator.multiply_vec(self)
        return result
    
    def rotate_y(self, angle:float) -> "vector_3":
        rotator = matrix_3x3(math.cos(angle), 0, -math.sin(angle), 
                             0, 1, 0,
                             math.sin(angle), 0, math.cos(angle))
        result = vector_3(0, 0, 0)
        result = rotator.multiply_vec(self)
        return result
    
    def rotate_z(self, angle:float) -> "vector_3":
        rotator = matrix_3x3(math.cos(angle), math.sin(angle), 0, 
                             -math.sin(angle), math.cos(angle), 0,
                             0, 0, 1)
        result = vector_3(0, 0, 0)
        result = rotator.multiply_vec(self)
        return result

    def rotate(self, angles:"vector_3") -> "vector_3":
        result = vector_3(0, 0, 0)
        result = vector_3.rotate_x(self, angles.x)
        result = vector_3.rotate_x(result, angles.y)
        result = vector_3.rotate_x(result, angles.z)
        return result


class vector_4:
    def __init__(self, x:float, y:float, z:float, w:float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def add(self, other:"vector_4") -> "vector_4":
        result = vector_4(0, 0, 0, 0)
        result.x = self.x + other.x
        result.y = self.y + other.y
        result.z = self.z + other.z
        result.w = self.w + other.w
        return result
    
    def subtract(self, other:"vector_4") -> "vector_4":
        result = vector_4(0, 0, 0, 0)
        result.x = self.x - other.x
        result.y = self.y - other.y
        result.z = self.z - other.z
        result.w = self.w - other.w
        return result
    
    def rotate_x(self, angle:float) -> "vector_4":
        result = vector_4(0, 0, 0, 0)
        temp = result
        temp.w = 1
        rotator = matrix_4x4(1, 0, 0, 0, 
                             0, math.cos(angle), -math.sin(angle), 0,
                             0, math.sin(angle), math.cos(angle), 0,
                             0, 0, 0, 1)
        result = matrix_4x4.multiply_vec(rotator, temp)
        result.w = 1
        return result
    
    def rotate_y(self, angle:float) -> "vector_4":
        rotator = matrix_4x4(math.cos(angle), 0, -math.sin(angle), 0, 
                             0, 1, 0, 0,
                             math.sin(angle), 0, math.cos(angle), 0,
                             0, 0, 0, 1)
        result = vector_4(0, 0, 0, 0)
        result = matrix_4x4.multiply_vec(rotator, self)
        return result
    
    def rotate_z(self, angle:float) -> "vector_4":
        rotator = matrix_4x4(math.cos(angle), math.sin(angle), 0, 0, 
                             -math.sin(angle), math.cos(angle), 0, 0,
                             0, 0, 1, 0,
                             0, 0, 0, 1)
        result = vector_4(0, 0, 0, 0)
        result = matrix_4x4.multiply_vec(rotator, self)
        return result

    def rotate(self, angles:"vector_4") -> "vector_4":
        """
        intrinsic rotation, z'- y''- x''',
        where x=roll, y=pitch, z=yaw
        """
        result = vector_4(0, 0, 0, 0)
        roll = angles.x
        pitch = angles.y
        yaw = angles.z
        result = vector_4.rotate_z(self, yaw)
        result = vector_4.rotate_y(result, pitch)
        result = vector_4.rotate_x(result, roll)
        return result

    def translate(self, translation:"vector_4") -> "vector_4":
        result = vector_4(0, 0, 0, 0)
        result = vector_4.add(self, translation)
        return result
    
    def scale(self, scaling:"vector_4") -> "vector_4":
        result = vector_4(0, 0, 0, 0)
        result.x = scaling*self.x
        result.y = scaling*self.y
        result.z = scaling*self.z
        return result
    
    def shear(self, translation:"vector_4") -> "vector_4":
        """
        scalar shear transformation,
        where x = x shear in y, y = x shear in z, z = y shear in z
        """
        result = vector_4(0, 0, 0, 0)
        shear_matrix =  matrix_4x4(1, translation.x, translation.y, 0,
                                   0, 1, translation.z, 0,
                                   0, 0, 1, 0,
                                   0, 0, 0, 1)
        result = matrix_4x4.multiply_vec(shear_matrix, self)
        return result

    def project(self, width:int, height:int, fov:float, near:float, far:float) -> "vector_4":
        aspect_ratio = width/height
        right = math.tan(fov/2)*near
        left = -right
        top = right*aspect_ratio
        bottom = -top
        result = vector_4(0, 0, 0, 0)
        projection_matrix = matrix_4x4(2*near/(right-left), 0, (right+left)/(right-left), 0,
                                       0, 2*near/(top-bottom), (top+bottom)/(top-bottom), 0,
                                       0, 0, -(far+near)/(far-near), -2*far*near/(far-near),
                                       0, 0, -1, 0)
        result = matrix_4x4.multiply_vec(projection_matrix, self)
        result.w = 1
        result.z = self.z
        return result
    
    def normalize(self) -> "vertex":
        return vertex(self.y/self.z, self.x/self.z)


class matrix_4x4:
    def __init__(self, a0:float, a1:float, a2:float, a3:float, b0:float, b1:float, b2:float, b3:float, c0:float, c1:float, c2:float, c3:float, d0:float, d1:float, d2:float, d3:float):
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.d0 = d0
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3

    def multiply(self, other:"matrix_4x4") -> "matrix_4x4":
        result = matrix_4x4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.a0 * other.a0 + self.b0 * other.a1 + self.c0 * other.a2 + self.d0 * other.a3
        self.a0 * other.b0 + self.b0 * other.b1 + self.c0 * other.b2 + self.d0 * other.b3
        self.a0 * other.c0 + self.b0 * other.c1 + self.c0 * other.c2 + self.d0 * other.c3
        self.a0 * other.d0 + self.b0 * other.d1 + self.c0 * other.d2 + self.d0 * other.d3
        self.a1 * other.a0 + self.b1 * other.a1 + self.c1 * other.a2 + self.d1 * other.a3
        self.a1 * other.b0 + self.b1 * other.b1 + self.c1 * other.b2 + self.d1 * other.b3
        self.a1 * other.c0 + self.b1 * other.c1 + self.c1 * other.c2 + self.d1 * other.c3
        self.a1 * other.d0 + self.b1 * other.d1 + self.c1 * other.d2 + self.d1 * other.d3
        self.a2 * other.a0 + self.b2 * other.a1 + self.c2 * other.a2 + self.d2 * other.a3
        self.a2 * other.b0 + self.b2 * other.b1 + self.c2 * other.b2 + self.d2 * other.b3
        self.a2 * other.c0 + self.b2 * other.c1 + self.c2 * other.c2 + self.d2 * other.c3
        self.a2 * other.d0 + self.b2 * other.d1 + self.c2 * other.d2 + self.d2 * other.d3
        self.a3 * other.a0 + self.b3 * other.a1 + self.c3 * other.a2 + self.d3 * other.a3
        self.a3 * other.b0 + self.b3 * other.b1 + self.c3 * other.b2 + self.d3 * other.b3
        self.a3 * other.c0 + self.b3 * other.c1 + self.c3 * other.c2 + self.d2 * other.c3
        self.a3 * other.d0 + self.b3 * other.d1 + self.c3 * other.d2 + self.d3 * other.d3
        return result

    def multiply_vec(self, other:"vector_4") -> "vector_4":
        result = vector_4(0, 0, 0, 0)
        result.x = self.a0*other.x + self.a1*other.x + self.a2*other.x + self.a3*other.x
        result.y = self.b0*other.y + self.b1*other.y + self.b2*other.y + self.b3*other.y
        result.z = self.c0*other.z + self.c1*other.z + self.c2*other.z + self.c3*other.z
        result.w = self.d0*other.w + self.d1*other.w + self.d2*other.w + self.d3*other.w
        return result


class vertex:
    def __init__(self, y:int, x:int):
        self.y = y
        self.x = x

    def draw(self, grid:grid, c:str=" # "):
        grid.set(self.y, self.x, c)

    def ndc_to_screen(self, width:int, height:int) -> "vertex":
        result = vertex(0, 0)
        result.x = round((self.x + 1) * 0.5 * width)
        result.y = round((1 - (self.y + 1) * 0.5) * height)
        return result


class line2d:
    def __init__(self, y0:int, x0:int, y1:int, x1:int):
        self.y0 = y0
        self.y1 = y1
        self.x0 = x0
        self.x1 = x1

    def drawhigh(self, grid:grid, y0:int, x0:int, y1:int, x1:int, c: str = " # "):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        D = (2 * dx) - dy
        x = x0
        if y0 < y1:
            y_step = 1
        else:
            y_step = -1

        for y in range(y0, y1 + y_step, y_step):
            grid.set(y, x, c)
            if D > 0:
                x = x + xi
                D = D + (2 * (dx - dy))
            else:
                D = D + 2 * dx

    def drawlow(self, grid:grid, y0:int, x0:int, y1:int, x1:int, c: str = " # "):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy
        D = (2 * dy) - dx
        y = y0
        if x0 < x1:
            x_step = 1
        else:
            x_step = -1

        for x in range(x0, x1 + x_step, x_step):
            grid.set(y, x, c)
            if D > 0:
                y = y + yi
                D = D + (2 * (dy - dx))
            else:
                D = D + 2 * dy

    def draw(self, grid, c: str = " # "):
        if abs(self.y1 - self.y0) < abs(self.x1 - self.x0):
            if self.x0 > self.x1:
                self.drawlow(grid, self.y1, self.x1, self.y0, self.x0, c)
            else:
                self.drawlow(grid, self.y0, self.x0, self.y1, self.x1, c)
        else:
            if self.y0 > self.y1:
                self.drawhigh(grid, self.y1, self.x1, self.y0, self.x0, c)
            else:
                self.drawhigh(grid, self.y0, self.x0, self.y1, self.x1, c)


class triangle2d:
    def __init__(self, y0:int, x0:int, y1:int, x1:int, y2:int, x2:int):
        self.y0 = y0
        self.y1 = y1
        self.x0 = x0
        self.x1 = x1
        self.y2 = y2
        self.x2 = x2


def deg_to_rad(a:float) -> float:
    result = math.pi*a/180
    return result


def render(grid:grid):
    for i in range(grid.h):
        for j in range(grid.w):
            print(grid.get(i, j), end="")
        print("")

main = grid(30, 30, " . ")
"""
main.set(9, 13)

l = line2d(17, 17, 8, 3)
l.draw(main)
"""


def get_input() -> str:
    while True:
        if msvcrt.kbhit(): #key is pressed
            key = msvcrt.getwch() #decode
            return key


points = []
points.append(vector_4(-1, -1, -1, 1))
points.append(vector_4(-1, -1, 1, 1))
points.append(vector_4(-1, 1, -1, 1))
points.append(vector_4(-1, 1, 1, 1))
points.append(vector_4(1, -1, -1, 1))
points.append(vector_4(1, -1, 1, 1))
points.append(vector_4(1, 1, -1, 1))
points.append(vector_4(1, 1, 1, 1))

while True:
    os.system("cls")
    for p in points:
        temp = p.project(30, 30, math.pi/2, 1, 20)
        point = temp.normalize()
        point = point.ndc_to_screen(30, 30)
        print(f"{point.x}; {point.y} | {p.x}; {p.y}; {p.z}")
        point.draw(main)

    render(main)
    main.clear()
    key = get_input()
    if key == "w":
        for p in points:
            p.z -= 0.1
    elif key == "s":
        for p in points:
            p.z += 0.1
    elif key == "a":
        for p in points:
            p.x -= 0.1
    elif key == "d":
        for p in points:
            p.x += 0.1
    elif key == "q":
        for p in points:
            p.y -= 0.1
    elif key == "e":
        for p in points:
            p.y += 0.1
    elif key == "o":
        angle = deg_to_rad(1)
        for i, p in enumerate(points):
            points[i] = p.rotate_x(angle)
    elif key == "p":
        for i, p in enumerate(points):
            points[i] = p.rotate_x(angle)
