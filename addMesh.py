import bpy
import os
from builtins import range
from . import GearFuncs
from . import gvars
from mathutils import Vector, Euler
from math import sin, cos, pi, atan, tan
from cmath import sqrt


def sqr(num):
    return num * num


def get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, val, side, c=0.25, tw=0.0):
    DiamRef = GearFuncs.getRefDiam(m, nTeeth)
    baseDiam = GearFuncs.getBaseDiam(m, nTeeth, pressureAngle)
    DiamT = GearFuncs.getTipDiam(m, nTeeth) + shiftX * 2
    if typeGear == 'ggm_internal':
        km = m
        maxU = abs(sqrt(sqr(DiamT + 2 * c * m) / (sqr(baseDiam)) - 1))
        minU = abs((pi * m / 4 + m * tan(pressureAngle)) / (DiamRef / 2))
        tw = - tw
    else:
        km = m + c*m
        maxU = abs(sqrt(sqr(DiamT) / (sqr(baseDiam)) - 1))
        minU = abs((pi * m / 4 + km * tan(pressureAngle)) / (DiamRef / 2))
    dX = km - shiftX
    l = abs(sqrt(sqr(dX) + sqr(pi * m / 4 + km * tan(pressureAngle))))
    k = 2 * pi / nTeeth
    dAng = 2 * GearFuncs.getEvolvAngle(DiamRef, m, nTeeth, pressureAngle) + 4 * shiftX * tan(pressureAngle) / DiamRef
    ang = abs(atan(dX / (pi * m / 4 + km * tan(pressureAngle))))
    if val < 0.5:
        u2 = minU + 2 * (uMinFt - minU) * val
        if ang < pi / 2 - u2:
            a1 = abs(ang - pi / 2 + u2)
        else:
            a1 = -abs(ang - pi / 2 + u2)
        vertEvolv = GearFuncs.getVertEvolv(DiamRef, u2)
        if side == 0:
            v3 = Vector((vertEvolv[0] - l * cos(a1), - vertEvolv[1] - l * sin(a1), 0))
            v3.rotate(Euler((0.0, 0.0, tw), 'XYZ'))
        else:
            v3 = Vector((vertEvolv[0] - l * cos(a1), vertEvolv[1] + l * sin(a1), 0))
            v3.rotate(Euler((0.0, 0.0, - tw), 'XYZ'))
    else:
        vertEvolv = GearFuncs.getVertEvolv(baseDiam, 2 * (val - 0.5) * (maxU - uMinEv) + uMinEv)
        if side == 0:
            v3 = Vector((vertEvolv[0], vertEvolv[1], 0))
            v3.rotate(Euler((0.0, 0.0, -k / 4 - dAng / 2 + tw), 'XYZ'))
        else:
            v3 = Vector((vertEvolv[0], - vertEvolv[1], 0))
            v3.rotate(Euler((0.0, 0.0, dAng / 2 + k / 4 - tw), 'XYZ'))
    return v3


def get_point_w_profile(m, nTeeth, dWorm, H, nTWorm, pressureAngle, shiftX, uMinEv, uMinFt, val, side, teeth, c=0.25, tw = 0.0):
    vertsEtalon = []
    vertsEtalon2 = []
    DiamT = GearFuncs.getTipDiam(m, nTeeth) + shiftX * 2
    DiamR = GearFuncs.getRootDiam(m, nTeeth, c) + shiftX * 2
    k = 2 * pi / nTeeth
    if H > 0:
        angA = angA2 = 0
        angB = angB2 = atan(2 * H / (DiamT - DiamR + dWorm))
    else:
        angA = angA2 = atan(2 * H / (DiamT - DiamR + dWorm))
        angB = angB2 = 0
    angC = atan(2 * H / (DiamT - DiamR + dWorm))
    radGear = DiamT / 2 + dWorm / 2
    vt = Vector((0, 0, 0))
    v3 = get_point_profile(m, nTeeth, pressureAngle, 'ggm_ext_spur', shiftX, uMinEv, uMinFt, val, 0, c, tw)
    v3_2 = get_point_profile(m, nTeeth, pressureAngle, 'ggm_ext_spur', shiftX, uMinEv, uMinFt,
                             val, 1, c, tw)
    v3.rotate(Euler((0.0, 0.0, k / 2), 'XYZ'))
    v3_2.rotate(Euler((0.0, 0.0, k / 2), 'XYZ'))
    v3.rotate(Euler((0.0, 0.0, (angC + 2 * nTWorm * pi - 2 * (teeth + 1) * pi) / nTeeth), 'XYZ'))
    v3_2.rotate(Euler((0.0, 0.0, (angC + 2 * nTWorm * pi - 2 * (teeth + 1) * pi) / nTeeth), 'XYZ'))
    v3[0] = v3[0] - radGear
    v3_2[0] = v3_2[0] - radGear
    v3.rotate(Euler((0.0, angC + 2 * nTWorm * pi - 2 * (teeth + 1) * pi, 0.0), 'XYZ'))
    v3_2.rotate(Euler((0.0, angC + 2 * nTWorm * pi - 2 * (teeth + 1) * pi, 0.0), 'XYZ'))
    hcon = tan(angC) * (radGear - abs(sqrt((v3[0] + radGear) * (v3[0] + radGear) + v3[1] * v3[1])))
    hcon2 = tan(angC) * (radGear - abs(sqrt((v3_2[0] + radGear) * (v3_2[0] + radGear) + v3_2[1] * v3_2[1])))
    while abs(v3[2] - hcon) > m / 1000 or abs(v3_2[2] - hcon2) > m / 1000:
        v3 = get_point_profile(m, nTeeth, pressureAngle, 'ggm_ext_spur', shiftX, uMinEv, uMinFt, val, 0, c, tw)
        v3_2 = get_point_profile(m, nTeeth, pressureAngle, 'ggm_ext_spur', shiftX, uMinEv, uMinFt,
                                 val, 1, c, tw)
        v3.rotate(Euler((0.0, 0.0, k / 2), 'XYZ'))
        v3_2.rotate(Euler((0.0, 0.0, k / 2), 'XYZ'))
        v3.rotate(Euler((0.0, 0.0, ((angA + angB) / 2 + 2 * nTWorm * pi - 2 * (teeth + 1) * pi) / nTeeth), 'XYZ'))
        v3_2.rotate(
            Euler((0.0, 0.0, ((angA2 + angB2) / 2 + 2 * nTWorm * pi - 2 * (teeth + 1) * pi) / nTeeth), 'XYZ'))
        v3[0] = v3[0] - radGear
        v3_2[0] = v3_2[0] - radGear
        v3.rotate(Euler((0.0, (angA + angB) / 2 + 2 * nTWorm * pi - 2 * (teeth + 1) * pi, 0.0), 'XYZ'))
        v3_2.rotate(Euler((0.0, (angA2 + angB2) / 2 + 2 * nTWorm * pi - 2 * (teeth + 1) * pi, 0.0), 'XYZ'))
        hcon = tan(angC) * (radGear - abs(sqrt((v3[0] + radGear) * (v3[0] + radGear) + v3[1] * v3[1])))
        hcon2 = tan(angC) * (radGear - abs(sqrt((v3_2[0] + radGear) * (v3_2[0] + radGear) + v3_2[1] * v3_2[1])))
        if hcon < v3[2]:
            angB = (angA + angB) / 2
        else:
            angA = (angA + angB) / 2
        if hcon2 < v3_2[2]:
            angB2 = (angA2 + angB2) / 2
        else:
            angA2 = (angA2 + angB2) / 2
    if H > 0:
        angA = angA2 = 0
        angB = angB2 = atan(2 * H / (DiamT - DiamR + dWorm))
    else:
        angA = angA2 = atan(2 * H / (DiamT - DiamR + dWorm))
        angB = angB2 = 0
    vertsEtalon.append(v3)
    vertsEtalon2.append(v3_2)
    vt = Vector((vertsEtalon[-1][0], vertsEtalon[-1][1], vertsEtalon[-1][2]))
    vt2 = Vector((vertsEtalon2[0][0], vertsEtalon2[0][1], vertsEtalon2[0][2]))
    vertsEtalon.clear()
    vertsEtalon2.clear()
    if side == 0:
        return vt
    else:
        return vt2


def createRackVerts(m, nTeeth, width, prezureAngle, shiftX, H, skew):
    verts = []
    v = Vector((1.25 * m - shiftX, -1.25 * pi * m + skew, H))
    verts.append(v)
    for n in range(nTeeth):
        v = Vector((1.25 * m - shiftX, pi * m * (n - 0.75) - (1.25 * m - shiftX) * tan(prezureAngle) + skew, H))
        verts.append(v)
        v = Vector((-m - shiftX, pi * m * (n - 0.75) + (m + shiftX) * tan(prezureAngle) + skew, H))
        verts.append(v)
        v = Vector((-m - shiftX, pi * m * (n - 0.25) - (m + shiftX) * tan(prezureAngle) + skew, H))
        verts.append(v)
        v = Vector((1.25 * m - shiftX, pi * m * (n - 0.25) + (1.25 * m - shiftX) * tan(prezureAngle) + skew, H))
        verts.append(v)
    v = Vector((1.25 * m - shiftX, pi * m * (nTeeth - 0.75) + skew, H))
    verts.append(v)
    return verts


def createRackMesh(m, nTeeth, prezureAngle, width, widthStep, shiftX, skew, name="Rack", isHerringbone=False):
    # os.system("cls")
    VEF = ([], [], [])
    nVerts1 = 2 * nTeeth + 2
    nVerts2 = 4 * nTeeth + 2
    v = Vector(((1.25 * m - shiftX) + m / 2, -1.25 * pi * m, 0))
    VEF[0].append(v)
    if isHerringbone:
        widthStep = 2 * widthStep
    for n in range(nTeeth):
        v = Vector(((1.25 * m - shiftX) + m / 2, pi * m * (n - 0.75) - (1.25 * m - shiftX) * tan(prezureAngle), 0))
        VEF[0].append(v)
        v = Vector(((1.25 * m - shiftX) + m / 2, pi * m * (n - 0.25) + (1.25 * m - shiftX) * tan(prezureAngle), 0))
        VEF[0].append(v)
    v = Vector(((1.25 * m - shiftX) + m / 2, pi * m * (nTeeth - 0.75), 0))
    VEF[0].append(v)
    g = createRackVerts(m, nTeeth, width, prezureAngle, shiftX, 0, 0)
    VEF[0].extend(g)
    g2 = createRackVerts(m, nTeeth, width, prezureAngle, shiftX, width, skew)
    VEF[0].extend(g2)
    v = Vector(((1.25 * m - shiftX) + m / 2, -1.25 * pi * m + skew, width))
    VEF[0].append(v)
    for n in range(nTeeth):
        v = Vector(
            ((1.25 * m - shiftX) + m / 2, pi * m * (n - 0.75) - (1.25 * m - shiftX) * tan(prezureAngle) + skew, width))
        VEF[0].append(v)
        v = Vector(
            ((1.25 * m - shiftX) + m / 2, pi * m * (n - 0.25) + (1.25 * m - shiftX) * tan(prezureAngle) + skew, width))
        VEF[0].append(v)
    v = Vector(((1.25 * m - shiftX) + m / 2, pi * m * (nTeeth - 0.75) + skew, width))
    VEF[0].append(v)
    v1 = 0
    v2 = 0
    for f in range(nTeeth):
        v1 = 2 + 2 * f
        v3 = nVerts1 + 4 * f + 1
        VEF[2].append((v1, v1 - 1, v3, v3 + 3))
        v1 = v1 + nVerts2 * 2 + nVerts1
        v3 = v3 + nVerts2
        VEF[2].append((v1, v3 + 3, v3, v1 - 1))
        v1 = nVerts1 + 1 + f * 4
        VEF[2].append((v1, v1 + 1, v1 + 2, v1 + 3))
        v1 = v1 + nVerts2
        VEF[2].append((v1, v1 + 3, v1 + 2, v1 + 1))
        for fb in range(4):
            v1 = nVerts1 + f * 4 + fb
            v2 = v1 + nVerts2
            VEF[2].append((v1, v2, v2 + 1, v1 + 1))
    VEF[2].append((v1 + 1, v2 + 1, v2 + 2, v1 + 2))
    for f in range(nTeeth + 1):
        v1 = 1 + 2 * f
        v3 = nVerts1 + 4 * f
        VEF[2].append((v1, v1 - 1, v3, v3 + 1))
        v1 = v1 + nVerts2 * 2 + nVerts1
        v3 = v3 + nVerts2
        VEF[2].append((v1, v3 + 1, v3, v1 - 1))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(VEF[0], VEF[1], VEF[2])
    mesh.update()
    return mesh


def createWormVerts(wType, m, nTeeth, dWorm, rezWorm, nTWorm, evolvStep, filletCurveStep, pressureAngle,
                    shiftX, uMinEv, uMinFt, angZ, c=0.25, tw=0.0):
    verts = []
    DiamRef = GearFuncs.getRefDiam(m, nTeeth)
    DiamT = GearFuncs.getTipDiam(m, nTeeth) + shiftX * 2
    k = 2 * pi / nTeeth
    valFlt = 0.5 / filletCurveStep
    valEvolv = 0.5 / evolvStep
    if wType == 'wt_globoid_2':
        for es in reversed(range(evolvStep + 1)):
            v = get_point_profile(m,
                                nTeeth,
                                pressureAngle,
                                'ggm_internal',
                                shiftX,
                                uMinEv,
                                uMinFt,
                                0.5 + valEvolv * es,
                                1,
                                c,
                                tw)
            for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
                v3 = Vector(v)
                v3.rotate(Euler((0.0, 0.0, -k / 2), 'XYZ'))
                v3.rotate(Euler((0.0, 0.0, rot * k / rezWorm), 'XYZ'))
                v3[0] = v3[0] - DiamT / 2 - dWorm / 2
                v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
                v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
                verts.append(v3)
        #############################################################
        for fs in reversed(range(filletCurveStep)):
            v = get_point_profile(m,
                                nTeeth,
                                pressureAngle,
                                'ggm_internal',
                                shiftX,
                                uMinEv,
                                uMinFt,
                                valFlt * fs,
                                1,
                                c,
                                tw)
            for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
                v3 = Vector(v)
                v3.rotate(Euler((0.0, 0.0, -k / 2), 'XYZ'))
                v3.rotate(Euler((0.0, 0.0, rot * k / rezWorm), 'XYZ'))
                v3[0] = v3[0] - DiamT / 2 - dWorm / 2
                v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
                v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
                verts.append(v3)
        for fs in range(filletCurveStep):
            v = get_point_profile(m, nTeeth, pressureAngle, 'ggm_internal', shiftX, uMinEv, uMinFt, valFlt * fs,
                                       0, c, tw)
            for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
                v3 = Vector(v)
                v3.rotate(Euler((0.0, 0.0, k / 2), 'XYZ'))
                v3.rotate(Euler((0.0, 0.0, rot * k / rezWorm), 'XYZ'))
                v3[0] = v3[0] - DiamT / 2 - dWorm / 2
                v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
                v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
                verts.append(v3)
        ###############################################################
        for es in range(evolvStep + 1):
            v = get_point_profile(m, nTeeth, pressureAngle, 'ggm_internal', shiftX, uMinEv, uMinFt,
                                       0.5 + valEvolv * es, 0, c, tw)
            for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
                v3 = Vector(v)                
                v3.rotate(Euler((0.0, 0.0, k / 2), 'XYZ'))
                v3.rotate(Euler((0.0, 0.0, rot * k / rezWorm), 'XYZ'))
                v3[0] = v3[0] - DiamT / 2 - dWorm / 2
                v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
                v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
                verts.append(v3)
    if wType == 'wt_globoid_1':
        for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
            v3 = Vector((1.25 * m + DiamRef / 2, -pi * m / 4 - 1.25 * m * tan(pressureAngle), 0))
            v3.rotate(Euler((0.0, 0.0, rot * k / rezWorm), 'XYZ'))
            v3[0] = v3[0] - DiamT / 2 - dWorm / 2
            v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
            v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
            verts.append(v3)
        for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
            v3 = Vector((-m + DiamRef / 2, -pi * m / 4 + m * tan(pressureAngle), 0))
            v3.rotate(Euler((0.0, 0.0, rot * k / rezWorm), 'XYZ'))
            v3[0] = v3[0] - DiamT / 2 - dWorm / 2
            v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
            v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
            verts.append(v3)
        for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
            v3 = Vector((-m + DiamRef / 2, pi * m / 4 - m * tan(pressureAngle), 0))
            v3.rotate(Euler((0.0, 0.0, rot * k / rezWorm), 'XYZ'))
            v3[0] = v3[0] - DiamT / 2 - dWorm / 2
            v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
            v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
            verts.append(v3)
        for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
            v3 = Vector((1.25 * m + DiamRef / 2, pi * m / 4 + 1.25 * m * tan(pressureAngle), 0))
            v3.rotate(Euler((0.0, 0.0, rot * k / rezWorm), 'XYZ'))
            v3[0] = v3[0] - DiamT / 2 - dWorm / 2
            v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
            v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
            verts.append(v3)
    if wType == 'wt_cylindrical':
        for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
            v3 = Vector((1.25 * m + DiamRef / 2, - pi * m / 4 - 1.25 * m * tan(pressureAngle), 0))
            v3[1] = v3[1] + rot * pi * m / rezWorm
            v3[0] = v3[0] - DiamT / 2 - dWorm / 2
            v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
            v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
            verts.append(v3)
        for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
            v3 = Vector((-m + DiamRef / 2, -pi * m / 4 + m * tan(pressureAngle), 0))
            v3[1] = v3[1] + rot * pi * m / rezWorm
            v3[0] = v3[0] - DiamT / 2 - dWorm / 2
            v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
            v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
            verts.append(v3)
        for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
            v3 = Vector((-m + DiamRef / 2, pi * m / 4 - m * tan(pressureAngle), 0))
            v3[1] = v3[1] + rot * pi * m / rezWorm
            v3[0] = v3[0] - DiamT / 2 - dWorm / 2
            v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
            v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
            verts.append(v3)
        for rot in range(-rezWorm * nTWorm, rezWorm * nTWorm + 1):
            v3 = Vector((1.25 * m + DiamRef / 2, pi * m / 4 + 1.25 * m * tan(pressureAngle), 0))
            v3[1] = v3[1] + rot * pi * m / rezWorm
            v3[0] = v3[0] - DiamT / 2 - dWorm / 2
            v3.rotate(Euler((0.0, 2 * rot * pi / rezWorm, 0.0), 'XYZ'))
            v3.rotate(Euler((0.0, angZ, 0.0), 'XYZ'))
            verts.append(v3)
    return verts


def createWormMesh(wType, m, nTeeth, dWorm, rezWorm, nTWorm, evolvStep, filletCurveStep, prezureAngle,
                   shiftX, angZ=0.0, name="Worm", c=0.25):
    # os.system("cls")
    VEF = ([], [], [])
    if wType == 'wt_globoid_2':
        st = (evolvStep + filletCurveStep) * 2
    else:
        st = 2
    u = GearFuncs.getCrossEvolv(m, nTeeth, prezureAngle, shiftX, 'ggm_internal', c)
    g1 = createWormVerts(wType, m, nTeeth, dWorm, rezWorm, nTWorm, evolvStep, filletCurveStep,
                         prezureAngle, shiftX, u[0], u[1], angZ)
    VEF[0].extend(g1)
    for es in range(st + 1):
        for nf in range(2 * rezWorm * nTWorm):
            VEF[2].append((nf + es * (2 * rezWorm * nTWorm + 1), nf + 1 + es * (2 * rezWorm * nTWorm + 1),
                           (es + 1) * (2 * rezWorm * nTWorm + 1)
                           + nf + 1, (es + 1) * (2 * rezWorm * nTWorm + 1) + nf))
    for cs in range(2 * rezWorm * nTWorm - rezWorm):
        VEF[2].append(((st + 1) * (2 * rezWorm * nTWorm + 1) + cs, (st + 1) * (2 * rezWorm * nTWorm + 1) + cs + 1,
                       cs + rezWorm + 1,
                       cs + rezWorm))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(VEF[0], VEF[1], VEF[2])
    mesh.update()
    return mesh


def createProfileVerts(m, diamHole, dWorm, nTeeth, evolvStep, filletCurveStep, tStep, bStep, pressureAngle,
                       typeGear, shiftX, angCon, skewAng, uMinEv, uMinFt, angZ, typeLay, c=0.25, tw=0.0):
    verts = []
    verts1 = []
    verts1_2 = []
    verts2 = []
    verts3 = []
    tVerts3 = []
    tVerts2 = []
    DiamRef = GearFuncs.getRefDiam(m, nTeeth)
    DiamT = GearFuncs.getTipDiam(m, nTeeth) + shiftX * 2
    k = 2 * pi / nTeeth
    if typeGear != 'ggm_internal':
        tA = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 1, 0, c).angle(
            get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 1, 1, c)) / 2
        DiamR = GearFuncs.getRootDiam(m, nTeeth, c) + shiftX * 2
    else:
        tA = (k - get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 0, 0, c).angle(
            get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 0, 1, c))) / 2
        DiamR = GearFuncs.getRootDiam(m, nTeeth, c) + shiftX * 2 + 0.5 * m
    tw = tA * (1 - tw)   
    rAng = 2 * pi / ((tStep + bStep) * nTeeth)
    dH = 0.0
    dL = m/2
    if typeGear == 'ggm_ext_bevel':
        dH = (dL + (DiamRef - DiamR) / 2) * sin(angCon)
    if typeLay != 0:
        if typeGear != 'ggm_internal':
            for r in range((tStep + bStep) * nTeeth):
                if angCon >= pi/2:
                    if typeGear == 'ggm_ext_bevel':
                        v1 = Vector(((DiamR / 2 - 2*dL), 0, 0))
                else:
                    v1 = Vector(((diamHole / 2), 0, 0))
                v1.rotate(Euler((0.0, 0.0, rAng * (r - tStep / 2)), 'XYZ'))                
                if angCon >= pi/2:
                    if typeGear == 'ggm_ext_bevel':
                        v1 = GearFuncs.rotTeeth(DiamRef + 2 * shiftX, v1, angCon)
                else:
                    v1[2] = - dH
                verts1.append(v1)
            for r in range((tStep + bStep) * nTeeth):
                v1 = Vector(((DiamR / 2 - dL), 0, 0))
                v1.rotate(Euler((0.0, 0.0, rAng * (r - tStep / 2)), 'XYZ'))
                if typeGear == 'ggm_ext_bevel':
                    v1 = GearFuncs.rotTeeth(DiamRef + 2 * shiftX, v1, angCon)                
                v1[2] = - dH
                verts1_2.append(v1)
        else:
            for r in range((tStep + bStep) * nTeeth):
                v1 = Vector(((diamHole / 2), 0, 0))
                v1.rotate(Euler((0.0, 0.0, (r + tStep / 2) * rAng), 'XYZ'))
                v1[2] = - dH
                verts1.append(v1)
            for r in range((tStep + bStep) * nTeeth):
                v1 = Vector(((DiamT / 2 + dL), 0, 0))
                v1.rotate(Euler((0.0, 0.0, (r + tStep / 2) * rAng), 'XYZ'))
                v1[2] = - dH
                verts1_2.append(v1)
    valFlt = 0.5 / filletCurveStep
    valEvolv = 0.5 / evolvStep
    if typeGear != 'ggm_internal':
        for fs in range(filletCurveStep):
            v3 = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, valFlt * fs, 0, c, tw)
            verts3.append(v3)
        for es in range(evolvStep + 1):
            v3 = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt,
                                   0.5 + valEvolv * es, 0, c, tw)
            verts3.append(v3)
        tAng = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 1, 0, c, tw).angle(
            get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 1, 1, c, tw)) / tStep
        for ts in range(1, tStep):
            v = Vector((v3[0], v3[1], v3[2]))
            v.rotate(Euler((0.0, 0.0, tAng * ts), 'XYZ'))
            verts3.append(v)
        for es in reversed(range(evolvStep + 1)):
            v3 = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt,
                                   0.5 + valEvolv * es, 1, c, tw)
            verts3.append(v3)
        for fs in reversed(range(filletCurveStep)):
            v3 = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, valFlt * fs, 1, c, tw)
            verts3.append(v3)
        vb = Vector((verts3[0][0], verts3[0][1], verts3[0][2]))
        vb.rotate(Euler((0.0, 0.0, k), 'XYZ'))
        bAng = (k - get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 0, 0, c, tw).angle(
            get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 0, 1, c, tw))) / bStep
        for bs in range(1, bStep):
            v = Vector((v3[0], v3[1], v3[2]))
            v.rotate(Euler((0.0, 0.0, bAng * bs), 'XYZ'))
            verts3.append(v)
    else:
        for es in reversed(range(evolvStep + 1)):
            v3 = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt,
                                   0.5 + valEvolv * es, 1, c, tw)
            verts3.append(v3)
        for fs in reversed(range(filletCurveStep)):
            v3 = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, valFlt * fs, 1, c,tw)
            verts3.append(v3)
        vb = Vector((verts3[0][0], verts3[0][1], verts3[0][2]))
        vb.rotate(Euler((0.0, 0.0, k), 'XYZ'))
        bAng = (k - get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 0, 0, c, tw).angle(
            get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 0, 1, c, tw))) / bStep
        for bs in range(1, bStep):
            v = Vector((v3[0], v3[1], v3[2]))
            v.rotate(Euler((0.0, 0.0, bAng * bs), 'XYZ'))
            verts3.append(v)
        for fs in range(filletCurveStep):
            v3 = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, valFlt * fs, 0, c, tw)
            v3.rotate(Euler((0.0, 0.0, k), 'XYZ'))
            verts3.append(v3)
        for es in range(evolvStep + 1):
            v3 = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt,
                                   0.5 + valEvolv * es, 0, c, tw)
            v3.rotate(Euler((0.0, 0.0, k), 'XYZ'))
            verts3.append(v3)
        tAng = get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 1, 0, c, tw).angle(
            get_point_profile(m, nTeeth, pressureAngle, typeGear, shiftX, uMinEv, uMinFt, 1, 1, c, tw)) / tStep
        for ts in range(1, tStep):
            v = Vector((v3[0], v3[1], v3[2]))
            v.rotate(Euler((0.0, 0.0, tAng * ts), 'XYZ'))
            verts3.append(v)
    if typeLay != 0:
        if typeGear != 'ggm_internal':
            for st in range(filletCurveStep + evolvStep):
                Ang = verts3[st].angle(verts3[2 * (filletCurveStep + evolvStep) + tStep - st]) / tStep
                for ts in range(1, tStep):
                    vt = Vector((verts3[st][0], verts3[st][1], verts3[st][2]))
                    vt.rotate(Euler((0.0, 0.0, Ang * ts), 'XYZ'))
                    verts2.append(vt)
        else:
            for st in range(filletCurveStep + evolvStep):
                Ang = verts3[st].angle(verts3[2 * (filletCurveStep + evolvStep) + bStep - st]) / bStep
                for ts in range(1, bStep):
                    vt = Vector((verts3[st][0], verts3[st][1], verts3[st][2]))
                    vt.rotate(Euler((0.0, 0.0, Ang * ts), 'XYZ'))
                    verts2.append(vt)

    for nt in range(1, nTeeth):
        for v3 in verts3:
            v = Vector((v3[0], v3[1], v3[2]))
            v.rotate(Euler((0.0, 0.0, nt * k), 'XYZ'))
            tVerts3.append(v)
        if typeLay != 0:
            for v2 in verts2:
                v = Vector((v2[0], v2[1], v2[2]))
                v.rotate(Euler((0.0, 0.0, nt * k), 'XYZ'))
                tVerts2.append(v)
    verts2.extend(tVerts2)
    verts3.extend(tVerts3)
    if typeGear == 'ggm_ext_bevel':
        for v in verts2:
            vbev = Vector((v[0], v[1], v[2]))
            vbev = GearFuncs.rotTeeth(DiamRef + 2 * shiftX, vbev, angCon)
            v[0] = vbev[0]
            v[1] = vbev[1]
            v[2] = vbev[2]
        for v in verts3:
            vbev = Vector((v[0], v[1], v[2]))
            vbev = GearFuncs.rotTeeth(DiamRef + 2 * shiftX, vbev, angCon)
            v[0] = vbev[0]
            v[1] = vbev[1]
            v[2] = vbev[2]
    if typeLay == 1:
        verts.extend(verts1)
        verts.extend(verts1_2)
        verts.extend(verts2)
        verts.extend(verts3)
    else:
        verts.extend(verts3)
        verts.extend(verts2)
        verts.extend(verts1_2)
        verts.extend(verts1)    
    for v in verts:
        v.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))

    return verts


def createWormGearVerts(m, diamHole, nTeeth, dWorm, H, nTWorm, evolvStep, filletCurveStep, tStep, bStep, pressureAngle,
                        shiftX, uMinEv, uMinFt, angZ, typeLay, c=0.25):
    verts = []
    verts1 = []
    verts1_2 = []
    verts2 = []
    verts3 = []
    vertsTmp1 = []
    vertsTmp2 = []
    vertsTmp = []
    DiamT = GearFuncs.getTipDiam(m, nTeeth) + shiftX * 2
    DiamR = GearFuncs.getRootDiam(m, nTeeth, c) + shiftX * 2
    k = 2 * pi / nTeeth
    angC = atan(2 * H / (DiamT - DiamR + dWorm))
    radGear = DiamT / 2 + dWorm / 2
    val = 1.0 / (filletCurveStep + evolvStep)
    for fs in range(filletCurveStep + evolvStep + 1):
        vt = get_point_w_profile(m, nTeeth, dWorm, H, nTWorm + 1, pressureAngle, shiftX, uMinEv, uMinFt, val * fs, 0,
                                 2 * nTWorm)
        vt2 = get_point_w_profile(m, nTeeth, dWorm, H, nTWorm + 1, pressureAngle, shiftX, uMinEv, uMinFt, val * fs, 1,
                                  1)
        vt2[0] = vt2[0] + radGear
        vt2.rotate(Euler((0.0, 0.0, -k * (2 * nTWorm - 1)), 'XYZ'))
        vt2[0] = vt2[0] - radGear
        vertsTmp1.append(vt)
        vertsTmp2.append(vt2)
    vertsTmp.extend(vertsTmp1)
    for v in reversed(vertsTmp2):
        vertsTmp.append(v)

    #############################################################

    vAt = Vector((vertsTmp[filletCurveStep + evolvStep][0] + radGear, vertsTmp[filletCurveStep + evolvStep][1])).angle(
        Vector((vertsTmp[filletCurveStep + evolvStep + 1][0] + radGear,
                vertsTmp[filletCurveStep + evolvStep + 1][1]))) / tStep
    vAb = (k - Vector((vertsTmp[0][0] + radGear, vertsTmp[0][1])).angle(Vector(
        (vertsTmp[2 * (filletCurveStep + evolvStep) + 1][0] + radGear, vertsTmp[2 * (filletCurveStep + evolvStep) + 1][
            1])))) / bStep
    rAng = 2 * pi / ((tStep + bStep) * nTeeth)
    ang0 = (Vector((vertsTmp[0][0] + radGear, vertsTmp[0][1])).angle(Vector((1.0, 0.0))) + Vector((vertsTmp[2 * (
            filletCurveStep + evolvStep) + 1][0] + radGear, vertsTmp[2 * (filletCurveStep + evolvStep) + 1][
                                                                                                       1])).angle(
        Vector((1.0, 0.0)))) / 2
    dL = (1 - cos(angC)) * (DiamT - DiamR) / 2
    if typeLay != 0:
        for r in range(tStep + bStep + 1):
            v1 = Vector(((diamHole / 2 - 2 * m + dL), 0, 0))
            # v1.rotate(Euler((0.0, 0.0, rAng * (r - tStep / 2) + 3*k / 2 - k * nTWorm), 'XYZ'))
            v1.rotate(Euler((0.0, 0.0, -ang0 + rAng * (bStep + tStep / 2) + r * rAng), 'XYZ'))
            v1[2] = H
            v1.rotate(Euler((0.0, 0.0, angZ), 'XYZ'))
            verts1.append(Vector((v1[0], v1[1], v1[2])))
        for r in range(tStep + bStep + 1):
            v1 = Vector(((DiamR/2 + shiftX - m + dL), 0, 0))
            v1.rotate(Euler((0.0, 0.0, -ang0 + rAng * (bStep + tStep / 2) + r * rAng), 'XYZ'))
            v1[2] = H
            v1.rotate(Euler((0.0, 0.0, angZ), 'XYZ'))
            verts1_2.append(Vector((v1[0], v1[1], v1[2])))

    for v in vertsTmp:
        v3t = Vector((v[0], v[1], v[2]))
        v3t[0] = v3t[0] + radGear
        if vertsTmp.index(v) != filletCurveStep + evolvStep + 1:
            v3t.rotate(Euler((0.0, 0.0, k), 'XYZ'))
            verts3.append(Vector((v3t[0], v3t[1], v3t[2])))
        else:
            # v3t.rotate(Euler((0.0, 0.0, k * t - vAt * (tStep - 1)), 'XYZ'))
            v3t.rotate(Euler((0.0, 0.0, k - vAt * (tStep - 1)), 'XYZ'))
            verts3.append(Vector((v3t[0], v3t[1], v3t[2])))
            for tS in range(tStep - 1):
                v3t.rotate(Euler((0.0, 0.0, vAt), 'XYZ'))
                verts3.append(Vector((v3t[0], v3t[1], v3t[2])))
        if vertsTmp.index(v) == 2 * (filletCurveStep + evolvStep) + 1:
            for bS in range(bStep - 1):
                v3t.rotate(Euler((0.0, 0.0, vAb), 'XYZ'))
                verts3.append(Vector((v3t[0], v3t[1], v3t[2])))
            v3t = Vector((vertsTmp[0][0] + radGear, vertsTmp[0][1], vertsTmp[0][2]))
            v3t.rotate(Euler((0.0, 0.0, 2 * k), 'XYZ'))
            verts3.append(Vector((v3t[0], v3t[1], v3t[2])))

        if vertsTmp.index(v) < filletCurveStep + evolvStep:
            vA2 = Vector((v[0] + radGear, v[1])).angle(Vector((vertsTmp[2 * (
                    filletCurveStep + evolvStep) + 1 - vertsTmp.index(v)][0] + radGear, vertsTmp[2 * (
                    filletCurveStep + evolvStep) + 1 - vertsTmp.index(v)][1]))) / tStep
            for tS in range(tStep - 1):
                v3t.rotate(Euler((0.0, 0.0, vA2), 'XYZ'))
                verts2.append(Vector((v3t[0], v3t[1], v3t[2])))
    if typeLay == 0:
        verts.extend(verts3)
    if typeLay == 1:
        verts.extend(verts1)
        verts.extend(verts1_2)
        verts.extend(verts2)
        verts.extend(verts3)
    if typeLay == 2:
        verts.extend(verts3)
        verts.extend(verts2)
        verts.extend(verts1_2)
        verts.extend(verts1)
    return verts


def createGearMesh(m, nTeeth, evolvStep, filletCurveStep, tStep, bStep, pressureAngle, typeGear, width, widthStep,
                   shiftX, angCon, skewAng, angZ=0.0, dWorm=0, nTWorm=0, name="GearGen", c=0.25, tw=0.0, fill_holes = False, diamHole = 0.0, isHerringbone = False):
    # os.system("cls")
    VEF = ([], [], [])
    fill_verts = []
    if typeGear == 'ggm_ext_worm_gear':
        topSt = tStep
        botSt = bStep
        nVerts1 = (botSt + topSt + 1)
        curveStep = filletCurveStep + evolvStep
        nVerts2Segm = curveStep * (topSt - 1)
        nVerts2 = nVerts2Segm
        nVerts3Segm = (curveStep + 1) * 2 + topSt + botSt - 1
        nVerts3 = nVerts3Segm
        nVerts = 4 * nVerts1 + 2 * nVerts2 + nVerts3 * (widthStep + 1)
        HPart = (width / widthStep)
        """ diamHoleMax = GearFuncs.getRootDiam(m, nTeeth, c) + 2 * shiftX
        if diamHole > diamHoleMax:
            diamHole = diamHoleMax """
        u = GearFuncs.getCrossEvolv(m, nTeeth, pressureAngle, shiftX, 'ggm_ext_worm_gear', c)
        g1 = createWormGearVerts(m, diamHole, nTeeth, dWorm, -width / 2, nTWorm, evolvStep, filletCurveStep, tStep,
                                 bStep, pressureAngle, shiftX, u[0], u[1], angZ, 1)
        VEF[0].extend(g1)
        for n in range(1, widthStep + 1):
            if n != widthStep:
                g2 = createWormGearVerts(m, diamHole, nTeeth, dWorm, HPart * n - width / 2, nTWorm, evolvStep,
                                         filletCurveStep, tStep, bStep, pressureAngle, shiftX, u[0], u[1], angZ, 0)
            else:
                g2 = createWormGearVerts(m, diamHole, nTeeth, dWorm, width / 2, nTWorm, evolvStep, filletCurveStep,
                                         tStep, bStep, pressureAngle, shiftX, u[0], u[1], angZ, 2)
            VEF[0].extend(g2)
        if fill_holes:
            rAng = 2 * pi / ((tStep + bStep) * nTeeth)
            # in development
    else:
        if typeGear == 'ggm_internal':
            topSt = bStep
            botSt = tStep
        else:
            topSt = tStep
            botSt = bStep
        nVerts1 = (botSt + topSt) * nTeeth
        curveStep = filletCurveStep + evolvStep
        nVerts2Segm = curveStep * (topSt - 1)
        nVerts2 = nVerts2Segm * nTeeth
        nVerts3Segm = (curveStep + 1) * 2 + topSt + botSt - 2
        nVerts3 = nVerts3Segm * nTeeth
        radRef = GearFuncs.getRefDiam(m, nTeeth) / 2 + shiftX
        origZ = GearFuncs.getOriginZ(m, nTeeth, typeGear, shiftX, angCon)
        if typeGear == 'ggm_ext_bevel':
            isHerringbone = False
            ang = angCon
            if angCon != 0 and angCon!=pi:
                if width >= radRef / sin(ang) - m:
                    width = radRef / sin(ang) - m
            else:
                ang = 0
        else:
            ang = 0.0
        if isHerringbone:
            widthStep = widthStep * 2
        nVerts = 4 * nVerts1 + 2 * nVerts2 + nVerts3 * (widthStep + 1)
        prBase = width * sin(ang)
        mPart = m * (prBase / radRef) / widthStep
        HPart = (width / widthStep) * cos(ang)
        shiftPart = shiftX * (prBase / radRef) / widthStep
        """ if typeGear != 'ggm_internal':
            diamHoleMax = GearFuncs.getRootDiam(m * (1 - prBase / radRef), nTeeth, c) - 2 * m + 2 * shiftX
            if diamHole > diamHoleMax:
                diamHole = diamHoleMax
        else:
            diamHoleMax = GearFuncs.getTipDiam(m * (1 - prBase / radRef), nTeeth) + 2 * m + 2 * shiftX
            if diamHole < diamHoleMax:
                diamHole = diamHoleMax """
        skewPart = skewAng / widthStep
        u = GearFuncs.getCrossEvolv(m, nTeeth, pressureAngle, shiftX, typeGear, c)
        ###################################################################################
        if typeGear == 'cyl_worm':
            if width > dWorm:
                width = dWorm
            angW = atan(width / (dWorm + GearFuncs.getTipDiam(m, nTeeth) - GearFuncs.getRootDiam(m, nTeeth, c)))
            partAngW = 2 * angW / widthStep
            skW = angW / nTeeth
            skWPart = 2 * skW / widthStep
            g1 = createProfileVerts(m, diamHole, dWorm, nTeeth, evolvStep, filletCurveStep, tStep, bStep,
                                    pressureAngle, typeGear, shiftX, angW, -skW, u[0], u[1], angZ, 1, c, tw)
            for v3 in g1:
                v3[2] = v3[2] - width / 2
        else:
            g1 = createProfileVerts(m, diamHole, dWorm, nTeeth, evolvStep, filletCurveStep, tStep, bStep,
                                    pressureAngle, typeGear, shiftX, ang, 0.0, u[0], u[1], angZ, 1, c, tw)
            for v3 in g1:
                v3[2] = v3[2] - origZ
        VEF[0].extend(g1)

        #if typeGear == 'ggm_internal' or typeGear == 'ggm_ext_herringbone':
        if isHerringbone:
            for n in range(1, widthStep + 1):
                if n < widthStep / 2:
                    g2 = createProfileVerts(m - n * mPart, diamHole, dWorm, nTeeth, evolvStep, filletCurveStep,
                                            tStep, bStep, pressureAngle, typeGear, shiftX - n * shiftPart, ang,
                                            skewPart * n, u[0], u[1], angZ, 0, c, tw)
                else:
                    if n != widthStep:
                        g2 = createProfileVerts(m - n * mPart, diamHole, dWorm, nTeeth, evolvStep,
                                                filletCurveStep, tStep, bStep, pressureAngle, typeGear,
                                                shiftX - n * shiftPart, ang, skewAng - skewPart * n,
                                                u[0], u[1], angZ, 0, c, tw)
                    else:
                        g2 = createProfileVerts(m - n * mPart, diamHole, dWorm, nTeeth, evolvStep,
                                                filletCurveStep, tStep, bStep, pressureAngle, typeGear,
                                                shiftX - n * shiftPart, ang, skewAng - skewPart * n,
                                                u[0], u[1], angZ, 2, c, tw)
                for v3 in g2:
                    v3[2] = v3[2] + HPart * n - origZ
                VEF[0].extend(g2)
        elif typeGear == 'cyl_worm':
            for n in range(1, widthStep + 1):
                if n != widthStep:
                    g2 = createProfileVerts(m - n * mPart,
                                            diamHole,
                                            dWorm,
                                            nTeeth,
                                            evolvStep,
                                            filletCurveStep,
                                            tStep,
                                            bStep,
                                            pressureAngle,
                                            typeGear,
                                            shiftX - n * shiftPart,
                                            angW - partAngW * n,
                                            skWPart * n - skW,
                                            u[0],
                                            u[1],
                                            angZ,
                                            0,
                                            c,
                                            tw)
                else:
                    g2 = createProfileVerts(m - n * mPart,
                                            diamHole,
                                            dWorm,
                                            nTeeth,
                                            evolvStep,
                                            filletCurveStep,
                                            tStep,
                                            bStep,
                                            pressureAngle,
                                            typeGear,
                                            shiftX - n * shiftPart,
                                            -angW,
                                            skW,
                                            u[0],
                                            u[1],
                                            angZ,
                                            2,
                                            c,
                                            tw)
                    for v3 in g2:
                        v3[2] = v3[2] + width / 2
                VEF[0].extend(g2)
        else:
            for n in range(1, widthStep + 1):
                if n != widthStep:
                    g2 = createProfileVerts(m - n * mPart, diamHole, dWorm, nTeeth, evolvStep, filletCurveStep,
                                            tStep, bStep, pressureAngle, typeGear, shiftX - n * shiftPart, ang,
                                            skewPart * n, u[0], u[1], angZ, 0, c, tw)
                else:
                    g2 = createProfileVerts(m - n * mPart, diamHole, dWorm, nTeeth, evolvStep, filletCurveStep,
                                            tStep, bStep, pressureAngle, typeGear, shiftX - n * shiftPart, ang,
                                            skewPart * n, u[0], u[1], angZ, 2, c, tw)
                for v3 in g2:
                    v3[2] = v3[2] + HPart * n - origZ
                VEF[0].extend(g2)
        if fill_holes:
            rAng = 2 * pi / ((tStep + bStep) * nTeeth)
            if typeGear == 'ggm_ext_bevel':
                width = VEF[0][-1][2] - VEF[0][0][2] 
                HPart = (width / widthStep)
            for n in range(1, widthStep):
                for r in range((tStep + bStep) * nTeeth):            
                    v1 = Vector(((diamHole / 2), 0, 0))
                    if typeGear != 'ggm_internal':
                        v1.rotate(Euler((0.0, 0.0, rAng * (r - tStep / 2)), 'XYZ'))
                    else:
                        v1.rotate(Euler((0.0, 0.0, rAng * (r + tStep / 2)), 'XYZ'))
                    #if typeGear != 'ggm_internal' and typeGear != 'ggm_ext_herringbone':
                    if not isHerringbone:
                        v1.rotate(Euler((0.0, 0.0, skewAng - skewPart*n), 'XYZ'))
                    v1.rotate(Euler((0.0, 0.0, angZ), 'XYZ'))
                    v1[2] = VEF[0][0][2] + width - HPart * n
                    fill_verts.append(v1)
            VEF[0].extend(fill_verts)
    # building polygons of covers
    if typeGear == 'ggm_ext_worm_gear':
        for p in range(nVerts1 - 1):
            v1 = p
            v2 = p + 1
            v3 = v2 + nVerts1
            v4 = v3 - 1
            v1_2 = v1 + nVerts - nVerts1
            v2_2 = v2 + nVerts - nVerts1
            v3_2 = v3 + nVerts - 3 * nVerts1
            v4_2 = v4 + nVerts - 3 * nVerts1
            VEF[2].append((v1, v2, v3, v4))
            VEF[2].append((v1_2, v4_2, v3_2, v2_2))
        for p in range(2):
            if (p % 2) == 0:
                if topSt != 1:
                    for pT in range(topSt):
                        v1 = (1 + p / 2) * nVerts1 + pT
                        v1_2 = v1 + nVerts - 3 * nVerts1
                        if pT == 0 or (pT != 0 and pT != (topSt - 1)):
                            v2 = v1 + 1
                            v2_2 = v1_2 + 1
                            v3 = nVerts1 * 2 + nVerts2Segm * p / 2 + pT
                            v3_2 = v3 + nVerts2 + nVerts3 * (widthStep + 1)
                            if pT == 0:
                                v4 = nVerts1 * 2 + nVerts2 + nVerts3Segm * p / 2 + pT
                                v4_2 = v4 + nVerts3 * widthStep
                            if pT != 0 and pT != (topSt - 1):
                                v4 = v3 - 1
                                v4_2 = v3_2 - 1
                        if pT == (topSt - 1):
                            v2 = v1 + 1
                            v2_2 = v1_2 + 1
                            v3 = nVerts1 * 2 + nVerts2 + nVerts3Segm * (p / 2 + 1) - botSt - 1
                            v3_2 = v3 + + nVerts3 * widthStep
                            v4 = nVerts1 * 2 + nVerts2Segm * p / 2 + pT - 1
                            v4_2 = v4 + nVerts2 + nVerts3 * (widthStep + 1)
                        VEF[2].append((v1, v2, v3, v4))
                        VEF[2].append((v1_2, v4_2, v3_2, v2_2))
                else:
                    v1 = nVerts1 + (botSt + 1) * p / 2
                    v1_2 = v1 + nVerts - 3 * nVerts1
                    v2 = v1 + 1
                    v2_2 = v1_2 + 1
                    v4 = nVerts1 * 2 + nVerts3Segm * p / 2
                    v4_2 = v4 + nVerts3 * widthStep
                    v3 = v4 + nVerts3Segm - botSt - 1
                    v3_2 = v4_2 + nVerts3Segm - botSt - 1
                    VEF[2].append((v1, v2, v3, v4))
                    VEF[2].append((v1_2, v4_2, v3_2, v2_2))
            else:
                for pB in range(botSt):
                    v1 = nVerts1 + topSt + nVerts1 * (p - 1) / 2 + pB
                    v1_2 = v1 + nVerts1 + 2 * nVerts2 + nVerts3 * (widthStep + 1)
                    v4 = nVerts1 * 2 + nVerts2 + nVerts3Segm * ((p - 1) / 2 + 1) - botSt - 1 + pB
                    v4_2 = v4 + nVerts3 * widthStep
                    v2 = nVerts1 + topSt + nVerts1 * (p - 1) / 2 + pB + 1
                    v2_2 = v2 + nVerts - 3 * nVerts1
                    v3 = v4 + 1
                    v3_2 = v4_2 + 1
                    VEF[2].append((v1, v2, v3, v4))
                    VEF[2].append((v1_2, v4_2, v3_2, v2_2))
        if topSt != 1:
            for eS in range(curveStep):
                for tS in range(topSt):
                    if tS == 0 and eS != (curveStep - 1):
                        v1 = nVerts1 * 2 + nVerts2 + eS
                        v1_2 = v1 + nVerts3 * widthStep
                        v2 = nVerts1 * 2 + (topSt - 1) * eS
                        v2_2 = v2 + nVerts3 * (widthStep + 1) + nVerts2
                        v3 = v2 + topSt - 1
                        v3_2 = v2_2 + topSt - 1
                        v4 = v1 + 1
                        v4_2 = v1_2 + 1
                    if tS != 0 and eS != (curveStep - 1) and tS != (topSt - 1):
                        v1 = nVerts1 * 2 + (topSt - 1) * eS + tS - 1
                        v1_2 = v1 + nVerts3 * (widthStep + 1) + nVerts2
                        v2 = v1 + 1
                        v2_2 = v1_2 + 1
                        v3 = nVerts1 * 2 + (topSt - 1) * (eS + 1) + tS
                        v3_2 = v3 + nVerts3 * (widthStep + 1) + nVerts2
                        v4 = v3 - 1
                        v4_2 = v3_2 - 1
                    if tS == (topSt - 1) and eS != (curveStep - 1):
                        v1 = nVerts1 * 2 + (topSt - 1) * eS + tS - 1
                        v1_2 = v1 + nVerts3 * (widthStep + 1) + nVerts2
                        v2 = nVerts1 * 2 + nVerts2 + nVerts3Segm - eS - botSt - 1
                        v2_2 = v2 + nVerts3 * widthStep
                        v3 = v2 - 1
                        v3_2 = v2_2 - 1
                        v4 = v1 + topSt - 1
                        v4_2 = v1_2 + topSt - 1
                    if eS == (curveStep - 1) and tS == 0:
                        v1 = nVerts1 * 2 + nVerts2 + eS + tS
                        v1_2 = v1 + nVerts3 * widthStep
                        v2 = nVerts1 * 2 + (topSt - 1) * eS + tS
                        v2_2 = v2 + nVerts3 * (widthStep + 1) + nVerts2
                        v3 = v1 + 2
                        v3_2 = v1_2 + 2
                        v4 = v1 + 1
                        v4_2 = v1_2 + 1
                    if eS == (curveStep - 1) and tS != 0 and tS != (topSt - 1):
                        v1 = nVerts1 * 2 + (topSt - 1) * eS + tS - 1
                        v1_2 = v1 + nVerts3 * (widthStep + 1) + nVerts2
                        v2 = v1 + 1
                        v2_2 = v1_2 + 1
                        v3 = nVerts1 * 2 + nVerts2 + eS + tS + 2
                        v3_2 = v3 + nVerts3 * widthStep
                        v4 = v3 - 1
                        v4_2 = v3_2 - 1
                    if eS == (curveStep - 1) and tS != 0 and tS == (topSt - 1):
                        v1 = nVerts1 * 2 + (topSt - 1) * eS + tS - 1
                        v1_2 = v1 + nVerts3 * (widthStep + 1) + nVerts2
                        v2 = nVerts1 * 2 + nVerts2 + eS + tS + 3
                        v2_2 = v2 + nVerts3 * widthStep
                        v3 = v2 - 1
                        v3_2 = v2_2 - 1
                        v4 = v2 - 2
                        v4_2 = v2_2 - 2
                    VEF[2].append((v1, v2, v3, v4))
                    VEF[2].append((v1_2, v4_2, v3_2, v2_2))
        else:
            for eS in range(curveStep):
                v1 = nVerts1 * 2 + eS
                v1_2 = v1 + nVerts3 * widthStep
                v2 = nVerts1 * 2 + nVerts3Segm - botSt - eS - 1
                v2_2 = v2 + nVerts3 * widthStep
                v3 = v2 - 1
                v3_2 = v2_2 - 1
                v4 = v1 + 1
                v4_2 = v1_2 + 1
                if typeGear == 'ggm_internal':
                    VEF[2].append((v1, v4, v3, v2))
                    VEF[2].append((v1_2, v2_2, v3_2, v4_2))
                else:
                    VEF[2].append((v1, v2, v3, v4))
                    VEF[2].append((v1_2, v4_2, v3_2, v2_2))
        # building polygons of lateral surface
        for p in range(widthStep):
            for cs in range(nVerts3 - 1):
                v1 = nVerts1 * 2 + nVerts2 + p * nVerts3 + cs
                v2 = v1 + 1
                v3 = v2 + nVerts3
                v4 = v3 - 1
                VEF[2].append((v1, v2, v3, v4))
    else:
        for p in range(nVerts1 - 1):
            v1 = p
            v1_2 = v1 + nVerts - nVerts1
            v2 = p + 1
            v2_2 = v2 + nVerts - nVerts1
            v3 = v2 + nVerts1
            v3_2 = v3 + nVerts - 3 * nVerts1
            v4 = p + nVerts1
            v4_2 = v4 + nVerts - 3 * nVerts1
            if typeGear == 'ggm_internal':
                VEF[2].append((v1, v4, v3, v2))
                VEF[2].append((v1_2, v2_2, v3_2, v4_2))
            else:
                VEF[2].append((v1, v2, v3, v4))
                VEF[2].append((v1_2, v4_2, v3_2, v2_2))
        v1 = nVerts1 - 1
        v1_2 = nVerts - 1
        v2 = 0
        v2_2 = nVerts - nVerts1
        v3 = nVerts1
        v3_2 = nVerts - 2 * nVerts1
        v4 = 2 * nVerts1 - 1
        v4_2 = nVerts - nVerts1 - 1
        if typeGear == 'ggm_internal':
            VEF[2].append((v1, v4, v3, v2))
            VEF[2].append((v1_2, v2_2, v3_2, v4_2))
        else:
            VEF[2].append((v1, v2, v3, v4))
            VEF[2].append((v1_2, v4_2, v3_2, v2_2))
        for p in range(nTeeth * 2):
            if (p % 2) == 0:
                if topSt != 1:
                    for pT in range(topSt):
                        v1 = (nTeeth + p / 2) * (topSt + botSt) + pT
                        v1_2 = v1 + nVerts - 3 * nVerts1
                        if pT == 0 or (pT != 0 and pT != (topSt - 1)):
                            v2 = v1 + 1
                            v2_2 = v1_2 + 1
                            v3 = nVerts1 * 2 + nVerts2Segm * p / 2 + pT
                            v3_2 = v3 + nVerts2 + nVerts3 * (widthStep + 1)
                            if pT == 0:
                                v4 = nVerts1 * 2 + nVerts2 + nVerts3Segm * p / 2 + pT
                                v4_2 = v4 + nVerts3 * widthStep
                            if pT != 0 and pT != (topSt - 1):
                                v4 = v3 - 1
                                v4_2 = v3_2 - 1
                        if pT == (topSt - 1):
                            v2 = v1 + 1
                            v2_2 = v1_2 + 1
                            v3 = nVerts1 * 2 + nVerts2 + nVerts3Segm * (p / 2 + 1) - botSt
                            v3_2 = v3 + + nVerts3 * widthStep
                            v4 = nVerts1 * 2 + nVerts2Segm * p / 2 + pT - 1
                            v4_2 = v4 + nVerts2 + nVerts3 * (widthStep + 1)
                        if typeGear == 'ggm_internal':
                            VEF[2].append((v1, v4, v3, v2))
                            VEF[2].append((v1_2, v2_2, v3_2, v4_2))
                        else:
                            VEF[2].append((v1, v2, v3, v4))
                            VEF[2].append((v1_2, v4_2, v3_2, v2_2))
                else:
                    v1 = nVerts1 + (botSt + 1) * p / 2
                    v1_2 = v1 + nVerts - 3 * nVerts1
                    v2 = v1 + 1
                    v2_2 = v1_2 + 1
                    v4 = nVerts1 * 2 + nVerts3Segm * p / 2
                    v4_2 = v4 + nVerts3 * widthStep
                    v3 = v4 + nVerts3Segm - botSt
                    v3_2 = v4_2 + nVerts3Segm - botSt
                    if typeGear == 'ggm_internal':
                        VEF[2].append((v1, v4, v3, v2))
                        VEF[2].append((v1_2, v2_2, v3_2, v4_2))
                    else:
                        VEF[2].append((v1, v2, v3, v4))
                        VEF[2].append((v1_2, v4_2, v3_2, v2_2))
            else:
                for pB in range(botSt):
                    v1 = nVerts1 + topSt + (topSt + botSt) * (p - 1) / 2 + pB
                    v1_2 = v1 + nVerts1 + 2 * nVerts2 + nVerts3 * (widthStep + 1)
                    v4 = nVerts1 * 2 + nVerts2 + nVerts3Segm * ((p - 1) / 2 + 1) - botSt + pB
                    v4_2 = v4 + nVerts3 * widthStep
                    if p != (nTeeth * 2 - 1) or pB != (botSt - 1):
                        v2 = nVerts1 + topSt + (topSt + botSt) * (p - 1) / 2 + pB + 1
                        v2_2 = v2 + nVerts - 3 * nVerts1
                        v3 = v4 + 1
                        v3_2 = v4_2 + 1
                    else:
                        v2 = nVerts1
                        v2_2 = v2 + nVerts - 3 * nVerts1
                        v3 = nVerts1 * 2 + nVerts2
                        v3_2 = v3 + nVerts3 * widthStep
                    if typeGear == 'ggm_internal':
                        VEF[2].append((v1, v4, v3, v2))
                        VEF[2].append((v1_2, v2_2, v3_2, v4_2))
                    else:
                        VEF[2].append((v1, v2, v3, v4))
                        VEF[2].append((v1_2, v4_2, v3_2, v2_2))
        for nT in range(nTeeth):
            if topSt != 1:
                for eS in range(curveStep):
                    for tS in range(topSt):
                        if tS == 0 and eS != (curveStep - 1):
                            v1 = nVerts1 * 2 + nVerts2 + nVerts3Segm * nT + eS
                            v1_2 = v1 + nVerts3 * widthStep
                            v2 = nVerts1 * 2 + nVerts2Segm * nT + (topSt - 1) * eS
                            v2_2 = v2 + nVerts3 * (widthStep + 1) + nVerts2
                            v3 = v2 + topSt - 1
                            v3_2 = v2_2 + topSt - 1
                            v4 = v1 + 1
                            v4_2 = v1_2 + 1
                        if tS != 0 and eS != (curveStep - 1) and tS != (topSt - 1):
                            v1 = nVerts1 * 2 + nVerts2Segm * nT + (topSt - 1) * eS + tS - 1
                            v1_2 = v1 + nVerts3 * (widthStep + 1) + nVerts2
                            v2 = v1 + 1
                            v2_2 = v1_2 + 1
                            v3 = nVerts1 * 2 + nVerts2Segm * nT + (topSt - 1) * (eS + 1) + tS
                            v3_2 = v3 + nVerts3 * (widthStep + 1) + nVerts2
                            v4 = v3 - 1
                            v4_2 = v3_2 - 1
                        if tS == (topSt - 1) and eS != (curveStep - 1):
                            v1 = nVerts1 * 2 + nVerts2Segm * nT + (topSt - 1) * eS + tS - 1
                            v1_2 = v1 + nVerts3 * (widthStep + 1) + nVerts2
                            v2 = nVerts1 * 2 + nVerts2 + nVerts3Segm * (nT + 1) - eS - botSt
                            v2_2 = v2 + nVerts3 * widthStep
                            v3 = v2 - 1
                            v3_2 = v2_2 - 1
                            v4 = v1 + topSt - 1
                            v4_2 = v1_2 + topSt - 1
                        if eS == (curveStep - 1) and tS == 0:
                            v1 = nVerts1 * 2 + nVerts2 + nVerts3Segm * nT + eS + tS
                            v1_2 = v1 + nVerts3 * widthStep
                            v2 = nVerts1 * 2 + nVerts2Segm * nT + (topSt - 1) * eS + tS
                            v2_2 = v2 + nVerts3 * (widthStep + 1) + nVerts2
                            v3 = v1 + 2
                            v3_2 = v1_2 + 2
                            v4 = v1 + 1
                            v4_2 = v1_2 + 1
                        if eS == (curveStep - 1) and tS != 0 and tS != (topSt - 1):
                            v1 = nVerts1 * 2 + nVerts2Segm * nT + (topSt - 1) * eS + tS - 1
                            v1_2 = v1 + nVerts3 * (widthStep + 1) + nVerts2
                            v2 = v1 + 1
                            v2_2 = v1_2 + 1
                            v3 = nVerts1 * 2 + nVerts2 + nVerts3Segm * nT + eS + tS + 2
                            v3_2 = v3 + nVerts3 * widthStep
                            v4 = v3 - 1
                            v4_2 = v3_2 - 1
                        if eS == (curveStep - 1) and tS != 0 and tS == (topSt - 1):
                            v1 = nVerts1 * 2 + nVerts2Segm * nT + (topSt - 1) * eS + tS - 1
                            v1_2 = v1 + nVerts3 * (widthStep + 1) + nVerts2
                            v2 = nVerts1 * 2 + nVerts2 + nVerts3Segm * nT + eS + tS + 3
                            v2_2 = v2 + nVerts3 * widthStep
                            v3 = v2 - 1
                            v3_2 = v2_2 - 1
                            v4 = v2 - 2
                            v4_2 = v2_2 - 2
                        if typeGear == 'ggm_internal':
                            VEF[2].append((v1, v4, v3, v2))
                            VEF[2].append((v1_2, v2_2, v3_2, v4_2))
                        else:
                            VEF[2].append((v1, v2, v3, v4))
                            VEF[2].append((v1_2, v4_2, v3_2, v2_2))
            else:
                for eS in range(curveStep):
                    v1 = nVerts1 * 2 + nT * nVerts3Segm + eS
                    v1_2 = v1 + nVerts3 * widthStep
                    v2 = nVerts1 * 2 + (nT + 1) * nVerts3Segm - botSt - eS
                    v2_2 = v2 + nVerts3 * widthStep
                    v3 = v2 - 1
                    v3_2 = v2_2 - 1
                    v4 = v1 + 1
                    v4_2 = v1_2 + 1
                    if typeGear == 'ggm_internal':
                        VEF[2].append((v1, v4, v3, v2))
                        VEF[2].append((v1_2, v2_2, v3_2, v4_2))
                    else:
                        VEF[2].append((v1, v2, v3, v4))
                        VEF[2].append((v1_2, v4_2, v3_2, v2_2))

        # building polygons of lateral surface
        for p in range(nVerts3 * widthStep):
            v1 = nVerts1 * 2 + nVerts2 + p
            if (p + 1) % nVerts3 != 0:
                v2 = v1 + 1
                v3 = v2 + nVerts3
                v4 = v3 - 1
            else:
                v2 = v1 - nVerts3 + 1
                v3 = v1 + 1
                v4 = v1 + nVerts3
            if typeGear == 'ggm_internal':
                VEF[2].append((v1, v4, v3, v2))
            else:
                VEF[2].append((v1, v2, v3, v4))
        # building polygons of fill
        if fill_holes:
            for w in range(widthStep):
                if w != widthStep - 1:                
                    for p in range(nVerts1):
                        if p != nVerts1 - 1:
                            v1 = nVerts-nVerts1 + w*nVerts1 + p
                            v2 = v1+1
                            v3 = nVerts+1 + w*nVerts1 + p
                            v4 = v3-1
                        else:
                            v1 = nVerts-1 + w*nVerts1
                            v2 = nVerts-nVerts1 + w*nVerts1
                            v3 = nVerts + w*nVerts1
                            v4 = v3 + nVerts1 -1
                        if typeGear == 'ggm_internal':
                            VEF[2].append((v1, v4, v3, v2))
                        else:
                            VEF[2].append((v1, v2, v3, v4))
                else:
                    for p in range(nVerts1-1):                    
                        v1 = nVerts-nVerts1 + w*nVerts1 + p
                        v2 = v1+1
                        v3 = 1 + p
                        v4 = v3-1
                        if typeGear == 'ggm_internal':
                            VEF[2].append((v1, v4, v3, v2))
                        else:
                            VEF[2].append((v1, v2, v3, v4))
                    v1 = nVerts-1 + w*nVerts1
                    v2 = nVerts-nVerts1 + w*nVerts1
                    v3 = 0
                    v4 = nVerts1-1
                    if typeGear == 'ggm_internal':
                        VEF[2].append((v1, v4, v3, v2))
                    else:
                        VEF[2].append((v1, v2, v3, v4))

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(VEF[0], VEF[1], VEF[2])
    mesh.update()
    return mesh

def createMesh(pr, context):    
    mesh = 0
    nm = ''
    tpG = ''
    if pr.ggm_Type == 'ggm_internal':
        nm = 'InternalGear'
        tpG = pr.ggm_Type
    elif pr.ggm_Type == 'ggm_external':
        tpG = pr.ggm_External_Type
        if pr.ggm_External_Type == 'ggm_ext_rack':
            nm = 'Rack'
        elif pr.ggm_External_Type == 'ggm_ext_spur':
            nm = 'SpurGear'
        elif pr.ggm_External_Type == 'ggm_ext_herringbone':
            nm = 'HerringboneGear'
        elif pr.ggm_External_Type == 'ggm_ext_bevel':
            nm = 'BevelGear'
        else:
            nm = 'WormGear'
    else:
        nm = 'WormGear'
        tpG = pr.ggm_wType
    if pr.ggm_Type == 'ggm_internal' or (pr.ggm_Type == 'ggm_external' and pr.ggm_External_Type != 'ggm_ext_rack' ):        
        mesh = createGearMesh(m=pr.ggm_module,
                            nTeeth=pr.ggm_nTeeth,
                            evolvStep=pr.ggm_evolvStep,
                            filletCurveStep=pr.ggm_filletCurveStep,
                            tStep=pr.ggm_tStep,
                            bStep=pr.ggm_bStep,
                            pressureAngle=pr.ggm_angle,
                            typeGear=tpG,
                            width=pr.ggm_width,
                            widthStep=pr.ggm_widthStep,
                            shiftX=pr.ggm_shiftX,
                            angCon=pr.ggm_angCon,
                            skewAng=pr.ggm_skewness,
                            angZ=pr.ggm_rotAng,
                            dWorm=pr.ggm_dWorm,
                            nTWorm=pr.ggm_nTWorm,
                            name=nm,
                            c=pr.ggm_c,
                            tw=pr.ggm_tw,
                            fill_holes=pr.ggm_fill_holes,
                            diamHole=pr.ggm_diam_hole,
                            isHerringbone=pr.ggm_isHerringbone)        
        if pr.ggm_Type == 'ggm_external':
            mesh["ggm_External_Type"] = pr.ggm_External_Type        
        mesh["ggm_tw"] = pr.ggm_tw
        mesh["ggm_bStep"] = pr.ggm_bStep
        mesh["ggm_tStep"] = pr.ggm_tStep        
        mesh["ggm_c"] = pr.ggm_c
        mesh["ggm_diam_hole"] = pr.ggm_diam_hole
        mesh["ggm_width"] = pr.ggm_width
        mesh["ggm_widthStep"] = pr.ggm_widthStep
        mesh["ggm_driver"] = pr.ggm_driver
        mesh["ggm_evolvStep"] = pr.ggm_evolvStep
        mesh["ggm_filletCurveStep"] = pr.ggm_filletCurveStep
        mesh["ggm_fill_holes"] = pr.ggm_fill_holes
        mesh["ggm_rotAng"] = pr.ggm_rotAng
        mesh["ggm_skewness"] = pr.ggm_skewness
        if pr.ggm_External_Type != 'ggm_ext_bevel':
            mesh["ggm_dRef"] = GearFuncs.getRefDiam(pr.ggm_module, pr.ggm_nTeeth) + 2 * pr.ggm_shiftX
            mesh["ggm_isHerringbone"] = pr.ggm_isHerringbone
        else:
            mesh["ggm_angCon"] = pr.ggm_angCon
            mesh["ggm_angShaft"] = pr.ggm_angShaft
            mesh["ggm_nTeeth2"] = pr.ggm_nTeeth2
            mesh["ggm_isHerringbone"] = False

        if pr.ggm_Type == 'ggm_worm':
            mesh["ggm_dWorm"] = pr.ggm_dWorm
            mesh["ggm_nTWorm"] = pr.ggm_nTWorm
    elif pr.ggm_Type == 'ggm_external' and pr.ggm_External_Type == 'ggm_ext_rack':
        mesh = createRackMesh(m=pr.ggm_module,
                            nTeeth=pr.ggm_nTeeth,
                            prezureAngle=pr.ggm_angle,
                            width=pr.ggm_width,
                            widthStep=pr.ggm_widthStep,
                            shiftX=pr.ggm_shiftX,
                            skew=pr.ggm_skewness,
                            name=nm)
        mesh["ggm_External_Type"] = pr.ggm_External_Type
        mesh["ggm_skewness"] = pr.ggm_skewness
        mesh["ggm_width"] = pr.ggm_width
        mesh["ggm_widthStep"] = pr.ggm_widthStep
        mesh["ggm_isHerringbone"] = pr.ggm_isHerringbone
    else:
        mesh = createWormMesh(wType=tpG,
                                m=pr.ggm_module,
                                nTeeth=pr.ggm_nTeeth,
                                dWorm=pr.ggm_dWorm,
                                rezWorm=pr.ggm_rezWorm,
                                nTWorm=pr.ggm_nTWorm,
                                evolvStep=pr.ggm_evolvStep,
                                filletCurveStep=pr.ggm_filletCurveStep,
                                prezureAngle=pr.ggm_angle,
                                shiftX=pr.ggm_shiftX,
                                angZ=0.0,
                                name=nm,
                                c=pr.ggm_c)
        mesh["ggm_wType"] = pr.ggm_wType
        mesh["ggm_dWorm"] = pr.ggm_dWorm
        mesh["ggm_nTWorm"] = pr.ggm_nTWorm
    mesh["ggm_Type"] = pr.ggm_Type    
    mesh["ggm_change"] = False
    mesh["ggm_module"] = pr.ggm_module
    mesh["ggm_angle"] = pr.ggm_angle
    mesh["ggm_nTeeth"] = pr.ggm_nTeeth
    mesh["ggm_shiftX"] = pr.ggm_shiftX
    return mesh

def editMesh(mesh, context, rA = 0.0):
    if mesh["ggm_Type"] == 'ggm_internal':
        nm = 'InternalGear'
        tpG = mesh["ggm_Type"]
    elif mesh["ggm_Type"] == 'ggm_external':
        tpG = mesh["ggm_External_Type"]
        if mesh["ggm_External_Type"] == 'ggm_ext_rack':
            nm = 'Rack'
        elif mesh["ggm_External_Type"] == 'ggm_ext_spur':
            nm = 'SpurGear'
        elif mesh["ggm_External_Type"] == 'ggm_ext_herringbone':
            nm = 'HerringboneGear'
        elif mesh["ggm_External_Type"] == 'ggm_ext_bevel':
            nm = 'BevelGear'
        else:
            nm = 'WormGear'
    else:
        nm = 'WormGear'
        tpG = mesh["ggm_wType"]
    if mesh["ggm_Type"] == 'ggm_internal' or (mesh["ggm_Type"] == 'ggm_external' and mesh["ggm_External_Type"] != 'ggm_ext_rack' ):
        rez_mesh = createGearMesh(m=mesh["ggm_module"],
                            nTeeth=mesh["ggm_nTeeth"],
                            evolvStep=mesh["ggm_evolvStep"],
                            filletCurveStep=mesh["ggm_filletCurveStep"],
                            tStep=mesh["ggm_tStep"],
                            bStep=mesh["ggm_bStep"],
                            pressureAngle=mesh["ggm_angle"],
                            typeGear=tpG,
                            width=mesh["ggm_width"],
                            widthStep=mesh["ggm_widthStep"],
                            shiftX=mesh["ggm_shiftX"],
                            angCon=mesh["ggm_angCon"],
                            skewAng=mesh["ggm_skewness"],
                            angZ=rA,
                            dWorm=mesh["ggm_dWorm"],
                            nTWorm=mesh["ggm_nTWorm"],
                            name=mesh.name,
                            c=mesh["ggm_c"],
                            tw=mesh["ggm_tw"],
                            fill_holes=mesh["ggm_fill_holes"],
                            diamHole=mesh["ggm_diam_hole"])
        if mesh["ggm_External_Type"] != 'ggm_ext_bevel':
            mesh["dRef"] = GearFuncs.getRefDiam(mesh["ggm_module"], mesh["ggm_nTeeth"]) + 2 * mesh["ggm_shiftX"]
    elif mesh["ggm_Type"] == 'ggm_external' and mesh["ggm_External_Type"] == 'ggm_ext_rack':
        rez_mesh = createRackMesh(m=mesh["ggm_module"],
                            nTeeth=mesh["ggm_nTeeth"],
                            prezureAngle=mesh["ggm_angle"],
                            width=mesh["ggm_width"],
                            widthStep=mesh["ggm_widthStep"],
                            shiftX=mesh["ggm_shiftX"],
                            skew=mesh["ggm_skewness"],
                            name=mesh.name)
    else:
        rez_mesh = createWormMesh(wType=tpG,
                                m=mesh["ggm_module"],
                                nTeeth=mesh["ggm_nTeeth"],
                                dWorm=mesh["ggm_dWorm"],
                                rezWorm=mesh["ggm_rezWorm"],
                                nTWorm=mesh["ggm_nTWorm"],
                                evolvStep=mesh["ggm_evolvStep"],
                                filletCurveStep=mesh["ggm_filletCurveStep"],
                                prezureAngle=mesh["ggm_angle"],
                                shiftX=mesh["ggm_shiftX"],
                                angZ=0.0,
                                name=mesh.name,
                                c=mesh["ggm_c"])
    rez_mesh["ggm_change"] = False
    return rez_mesh