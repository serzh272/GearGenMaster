import bpy
from builtins import range
from mathutils import Vector, Euler, Matrix
from math import sin, radians, cos, pi, atan
from bpy.props import IntProperty, FloatProperty, EnumProperty, BoolProperty
from . import addMesh

GearParameters = [
    "ggm_Type",
    "ggm_External_Type",
    "ggm_nTeeth",
    "ggm_module",
    "ggm_width",
    "ggm_diam_hole",
    "ggm_widthStep",
    "ggm_skewness",
    "ggm_evolvStep",
    "ggm_filletCurveStep",
    "ggm_tStep",
    "ggm_bStep",
    "ggm_shiftX",
    "ggm_c",
    "ggm_angle",
    "ggm_angCon",
    "ggm_angShaft",
    "ggm_rotAng",
    "ggm_driver",
    "ggm_fill_holes",
    "ggm_tw",
    "ggm_wType",
    "ggm_dWorm",
    "ggm_rezWorm",
    "ggm_nTWorm",
    "ggm_isHerringbone",
        ]

class AddGear(bpy.types.Operator):
    """Add a gear mesh"""
    bl_idname = "mesh.new_operator"
    bl_label = "New operator"
    bl_options = {'REGISTER', 'UNDO'}
    ggm_change : BoolProperty(name = "Change",
                default = False,
                description = "change Gear")
    is_pair : BoolProperty(name = "is_pair",
                default = False,
                description = "add pair of gear")
    gearTypeList = [('ggm_internal','INTERNAL','Internal gear'),
                    ('ggm_external', 'EXTERNAL', 'External gear'),
                    ('ggm_worm','WORM','Worm drive')]
    ggm_Type : EnumProperty(attr='ggm_Type',
                            name='Type',
                            description='Choose type of gear',
                            items=gearTypeList,
                            options={'SKIP_SAVE'},
                            default='ggm_external')
    externalGearList = [('ggm_ext_rack','RACK','Rack'),
                        ('ggm_ext_spur','SPUR','Spur Gear'),
                        ('ggm_ext_bevel','BEVEL','Bevel Gear'),
                        ('ggm_ext_worm_gear','WORM GEAR','Worm Gear')]
    ggm_External_Type : EnumProperty(attr='ggm_External_Type',
                            name='External Gear Type',
                            description='Choose type of external gear',
                            items=externalGearList,
                            options={'SKIP_SAVE'},
                            default='ggm_ext_spur')    
    ggm_nTeeth : IntProperty(name="Z",
                         description="Number of teeth",
                         min=6,
                         options={'SKIP_SAVE'},
                         default=12)
    ggm_nTeeth2 : IntProperty(name="Z2",
                         description="Number of teeth",
                         min=6,
                         options={'SKIP_SAVE'},
                         default=12)
    ggm_module : FloatProperty(name="Module",
                           description="Module of the gear",
                           min=0.05,
                           max=100.0,
                           unit='LENGTH',
                           default=0.2)
    ggm_width : FloatProperty(name="Width",
                          description="Width of the gear",
                          min=0.1,
                          max=100.0,
                          unit='LENGTH',
                          default=0.5)
    ggm_diam_hole : FloatProperty(name="Hole Diameter",
                          description="Diameter of hole",
                          min=0.0,
                          unit='LENGTH',
                          default= 1.0)
    ggm_widthStep : IntProperty(name="Width Step",
                            description="Definition of the width of teeth",
                            min=1,
                            max=30,
                            default=1)
    ggm_skewness : FloatProperty(name="Skewness",
                             description="Skewness of the teeth",
                             min=radians(-90),
                             max=radians(90),
                             options={'SKIP_SAVE'},
                             unit='ROTATION',
                             default=0.0)
    ggm_evolvStep : IntProperty(name="Def. of evolute",
                            description="Definition of the evolute",
                            min=3,
                            max=30,
                            default=3)
    ggm_filletCurveStep : IntProperty(name="Def. of fillet curve",
                                  description="Definition of the fillet curve",
                                  min=3,
                                  max=30,
                                  default=3)
    ggm_tStep : IntProperty(name="Def. of top land",
                        description="Definition of the top land",
                        min=1,
                        max=30,
                        options={'SKIP_SAVE'},
                        default=3)
    ggm_bStep : IntProperty(name="Def. of bottom land",
                        description="Definition of the bottom land",
                        min=1,
                        max=30,
                        options={'SKIP_SAVE'},
                        default=1)
    ggm_shiftX : FloatProperty(name="ShiftX",
                           description="Shift of the profile",
                           min=-4.000,
                           max=4.000,
                           precision=3,
                           options={'SKIP_SAVE'},
                           step=0.1,
                           unit='LENGTH',
                           default=0.000)
    ggm_c : FloatProperty(name="C",
                      description="Tip and Root Clearance",
                      min=0.0,
                      max=1.0,
                      precision=2,
                      options={'SKIP_SAVE'},
                      step=0.01,
                      unit='LENGTH',
                      default=0.25)
    ggm_angle : FloatProperty(name="Pressure Angle",
                          description="Pressure angle, skewness of tooth tip",
                          min=0.0,
                          max=radians(45.0),
                          unit='ROTATION',
                          default=radians(20.0))
    ggm_angCon : FloatProperty(name="Cone Angle",
                          description="Cone Angle of Bevel Gear",
                          min=0.0,
                          max=radians(180.0),
                          unit='ROTATION',
                          default=radians(0.0))
    ggm_rotAng : FloatProperty(name="Rotation Angle",
                           description="Rotation Angle Of Gear",
                           options={'SKIP_SAVE'},
                           unit='ROTATION',
                           default=radians(0.0))
    ggm_angShaft : FloatProperty(name="Shafts angle",
                             description="Angle between shafts",
                             min=radians(1),
                             max=radians(179),
                             options={'SKIP_SAVE'},
                             unit='ROTATION',
                             default=radians(90))
    ggm_driver : BoolProperty(name="Add Driver",
                          description="Add Driver to Gear",
                          options={'SKIP_SAVE'},
                          default=False)
    ggm_isHerringbone : BoolProperty(name="Is HerringBone",
                          description="Is HerringBone",
                          options={'SKIP_SAVE'},
                          default=False)
    ggm_fill_holes : BoolProperty(name="Fill Holes",
                          description="Fill Holes",
                          options={'SKIP_SAVE'},
                          default=True)
    ggm_tw : FloatProperty(name="Tooth Width",
                           description="Width of Tooth",
                           min=0.0,
                           max=1.0,
                           unit='NONE',
                           default=1.0)
    wormTypeList = [('wt_cylindrical', 'Cylindrical', 'Cylindrical worm'),
                    ('wt_globoid_2', 'Globoid Worm (involute)', 'Globoid worm (involute)'), 
                    ('wt_globoid_1', 'Globoid (simple)', 'Simple Globoid Worm')]
    ggm_wType : EnumProperty(name='Worm Type',
                         description='Choose the type of worm',
                         items=wormTypeList, default='wt_globoid_2')
    ggm_dWorm : FloatProperty(name="Diameter of worm",
                          description="Diameter of worm",
                          min=1,
                          unit='LENGTH',
                          default=1)
    ggm_rezWorm : IntProperty(name="rezolution of worm",
                          description="rezolution of worm",
                          min=16,
                          default=16)
    ggm_nTWorm : IntProperty(name="nTeeth of worm",
                         description="nTeeth of worm",
                         min=2,
                         max=16,
                         default=4)
    def draw(self, context):
        layout = self.layout        
        col = layout.column(align=True)
        if self.ggm_change != True:
            col.prop(self, 'ggm_Type')        
            if self.ggm_Type == 'ggm_internal':
                pass
            elif self.ggm_Type == 'ggm_external':
                col.prop(self, 'ggm_External_Type')
            else:
                col.prop(self, 'ggm_wType')        
        if self.ggm_Type == 'ggm_external' and self.ggm_External_Type == 'ggm_ext_bevel':
            if not self.is_pair:
                split = layout.split()
                col = split.column()
                sub = col.column(align=True)
                sub.label(text="Pinion:")
                sub.prop(self, 'ggm_nTeeth')
                col = split.column()
                sub = col.column(align=True)
                sub.label(text="Gear:")
                sub.prop(self, 'ggm_nTeeth2')
                col = layout.column(align=True)            
        else:            
            col.prop(self, 'ggm_nTeeth')
        if self.ggm_Type == 'ggm_worm':
            col.prop(self, 'ggm_nTWorm')
        else:
            col.prop(self, 'ggm_tw')
        if not self.is_pair:
            col.prop(self, 'ggm_module')
            col.prop(self, 'ggm_angle')
        col.prop(self, 'ggm_c')
        if self.ggm_Type != 'ggm_worm':
            col.prop(self, 'ggm_width')
            col.prop(self, 'ggm_widthStep')
        else:
            col.prop(self, 'ggm_dWorm')        
        col.prop(self, 'ggm_evolvStep')
        col.prop(self, 'ggm_filletCurveStep')
        if self.ggm_Type != 'ggm_worm':
            col.prop(self, 'ggm_tStep')
            col.prop(self, 'ggm_bStep')
            col.prop(self, 'ggm_diam_hole')
            col.prop(self, 'ggm_rotAng')
            if not self.is_pair:
                col.prop(self, 'ggm_skewness')
            if self.ggm_Type != 'ggm_external' or self.ggm_External_Type != 'ggm_ext_bevel':
                if not self.is_pair:
                    col.prop(self, 'ggm_isHerringbone')
        else:
            col.prop(self, 'ggm_rezWorm')
        if self.ggm_Type == 'ggm_external' and self.ggm_External_Type == 'ggm_ext_bevel':
            if not self.is_pair:
                col.prop(self, 'ggm_angShaft')

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        world_matr = Matrix.Translation(bpy.context.scene.cursor.location)
        rA = 0.0
        self.ggm_angCon = 0.0
        self.is_pair = False
        if self.ggm_Type == 'ggm_external':
            if self.ggm_External_Type == 'ggm_ext_bevel':
                if self.ggm_angShaft != 0.0 and self.ggm_angShaft != pi:            
                    self.ggm_angCon = pi / 2 - atan((self.ggm_nTeeth2 / self.ggm_nTeeth + cos(self.ggm_angShaft)) / sin(self.ggm_angShaft))
                world_matr @= Matrix.Translation((0,0,addMesh.GearFuncs.getOriginZ(self.ggm_module, self.ggm_nTeeth, 'ggm_ext_bevel', self.ggm_shiftX,
                                                                                    self.ggm_angCon) + 1.75 * self.ggm_module * sin(self.ggm_angCon)))
        prBase = self.ggm_width * sin(self.ggm_angCon)
        radRef = addMesh.GearFuncs.getRefDiam(self.ggm_module, self.ggm_nTeeth) / 2 + self.ggm_shiftX
        if self.ggm_Type != 'ggm_internal':
            diamHoleMax = addMesh.GearFuncs.getRootDiam(self.ggm_module * (1 - prBase / radRef), self.ggm_nTeeth, self.ggm_c) - 2 * self.ggm_module + 2 * self.ggm_shiftX
            if self.ggm_diam_hole > diamHoleMax:
                self.ggm_diam_hole = diamHoleMax
        else:
            diamHoleMax = addMesh.GearFuncs.getTipDiam(self.ggm_module * (1 - prBase / radRef), self.ggm_nTeeth) + 2 * self.ggm_module + 2 * self.ggm_shiftX
            if self.ggm_diam_hole < diamHoleMax:
                self.ggm_diam_hole = diamHoleMax
        if bpy.context.mode == "OBJECT":            
            mesh = addMesh.createMesh(self, context)
            if context.selected_objects != [] and context.active_object and ('ggm_Type' in context.active_object.data.keys()):
                obAct = context.active_object
                if (self.ggm_change == True):                    
                    oldmesh = obAct.data
                    oldmeshname = obAct.data.name
                    obAct.data = mesh
                    for mtl in oldmesh.materials:
                        obAct.data.materials.append(mtl)
                    bpy.data.meshes.remove(oldmesh)
                    obAct.data.name = oldmeshname
                    for prm in GearParameters:
                        if prm in obAct.data:
                            obAct.data[prm] = getattr(self, prm)
                else:                    
                    w_matr = obAct.matrix_world
                    if obAct.data["ggm_Type"] == 'ggm_internal':
                        if self.ggm_Type == 'ggm_external':
                            if self.ggm_External_Type == 'ggm_ext_spur':                                
                                self.is_pair = True
                                self.ggm_isHerringbone = obAct.data["ggm_isHerringbone"]
                                r = (self.ggm_module * self.ggm_nTeeth - self.ggm_module * obAct.data['ggm_nTeeth']) / 2 - self.ggm_shiftX
                                self.ggm_skewness = obAct.data['ggm_skewness'] * (obAct.data['ggm_nTeeth'] / self.ggm_nTeeth)
                                world_matr = w_matr @ Matrix.Translation((-r * cos(self.ggm_rotAng), -r * sin(self.ggm_rotAng), 0)) @ Matrix.Rotation(obAct.data['ggm_rotAng'] * obAct.data['ggm_nTeeth'] / self.ggm_nTeeth - self.ggm_rotAng * obAct.data['ggm_nTeeth'] / self.ggm_nTeeth, 4, 'Z')
                    elif obAct.data["ggm_Type"] == 'ggm_external':
                        if obAct.data["ggm_External_Type"] == 'ggm_ext_spur':                            
                            if self.ggm_Type == 'ggm_external':
                                if self.ggm_External_Type == 'ggm_ext_spur':
                                    self.is_pair = True
                                    self.ggm_isHerringbone = obAct.data["ggm_isHerringbone"]
                                    r = (self.ggm_module * obAct.data['ggm_nTeeth'] + self.ggm_module * self.ggm_nTeeth) / 2 + self.ggm_shiftX + obAct.data['ggm_shiftX']
                                    rA = pi - pi / self.ggm_nTeeth + self.ggm_rotAng * obAct.data['ggm_nTeeth'] / self.ggm_nTeeth + self.ggm_rotAng - (obAct.data['ggm_rotAng'])* \
                                        obAct.data['ggm_nTeeth'] / self.ggm_nTeeth
                                    self.ggm_skewness = -obAct.data['ggm_skewness'] * (obAct.data['ggm_nTeeth'] / self.ggm_nTeeth)
                                    world_matr = w_matr @ Matrix.Translation((r * cos(self.ggm_rotAng), r * sin(self.ggm_rotAng), 0)) @ Matrix.Rotation(rA-self.ggm_rotAng, 4, 'Z')
                                elif self.ggm_External_Type == 'ggm_ext_rack':
                                    self.is_pair = True
                                    self.ggm_isHerringbone = obAct.data["ggm_isHerringbone"]
                                    r = self.ggm_module * obAct.data['ggm_nTeeth'] / 2 + obAct.data['ggm_shiftX']
                                    rA = pi - pi / self.ggm_nTeeth + self.ggm_rotAng * obAct.data['ggm_nTeeth'] / self.ggm_nTeeth + self.ggm_rotAng - obAct.data['ggm_rotAng'] * \
                                        obAct.data['ggm_nTeeth'] / self.ggm_nTeeth
                                    self.ggm_skewness = obAct.data['ggm_skewness']*obAct.data["ggm_dRef"]/2
                                    world_matr = w_matr @ Matrix.Translation((r * (cos(self.ggm_rotAng) + self.ggm_rotAng * sin(self.ggm_rotAng)), r * (sin(self.ggm_rotAng) - self.ggm_rotAng * cos(self.ggm_rotAng)), 0)) @ Matrix.Rotation(self.ggm_rotAng, 4, 'Z') @ Matrix.Translation((0, (obAct.data['ggm_rotAng']%(2*pi/obAct.data['ggm_nTeeth']))*obAct.data["ggm_dRef"]/2, 0)) 
                            elif self.ggm_Type == 'ggm_internal':
                                self.is_pair = True
                                self.ggm_isHerringbone = obAct.data["ggm_isHerringbone"]
                                r = (self.ggm_module * self.ggm_nTeeth - self.ggm_module * obAct.data['ggm_nTeeth']) / 2 - self.ggm_shiftX
                                self.ggm_skewness = obAct.data['ggm_skewness'] * (obAct.data['ggm_nTeeth'] / self.ggm_nTeeth)
                                world_matr = w_matr @ Matrix.Translation((-r * cos(self.ggm_rotAng), -r * sin(self.ggm_rotAng), 0)) @ Matrix.Rotation(obAct.data['ggm_rotAng'] * obAct.data['ggm_nTeeth'] / self.ggm_nTeeth - self.ggm_rotAng * obAct.data['ggm_nTeeth'] / self.ggm_nTeeth, 4, 'Z')
                        elif obAct.data["ggm_External_Type"] == 'ggm_ext_bevel':
                            if self.ggm_Type == 'ggm_external':
                                if self.ggm_External_Type == 'ggm_ext_bevel':
                                    self.is_pair = True
                                    self.ggm_angShaft = obAct.data['ggm_angShaft']
                                    self.ggm_nTeeth = obAct.data['ggm_nTeeth2']
                                    self.ggm_angCon = pi / 2 - atan((obAct.data['ggm_nTeeth'] / self.ggm_nTeeth + cos(self.ggm_angShaft)) / sin(self.ggm_angShaft))
                                    world_matr = w_matr @ Matrix.Rotation(- pi / obAct.data['ggm_nTeeth'], 4, 'Z') @ Matrix.Rotation(-self.ggm_angShaft, 4, 'Y')
                        elif obAct.data["ggm_External_Type"] == 'ggm_ext_rack':
                            if self.ggm_Type == 'ggm_external':
                                if self.ggm_External_Type == 'ggm_ext_spur':
                                    self.is_pair = True
                                    self.ggm_isHerringbone = obAct.data["ggm_isHerringbone"]
                                    r = self.ggm_module * self.ggm_nTeeth / 2 + self.ggm_shiftX
                                    world_matr = w_matr @ Matrix.Translation((-r, self.ggm_rotAng*addMesh.GearFuncs.getRefDiam(self.ggm_module, self.ggm_nTeeth)/2, 0)) @ Matrix.Rotation(-self.ggm_rotAng*2, 4, 'Z')
                        else:
                            pass
                    else:
                        pass
            else:                
                skewness = self.ggm_skewness
                self.is_pair = False
            if self.ggm_change != True:
                mesh = addMesh.createMesh(self, context)
                base = addMesh.GearFuncs.create_mesh_obj(context, mesh)
                ob = bpy.context.active_object
                ob.matrix_world = world_matr

                if self.ggm_driver == True:
                    obDrive = ob.driver_add("rotation_euler", 2)
                    obDrive.driver.type = 'SCRIPTED'
                    rotvar = obDrive.driver.variables.new()
                    rotvar.name = 'rotSpur'
                    rotvar.type = 'TRANSFORMS'
                    rotvar.targets[0].transform_type = 'ROT_Z'
                    rotvar.targets[0].transform_space = 'WORLD_SPACE'
                    rotvar.targets[0].id = ob
                    obDrive.driver.expression = "-rotSpur/" + str(self.ggm_nTeeth/obAct.data['ggm_nTeeth'])
        return {'FINISHED'}

    def invoke(self, context, event):
        self.execute(context)        
        return {'FINISHED'}

def Gear_contex_menu(self, context):
    bl_label = 'Change'

    ob = context.object
    layout = self.layout

    if 'ggm_Type' in ob.data.keys():
        props = layout.operator("mesh.new_operator", text="Edit Gear")
        props.ggm_change = True
        for prm in GearParameters:
            if prm in ob.data:
                setattr(props, prm, ob.data[prm])
        layout.separator()


classes = (
    AddGear,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(Gear_contex_menu)

def unregister():    
    from bpy.utils import unregister_class
    bpy.types.VIEW3D_MT_object_context_menu.remove(Gear_contex_menu)
    for cls in reversed(classes):
        unregister_class(cls)