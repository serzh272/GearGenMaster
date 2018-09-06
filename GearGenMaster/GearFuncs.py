from mathutils import Vector, Euler
from math import sin, radians, cos, acos, pi, tan
from cmath import sqrt


# Функция поворота точки с координатами Vec вокруг окружности диаметра rotDiam на угол rotAng
def rotTeeth(rotDiam, vec, rotAng):
    ang = vec.angle(Vector((10, 0.0, 0.0)))
    k = 2 * vec.length / rotDiam
    m = Vector((vec[0] / k, vec[1] / k, vec[2] / k))
    e = vec - m
    if vec[1] >= 0:
        e.rotate(Euler((0.0, 0.0, -ang), 'XYZ'))
        e.rotate(Euler((0.0, -rotAng, ang), 'XYZ'))
    else:
        e.rotate(Euler((0.0, 0.0, ang), 'XYZ'))
        e.rotate(Euler((0.0, -rotAng, -ang), 'XYZ'))
    return m + e


# Функция создания объекта на основе mesh
def create_mesh_obj(context, mesh):
    from bpy_extras import object_utils
    return object_utils.object_data_add(context, mesh, operator=None)

# Функция для расчета диаметра базовой окружности
def getBaseDiam(module, nTeeth, pressureAngle):
    return getRefDiam(module, nTeeth) * sin(pi / 2 - pressureAngle)

# Функция для расчета диаметра делительной окружности
def getRefDiam(module, nTeeth):
    return 1.0 * module * nTeeth

# Функция для расчета диаметра окружности вершин зубьев
def getTipDiam(module, nTeeth):
    return getRefDiam(module, nTeeth) + 2.0 * module

# Функция для расчета диаметра окружности впадин зубьев
def getRootDiam(module, nTeeth, c = 0.25):
    return getTipDiam(module, nTeeth) - (4.0+2*c) * module

# Функция для расчета эвольвентного угла в зависимости от диаметра Diam
def getEvolvAngle(Diam, module, nTeeth, pressureAngle):
    u = abs(sqrt(Diam * Diam / (
                    getBaseDiam(module, nTeeth, pressureAngle) * getBaseDiam(module, nTeeth, pressureAngle)) - 1))
    return u - acos(getBaseDiam(module, nTeeth, pressureAngle) / Diam)

# Функция для расчета точек эвольвенты на базе окружности диаметром Diam
def getVertEvolv(Diam, radAngle):
    x = (Diam / 2) * (cos(radAngle) + radAngle * sin(radAngle))
    y = (Diam / 2) * (sin(radAngle) - radAngle * cos(radAngle))
    return Vector((x, y))

# Функция для расчета пересечения удлиненной эвольвенты впадины зуба и эвольвенты зуба
def getCrossEvolv(m, nTeeth, prezureAngle, shiftX, typeGear):
    DiamRef = getRefDiam(m, nTeeth)
    baseDiam = getBaseDiam(m, nTeeth, prezureAngle)
    if typeGear == 'internal':
        km = m
        DiamR = getRootDiam(m, nTeeth) + shiftX * 2 + 0.5 * m
    else:
        km = 1.25 * m
        DiamR = getRootDiam(m, nTeeth) + 2 * shiftX

    def getEvolvAngle(Diam):
        u = abs(sqrt(Diam * Diam / (baseDiam * baseDiam) - 1))
        if baseDiam / Diam > 1:
            evAng = u
        else:
            evAng = u - acos(baseDiam / Diam)
        return Vector((evAng, u))

    def getEvolvAngle2(Diam):
        u = 0.0
        dX = km - shiftX
        evAng = getEvolvAngle(DiamRef)[0]
        dAng2 = 2 * shiftX * tan(prezureAngle) / DiamRef
        if (DiamRef - 2 * dX) / Diam <= 1:
            a1 = acos((DiamRef - 2 * dX) / Diam)
            a2 = evAng + radians(90 / nTeeth) + dAng2
            u = ((Diam / 2) * sin(a1) + pi * m / 4 + km * tan(prezureAngle)) / (DiamRef / 2)
            da = (a1 + a2) - u
        else:
            da = 10.0
        return Vector((da, u))

    if baseDiam <= DiamR:
        xD = DiamR
    else:
        xD = baseDiam
    dD = (DiamRef - xD) / 2
    diamArr = Vector((xD, xD + dD, DiamRef))
    n = 0
    while abs(getEvolvAngle(diamArr[1])[0] - getEvolvAngle2(diamArr[1])[0]) > m / 1000 or dD > m / 1000:
        dD = dD / 2
        if abs(getEvolvAngle(diamArr[0])[0] - getEvolvAngle2(diamArr[0])[0]) <= abs(
                getEvolvAngle(diamArr[1])[0] - getEvolvAngle2(diamArr[1])[0]):
            i = 0
        else:
            i = 1
        if abs(getEvolvAngle(diamArr[i])[0] - getEvolvAngle2(diamArr[i])[0]) > abs(
                getEvolvAngle(diamArr[2])[0] - getEvolvAngle2(diamArr[2])[0]):
            i = 2
        diamArr[1] = diamArr[i]
        if diamArr[1] - dD < xD:
            diamArr[0] = xD
            diamArr[1] = xD + dD
        else:
            diamArr[0] = diamArr[1] - dD
        diamArr[2] = diamArr[1] + dD
        n = n + 1
        if i == 0 and n > 15:
            break
    return Vector((getEvolvAngle(diamArr[i])[1], getEvolvAngle2(diamArr[i])[1]))

# Функция для расчета точки начала координат
def getOriginZ(m, nTeeth, typeGear, shiftX, angCon):
    if typeGear == 'bevel':
        radRef = getRefDiam(m, nTeeth) / 2 + shiftX
        zOrig = radRef / tan(angCon)
    else:
        zOrig = 0.0
    return zOrig
