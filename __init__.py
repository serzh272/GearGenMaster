bl_info = {
    "name": "GearGenMaster",
    "author": "Sergey Drachev",
    "version": (0, 1, 6),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh",
    "description": "Add gears",
    "warning": "",
    "category": "Add Mesh",
}

if "bpy" in locals():
    import importlib

    importlib.reload(GearGenMaster)
    print("GearGen: Reloaded multifiles")
else:
    import bpy
    if bpy.app.version >= (2, 80, 0):
        from . import GearGenMaster
    else:
        from . import GearGenMaster_2_79 as GearGenMaster

    print("GearGen: Imported multifiles")
import bpy, os, sys


def load_icons():
    global custom_icons
    import bpy.utils.previews
    custom_icons = bpy.utils.previews.new()
    path = os.path.join(os.path.dirname(__file__), "icons", "gears.png")
    custom_icons.load("geargen_icon", path, 'IMAGE')
    path = os.path.join(os.path.dirname(__file__), "icons", "spur.png")
    custom_icons.load("spur_icon", path, 'IMAGE')
    path = os.path.join(os.path.dirname(__file__), "icons", "internal.png")
    custom_icons.load("internal_icon", path, 'IMAGE')
    path = os.path.join(os.path.dirname(__file__), "icons", "bevel.png")
    custom_icons.load("bevel_icon", path, 'IMAGE')
    path = os.path.join(os.path.dirname(__file__), "icons", "worm.png")
    custom_icons.load("worm_icon", path, 'IMAGE')


def unload_icons():
    global custom_icons
    bpy.utils.previews.remove(custom_icons)


class Geargen_add(bpy.types.Menu):
    bl_idname = "mesh.GearGenMaster"
    bl_label = "GearGenMaster"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_spur_gear_add",
                        text="Add Spur Gear", icon_value=custom_icons["spur_icon"].icon_id)
        layout.operator("mesh.primitive_rack_add",
                        text="Add Rack")
        layout.operator("mesh.primitive_herringbone_gear_add",
                        text="Add Herringbone Gear", icon_value=custom_icons["spur_icon"].icon_id)
        layout.operator("mesh.primitive_internal_gear_add",
                        text="Add Internal Gear", icon_value=custom_icons["internal_icon"].icon_id)
        layout.operator("mesh.primitive_bevel_gear_add",
                        text="Add Bevel Gears", icon_value=custom_icons["bevel_icon"].icon_id)
        layout.operator("mesh.primitive_worm_add",
                        text="Add worm drive", icon_value=custom_icons["worm_icon"].icon_id)


# ////////////////////////////////////////////////////////////////////////////////
def menu_function(self, context):
    global custom_icons
    self.layout.menu(Geargen_add.bl_idname, text="GearGenMaster", icon_value=custom_icons["geargen_icon"].icon_id)
    
def menu_func_gear(self, context):
    layout = self.layout
    layout.separator()
    oper = layout.operator(GearGenMaster.AddGear.bl_idname, text="GearGenMaster (test)", icon_value=custom_icons["geargen_icon"].icon_id)
    oper.ggm_change = False

classes = (
    Geargen_add,
)

def register():
    load_icons()
    if bpy.app.version >= (2, 80, 0):
        from bpy.utils import register_class
        for cls in classes:
            register_class(cls)
        GearGenMaster.register()
        bpy.types.VIEW3D_MT_mesh_add.append(menu_func_gear)
        bpy.types.VIEW3D_MT_mesh_add.append(menu_function)
    else:
        bpy.utils.register_module(__name__)
        bpy.types.INFO_MT_mesh_add.append(menu_function)

def unregister():
    if bpy.app.version >= (2, 80, 0):
        bpy.types.VIEW3D_MT_mesh_add.remove(menu_func_gear)
        bpy.types.VIEW3D_MT_mesh_add.remove(menu_function)
        GearGenMaster.unregister()
        from bpy.utils import unregister_class
        for cls in reversed(classes):
            unregister_class(cls)
    else:
        bpy.types.INFO_MT_mesh_add.remove(menu_function)        
        bpy.utils.unregister_module(__name__)
    global custom_icons
    unload_icons()


if __name__ == "__main__":
    register()