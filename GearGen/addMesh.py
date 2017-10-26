import bpy
import os
from builtins import range
from mathutils import Vector, Euler
from math import sin, cos, pi, atan, tan
from cmath import sqrt
from test._test_multiprocessing import sqr
from GearGen.GearFuncs import *
def sqr (num):
	return num*num
def createProfileVerts(m, diamHole, nTeeth, width, evolvStep, filletCurveStep, tStep, bStep, prezureAngle, typeGear, shiftX, angCon, H, skewAng, uMinEv, uMinFt, angZ, typeLay):
    
    verts = []
    verts1 = []
    verts1_2 = []
    verts2 = []
    verts3 = []
    tVerts3 = []
    tVerts = []
    DiamRef = getRefDiam(m, nTeeth) 
    baseDiam = getBaseDiam(m, nTeeth, prezureAngle)
    DiamT = getTipDiam(m, nTeeth)+shiftX*2
    if typeGear == '2':
        km = m
        DiamR = getRootDiam(m, nTeeth) + shiftX*2 + 0.5*m
        maxU = abs(sqrt(sqr(DiamT + 0.5*m)/(sqr(baseDiam))-1))
        Umin = abs((pi * m / 4 + m * tan(prezureAngle)) / (DiamRef / 2))
    else:
        km = 1.25*m
        DiamR = getRootDiam(m, nTeeth) + shiftX*2
        maxU = abs(sqrt(sqr(DiamT)/(sqr(baseDiam))-1))
        Umin = abs((pi * m / 4 + km * tan(prezureAngle)) / (DiamRef / 2))
    dX = km - shiftX
    l = abs(sqrt(sqr(dX) + sqr(pi*m/4+km*tan(prezureAngle))))    
      
        
    evolvList = []    
    k = 2*pi/nTeeth
    dU = (uMinFt - Umin)/filletCurveStep
    stepU1 = (maxU-uMinEv)/evolvStep
    for n in range(evolvStep+1):
        evolvList.append(n*stepU1 + uMinEv)
    dAng = 2*getEvolvAngle(DiamRef, m, nTeeth, prezureAngle) + 4*shiftX*tan(prezureAngle)/DiamRef
    midAng = k/4 + dAng/2
    ang = abs(atan(dX/(pi*m/4+km*tan(prezureAngle))))
    rAng = 2*pi/((tStep+bStep)*nTeeth)
    dH = 0.0
    dL = m/2
    if typeGear == '3':        
        dH = (dL + (DiamRef - DiamR)/2)*sin(angCon)
    if typeLay != 0:
        if typeGear != '2':
            for r in range((tStep+bStep)*nTeeth):
                v1 = Vector(((diamHole/2), 0, 0))
                v1.rotate(Euler((0.0, 0.0, rAng*(r - tStep/2)), 'XYZ'))
                v1[2] = H - dH
                v1.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                verts1.append(v1)
            for r in range((tStep+bStep)*nTeeth):
                v1 = Vector(((DiamR/2-dL), 0, 0))
                v1.rotate(Euler((0.0, 0.0, rAng*(r - tStep/2)), 'XYZ'))
                if typeGear == '3':
                    v1 = rotTeeth(DiamRef+2*shiftX, v1, angCon)
                v1[2] = H - dH
                v1.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                verts1_2.append(v1)
        else:
            for r in range((tStep+bStep)*nTeeth):
                v1 = Vector(((diamHole/2), 0, 0))
                v1.rotate(Euler((0.0, 0.0, (r + tStep/2 ) * rAng), 'XYZ'))
                v1[2] = H - dH
                v1.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                verts1.append(v1)
            for r in range((tStep+bStep)*nTeeth):
                v1 = Vector(((DiamT/2+dL), 0, 0))
                v1.rotate(Euler((0.0, 0.0, (r + tStep/2 ) * rAng), 'XYZ'))
                if typeGear == '3':
                    v1 = rotTeeth(DiamRef+2*shiftX, v1, angCon)
                v1[2] = H - dH
                v1.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                verts1_2.append(v1)
        
    
    for i in range(nTeeth*2):
        v0 = Vector((5.0, 0.0, 0.0))
        v0.rotate(Euler((0.0, 0.0, k*i/2), 'XYZ'))
        if (i % 2) == 0:
            ###############################################################
            
            for u2 in range(filletCurveStep):
                u2 = Umin + dU*u2
                if ang < pi/2 - u2:
                    a1 = abs(ang - pi/2 + u2)
                else:
                    a1 = -abs(ang - pi/2 + u2)
                rotVec2 = i*k/2+dAng/2 + k/4
                vertEvolv = getVertEvolv(DiamRef, u2)
                v3 = Vector((vertEvolv[0] - l*cos(a1), - vertEvolv[1] - l*sin(a1),0))
                v3.rotate(Euler((0.0, 0.0, rotVec2 - midAng), 'XYZ'))
                vA2 = 2*v3.angle(v0)/tStep
                if typeLay != 0:
                    for tS in range(tStep-1):
                        v2 = Vector((v3[0], v3[1], 0.0))
                        v2.rotate(Euler((0.0, 0.0, vA2*(tS + 1)), 'XYZ'))
                        if typeGear == '3':
                            v2 = rotTeeth(DiamRef+2*shiftX, v2, angCon)
                        v2[2] = v2[2] + H
                        if typeGear != '2':
                            v2.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                            verts2.append(Vector((v2[0],v2[1],v2[2])))
                        
                if typeGear == '3':
                    v3 = rotTeeth(DiamRef+2*shiftX, v3, angCon)
                v3[2] = v3[2] + H
                v3.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                if i == 0:
                    tVerts3.append(v3)
                else:
                    verts3.append(v3)
            ###############################################################
            for u in evolvList:
                rotVec1 = i*k/2
                vertEvolv = getVertEvolv(baseDiam, u)
                v3 = Vector((vertEvolv[0], vertEvolv[1], 0))
                v3.rotate(Euler((0.0, 0.0,rotVec1 - midAng), 'XYZ'))
                vA2 = 2*v3.angle(v0)/tStep
                
                if u == evolvList[-1]:
                    for tS in range(tStep-1):
                        v2 = Vector((v3[0], v3[1], 0.0))
                        v2.rotate(Euler((0.0, 0.0, vA2*(tS+1)), 'XYZ'))
                        if typeGear == '3':
                            v2 = rotTeeth(DiamRef+2*shiftX, v2, angCon)
                        v2[2] = v2[2] + H
                        v2.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                        tVerts.append(Vector((v2[0],v2[1],v2[2])))
                if typeLay != 0:
                    for tS in range(tStep-1):
                        v2 = Vector((v3[0], v3[1], 0.0))
                        v2.rotate(Euler((0.0, 0.0, vA2*(tS+1)), 'XYZ'))
                        if typeGear == '3':
                            v2 = rotTeeth(DiamRef+2*shiftX, v2, angCon)
                        v2[2] = v2[2] + H
                        if u != evolvList[-1] and typeGear != '2':
                            v2.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                            verts2.append(Vector((v2[0],v2[1],v2[2])))
                
                if typeGear == '3':
                    v3 = rotTeeth(DiamRef+2*shiftX, v3, angCon)
                v3[2] = v3[2] + H
                v3.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                if i == 0:
                    tVerts3.append(v3)
                    tVerts3.extend(tVerts)
                else:
                    verts3.append(v3)
                    verts3.extend(tVerts)
                tVerts.clear()
                                
        else:
            for u in reversed(evolvList):
                rotVec1 = i*k/2+dAng
                vertEvolv = getVertEvolv(baseDiam, u)
                v3 = Vector((vertEvolv[0], - vertEvolv[1], 0))
                v3.rotate(Euler((0.0, 0.0,rotVec1 - midAng), 'XYZ'))
                vA2 = 2*v3.angle(v0)/bStep
                if typeGear == '2':
                    for tS in range(bStep-1):
                        v2 = Vector((v3[0], v3[1], 0.0))
                        v2.rotate(Euler((0.0, 0.0, vA2*(tS+1)), 'XYZ'))
                        if typeGear == '3':
                            v2 = rotTeeth(DiamRef+2*shiftX, v2, angCon)
                        v2[2] = v2[2] + H
                        v2.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                        verts2.append(Vector((v2[0],v2[1],v2[2])))
                if typeGear == '3':
                    v3 = rotTeeth(DiamRef+2*shiftX, v3, angCon)
                v3[2] = v3[2] + H #+ dH
                v3.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                verts3.append(v3)
                verts3.extend(tVerts)
                tVerts.clear()
            #############################################################
            for u2 in reversed(range(filletCurveStep)):
                j = u2
                u2 = Umin + dU*u2
                if ang < pi/2 - u2:
                    a1 = abs(ang - pi/2 + u2)
                else:
                    a1 = -abs(ang - pi/2 + u2)
                vertEvolv = getVertEvolv(DiamRef, u2)
                v3 = Vector((vertEvolv[0] - l*cos(a1),  vertEvolv[1] + l*sin(a1),0))
                rotVec2 = i*k/2+dAng/2- k/4
                v3.rotate(Euler((0.0, 0.0,rotVec2 - midAng), 'XYZ'))
                vA2 = 2*v3.angle(v0)/bStep
                
                for tS in range(bStep-1):
                    v2 = Vector((v3[0], v3[1], 0.0))
                    v2.rotate(Euler((0.0, 0.0, vA2*(tS+1)), 'XYZ'))
                    if typeGear == '3':
                        v2 = rotTeeth(DiamRef+2*shiftX, v2, angCon)
                    v2[2] = v2[2] + H
                    v2.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                    if j == 0:
                        tVerts.append(Vector((v2[0],v2[1],v2[2])))
                    elif typeGear == '2':
                        verts2.append(Vector((v2[0],v2[1],v2[2])))
                if typeGear == '3':
                    v3 = rotTeeth(DiamRef+2*shiftX, v3, angCon)
                v3[2] = v3[2] + H
                v3.rotate(Euler((0.0, 0.0, angZ + skewAng), 'XYZ'))
                verts3.append(v3)
                verts3.extend(tVerts)
                tVerts.clear()
    
        
    if typeLay == 0:
        if typeGear == '2':
            verts.extend(verts3)
            verts.extend(tVerts3)
        else:
            verts.extend(tVerts3)
            verts.extend(verts3)
    if typeLay == 1:
        verts.extend(verts1)
        verts.extend(verts1_2)
        verts.extend(verts2)
        if typeGear == '2':
            verts.extend(verts3)
            verts.extend(tVerts3)
        else:
            verts.extend(tVerts3)
            verts.extend(verts3)
    if typeLay == 2:
        if typeGear == '2':
            verts.extend(verts3)
            verts.extend(tVerts3)
        else:
            verts.extend(tVerts3)
            verts.extend(verts3)
        verts.extend(verts2)
        verts.extend(verts1_2)
        verts.extend(verts1)
    return verts
        
def createGearMesh(m, nTeeth, evolvStep, filletCurveStep, tStep, bStep, prezureAngle, typeGear, width, widthStep, shiftX, angCon, skewAng, angZ=0.0,  name = "GearGen"): 
    os.system("cls")
    VEF = ([],[],[])
    if typeGear == '2':
        topSt = bStep
        botSt = tStep
    else:
        topSt = tStep
        botSt = bStep
    nVerts1 = (botSt + topSt)*nTeeth
    curveStep = filletCurveStep + evolvStep
    nVerts2Segm = (curveStep)*(topSt-1)
    nVerts2 = nVerts2Segm*nTeeth
    nVerts3Segm = (curveStep +1)*2 + topSt + botSt - 2
    nVerts3 = nVerts3Segm*nTeeth
    radRef = getRefDiam(m, nTeeth)/2 + shiftX    
    origZ = getOriginZ(m, nTeeth, typeGear, shiftX, angCon)
    if typeGear == '3':
        ang = angCon
        if width >= radRef/sin(ang) - m:
            width = radRef/sin(ang) - m
    else:
        ang = 0.0
    if typeGear == '2' or typeGear == '4':
        widthStep = widthStep*2
    nVerts = 4*nVerts1 + 2*nVerts2 + nVerts3*(widthStep+1)
    prBase = width*sin(ang)
    mPart = m*(prBase/radRef)/widthStep
    HPart = (width/widthStep)*cos(ang)
    shiftPart = shiftX*(prBase/radRef)/widthStep
    if typeGear != '2':
        diamHole = getRootDiam(m*(1 - prBase/radRef), nTeeth) - 2*m + 2*shiftX
    else:
        diamHole = getTipDiam(m*(1 - prBase/radRef), nTeeth) + 2*m + 2*shiftX
    skewPart = skewAng/widthStep
    u = getCrossEvolv2(m, nTeeth, prezureAngle, shiftX, typeGear)
    ###################################################################################
    g1 = createProfileVerts(m, diamHole, nTeeth, width, evolvStep, filletCurveStep, tStep, bStep, prezureAngle, typeGear, shiftX, ang, -origZ, 0.0, u[0], u[1], angZ, 1)
    VEF[0].extend(g1)
    
    if typeGear == '2' or typeGear == '4':
        for n in range(1, widthStep + 1):
            if n < widthStep/2:
                g2 = createProfileVerts(m-n*mPart, diamHole, nTeeth, width, evolvStep, filletCurveStep, tStep, bStep, prezureAngle, typeGear, shiftX - n*shiftPart, ang, HPart*n - origZ, skewPart*n, u[0], u[1], angZ, 0)
                VEF[0].extend(g2)
            else:
                if n != widthStep:
                    g2 = createProfileVerts(m-n*mPart, diamHole, nTeeth, width, evolvStep, filletCurveStep, tStep, bStep, prezureAngle, typeGear, shiftX - n*shiftPart, ang, HPart*n - origZ,skewAng - skewPart*n, u[0], u[1], angZ, 0)
                else:
                    g2 = createProfileVerts(m-n*mPart, diamHole, nTeeth, width, evolvStep, filletCurveStep, tStep, bStep, prezureAngle, typeGear, shiftX - n*shiftPart, ang, HPart*n - origZ,skewAng - skewPart*n, u[0], u[1], angZ, 2)
                VEF[0].extend(g2)
    else:
        for n in range(1, widthStep + 1):
            if n != widthStep:
                g2 = createProfileVerts(m-n*mPart, diamHole, nTeeth, width, evolvStep, filletCurveStep, tStep, bStep, prezureAngle, typeGear, shiftX - n*shiftPart, ang, HPart*n - origZ, skewPart*n, u[0], u[1], angZ, 0)
            else:
                g2 = createProfileVerts(m-n*mPart, diamHole, nTeeth, width, evolvStep, filletCurveStep, tStep, bStep, prezureAngle, typeGear, shiftX - n*shiftPart, ang, HPart*n - origZ, skewPart*n, u[0], u[1], angZ, 2)
            VEF[0].extend(g2)
   
    
    """ building poligons for caps """
    
    for p in range(nVerts1-1):
        v1 = p
        v1_2 = v1 + nVerts - nVerts1
        v2 = p + 1
        v2_2 = v2 + nVerts - nVerts1
        v3 = v2 + nVerts1
        v3_2 = v3+ nVerts - 3*nVerts1
        v4 = p + nVerts1
        v4_2 = v4+ nVerts -3*nVerts1
        if typeGear == '2':
            VEF[2].append((v1, v4, v3, v2))
            VEF[2].append((v1_2,v2_2,v3_2,v4_2))
        else:
            VEF[2].append((v1, v2, v3, v4))
            VEF[2].append((v1_2,v4_2,v3_2,v2_2))
    v1 = nVerts1-1
    v1_2 = nVerts - 1
    v2 = 0
    v2_2 = nVerts - nVerts1
    v3 = nVerts1
    v3_2 = nVerts - 2*nVerts1
    v4 = 2*nVerts1-1
    v4_2 = nVerts - nVerts1 - 1
    if typeGear == '2':
        VEF[2].append((v1, v4, v3, v2))
        VEF[2].append((v1_2,v2_2,v3_2,v4_2))
    else:
        VEF[2].append((v1, v2, v3, v4))
        VEF[2].append((v1_2,v4_2,v3_2,v2_2))
    for p in range(nTeeth*2):
        if (p % 2) == 0:
            if topSt != 1:
                for pT in range(topSt):
                    v1 = (nTeeth + p/2)*(topSt + botSt) + pT
                    v1_2 = v1 + nVerts - 3*nVerts1
                    if pT == 0 or (pT != 0 and pT != (topSt - 1)):
                        v2 = v1 + 1
                        v2_2 = v1_2 + 1
                        v3 = nVerts1*2 + nVerts2Segm*p/2 + pT
                        v3_2 = v3 + nVerts2 + nVerts3*(widthStep+1)
                        if pT == 0:
                            v4 = nVerts1*2 + nVerts2 + nVerts3Segm*p/2 + pT
                            v4_2 = v4 + nVerts3*widthStep
                        if pT != 0 and pT != (topSt - 1):
                            v4 = v3 - 1
                            v4_2 = v3_2 - 1
                    if pT == (topSt - 1):
                        v2 = v1 + 1
                        v2_2 = v1_2 + 1
                        v3 = nVerts1*2 + nVerts2 + nVerts3Segm*(p/2 + 1) - botSt
                        v3_2 = v3 + + nVerts3*widthStep
                        v4 = nVerts1*2 + nVerts2Segm*p/2 + pT - 1
                        v4_2 = v4 + nVerts2 + nVerts3*(widthStep+1)                    
                    if typeGear == '2':
                        VEF[2].append((v1, v4, v3, v2))
                        VEF[2].append((v1_2,v2_2,v3_2,v4_2))
                    else:
                        VEF[2].append((v1, v2, v3, v4))
                        VEF[2].append((v1_2,v4_2,v3_2,v2_2))
            else:
                v1 = nVerts1 + (botSt+1)*p/2
                v1_2 = v1 + nVerts -3*nVerts1
                v2 = v1 + 1
                v2_2 = v1_2 + 1
                v4 = nVerts1*2 + nVerts3Segm*p/2
                v4_2 = v4 + nVerts3*widthStep
                v3 = v4 + nVerts3Segm - botSt
                v3_2 = v4_2 + nVerts3Segm - botSt                
                if typeGear == '2':
                    VEF[2].append((v1, v4, v3, v2))
                    VEF[2].append((v1_2,v2_2,v3_2,v4_2))
                else:
                    VEF[2].append((v1, v2, v3, v4))
                    VEF[2].append((v1_2,v4_2,v3_2,v2_2))
                
        else:
            for pB in range(botSt):
                v1 = nVerts1 + topSt + (topSt + botSt)*(p-1)/2 + pB
                v1_2 = v1 + nVerts1 + 2*nVerts2 + nVerts3*(widthStep + 1)
                v4 = nVerts1*2 + nVerts2 + nVerts3Segm*((p-1)/2 + 1) - botSt + pB
                v4_2 = v4 + nVerts3*widthStep
                if p != (nTeeth*2 - 1) or pB != (botSt - 1):
                    v2 = nVerts1 + topSt + (topSt + botSt)*(p-1)/2 + pB + 1
                    v2_2 = v2 + nVerts -3*nVerts1
                    v3 = v4 + 1
                    v3_2 = v4_2 + 1
                else:
                    v2 = nVerts1
                    v2_2 = v2 + nVerts -3*nVerts1
                    v3 = nVerts1*2 + nVerts2
                    v3_2 = v3 + nVerts3*widthStep
                
                if typeGear == '2':
                    VEF[2].append((v1, v4, v3, v2))
                    VEF[2].append((v1_2,v2_2,v3_2,v4_2))
                else:
                    VEF[2].append((v1, v2, v3, v4))
                    VEF[2].append((v1_2,v4_2,v3_2,v2_2))
    for nT in range(nTeeth):
        if topSt != 1:
            for eS in range(curveStep):            
                for tS in range(topSt):
                    if tS == 0 and eS != (curveStep - 1):
                        v1 = nVerts1*2 + nVerts2 + nVerts3Segm*nT + eS
                        v1_2 = v1 + nVerts3*widthStep
                        v2 = nVerts1*2 + nVerts2Segm*nT + (topSt - 1)*eS
                        v2_2 = v2 + nVerts3*(widthStep+1) + nVerts2
                        v3 = v2 + topSt - 1
                        v3_2 = v2_2 + topSt - 1
                        v4 = v1 + 1
                        v4_2 = v1_2 + 1
                    if tS !=0 and eS != (curveStep - 1) and tS != (topSt-1):
                        v1 = nVerts1*2 + nVerts2Segm*nT + (topSt - 1)*eS + tS - 1
                        v1_2 = v1 + nVerts3*(widthStep+1) + nVerts2
                        v2 = v1 + 1
                        v2_2 = v1_2 + 1
                        v3 = nVerts1*2 + nVerts2Segm*nT + (topSt - 1)*(eS+1) + tS
                        v3_2 = v3 + nVerts3*(widthStep+1) + nVerts2
                        v4 = v3 - 1
                        v4_2 = v3_2 - 1
                    if tS == (topSt-1) and eS != (curveStep - 1):
                        v1 = nVerts1*2 + nVerts2Segm*nT + (topSt - 1)*eS + tS - 1
                        v1_2 = v1 + nVerts3*(widthStep+1) + nVerts2
                        v2 = nVerts1*2 + nVerts2 + nVerts3Segm*(nT+1) - eS - botSt
                        v2_2 = v2 + nVerts3*widthStep
                        v3 = v2 - 1
                        v3_2 = v2_2 - 1
                        v4 = v1 + topSt - 1
                        v4_2 = v1_2 + topSt - 1
                    if eS == (curveStep - 1) and tS == 0:
                        v1 = nVerts1*2 + nVerts2 + nVerts3Segm*nT + eS + tS
                        v1_2 = v1 + nVerts3*widthStep
                        v2 = nVerts1*2 + nVerts2Segm*nT + (topSt - 1)*eS + tS
                        v2_2 = v2 + nVerts3*(widthStep+1) + nVerts2
                        v3 = v1 + 2
                        v3_2 = v1_2 + 2
                        v4 = v1 + 1
                        v4_2 = v1_2 + 1
                    if eS == (curveStep - 1) and tS != 0 and tS != (topSt - 1):
                        v1 = nVerts1*2 + nVerts2Segm*nT + (topSt - 1)*eS + tS - 1
                        v1_2 = v1 + nVerts3*(widthStep+1) + nVerts2
                        v2 = v1 + 1
                        v2_2 = v1_2 + 1
                        v3 = nVerts1*2 + nVerts2 + nVerts3Segm*nT + eS + tS + 2
                        v3_2 = v3 + nVerts3*widthStep
                        v4 = v3 - 1
                        v4_2 = v3_2 - 1
                    if eS == (curveStep - 1) and tS != 0 and tS == (topSt - 1):
                        v1 = nVerts1*2 + nVerts2Segm*nT + (topSt - 1)*eS + tS - 1
                        v1_2 = v1 + nVerts3*(widthStep+1) + nVerts2
                        v2 = nVerts1*2 + nVerts2 + nVerts3Segm*nT + eS + tS + 3
                        v2_2 = v2 + nVerts3*widthStep
                        v3 = v2 - 1
                        v3_2 = v2_2 - 1
                        v4 = v2 - 2
                        v4_2 = v2_2 - 2
                    if typeGear == '2':
                        VEF[2].append((v1, v4, v3, v2))
                        VEF[2].append((v1_2,v2_2,v3_2,v4_2))
                    else:
                        VEF[2].append((v1, v2, v3, v4))
                        VEF[2].append((v1_2,v4_2,v3_2,v2_2))
        else:
            for eS in range(curveStep):
                v1 = nVerts1*2 + nT*nVerts3Segm + eS
                v1_2 = v1 + nVerts3*widthStep
                v2 = nVerts1*2 + (nT+1)*nVerts3Segm - botSt - eS
                v2_2 = v2 + nVerts3*widthStep
                v3 = v2 - 1
                v3_2 = v2_2 - 1
                v4 = v1 + 1
                v4_2 = v1_2 + 1     
                if typeGear == '2':
                    VEF[2].append((v1, v4, v3, v2))
                    VEF[2].append((v1_2,v2_2,v3_2,v4_2))
                else:
                    VEF[2].append((v1, v2, v3, v4))
                    VEF[2].append((v1_2,v4_2,v3_2,v2_2))
               
    
    """building poligons for side surface"""
    for p in range(nVerts3*widthStep):
        v1 = nVerts1*2 + nVerts2 + p        
        if (p + 1) % nVerts3 != 0:
            v2 = v1 + 1
            v3 = v2 + nVerts3  
            v4 = v3 - 1
        else:
            v2 = v1 - nVerts3 + 1
            v3 = v1 + 1
            v4 = v1 + nVerts3 
        if typeGear == '2':
            VEF[2].append((v1, v4, v3, v2))
        else:
            VEF[2].append((v1, v2, v3, v4))
        
    mesh = bpy.data.meshes.new(name)    
    mesh.from_pydata(VEF[0],VEF[1], VEF[2])
    mesh.update()
    return mesh
