import bpy
import numpy as np
from builtins import range
from mathutils import Vector, Euler
from math import sin, radians, cos, pi, atan
from bpy.props import IntProperty, FloatProperty, EnumProperty, BoolProperty
from . import addMesh


class AddSpurGear(bpy.types.Operator):
    """Add a gear mesh"""
    bl_idname = "mesh.primitive_spur_gear_add"
    bl_label = "Add_Spur_Gear"
    bl_options = {'REGISTER', 'UNDO'}

    nTeeth : IntProperty(name="Z",
                         description="Number of teeth",
                         min=6,
                         max=265,
                         options={'SKIP_SAVE'},
                         default=12)
    module : FloatProperty(name="Module",
                           description="Module of the gear",
                           min=0.05,
                           max=100.0,
                           unit='LENGTH',
                           default=0.2)
    width : FloatProperty(name="Width, thickness of gear",
                          description="Width of the gear",
                          min=0.1,
                          max=100.0,
                          unit='LENGTH',
                          default=0.5)
    diam_hole : FloatProperty(name="Hole Diameter",
                          description="Diameter of hole",
                          min=0.0,
                          unit='LENGTH',
                          default= 1.0)
    widthStep : IntProperty(name="Width Step",
                            description="Definition of the width of teeth",
                            min=1,
                            max=30,
                            default=1)
    skewness : FloatProperty(name="Skewness",
                             description="Skewness of the teeth",
                             min=radians(-90),
                             max=radians(90),
                             options={'SKIP_SAVE'},
                             unit='ROTATION',
                             default=0.0)
    evolvStep : IntProperty(name="Def. of evolute",
                            description="Definition of the evolute",
                            min=3,
                            max=30,
                            default=3)
    filletCurveStep : IntProperty(name="Def. of fillet curve",
                                  description="Definition of the fillet curve",
                                  min=3,
                                  max=30,
                                  default=3)
    tStep : IntProperty(name="Def. of top land",
                        description="Definition of the top land",
                        min=1,
                        max=30,
                        options={'SKIP_SAVE'},
                        default=3)
    bStep : IntProperty(name="Def. of bottom land",
                        description="Definition of the bottom land",
                        min=1,
                        max=30,
                        options={'SKIP_SAVE'},
                        default=1)
    shiftX : FloatProperty(name="ShiftX",
                           description="Shift of the profile",
                           min=-4.000,
                           max=4.000,
                           precision=3,
                           options={'SKIP_SAVE'},
                           step=0.1,
                           unit='LENGTH',
                           default=0.000)
    c : FloatProperty(name="C",
                      description="Tip and Root Clearance",
                      min=0.0,
                      max=1.0,
                      precision=2,
                      options={'SKIP_SAVE'},
                      step=0.01,
                      unit='LENGTH',
                      default=0.25)
    angle : FloatProperty(name="Pressure Angle",
                          description="Pressure angle, skewness of tooth tip",
                          min=0.0,
                          max=radians(45.0),
                          unit='ROTATION',
                          default=radians(20.0))
    rotAng : FloatProperty(name="Rotation Angle",
                           description="Rotation Angle Of Gear",
                           options={'SKIP_SAVE'},
                           min=0.0,
                           max=radians(360.0),
                           unit='ROTATION',
                           default=radians(0.0))
    driver : BoolProperty(name="Add Driver",
                          description="Add Driver to Gear",
                          options={'SKIP_SAVE'},
                          default=False)
    fill_holes : BoolProperty(name="Fill Holes",
                          description="Fill Holes",
                          options={'SKIP_SAVE'},
                          default=False)
    tw : FloatProperty(name="Tooth Width",
                           description="Width of Tooth",
                           min=0.0,
                           max=1.0,
                           unit='NONE',
                           default=1.0)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Main Properties")
        col = box.column(align=True)
        col.prop(self, 'nTeeth')
        col.prop(self, 'module')
        col.prop(self, 'c')
        col.prop(self, 'angle')
        col.prop(self, 'shiftX')
        col.prop(self, 'tw')
        col.prop(self, 'width')
        col.prop(self, 'diam_hole')
        box = layout.box()
        box.label(text="Mesh Properties")
        col = box.column(align=True)        
        col.prop(self, 'widthStep')
        col.prop(self, 'evolvStep')
        col.prop(self, 'filletCurveStep')
        col.prop(self, 'tStep')
        col.prop(self, 'bStep')
        col.prop(self, 'fill_holes')
        box = layout.box()
        box.label(text="Deformations")
        col = box.column(align=True)
        col.prop(self, 'skewness')
        col.prop(self, 'rotAng')
        col = layout.box()
        col.prop(self, 'driver')

    def execute(self, context):
        if bpy.context.selected_objects == []:
            mesh = addMesh.createGearMesh(typeGear='spur',
                                          m=self.module,
                                          nTeeth=self.nTeeth,
                                          evolvStep=self.evolvStep,
                                          filletCurveStep=self.filletCurveStep,
                                          tStep=self.tStep,
                                          bStep=self.bStep,
                                          pressureAngle=self.angle,
                                          shiftX=self.shiftX,
                                          width=self.width,
                                          widthStep=self.widthStep,
                                          skewAng=self.skewness,
                                          angCon=0.0,
                                          angZ=self.rotAng,
                                          name="SpurGear",
                                          c=self.c,
                                          tw=self.tw,
                                          fill_holes=self.fill_holes,
                                          diamHole=self.diam_hole)
            base = addMesh.GearFuncs.create_mesh_obj(context, mesh)
            matr = np.array([1, 2, 3])
            print(matr)
            ob = bpy.context.active_object
            ob['type'] = "spur"
            ob['module'] = self.module
            ob['nTeeth'] = self.nTeeth
            ob['dRef'] = addMesh.GearFuncs.getRefDiam(self.module, self.nTeeth) + 2 * self.shiftX
            ob['skewAng'] = self.skewness
            ob['rotAng'] = self.rotAng % (2 * pi / self.nTeeth)
            ob['shiftX'] = self.shiftX
        else:
            if "type" in bpy.context.selected_objects[0]:
                if bpy.context.selected_objects.__len__() == 1 and bpy.context.selected_objects[0]['type'] == "spur":
                    ob1 = bpy.context.selected_objects[0]
                    r = (self.module * ob1['nTeeth'] + self.module * self.nTeeth) / 2 + self.shiftX + ob1['shiftX']
                    rA = pi - pi / self.nTeeth + self.rotAng * ob1['nTeeth'] / self.nTeeth + self.rotAng - ob1['rotAng'] * \
                         ob1['nTeeth'] / self.nTeeth
                    mesh2 = addMesh.createGearMesh(typeGear='spur',
                                                   m=self.module,
                                                   nTeeth=self.nTeeth,
                                                   evolvStep=self.evolvStep,
                                                   filletCurveStep=self.filletCurveStep,
                                                   tStep=self.tStep,
                                                   bStep=self.bStep,
                                                   pressureAngle=self.angle,
                                                   shiftX=self.shiftX,
                                                   width=self.width,
                                                   widthStep=self.widthStep,
                                                   skewAng=-ob1['skewAng'] * (ob1['nTeeth'] / self.nTeeth),
                                                   angCon=0.0,
                                                   angZ=rA,
                                                   c=self.c,
                                                   tw=self.tw,
                                                   fill_holes=self.fill_holes,
                                                   diamHole=self.diam_hole)
                    base2 = addMesh.GearFuncs.create_mesh_obj(context, mesh2)
                    ob2 = bpy.context.active_object
                    ob2.location.x = ob1.location[0] + r * cos(self.rotAng)
                    ob2.location.y = ob1.location[1] + r * sin(self.rotAng)
                    ob2.location.z = ob1.location[2]
                    ob2['type'] = "spur"
                    ob2['module'] = self.module
                    ob2['nTeeth'] = self.nTeeth
                    ob2['dRef'] = addMesh.GearFuncs.getRefDiam(self.module, self.nTeeth) + 2 * self.shiftX
                    ob2['skewAng'] = -ob1['skewAng'] * (ob1['nTeeth'] / self.nTeeth)
                    ob2['rotAng'] = rA % (2 * pi / self.nTeeth)
                    ob2['shiftX'] = self.shiftX
                    if self.driver == True:
                        obDrive = ob2.driver_add("rotation_euler", 2)
                        obDrive.driver.type = 'SCRIPTED'
                        rotvar = obDrive.driver.variables.new()
                        rotvar.name = 'rotSpur'
                        rotvar.type = 'TRANSFORMS'
                        rotvar.targets[0].transform_type = 'ROT_Z'
                        rotvar.targets[0].transform_space = 'WORLD_SPACE'
                        rotvar.targets[0].id = ob1
                        obDrive.driver.expression = "-rotSpur/" + str(self.nTeeth/ob1['nTeeth'])
                elif bpy.context.selected_objects.__len__() == 1 and bpy.context.selected_objects[0]['type'] == "rack":
                    ob1 = bpy.context.selected_objects[0]
                    r = self.module * self.nTeeth / 2 + self.shiftX
                    rA = pi - pi / self.nTeeth + self.rotAng * ob1['nTeeth'] / self.nTeeth + self.rotAng - ob1['rotAng'] * \
                         ob1['nTeeth'] / self.nTeeth
                    mesh2 = addMesh.createGearMesh(typeGear='spur',
                                                   m=self.module,
                                                   nTeeth=self.nTeeth,
                                                   evolvStep=self.evolvStep,
                                                   filletCurveStep=self.filletCurveStep,
                                                   tStep=self.tStep,
                                                   bStep=self.bStep,
                                                   pressureAngle=self.angle,
                                                   shiftX=self.shiftX,
                                                   width=self.width,
                                                   widthStep=self.widthStep,
                                                   skewAng=-self.skewness * (ob1['nTeeth'] / self.nTeeth),
                                                   angCon=0.0,
                                                   angZ=-self.rotAng,
                                                   c=self.c,
                                                   tw=self.tw,
                                                   fill_holes=self.fill_holes,
                                                   diamHole=self.diam_hole)
                    base2 = addMesh.GearFuncs.create_mesh_obj(context, mesh2)
                    ob2 = bpy.context.active_object
                    ob2.location.x = ob1.location[0] - r
                    ob2.location.y = ob1.location[1] + self.rotAng*addMesh.GearFuncs.getRefDiam(self.module, self.nTeeth)/2
                    ob2.location.z = ob1.location[2]
                    ob2['type'] = "spur"
                    ob2['module'] = self.module
                    ob2['nTeeth'] = self.nTeeth
                    ob2['dRef'] = addMesh.GearFuncs.getRefDiam(self.module, self.nTeeth) + 2 * self.shiftX
                    ob2['skewAng'] = -self.skewness * (ob1['nTeeth'] / self.nTeeth)
                    ob2['rotAng'] = 0
                    ob2['shiftX'] = self.shiftX
                else:
                    self.report({'INFO'}, "Select one spur gear!")
            else:
                self.report({'INFO'}, "Select object created by GearGenMaster!")
        return {'FINISHED'}
        # ////////////////////////////////////////////////////////////////////////////////


class AddRack(bpy.types.Operator):
    """Add a rack"""
    bl_idname = "mesh.primitive_rack_add"
    bl_label = "Add_Rack"
    bl_options = {'REGISTER', 'UNDO'}

    nTeeth : IntProperty(name="Z",
                         description="Number of teeth",
                         min=6,
                         max=265,
                         options={'SKIP_SAVE'},
                         default=12)
    module : FloatProperty(name="Module",
                           description="Module of the gear",
                           min=0.05,
                           max=100.0,
                           unit='LENGTH',
                           default=0.2)
    width : FloatProperty(name="Width, thickness of gear",
                          description="Width of the gear",
                          min=0.1,
                          max=100.0,
                          unit='LENGTH',
                          default=0.5)
    widthStep : IntProperty(name="Width Step",
                            description="Definition of the width of teeth",
                            min=1,
                            max=30,
                            default=1)
    skewness : FloatProperty(name="Skewness",
                             description="Skewness of the teeth",
                             min=radians(-90),
                             max=radians(90),
                             options={'SKIP_SAVE'},
                             unit='LENGTH',
                             default=0.0)
    shiftX : FloatProperty(name="ShiftX",
                           description="Shift of the profile",
                           min=-4.000,
                           max=4.000,
                           precision=3,
                           options={'SKIP_SAVE'},
                           step=0.1,
                           unit='LENGTH',
                           default=0.000)
    c : FloatProperty(name="C",
                      description="Tip and Root Clearance",
                      min=0.0,
                      max=1.0,
                      precision=2,
                      options={'SKIP_SAVE'},
                      step=0.01,
                      unit='LENGTH',
                      default=0.25)
    angle : FloatProperty(name="Pressure Angle",
                          description="Pressure angle, skewness of tooth tip",
                          min=0.0,
                          max=radians(45.0),
                          unit='ROTATION',
                          default=radians(20.0))
    rotAng : FloatProperty(name="Rotation Angle",
                           description="Rotation Angle Of Gear",
                           options={'SKIP_SAVE'},
                           min=0.0,
                           max=radians(360.0),
                           unit='ROTATION',
                           default=radians(0.0))

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        box.prop(self, 'nTeeth')
        box.prop(self, 'shiftX')
        box.prop(self, 'c')
        col = layout.column(align=True)
        col.prop(self, 'module')
        col.prop(self, 'width')
        col.prop(self, 'widthStep')

        box = layout.box()
        box.prop(self, 'angle')
        box.prop(self, 'skewness')
        box = layout.box()
        box.prop(self, 'rotAng')

    def execute(self, context):
        if not bpy.context.selected_objects:
            mesh = addMesh.createRackMesh(m=self.module,
                                          nTeeth=self.nTeeth,
                                          prezureAngle=self.angle,
                                          shiftX=self.shiftX,
                                          width=self.width,
                                          widthStep=self.widthStep,
                                          skew=self.skewness,
                                          name="Rack")
            base = addMesh.GearFuncs.create_mesh_obj(context, mesh)
            ob = bpy.context.active_object
            ob['type'] = "rack"
            ob['module'] = self.module
            ob['nTeeth'] = self.nTeeth
            ob['skewAng'] = self.skewness
            ob['rotAng'] = self.rotAng % (2 * pi / self.nTeeth)
            ob['shiftX'] = self.shiftX
        else:
            if "type" in bpy.context.selected_objects[0]:
                if bpy.context.selected_objects.__len__() == 1 and bpy.context.selected_objects[0]['type'] == "spur":
                    ob1 = bpy.context.selected_objects[0]
                    r = self.module * ob1['nTeeth'] / 2 + ob1['shiftX']
                    rA = pi - pi / self.nTeeth + self.rotAng * ob1['nTeeth'] / self.nTeeth + self.rotAng - ob1['rotAng'] * \
                         ob1['nTeeth'] / self.nTeeth
                    mesh2 = addMesh.createRackMesh(m=self.module,
                                                   nTeeth=self.nTeeth,
                                                   prezureAngle=self.angle,
                                                   shiftX=self.shiftX,
                                                   width=self.width,
                                                   widthStep=self.widthStep,
                                                   skew=self.skewness,
                                                   name="Rack")
                    base2 = addMesh.GearFuncs.create_mesh_obj(context, mesh2)
                    ob2 = bpy.context.active_object
                    vec = Vector((r * (cos(self.rotAng) + self.rotAng * sin(self.rotAng)), 
                                    r * (sin(self.rotAng) - self.rotAng * cos(self.rotAng)), 
                                    0.0))
                    vec.rotate(Euler((ob1.rotation_euler.x, ob1.rotation_euler.y, ob1.rotation_euler.z), 'XYZ'))
                    ob2.location.x = ob1.location[0] + vec[0]
                    ob2.location.y = ob1.location[1] + vec[1]
                    ob2.location.z = ob1.location[2] + vec[2]
                    ob2.rotation_euler.z = self.rotAng
                    ob2['type'] = "rack"
                    ob2['module'] = self.module
                    ob2['nTeeth'] = self.nTeeth
                    ob2['dRef'] = addMesh.GearFuncs.getRefDiam(self.module, self.nTeeth) + 2 * self.shiftX
                    ob2['skewAng'] = -self.skewness * (ob1['nTeeth'] / self.nTeeth)
                    ob2['rotAng'] = rA % (2 * pi / self.nTeeth)
                    ob2['shiftX'] = self.shiftX
                else:
                    self.report({'INFO'}, "Select one spur gear!")
            else:
                self.report({'INFO'}, "Select object created by GearGenMaster!")
        return {'FINISHED'}
        # ////////////////////////////////////////////////////////////////////////////////


class AddHerringboneGear(bpy.types.Operator):
    """Add a gear mesh"""
    bl_idname = "mesh.primitive_herringbone_gear_add"
    bl_label = "Add_Herringbone_Gear"
    bl_options = {'REGISTER', 'UNDO'}

    nTeeth : IntProperty(name="Z",
                         description="Number of teeth",
                         min=6,
                         max=265,
                         options={'SKIP_SAVE'},
                         default=12)
    module : FloatProperty(name="Module",
                           description="Module of the gear",
                           min=0.05,
                           max=100.0,
                           unit='LENGTH',
                           default=0.2)
    width : FloatProperty(name="Width, thickness of gear",
                          description="Width of the gear",
                          min=0.1,
                          max=100.0,
                          unit='LENGTH',
                          default=0.5)
    diam_hole : FloatProperty(name="Hole Diameter",
                          description="Diameter of hole",
                          min=0.0,
                          unit='LENGTH',
                          default= 1.0)      
    widthStep : IntProperty(name="Width Step",
                            description="Definition of the width of teeth",
                            min=1,
                            max=30,
                            default=1)
    skewness : FloatProperty(name="Skewness",
                             description="Skewness of the teeth",
                             min=radians(-90),
                             max=radians(90),
                             options={'SKIP_SAVE'},
                             unit='ROTATION',
                             default=0.0)
    evolvStep : IntProperty(name="Def. of evolute",
                            description="Definition of the evolute",
                            min=3,
                            max=30,
                            default=3)
    filletCurveStep : IntProperty(name="Def. of fillet curve",
                                  description="Definition of the fillet curve",
                                  min=3,
                                  max=30,
                                  default=3)
    nSat : IntProperty(name="Num. of sattelites",
                       description="Number of sattelites",
                       min=1,
                       max=30,
                       options={'SKIP_SAVE'},
                       default=1)
    tStep : IntProperty(name="Def. of top land",
                        description="Definition of the top land",
                        options={'SKIP_SAVE'},
                        min=1,
                        max=30,
                        default=3)
    bStep : IntProperty(name="Def. of bottom land",
                        description="Definition of the bottom land",
                        options={'SKIP_SAVE'},
                        min=1,
                        max=30,
                        default=1)
    shiftX : FloatProperty(name="ShiftX",
                           description="Shift of the profile",
                           min=-4.0,
                           max=4.0,
                           step=0.1,
                           options={'SKIP_SAVE'},
                           unit='LENGTH',
                           default=0.0)
    c : FloatProperty(name="C",
                      description="Tip and Root Clearance",
                      min=0.0,
                      max=1.0,
                      precision=2,
                      options={'SKIP_SAVE'},
                      step=0.01,
                      unit='LENGTH',
                      default=0.25)
    angle : FloatProperty(name="Pressure Angle",
                          description="Pressure angle, skewness of tooth tip",
                          min=0.0,
                          max=radians(45.0),
                          unit='ROTATION',
                          default=radians(20.0))
    rotAng : FloatProperty(name="Rotation Angle",
                           description="Rotation Angle Of Gear",
                           options={'SKIP_SAVE'},
                           min=0.0,
                           max=radians(360.0),
                           unit='ROTATION',
                           default=radians(0.0))
    driver : BoolProperty(name="Add Driver",
                          description="Add Driver to Gear",
                          options={'SKIP_SAVE'},
                          default=False)
    fill_holes : BoolProperty(name="Fill Holes",
                          description="Fill Holes",
                          options={'SKIP_SAVE'},
                          default=False)
    is_sat : BoolProperty(name="Is Satellite",
                          description="Satellite of gear",
                          options={'SKIP_SAVE'},
                          default=False)
    tw: FloatProperty(name="Tooth Width",
                      description="Width of Tooth",
                      min=0.0,
                      max=1.0,
                      unit='LENGTH',
                      default=1.0)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Main Properties")
        col = box.column(align=True)
        col.prop(self, 'nTeeth')
        col.prop(self, 'module')
        col.prop(self, 'c')
        col.prop(self, 'angle')
        col.prop(self, 'shiftX')
        col.prop(self, 'tw')
        col.prop(self, 'width')
        col.prop(self, 'diam_hole')
        box = layout.box()
        box.label(text="Mesh Properties")
        col = box.column(align=True)        
        col.prop(self, 'widthStep')
        col.prop(self, 'evolvStep')
        col.prop(self, 'filletCurveStep')
        col.prop(self, 'tStep')
        col.prop(self, 'bStep')
        col.prop(self, 'fill_holes')
        box = layout.box()
        box.label(text="Deformations")
        col = box.column(align=True)
        col.prop(self, 'skewness')
        col.prop(self, 'rotAng')
        box = layout.box()
        box.prop(self, 'is_sat')      
        if self.is_sat:
            box.prop(self, 'nSat')
            box.prop(self, 'driver')
        else:
            self.nSat = 1        

    def execute(self, context):
        if not bpy.context.selected_objects:
            mesh = addMesh.createGearMesh(typeGear='Hbone',
                                          m=self.module,
                                          nTeeth=self.nTeeth,
                                          evolvStep=self.evolvStep,
                                          filletCurveStep=self.filletCurveStep,
                                          tStep=self.tStep,
                                          bStep=self.bStep,
                                          pressureAngle=self.angle,
                                          shiftX=self.shiftX,
                                          width=self.width,
                                          widthStep=self.widthStep,
                                          skewAng=self.skewness,
                                          angCon=0.0,
                                          angZ=self.rotAng,
                                          name="HerringboneGear",
                                          c=self.c,
                                          tw=self.tw,
                                          fill_holes=self.fill_holes,
                                          diamHole=self.diam_hole)
            base = addMesh.GearFuncs.create_mesh_obj(context, mesh)
            ob = bpy.context.active_object
            ob['type'] = "herringbone"
            ob['module'] = self.module
            ob['nTeeth'] = self.nTeeth
            ob['dRef'] = addMesh.GearFuncs.getRefDiam(self.module, self.nTeeth) + 2 * self.shiftX
            ob['skewAng'] = self.skewness
            ob['rotAng'] = self.rotAng % (2 * pi / self.nTeeth)
        else:
            if "type" in bpy.context.selected_objects[0]:
                if bpy.context.selected_objects.__len__() == 1:
                    if bpy.context.selected_objects[0]['type'] == "internal":
                        ob1 = bpy.context.selected_objects[0]
                        r = (self.module * ob1['nTeeth'] - self.module * self.nTeeth) / 2 - self.shiftX
                        for nS in range(self.nSat):
                            rotAng = self.rotAng + nS * (2 * pi / self.nSat)
                            rA = -rotAng * ob1['nTeeth'] / self.nTeeth + rotAng + ob1['rotAng'] * ob1[
                                'nTeeth'] / self.nTeeth
                            mesh = addMesh.createGearMesh(typeGear='Hbone',
                                                          m=self.module,
                                                          nTeeth=self.nTeeth,
                                                          evolvStep=self.evolvStep,
                                                          filletCurveStep=self.filletCurveStep,
                                                          tStep=self.tStep,
                                                          bStep=self.bStep,
                                                          pressureAngle=self.angle,
                                                          shiftX=self.shiftX,
                                                          width=self.width,
                                                          widthStep=self.widthStep,
                                                          skewAng=ob1['skewAng'] * (ob1['nTeeth'] / self.nTeeth),
                                                          angCon=0.0,
                                                          angZ=rA,
                                                          c=self.c,
                                                          tw=self.tw,
                                                          fill_holes=self.fill_holes,
                                                          diamHole=self.diam_hole)
                            base = addMesh.GearFuncs.create_mesh_obj(context, mesh)
                            ob2 = bpy.context.active_object
                            ob2['type'] = "herringbone"
                            ob2['module'] = self.module
                            ob2['nTeeth'] = self.nTeeth
                            ob2['dRef'] = addMesh.GearFuncs.getRefDiam(self.module, self.nTeeth) + 2 * self.shiftX
                            ob2['skewAng'] = ob1['skewAng'] * (ob1['nTeeth'] / self.nTeeth)
                            ob2['rotAng'] = rA % (2 * pi / self.nTeeth)
                            ob2.location.x = ob1.location.x + r * cos(rotAng)
                            ob2.location.y = ob1.location.y + r * sin(rotAng)
                            ob2.location.z = ob1.location.z
                    elif bpy.context.selected_objects[0]['type'] == "herringbone":
                        ob1 = bpy.context.selected_objects[0]
                        r = (self.module * ob1['nTeeth'] + self.module * self.nTeeth) / 2 + self.shiftX
                        for nS in range(self.nSat):
                            rotAng = self.rotAng + nS * (2 * pi / self.nSat)
                            rA = pi - pi / self.nTeeth + rotAng * ob1['nTeeth'] / self.nTeeth + rotAng - ob1['rotAng'] * \
                                 ob1['nTeeth'] / self.nTeeth
                            mesh = addMesh.createGearMesh(typeGear='Hbone',
                                                          m=self.module,
                                                          nTeeth=self.nTeeth,
                                                          evolvStep=self.evolvStep,
                                                          filletCurveStep=self.filletCurveStep,
                                                          tStep=self.tStep,
                                                          bStep=self.bStep,
                                                          pressureAngle=self.angle,
                                                          shiftX=self.shiftX,
                                                          width=self.width,
                                                          widthStep=self.widthStep,
                                                          skewAng=-ob1['skewAng'] * (ob1['nTeeth'] / self.nTeeth),
                                                          angCon=0.0,
                                                          angZ=rA,
                                                          c=self.c,
                                                          tw=self.tw,
                                                          fill_holes=self.fill_holes,
                                                          diamHole=self.diam_hole)
                            base = addMesh.GearFuncs.create_mesh_obj(context, mesh)
                            ob2 = bpy.context.active_object
                            ob2.location.x = ob1.location[0] + r * cos(rotAng)
                            ob2.location.y = ob1.location[1] + r * sin(rotAng)
                            ob2.location.z = ob1.location[2]
                            ob2['type'] = "herringbone"
                            ob2['module'] = self.module
                            ob2['nTeeth'] = self.nTeeth
                            ob2['dRef'] = addMesh.GearFuncs.getRefDiam(self.module, self.nTeeth) + 2 * self.shiftX
                            ob2['skewAng'] = -ob1['skewAng'] * (ob1['nTeeth'] / self.nTeeth)
                            ob2['rotAng'] = rA % (2 * pi / self.nTeeth)
                            if self.driver == True:
                                obDrive = ob2.driver_add("rotation_euler", 2)
                                obDrive.driver.type = 'SCRIPTED'
                                rotvar = obDrive.driver.variables.new()
                                rotvar.name = 'rotSpur'
                                rotvar.type = 'TRANSFORMS'
                                rotvar.targets[0].transform_type = 'ROT_Z'
                                rotvar.targets[0].transform_space = 'WORLD_SPACE'
                                rotvar.targets[0].id = ob1
                                obDrive.driver.expression = "-rotSpur/" + str(self.nTeeth / ob1['nTeeth'])
                    else:
                        self.report({'INFO'}, "Select one herringbone or internal gear!")
            else:
                self.report({'INFO'}, "Select object created by GearGenMaster!")
        return {'FINISHED'}
        # ////////////////////////////////////////////////////////////////////////////////


class AddInternalGear(bpy.types.Operator):
    """Add a gear mesh"""
    bl_idname = "mesh.primitive_internal_gear_add"
    bl_label = "Add_Internal_Gear"
    bl_options = {'REGISTER', 'UNDO'}

    nTeeth : IntProperty(name="Z",
                         description="Number of teeth",
                         min=18,
                         max=265,
                         options={'SKIP_SAVE'},
                         default=24)
    module : FloatProperty(name="Module",
                           description="Module of the gear",
                           min=0.05,
                           max=100.0,
                           unit='LENGTH',
                           default=0.2)
    width : FloatProperty(name="Width, thickness of gear",
                          description="Width of the gear",
                          min=0.1,
                          max=100.0,
                          unit='LENGTH',
                          default=0.5)
    diam_hole : FloatProperty(name="Diameter",
                          description="Diameter",
                          min=0.0,
                          unit='LENGTH',
                          default= 1.0)      
    widthStep : IntProperty(name="Width Step",
                            description="Definition of the width of teeth",
                            min=1,
                            max=30,
                            default=1)
    skewness : FloatProperty(name="Skewness",
                             description="Skewness of the teeth",
                             min=radians(-90),
                             max=radians(90),
                             options={'SKIP_SAVE'},
                             unit='ROTATION',
                             default=0.0)
    evolvStep : IntProperty(name="Def. of evolute",
                            description="Definition of the evolute",
                            min=3,
                            max=30,
                            default=3)
    filletCurveStep : IntProperty(name="Def. of fillet curve",
                                  description="Definition of the fillet curve",
                                  min=3,
                                  max=30,
                                  default=3)
    tStep : IntProperty(name="Def. of top land",
                        description="Definition of the top land",
                        options={'SKIP_SAVE'},
                        min=1,
                        max=30,
                        default=1)
    bStep : IntProperty(name="Def. of bottom land",
                        description="Definition of the bottom land",
                        options={'SKIP_SAVE'},
                        min=1,
                        max=30,
                        default=3)
    shiftX : FloatProperty(name="ShiftX",
                           description="Shift of the profile of pinion",
                           min=-4.0,
                           max=4.0,
                           step=0.1,
                           options={'SKIP_SAVE'},
                           unit='LENGTH',
                           default=0.0)
    c : FloatProperty(name="C",
                      description="Tip and Root Clearance",
                      min=0.0,
                      max=1.0,
                      precision=2,
                      options={'SKIP_SAVE'},
                      step=0.01,
                      unit='LENGTH',
                      default=0.25)
    angle : FloatProperty(name="Pressure Angle",
                          description="Pressure angle, skewness of tooth tip",
                          min=0.0,
                          max=radians(45.0),
                          unit='ROTATION',
                          default=radians(20.0))
    rotAng : FloatProperty(name="Rotation Angle",
                           description="Rotation Angle Of Gear",
                           min=0.0,
                           max=radians(360.0),
                           options={'SKIP_SAVE'},
                           unit='ROTATION',
                           default=radians(0.0))
    tw: FloatProperty(name="Tooth Width",
                      description="Width of Tooth",
                      min=0.0,
                      max=1.0,
                      unit='LENGTH',
                      default=1.0)
    fill_holes : BoolProperty(name="Fill Holes",
                          description="Fill Holes",
                          options={'SKIP_SAVE'},
                          default=False)
    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Main Properties")
        col = box.column(align=True)
        col.prop(self, 'nTeeth')
        col.prop(self, 'shiftX')
        col.prop(self, 'tw')
        col.prop(self, 'c')
        col.prop(self, 'module')
        col.prop(self, 'angle')
        box = layout.box()
        box.label(text="Gear Properties")
        col = box.column(align=True)
        col.prop(self, 'width')
        col.prop(self, 'diam_hole')
        col.prop(self, 'widthStep')
        col.prop(self, 'evolvStep')
        col.prop(self, 'filletCurveStep')
        col.prop(self, 'tStep')
        col.prop(self, 'bStep')
        col.prop(self, 'fill_holes')
        col.prop(self, 'skewness')
        box = layout.box()
        box.prop(self, 'rotAng')

    def execute(self, context):
        mesh = addMesh.createGearMesh(typeGear='internal',
                                      m=self.module,
                                      nTeeth=self.nTeeth,
                                      evolvStep=self.evolvStep,
                                      filletCurveStep=self.filletCurveStep,
                                      tStep=self.bStep,
                                      bStep=self.tStep,
                                      pressureAngle=self.angle,
                                      shiftX=self.shiftX,
                                      width=self.width,
                                      widthStep=self.widthStep,
                                      skewAng=self.skewness,
                                      angCon=0.0,
                                      angZ=self.rotAng,
                                      name="InternalGear",
                                      c=self.c,
                                      tw=self.tw,
                                      fill_holes=self.fill_holes,
                                      diamHole=self.diam_hole)
        base = addMesh.GearFuncs.create_mesh_obj(context, mesh)
        ob = bpy.context.active_object
        ob['type'] = "internal"
        ob['module'] = self.module
        ob['nTeeth'] = self.nTeeth
        ob['dRef'] = addMesh.GearFuncs.getRefDiam(self.module, self.nTeeth) + 2 * self.shiftX
        ob['skewAng'] = self.skewness
        ob['rotAng'] = self.rotAng % (2 * pi / self.nTeeth)
        return {'FINISHED'}
        # ////////////////////////////////////////////////////////////////////////////////


class AddBevelGear(bpy.types.Operator):
    """Add a gear mesh"""
    bl_idname = "mesh.primitive_bevel_gear_add"
    bl_label = "Add_Bevel_Gears"
    bl_options = {'REGISTER', 'UNDO'}

    nTeeth1 : IntProperty(name="Z1",
                          description="Number of teeth on the pinion",
                          min=6,
                          options={'SKIP_SAVE'},
                          default=12)
    nTeeth2 : IntProperty(name="Z2",
                          description="Number of teeth on the gear",
                          min=6,
                          options={'SKIP_SAVE'},
                          default=12)
    module : FloatProperty(name="Module",
                           description="Module of the gear",
                           min=0.05,
                           max=100.0,
                           unit='LENGTH',
                           default=0.2)
    width : FloatProperty(name="Width, thickness of gear",
                          description="Width of the gear",
                          min=0.1,
                          unit='LENGTH',
                          default=0.5)
    diam_hole1 : FloatProperty(name="Pinion hole Diameter",
                          description="Diameter of pinion hole",
                          min=0.0,
                          unit='LENGTH',
                          default= 1.0)
    diam_hole2 : FloatProperty(name="Gear hole Diameter",
                          description="Diameter of gear hole",
                          min=0.0,
                          unit='LENGTH',
                          default= 1.0)
    widthStep : IntProperty(name="Width Step",
                            description="Definition of the width of teeth",
                            min=1,
                            default=1)
    angShaft : FloatProperty(name="Shafts angle",
                             description="Angle between shafts",
                             min=radians(1),
                             max=radians(179),
                             options={'SKIP_SAVE'},
                             unit='ROTATION',
                             default=radians(90))
    skewness : FloatProperty(name="Skewness",
                             description="Skewness of the teeth",
                             min=radians(-90),
                             max=radians(90),
                             options={'SKIP_SAVE'},
                             unit='ROTATION',
                             default=0.0)
    evolvStep : IntProperty(name="Def. of evolute",
                            description="Definition of the evolute",
                            min=3,
                            max=30,
                            default=3)
    filletCurveStep : IntProperty(name="Def. of fillet curve",
                                  description="Definition of the fillet curve",
                                  min=3,
                                  max=30,
                                  default=3)
    tStep : IntProperty(name="Def. of top land",
                        description="Definition of the top land",
                        options={'SKIP_SAVE'},
                        min=1,
                        max=30,
                        default=3)
    bStep : IntProperty(name="Def. of bottom land",
                        description="Definition of the bottom land",
                        options={'SKIP_SAVE'},
                        min=1,
                        max=30,
                        default=1)
    shiftX1 : FloatProperty(name="ShiftX1",
                            description="Shift of the profile of pinion",
                            min=-4.0,
                            max=4.0,
                            step=0.1,
                            options={'SKIP_SAVE'},
                            unit='LENGTH',
                            default=0.0)
    shiftX2 : FloatProperty(name="ShiftX2",
                            description="Shift of the profile of gear",
                            min=-4.0,
                            max=4.0,
                            step=0.1,
                            options={'SKIP_SAVE'},
                            unit='LENGTH',
                            default=0.0)
    angle : FloatProperty(name="Pressure Angle",
                          description="Pressure angle, skewness of tooth tip",
                          min=0.0,
                          max=radians(45.0),
                          unit='ROTATION',
                          default=radians(20.0))
    rotAng : FloatProperty(name="Rotation Angle",
                           description="Rotation Angle Of Gear",
                           min=0.0,
                           max=radians(360.0),
                           options={'SKIP_SAVE'},
                           unit='ROTATION',
                           default=radians(0.0))
    tw1: FloatProperty(name="Tooth Width",
                      description="Width of Tooth",
                      min=0.0,
                      max=1.0,
                      unit='LENGTH',
                      default=1.0)
    tw2: FloatProperty(name="Tooth Width",
                      description="Width of Tooth",
                      min=0.0,
                      max=1.0,
                      unit='LENGTH',
                      default=1.0)
    fill_holes : BoolProperty(name="Fill Holes",
                          description="Fill Holes",
                          options={'SKIP_SAVE'},
                          default=False)
    # driver : BoolProperty(name="Add Driver",
    #                      description="Add Driver to Gear",
    #                      options={'SKIP_SAVE'},
    #                      default=False)

    def draw(self, context):
        layout = self.layout
        split = layout.split()

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Pinion:")
        sub.prop(self, 'nTeeth1')
        sub.prop(self, 'tw1')
        sub.prop(self, 'diam_hole1')
        # sub.prop(self, 'shiftX1')

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Gear:")
        sub.prop(self, 'nTeeth2')
        sub.prop(self, 'tw2')
        sub.prop(self, 'diam_hole2')
        # sub.prop(self, 'shiftX2')
        col = layout.column(align=True)
        col.prop(self, 'module')
        col.prop(self, 'width')
        col.prop(self, 'widthStep')
        col.prop(self, 'evolvStep')
        col.prop(self, 'filletCurveStep')
        col.prop(self, 'tStep')
        col.prop(self, 'bStep')
        col.prop(self, 'fill_holes')
        box = layout.box()
        box.prop(self, 'angle')
        box.prop(self, 'skewness')
        box.prop(self, 'angShaft')
        box = layout.box()
        box.prop(self, 'rotAng')
        # box = layout.box()
        # box.prop(self, 'driver')

    def execute(self, context):
        if self.angShaft == 0 or self.angShaft == pi:
            angcon1 = 0
            angcon2 = 0
        else:
            angcon1 = pi / 2 - atan((self.nTeeth2 / self.nTeeth1 + cos(self.angShaft)) / sin(self.angShaft))
            angcon2 = pi / 2 - atan((self.nTeeth1 / self.nTeeth2 + cos(self.angShaft)) / sin(self.angShaft))
        origZ = addMesh.GearFuncs.getOriginZ(self.module, self.nTeeth1, 'bevel', self.shiftX1,
                                             angcon1) + 1.75 * self.module * sin(angcon1) + bpy.context.scene.cursor.location[2]
        mesh = addMesh.createGearMesh(typeGear='bevel',
                                      m=self.module,
                                      nTeeth=self.nTeeth1,
                                      evolvStep=self.evolvStep,
                                      filletCurveStep=self.filletCurveStep,
                                      tStep=self.tStep,
                                      bStep=self.bStep,
                                      pressureAngle=self.angle,
                                      shiftX=self.shiftX1,
                                      width=self.width,
                                      widthStep=self.widthStep,
                                      skewAng=self.skewness,
                                      angCon=angcon1,
                                      angZ=self.rotAng,
                                      name="BevelGear",
                                      tw=self.tw1,
                                      fill_holes=self.fill_holes,
                                      diamHole=self.diam_hole1)
        base = addMesh.GearFuncs.create_mesh_obj(context, mesh)
        ob1 = bpy.context.active_object
        ob1['type'] = "bevel"
        ob1['module'] = self.module
        ob1['nTeeth'] = self.nTeeth1
        ob1['shaftAng'] = self.angShaft
        ob1['skewAng'] = self.skewness
        ob1['rotAng'] = self.rotAng % (2 * pi / self.nTeeth1)
        ob1.location.z = origZ
        mesh2 = addMesh.createGearMesh(typeGear='bevel',
                                       m=self.module,
                                       nTeeth=self.nTeeth2,
                                       evolvStep=self.evolvStep,
                                       filletCurveStep=self.filletCurveStep,
                                       tStep=self.tStep,
                                       bStep=self.bStep,
                                       pressureAngle=self.angle,
                                       shiftX=self.shiftX2,
                                       width=self.width,
                                       widthStep=self.widthStep,
                                       skewAng=-self.skewness * (self.nTeeth1 / self.nTeeth2),
                                       angCon=angcon2,
                                       angZ=pi - pi / self.nTeeth2,
                                       name="BevelGear",
                                       tw=self.tw2,
                                       fill_holes=self.fill_holes,
                                       diamHole=self.diam_hole2)
        base2 = addMesh.GearFuncs.create_mesh_obj(context, mesh2)
        ob2 = bpy.context.active_object
        ob2['type'] = "bevel"
        ob2['module'] = self.module
        ob2['nTeeth'] = self.nTeeth2
        ob2['shaftAng'] = self.angShaft
        ob2['skewAng'] = -self.skewness * (self.nTeeth1 / self.nTeeth2)
        ob2.rotation_euler.y = -self.angShaft
        ob2.location.z = origZ
        ob2.rotation_euler.z = self.rotAng
        return {'FINISHED'}


class AddWorm(bpy.types.Operator):
    bl_idname = "mesh.primitive_worm_add"
    bl_label = "Add worm drive"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    wormTypeList = [('wt_cylindrical', 'Cylindrical', 'Cylindrical worm'),
                    ('wt_globoid_2', 'Globoid 2', 'Globoid worm 2'), ('wt_globoid_1', 'Globoid 1', 'Globoid worm 1')]
    wType : EnumProperty(name='Worm Type',
                         description='Choose the type of worm',
                         items=wormTypeList, default='wt_globoid_2')
    nTeeth : IntProperty(name="Z",
                         description="Number of teeth",
                         min=48,
                         max=265,
                         default=48)
    module : FloatProperty(name="Module",
                           description="Module of the gear",
                           min=0.05,
                           max=100.0,
                           unit='LENGTH',
                           default=0.2)
    dWorm : FloatProperty(name="Diameter of worm",
                          description="Diameter of worm",
                          min=1,
                          max=100.0,
                          unit='LENGTH',
                          default=1)
    rezWorm : IntProperty(name="rezolution of worm",
                          description="rezolution of worm",
                          min=16,
                          max=300,
                          default=16)
    nTWorm : IntProperty(name="nTeeth of worm",
                         description="nTeeth of worm",
                         min=2,
                         max=16,
                         default=4)
    width : FloatProperty(name="Width, thickness of gear",
                          description="Width of the gear",
                          min=0.1,
                          max=100.0,
                          unit='LENGTH',
                          default=1.5)
    widthStep : IntProperty(name="Width Step",
                            description="Definition of the width of teeth",
                            min=3,
                            max=30,
                            default=3)
    evolvStep : IntProperty(name="Def. of evolute",
                            description="Definition of the evolute",
                            min=3,
                            max=30,
                            default=3)
    filletCurveStep : IntProperty(name="Def. of fillet curve",
                                  description="Definition of the fillet curve",
                                  min=3,
                                  max=30,
                                  default=3)
    tStep : IntProperty(name="Def. of top land",
                        description="Definition of the top land",
                        min=1,
                        max=30,
                        default=1)
    bStep : IntProperty(name="Def. of bottom land",
                        description="Definition of the bottom land",
                        min=1,
                        max=30,
                        default=1)
    shiftX : FloatProperty(name="ShiftX",
                           description="Shift of the profile",
                           min=-4.0,
                           max=4.0,
                           step=0.1,
                           unit='LENGTH',
                           default=0.0)
    c : FloatProperty(name="C",
                      description="Tip and Root Clearance",
                      min=0.0,
                      max=1.0,
                      precision=2,
                      options={'SKIP_SAVE'},
                      step=0.01,
                      unit='LENGTH',
                      default=0.25)
    angle : FloatProperty(name="Pressure Angle",
                          description="Pressure angle, skewness of tooth tip",
                          min=0.0,
                          max=radians(45.0),
                          unit='ROTATION',
                          default=radians(20.0))
    rotAng : FloatProperty(name="Rotation Angle",
                           description="Rotation Angle Of Gear",
                           min=0.0,
                           max=radians(360.0),
                           unit='ROTATION',
                           default=radians(0.0))
    fill_holes : BoolProperty(name="Fill Holes",
                          description="Fill Holes",
                          options={'SKIP_SAVE'},
                          default=False)
    diam_hole : FloatProperty(name="Hole Diameter",
                          description="Diameter of hole",
                          min=0.0,
                          unit='LENGTH',
                          default= 1.0)
    driver : BoolProperty(name="Add Driver",
                         description="Add Driver to Gear",
                         options={'SKIP_SAVE'},
                         default=False)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(self, 'wType')
        box = layout.box()
        box.label(text="Main Properties")
        col = box.column(align=True)
        col.prop(self, 'nTeeth')
        col.prop(self, 'module')
        col.prop(self, 'angle')
        # col.prop(self, 'shiftX')
        col.prop(self, 'c')
        box = layout.box()
        box.label(text="Worm Properties")
        col = box.column(align=True)
        col.prop(self, 'dWorm')
        col.prop(self, 'rezWorm')
        col.prop(self, 'nTWorm')
        box = layout.box()
        box.label(text="Gear Properties")
        col = box.column(align=True)
        col.prop(self, 'width')
        col.prop(self, 'widthStep')
        col.prop(self, 'evolvStep')
        col.prop(self, 'filletCurveStep')
        col.prop(self, 'tStep')
        col.prop(self, 'bStep')
        col.prop(self, 'diam_hole')
        #col.prop(self, 'fill_holes')
        # =======================================================================
        box = layout.box()
        box.prop(self, 'driver')
        # =======================================================================

    def execute(self, context):
        mesh = addMesh.createWormMesh(wType=self.wType,
                                      m=self.module,
                                      nTeeth=self.nTeeth,
                                      dWorm=self.dWorm,
                                      rezWorm=self.rezWorm,
                                      nTWorm=self.nTWorm,
                                      evolvStep=self.evolvStep,
                                      filletCurveStep=self.filletCurveStep,
                                      prezureAngle=self.angle,
                                      shiftX=self.shiftX,
                                      angZ=0.0,
                                      c=self.c)
        base = addMesh.GearFuncs.create_mesh_obj(context, mesh)
        ob = base
        ob['module'] = self.module
        ob['nTeeth'] = self.nTeeth
        ob['rotAng'] = self.rotAng % (2 * pi / self.nTeeth)
        if self.wType == 'wt_globoid_1':
            ob['type'] = "globoid1_worm"
        if self.wType == 'wt_globoid_2':
            ob['type'] = "globoid2_worm"
        if self.wType == 'wt_cylindrical':
            self.report({'INFO'}, "This type in developing!!!")

            # ===================================================================
            # DEVELOPMENT
            # ob['type'] = "cyl_worm"
            # mesh2 = addMesh.GearMesh(typeGear = 'cyl_worm',
            #                           m=self.module,
            #                           nTeeth=self.nTeeth,
            #                           evolvStep=self.evolvStep,
            #                           filletCurveStep=self.filletCurveStep,
            #                           tStep=self.tStep,
            #                           bStep=self.bStep,
            #                           prezureAngle=self.angle,
            #                           shiftX=self.shiftX,
            #                           width=self.width,
            #                           widthStep=self.widthStep,
            #                           skewAng=0,
            #                           angCon=0.0,
            #                           angZ= self.rotAng/self.nTeeth + pi,
            #                           dWorm = self.dWorm,
            #                           name="CylWorm")
            # base2 = addMesh.GearFuncs.create_mesh_obj(context, mesh2)
            # ob2 = bpy.context.active_object            
            # ob2.location.x = ob2.location.x + (getTipDiam(self.module, self.nTeeth) + self.dWorm)/2
            # ===================================================================
        #else:
        mesh2 = addMesh.createGearMesh(typeGear='gl_worm',
                                       m=self.module,
                                       nTeeth=self.nTeeth,
                                       evolvStep=self.evolvStep,
                                       filletCurveStep=self.filletCurveStep,
                                       tStep=self.tStep,
                                       bStep=self.bStep,
                                       pressureAngle=self.angle,
                                       shiftX=self.shiftX,
                                       width=self.width,
                                       widthStep=self.widthStep,
                                       skewAng=0,
                                       angCon=0.0,
                                       angZ=0.0,
                                       dWorm=self.dWorm,
                                       nTWorm=self.nTWorm,
                                       name="GloboidWorm",
                                       c=self.c,
                                       fill_holes=self.fill_holes,
                                       diamHole=self.diam_hole)
        bpy.context.scene.cursor.location[0] = ob.location.x - (addMesh.GearFuncs.getTipDiam(self.module, self.nTeeth) + self.dWorm) / 2
        base2 = addMesh.GearFuncs.create_mesh_obj(context, mesh2)
        #ob2 = bpy.context.active_object
        ob2 = base2
        bpy.context.scene.cursor.location[0] = ob.location.x
        #ob2.location.x = ob.location.x - (addMesh.GearFuncs.getTipDiam(self.module, self.nTeeth) + self.dWorm) / 2
        ob2['nTeeth'] = self.nTeeth
        for i in range(self.nTWorm*2 - 2):
            ob2.rotation_euler.z = 2*pi/self.nTeeth * i
            shr_mod = ob2.modifiers.new(name='myShrinkWrap', type='SHRINKWRAP')
            shr_mod.wrap_method = 'PROJECT'
            shr_mod.use_negative_direction = True
            shr_mod.use_positive_direction = False
            shr_mod.target = ob
            shr_mod.cull_face = 'FRONT'
            shr_mod.project_limit = 0.1
            bpy.context.view_layer.objects.active = ob2
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="myShrinkWrap")
        ob2.rotation_euler.z = 0
        bpy.ops.object.add(type='EMPTY', location=(-(addMesh.GearFuncs.getTipDiam(self.module, self.nTeeth) + self.dWorm) / 2 + bpy.context.scene.cursor.location[0], bpy.context.scene.cursor.location[1], bpy.context.scene.cursor.location[2]), rotation=(0.0, 0.0, 2*pi/self.nTeeth))
        emp = bpy.context.active_object
        arr_mod = ob2.modifiers.new(name='myArray', type='ARRAY')
        arr_mod.use_relative_offset = False
        arr_mod.use_object_offset = True
        arr_mod.offset_object = emp
        arr_mod.count = self.nTeeth
        arr_mod.use_merge_vertices = True
        arr_mod.use_merge_vertices_cap = True
        bpy.context.view_layer.objects.active = ob2
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="myArray")
        bpy.ops.object.delete(use_global=False)
        if self.driver:
            obDrive = ob2.driver_add("rotation_euler", 2)
            obDrive.driver.type = 'SCRIPTED'
            rotvar = obDrive.driver.variables.new()
            rotvar.name = 'rotWorm'
            rotvar.type = 'TRANSFORMS'
            rotvar.targets[0].transform_type = 'ROT_Y'
            rotvar.targets[0].transform_space = 'WORLD_SPACE'
            rotvar.targets[0].id = ob
            obDrive.driver.expression = "-rotWorm/" + str(self.nTeeth)
            # rotvar.targets[0].data_path = "[\"nTeeth\"]"
        
        return {'FINISHED'}

classes = (
    AddSpurGear,
    AddRack,
    AddHerringboneGear,
    AddInternalGear,
    AddBevelGear,
    AddWorm,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)