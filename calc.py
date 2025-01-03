from math import degrees, atan, cos, sin, radians

def find_degree(a, b, old_result=0):
    result = old_result
    if not a == 0 and not b == 0:
        result = degrees(atan(b / a))
        if a >= 0: result += 180
    return result

def find_a(degree, c):
    return cos(radians(degree)) * c

def find_b(degree, c):
    return sin(radians(degree)) * c

def find_c(a, b):
    return (a ** 2 + b ** 2) ** .5