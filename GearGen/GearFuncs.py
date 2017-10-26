from mathutils import Vector, Euler
from math import sin, radians, cos, acos, pi, tan
from cmath import sqrt

def rotTeeth(rotDiam, Vec, rotAng):
    ang = Vec.angle(Vector((10,0.0,0.0)))
    k = 2*Vec.length/rotDiam
    m = Vector((Vec[0]/k, Vec[1]/k, Vec[2]/k))
    e = Vec-m
    if Vec[1] >= 0:
        e.rotate(Euler((0.0, 0.0, -ang), 'XYZ'))
        e.rotate(Euler((0.0, -rotAng, ang), 'XYZ'))
    else:
        e.rotate(Euler((0.0, 0.0, ang), 'XYZ'))
        e.rotate(Euler((0.0, -rotAng, -ang), 'XYZ'))
    return m + e

def create_mesh_obj(context, mesh):    
    from bpy_extras import object_utils
    return object_utils.object_data_add(context, mesh, operator=None)


def getBaseDiam(module, nTeeth, prezureAngle):
    return getRefDiam(module, nTeeth)*sin(pi/2-prezureAngle)

def getRefDiam(module, nTeeth):
    return 1.0*module*nTeeth

def getTipDiam(module, nTeeth):
    return getRefDiam(module, nTeeth)+2.0*module
    
def getRootDiam(module, nTeeth):
    return getTipDiam(module, nTeeth)-4.5*module
    

def getEvolvAngle(Diam, module, nTeeth, prezureAngle):
    u = abs(sqrt(Diam*Diam/(getBaseDiam(module, nTeeth, prezureAngle)*getBaseDiam(module, nTeeth, prezureAngle))-1))
    return u - acos(getBaseDiam(module, nTeeth, prezureAngle)/Diam)

def getVertEvolv(Diam, radAngle):
    x = (Diam/2)*(cos(radAngle) + radAngle*sin(radAngle))
    y = (Diam/2)*(sin(radAngle) - radAngle*cos(radAngle))
    return Vector((x,y))

def getCrossEvolv2(m, nTeeth, prezureAngle, shiftX, typeGear):    
    DiamRef = getRefDiam(m, nTeeth) 
    baseDiam = getBaseDiam(m, nTeeth, prezureAngle)
    if typeGear == '2':
        km = m
        DiamR = getRootDiam(m, nTeeth) + shiftX*2 + 0.5*m
    else:
        km = 1.25*m
        DiamR = getRootDiam(m, nTeeth) + 2*shiftX
    def getEvolvAngle(Diam):
        u = abs(sqrt(Diam*Diam/(baseDiam*baseDiam)-1))
        if baseDiam/Diam > 1:
            evAng = u
        else:
            evAng = u - acos(baseDiam/Diam)
        return Vector((evAng, u))
    
    def getEvolvAngle2(Diam):
        u = 0.0
        dX = km - shiftX
        evAng = getEvolvAngle(DiamRef)[0]
        dAng2 = 2*shiftX*tan(prezureAngle)/DiamRef
        if (DiamRef - 2*dX)/Diam <=1:
            a1 = acos((DiamRef - 2*dX)/Diam)
            a2 = evAng + radians(90/nTeeth)+dAng2
            u = ((Diam/2)*sin(a1) + pi*m/4 + km*tan(prezureAngle))/(DiamRef/2)            
            da = (a1 + a2) - u
        else:
            da = 10.0
        return Vector((da, u))
    if baseDiam <= DiamR:
        xD = DiamR
    else:
        xD = baseDiam
    dD = (DiamRef - xD)/2
    diamArr = Vector((xD, xD + dD, DiamRef))
    n = 0
    while abs(getEvolvAngle(diamArr[1])[0] - getEvolvAngle2(diamArr[1])[0]) > m/1000000:
        dD = dD/2
        if abs(getEvolvAngle(diamArr[0])[0] - getEvolvAngle2(diamArr[0])[0]) <= abs(getEvolvAngle(diamArr[1])[0] - getEvolvAngle2(diamArr[1])[0]):
            i = 0
            
        else:
            i = 1
        if abs(getEvolvAngle(diamArr[i])[0] - getEvolvAngle2(diamArr[i])[0]) > abs(getEvolvAngle(diamArr[2])[0] - getEvolvAngle2(diamArr[2])[0]):
            i = 2
        diamArr[1] = diamArr[i]        
        if diamArr[1] - dD < xD:
            diamArr[0] = xD
            diamArr[1] = xD + dD
        else:
            diamArr[0] = diamArr[1] - dD
        diamArr[2] = diamArr[1] + dD
        n = n + 1
        if i == 0 and n > 10:
            break
    return Vector((getEvolvAngle(diamArr[i])[1], getEvolvAngle2(diamArr[i])[1]))

def getOriginZ(m, nTeeth, typeGear, shiftX, angCon):
    if typeGear == '3':
        radRef = getRefDiam(m, nTeeth)/2 + shiftX
        zOrig = radRef/tan(angCon)
    else:
        zOrig = 0.0
    return zOrig
