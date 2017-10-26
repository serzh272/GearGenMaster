import bpy
from builtins import range
from math import sin, radians, cos, pi, atan
from bpy.props import IntProperty, FloatProperty
from GearGen.addMesh import *

class Geargen_add(bpy.types.Menu):
    bl_idname = "mesh.GearGen"
    bl_label = "GearGen"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_spur_gear_add",
                        text="Add Spur Gear")
        layout.operator("mesh.primitive_herringbone_gear_add",
                        text="Add Herringbone Gear")
        layout.operator("mesh.primitive_internal_gear_add",
                        text="Add Internal Gear")
        layout.operator("mesh.primitive_bevel_gear_add",
                        text="Add Bevel Gears")

class AddSpurGear(bpy.types.Operator):
    """Add a gear mesh"""
    bl_idname = "mesh.primitive_spur_gear_add"
    bl_label = "Add_Spur_Gear"
    bl_options = {'REGISTER', 'UNDO'}
    
    nTeeth = IntProperty(name="Z",
        description="Number of teeth",
        min=6,
        max=265,
        options = {'SKIP_SAVE'},
        default=12)
    module = FloatProperty(name="Module",
        description="Module of the gear",
        min=0.05,
        max=100.0,
        unit='LENGTH',
        default=0.2)
    width = FloatProperty(name="Width, thickness of gear",
        description="Width of the gear",
        min=0.1,
        max=100.0,
        unit='LENGTH',
        default=0.5)    
    widthStep = IntProperty(name="Width Step",
        description="Definition of the width of teeth",
        min=1,
        max=30,
        default=1)
    skewness = FloatProperty(name="Skewness",
        description="Skewness of the teeth",
        min=radians(-90),
        max=radians(90),
        options = {'SKIP_SAVE'},
        unit='ROTATION',
        default=0.0)
    evolvStep = IntProperty(name="Def. of evolute",
        description="Definition of the evolute",
        min=3,
        max=30,
        default=3)
    filletCurveStep = IntProperty(name="Def. of fillet curve",
        description="Definition of the fillet curve",
        min=3,
        max=30,
        default=3)
    tStep = IntProperty(name="Def. of top land",
        description="Definition of the top land",
        min=1,
        max=30,        
        options = {'SKIP_SAVE'},
        default=3)
    bStep = IntProperty(name="Def. of bottom land",
        description="Definition of the bottom land",
        min=1,
        max=30,
        options = {'SKIP_SAVE'},
        default=1)
    shiftX = FloatProperty(name="ShiftX",
        description="Shift of the profile",
        min=-4.000,
        max=4.000,
        precision = 3,
        options = {'SKIP_SAVE'},
        step = 0.1,
        unit='LENGTH',
        default=0.000)
    angle = FloatProperty(name="Pressure Angle",
        description="Pressure angle, skewness of tooth tip",
        min=0.0,
        max=radians(45.0),
        unit='ROTATION',
        default=radians(20.0))    
    rotAng = FloatProperty(name="Rotation Angle",
        description="Rotation Angle Of Gear",
        options = {'SKIP_SAVE'},
        min=0.0,
        max=radians(360.0),
        unit='ROTATION',
        default=radians(0.0))
    
    def draw(self, context):
        layout = self.layout 
        box = layout.box()
        
        box.prop(self, 'nTeeth')
        box.prop(self, 'shiftX')
        col = layout.column(align = True)
        col.prop(self, 'module')
        col.prop(self, 'width')
        col.prop(self, 'widthStep')
        col.prop(self, 'evolvStep')
        col.prop(self, 'filletCurveStep')
        col.prop(self, 'tStep')
        col.prop(self, 'bStep')   
                            
        box = layout.box()        
        box.prop(self, 'angle')
        box.prop(self, 'skewness')
        box = layout.box()        
        box.prop(self, 'rotAng')
    def execute(self, context):        
        if bpy.context.selected_objects == []:
            mesh = createGearMesh(typeGear = '1',
                                  m=self.module,
                                  nTeeth=self.nTeeth,
                                  evolvStep=self.evolvStep,
                                  filletCurveStep=self.filletCurveStep,
                                  tStep=self.tStep,
                                  bStep=self.bStep,
                                  prezureAngle=self.angle,
                                  shiftX=self.shiftX,
                                  width=self.width,
                                  widthStep=self.widthStep,
                                  skewAng=self.skewness,
                                  angCon=0.0,
                                  angZ= self.rotAng)
            base = create_mesh_obj(context, mesh)
            ob = bpy.context.active_object
            ob['type'] = "spur"
            ob['module'] = self.module
            ob['nTeeth'] = self.nTeeth
            ob['dRef'] = getRefDiam(self.module, self.nTeeth) + 2*self.shiftX
            ob['skewAng'] = self.skewness
            ob['rotAng'] = self.rotAng%(2*pi/self.nTeeth)
            ob['shiftX'] = self.shiftX
        else:
            if bpy.context.selected_objects.__len__() == 1 and bpy.context.selected_objects[0]['type'] == "spur":
                ob1 = bpy.context.selected_objects[0]
                r = (self.module*ob1['nTeeth']+self.module*self.nTeeth)/2 + self.shiftX + ob1['shiftX']
                rA = pi - pi/self.nTeeth + self.rotAng*ob1['nTeeth']/self.nTeeth + self.rotAng - ob1['rotAng']*ob1['nTeeth']/self.nTeeth
                mesh2 = createGearMesh(typeGear = '1',
                                      m=self.module,
                                      nTeeth=self.nTeeth,
                                      evolvStep=self.evolvStep,
                                      filletCurveStep=self.filletCurveStep,
                                      tStep=self.tStep,
                                      bStep=self.bStep,
                                      prezureAngle=self.angle,
                                      shiftX=self.shiftX,
                                      width=self.width,
                                      widthStep=self.widthStep,
                                      skewAng=-self.skewness*(ob1['nTeeth']/self.nTeeth),
                                      angCon=0.0,
                                      angZ= rA)
                base2 = create_mesh_obj(context, mesh2)
                ob2 = bpy.context.active_object
                ob2.location.x = ob1.location[0] + r*cos(self.rotAng)
                ob2.location.y = ob1.location[1] + r*sin(self.rotAng)
                ob2.location.z = ob1.location[2]
                ob2['type'] = "spur"
                ob2['module'] = self.module
                ob2['nTeeth'] = self.nTeeth
                ob2['dRef'] = getRefDiam(self.module, self.nTeeth) + 2*self.shiftX
                ob2['skewAng'] = -self.skewness*(ob1['nTeeth']/self.nTeeth)
                ob2['rotAng'] = rA%(2*pi/self.nTeeth)
                ob2['shiftX'] = self.shiftX
            else:
                self.report({'INFO'}, "Select one spur gear!")
        return {'FINISHED'}          
    #////////////////////////////////////////////////////////////////////////////////
class AddHerringboneGear(bpy.types.Operator):
    """Add a gear mesh"""
    bl_idname = "mesh.primitive_herringbone_gear_add"
    bl_label = "Add_Herringbone_Gear"
    bl_options = {'REGISTER', 'UNDO'}
    
    nTeeth = IntProperty(name="Z",
        description="Number of teeth",
        min=6,
        max=265,
        options = {'SKIP_SAVE'},
        default=12)
    module = FloatProperty(name="Module",
        description="Module of the gear",
        min=0.05,
        max=100.0,
        unit='LENGTH',
        default=0.2)
    width = FloatProperty(name="Width, thickness of gear",
        description="Width of the gear",
        min=0.1,
        max=100.0,
        unit='LENGTH',
        default=0.5)    
    widthStep = IntProperty(name="Width Step",
        description="Definition of the width of teeth",
        min=1,
        max=30,
        default=1)
    skewness = FloatProperty(name="Skewness",
        description="Skewness of the teeth",
        min=radians(-90),
        max=radians(90),
        options = {'SKIP_SAVE'},
        unit='ROTATION',
        default=0.0)
    evolvStep = IntProperty(name="Def. of evolute",
        description="Definition of the evolute",
        min=3,
        max=30,
        default=3)
    filletCurveStep = IntProperty(name="Def. of fillet curve",
        description="Definition of the fillet curve",
        min=3,
        max=30,
        default=3)
    nSat = IntProperty(name="Num. of sattelites",
        description="Number of sattelites",
        min=1,
        max=30,
        options = {'SKIP_SAVE'},
        default=1)
    tStep = IntProperty(name="Def. of top land",
        description="Definition of the top land",
        options = {'SKIP_SAVE'},
        min=1,
        max=30,
        default=3)
    bStep = IntProperty(name="Def. of bottom land",
        description="Definition of the bottom land",
        options = {'SKIP_SAVE'},
        min=1,
        max=30,
        default=1)
    shiftX = FloatProperty(name="ShiftX",
        description="Shift of the profile",
        min=-4.0,
        max=4.0,
        step = 0.1,
        options = {'SKIP_SAVE'},
        unit='LENGTH',
        default=0.0)
    angle = FloatProperty(name="Pressure Angle",
        description="Pressure angle, skewness of tooth tip",
        min=0.0,
        max=radians(45.0),
        unit='ROTATION',
        default=radians(20.0))
    rotAng = FloatProperty(name="Rotation Angle",
        description="Rotation Angle Of Gear",
        options = {'SKIP_SAVE'},
        min=0.0,
        max=radians(360.0),
        unit='ROTATION',
        default=radians(0.0))
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, 'nTeeth')
        box.prop(self, 'shiftX')
        col = layout.column(align = True)
        col.prop(self, 'module')
        col.prop(self, 'width')
        col.prop(self, 'widthStep')
        col.prop(self, 'evolvStep')
        col.prop(self, 'filletCurveStep')
        col.prop(self, 'tStep')
        col.prop(self, 'bStep')   
                            
        box = layout.box()        
        box.prop(self, 'angle')
        box.prop(self, 'skewness')
        box = layout.box()        
        box.prop(self, 'rotAng')
        box.prop(self, 'nSat')
    def execute(self, context):
        if bpy.context.selected_objects == []:
            mesh = createGearMesh(typeGear = '4',
                                  m=self.module,
                                  nTeeth=self.nTeeth,
                                  evolvStep=self.evolvStep,
                                  filletCurveStep=self.filletCurveStep,
                                  tStep=self.tStep,
                                  bStep=self.bStep,
                                  prezureAngle=self.angle,
                                  shiftX=self.shiftX,
                                  width=self.width,
                                  widthStep=self.widthStep,
                                  skewAng=self.skewness,
                                  angCon=0.0,
                                  angZ= self.rotAng)
            base = create_mesh_obj(context, mesh)
            ob = bpy.context.active_object
            ob['type'] = "herringbone"
            ob['module'] = self.module
            ob['nTeeth'] = self.nTeeth
            ob['dRef'] = getRefDiam(self.module, self.nTeeth) + 2*self.shiftX
            ob['skewAng'] = self.skewness
            ob['rotAng'] = self.rotAng%(2*pi/self.nTeeth)            
        else:
            if bpy.context.selected_objects.__len__() == 1:
                if bpy.context.selected_objects[0]['type'] == "internal":
                    ob1 = bpy.context.selected_objects[0]
                    r = (self.module*ob1['nTeeth']-self.module*self.nTeeth)/2 - self.shiftX
                    for nS in range(self.nSat):
                        rotAng = self.rotAng + nS*(2*pi/self.nSat)
                        rA = -rotAng*ob1['nTeeth']/self.nTeeth + rotAng + ob1['rotAng']*ob1['nTeeth']/self.nTeeth
                        mesh = createGearMesh(typeGear = '4',
                                          m=self.module,
                                          nTeeth=self.nTeeth,
                                          evolvStep=self.evolvStep,
                                          filletCurveStep=self.filletCurveStep,
                                          tStep=self.tStep,
                                          bStep=self.bStep,
                                          prezureAngle=self.angle,
                                          shiftX=self.shiftX,
                                          width=self.width,
                                          widthStep=self.widthStep,
                                          skewAng=ob1['skewAng']*(ob1['nTeeth']/self.nTeeth),
                                          angCon=0.0,
                                          angZ= rA)
                        base = create_mesh_obj(context, mesh)
                        ob2 = bpy.context.active_object
                        ob2['type'] = "herringbone"
                        ob2['module'] = self.module
                        ob2['nTeeth'] = self.nTeeth
                        ob2['dRef'] = getRefDiam(self.module, self.nTeeth) + 2*self.shiftX
                        ob2['skewAng'] = self.skewness
                        ob2['rotAng'] = rA%(2*pi/self.nTeeth)
                        ob2.location.x = ob1.location.x + r*cos(rotAng)
                        ob2.location.y = ob1.location.y + r*sin(rotAng)
                        ob2.location.z = ob1.location.z
                elif bpy.context.selected_objects[0]['type'] == "herringbone":
                    ob1 = bpy.context.selected_objects[0]
                    r = (self.module*ob1['nTeeth']+self.module*self.nTeeth)/2 + self.shiftX
                    for nS in range(self.nSat):
                        rotAng = self.rotAng + nS*(2*pi/self.nSat)
                        rA = pi - pi/self.nTeeth + rotAng*ob1['nTeeth']/self.nTeeth + rotAng - ob1['rotAng']*ob1['nTeeth']/self.nTeeth
                        mesh = createGearMesh(typeGear = '4',
                                          m=self.module,
                                          nTeeth=self.nTeeth,
                                          evolvStep=self.evolvStep,
                                          filletCurveStep=self.filletCurveStep,
                                          tStep=self.tStep,
                                          bStep=self.bStep,
                                          prezureAngle=self.angle,
                                          shiftX=self.shiftX,
                                          width=self.width,
                                          widthStep=self.widthStep,
                                          skewAng=-ob1['skewAng']*(ob1['nTeeth']/self.nTeeth),
                                          angCon=0.0,
                                          angZ= rA)
                        base = create_mesh_obj(context, mesh)
                        ob2 = bpy.context.active_object
                        ob2.location.x = ob1.location[0] + r*cos(rotAng)
                        ob2.location.y = ob1.location[1] + r*sin(rotAng)
                        ob2.location.z = ob1.location[2]
                        ob2['type'] = "herringbone"
                        ob2['module'] = self.module
                        ob2['nTeeth'] = self.nTeeth
                        ob2['dRef'] = getRefDiam(self.module, self.nTeeth) + 2*self.shiftX
                        ob2['skewAng'] = -ob1['skewAng']*(ob1['nTeeth']/self.nTeeth)
                        ob2['rotAng'] = rA%(2*pi/self.nTeeth)
                else:
                    self.report({'INFO'}, "Select one herringbone or internal gear!")
            
        return {'FINISHED'}          
    #////////////////////////////////////////////////////////////////////////////////
class AddInternalGear(bpy.types.Operator):
    """Add a gear mesh"""
    bl_idname = "mesh.primitive_internal_gear_add"
    bl_label = "Add_Internal_Gear"
    bl_options = {'REGISTER', 'UNDO'}
    
    nTeeth = IntProperty(name="Z",
        description="Number of teeth",
        min=18,
        max=265,
        options = {'SKIP_SAVE'},
        default=24)
    module = FloatProperty(name="Module",
        description="Module of the gear",
        min=0.05,
        max=100.0,
        unit='LENGTH',
        default=0.2)
    width = FloatProperty(name="Width, thickness of gear",
        description="Width of the gear",
        min=0.1,
        max=100.0,
        unit='LENGTH',
        default=0.5)    
    widthStep = IntProperty(name="Width Step",
        description="Definition of the width of teeth",
        min=1,
        max=30,
        default=1)
    skewness = FloatProperty(name="Skewness",
        description="Skewness of the teeth",
        min=radians(-90),
        max=radians(90),
        options = {'SKIP_SAVE'},
        unit='ROTATION',
        default=0.0)
    evolvStep = IntProperty(name="Def. of evolute",
        description="Definition of the evolute",
        min=3,
        max=30,
        default=3)
    filletCurveStep = IntProperty(name="Def. of fillet curve",
        description="Definition of the fillet curve",
        min=3,
        max=30,
        default=3)
    tStep = IntProperty(name="Def. of top land",
        description="Definition of the top land",
        options = {'SKIP_SAVE'},
        min=1,
        max=30,
        default=1)
    bStep = IntProperty(name="Def. of bottom land",
        description="Definition of the bottom land",
        options = {'SKIP_SAVE'},
        min=1,
        max=30,
        default=3)
    shiftX = FloatProperty(name="ShiftX",
        description="Shift of the profile of pinion",
        min=-4.0,
        max=4.0,
        step = 0.1,
        options = {'SKIP_SAVE'},
        unit='LENGTH',
        default=0.0)
    angle = FloatProperty(name="Pressure Angle",
        description="Pressure angle, skewness of tooth tip",
        min=0.0,
        max=radians(45.0),
        unit='ROTATION',
        default=radians(20.0))
    rotAng = FloatProperty(name="Rotation Angle",
        description="Rotation Angle Of Gear",
        min=0.0,
        max=radians(360.0),
        options = {'SKIP_SAVE'},
        unit='ROTATION',
        default=radians(0.0))
    
    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.prop(self, 'nTeeth')
        box.prop(self, 'shiftX')
        
        col = layout.column(align = True)
        col.prop(self, 'module')
        col.prop(self, 'width')
        col.prop(self, 'widthStep')
        col.prop(self, 'evolvStep')
        col.prop(self, 'filletCurveStep')
        col.prop(self, 'tStep')
        col.prop(self, 'bStep')   
                            
        box = layout.box()        
        box.prop(self, 'angle')
        box.prop(self, 'skewness')
        box = layout.box()        
        box.prop(self, 'rotAng')
    def execute(self, context):
        mesh = createGearMesh(typeGear = '2',
                              m=self.module,
                              nTeeth=self.nTeeth,
                              evolvStep=self.evolvStep,
                              filletCurveStep=self.filletCurveStep,
                              tStep=self.tStep,
                              bStep=self.bStep,
                              prezureAngle=self.angle,
                              shiftX=self.shiftX,
                              width=self.width,
                              widthStep=self.widthStep,
                              skewAng=self.skewness,
                              angCon=0.0,
                              angZ=self.rotAng)
        base = create_mesh_obj(context, mesh)
        ob = bpy.context.active_object
        ob['type'] = "internal"
        ob['module'] = self.module
        ob['nTeeth'] = self.nTeeth
        ob['dRef'] = getRefDiam(self.module, self.nTeeth) + 2*self.shiftX
        ob['skewAng'] = self.skewness
        ob['rotAng'] = self.rotAng%(2*pi/self.nTeeth)
        return {'FINISHED'}          
    #////////////////////////////////////////////////////////////////////////////////    
class AddBevelGear(bpy.types.Operator):
    """Add a gear mesh"""
    bl_idname = "mesh.primitive_bevel_gear_add"
    bl_label = "Add_Bevel_Gears"
    bl_options = {'REGISTER', 'UNDO'}
    
    nTeeth1 = IntProperty(name="Z1",
        description="Number of teeth on the pinion",
        min=6,
        max=265,
        options = {'SKIP_SAVE'},
        default=12)
    nTeeth2 = IntProperty(name="Z2",
        description="Number of teeth on the gear",
        min=6,
        max=265,
        options = {'SKIP_SAVE'},
        default=12)
    module = FloatProperty(name="Module",
        description="Module of the gear",
        min=0.05,
        max=100.0,
        unit='LENGTH',
        default=0.2)
    width = FloatProperty(name="Width, thickness of gear",
        description="Width of the gear",
        min=0.1,
        max=100.0,
        unit='LENGTH',
        default=0.5)    
    widthStep = IntProperty(name="Width Step",
        description="Definition of the width of teeth",
        min=1,
        max=30,
        default=1)
    angShaft = FloatProperty(name="Shafts angle",
        description="Angle between shafts",
        min=radians(20),
        max=radians(170),
        options = {'SKIP_SAVE'},
        unit='ROTATION',
        default=radians(90))
    skewness = FloatProperty(name="Skewness",
        description="Skewness of the teeth",
        min=radians(-90),
        max=radians(90),
        options = {'SKIP_SAVE'},
        unit='ROTATION',
        default=0.0)
    evolvStep = IntProperty(name="Def. of evolute",
        description="Definition of the evolute",
        min=3,
        max=30,
        default=3)
    filletCurveStep = IntProperty(name="Def. of fillet curve",
        description="Definition of the fillet curve",
        min=3,
        max=30,
        default=3)
    tStep = IntProperty(name="Def. of top land",
        description="Definition of the top land",
        options = {'SKIP_SAVE'},
        min=1,
        max=30,
        default=3)
    bStep = IntProperty(name="Def. of bottom land",
        description="Definition of the bottom land",
        options = {'SKIP_SAVE'},
        min=1,
        max=30,
        default=1)
    shiftX1 = FloatProperty(name="ShiftX1",
        description="Shift of the profile of pinion",
        min=-4.0,
        max=4.0,
        step = 0.1,
        options = {'SKIP_SAVE'},
        unit='LENGTH',
        default=0.0)
    shiftX2 = FloatProperty(name="ShiftX2",
        description="Shift of the profile of gear",
        min=-4.0,
        max=4.0,
        step = 0.1,
        options = {'SKIP_SAVE'},
        unit='LENGTH',
        default=0.0)
    angle = FloatProperty(name="Pressure Angle",
        description="Pressure angle, skewness of tooth tip",
        min=0.0,
        max=radians(45.0),
        unit='ROTATION',
        default=radians(20.0))
    rotAng = FloatProperty(name="Rotation Angle",
        description="Rotation Angle Of Gear",
        min=0.0,
        max=radians(360.0),
        options = {'SKIP_SAVE'},
        unit='ROTATION',
        default=radians(0.0))
    
    def draw(self, context):
        layout = self.layout
        box = self.layout.box()
        box.prop(self, 'bf_Type_Gear')
        split = layout.split()
        
        col = split.column()
        sub = col.column(align = True)
        sub.label(text="Pinion:")
        sub.prop(self, 'nTeeth1')
        sub.prop(self, 'shiftX1')
        
        col = split.column()
        sub = col.column(align = True)
        sub.label(text="Gear:")
        sub.prop(self, 'nTeeth2')
        sub.prop(self, 'shiftX2')
        
        col = layout.column(align = True)
        col.prop(self, 'module')
        col.prop(self, 'width')
        col.prop(self, 'widthStep')
        col.prop(self, 'evolvStep')
        col.prop(self, 'filletCurveStep')
        col.prop(self, 'tStep')
        col.prop(self, 'bStep')   
                            
        box = layout.box()        
        box.prop(self, 'angle')
        box.prop(self, 'skewness')
        box.prop(self, 'angShaft')
        box = layout.box()        
        box.prop(self, 'rotAng')
        
    def execute(self, context):
        angcon1 = pi/2 - atan((self.nTeeth2/self.nTeeth1 + cos(self.angShaft))/sin(self.angShaft))
        angcon2 = pi/2 - atan((self.nTeeth1/self.nTeeth2 + cos(self.angShaft))/sin(self.angShaft))
        origZ = getOriginZ(self.module, self.nTeeth1, '3', self.shiftX1, angcon1)+1.25*self.module*sin(angcon1) + (self.module/2)*sin(angcon1) + bpy.context.scene.cursor_location[2]
        mesh = createGearMesh(typeGear = '3',
                              m=self.module,
                              nTeeth=self.nTeeth1,
                              evolvStep=self.evolvStep,
                              filletCurveStep=self.filletCurveStep,
                              tStep=self.tStep,
                              bStep=self.bStep,
                              prezureAngle=self.angle,
                              shiftX=self.shiftX1,
                              width=self.width,
                              widthStep=self.widthStep,
                              skewAng=self.skewness,
                              angCon=angcon1,
                              angZ=self.rotAng)
        base = create_mesh_obj(context, mesh)
        ob1 = bpy.context.active_object
        ob1['type'] = "bevel"
        ob1['module'] = self.module
        ob1['nTeeth'] = self.nTeeth1
        ob1['shaftAng'] = self.angShaft
        ob1['skewAng'] = self.skewness
        ob1['rotAng'] = self.rotAng%(2*pi/self.nTeeth1)
        ob1.location.z = origZ
        mesh2 = createGearMesh(typeGear = '3',
                              m=self.module,
                              nTeeth=self.nTeeth2,
                              evolvStep=self.evolvStep,
                              filletCurveStep=self.filletCurveStep,
                              tStep=self.tStep,
                              bStep=self.bStep,
                              prezureAngle=self.angle,
                              shiftX=self.shiftX2,
                              width=self.width,
                              widthStep=self.widthStep,
                              skewAng=-self.skewness*(self.nTeeth1/self.nTeeth2),
                              angCon=angcon2,
                              angZ=pi - pi/self.nTeeth2 )
        base2 = create_mesh_obj(context, mesh2)        
        ob2 = bpy.context.active_object
        ob2['type'] = "bevel"
        ob2['module'] = self.module
        ob2['nTeeth'] = self.nTeeth2
        ob2['shaftAng'] = self.angShaft
        ob2['skewAng'] = -self.skewness*(self.nTeeth1/self.nTeeth2)
        ob2.rotation_euler.y = -self.angShaft
        ob2.location.z = origZ
        ob2.rotation_euler.z = self.rotAng       
        return {'FINISHED'}