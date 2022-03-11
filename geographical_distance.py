import math

xi = 16.47
yi = 96.10
xj = 19.41
yj = 97.13

pi = 3.141592

deg = int(xi)
min = xi - deg
latitude_i = pi * (deg + (5.0 * min / 3.0)) / 180.0

deg = int(yi)
min = yi - deg
longtitude_i = pi * (deg + (5.0 * min / 3.0)) / 180.0

deg = int(xj)
min = xj - deg
latitude_j = pi * (deg + (5.0 * min / 3.0)) / 180.0

deg = int(yj)
min = yj - deg
longtitude_j = pi * (deg + (5.0 * min / 3.0)) / 180.0

q1 = math.cos(longtitude_i - longtitude_j)
q2 = math.cos(latitude_i - latitude_j)
q3 = math.cos(latitude_i + latitude_j)

r = 6378.388

print(0.5 * ((1 + q1) * q2 - (1 - q1) * q3) + 1)

dij = int(r * math.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0)

print(dij)