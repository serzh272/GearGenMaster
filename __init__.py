bl_info = {
    "name": "GearGenMaster",
    "author": "Sergey Drachev",
    "version": (0, 1, 7),
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



# ////////////////////////////////////////////////////////////////////////////////    
def menu_func_gear(self, context):
    layout = self.layout
    layout.separator()
    oper = layout.operator(GearGenMaster.AddGear.bl_idname, text="GearGenMaster", icon_value=custom_icons["spur_icon"].icon_id)
    oper.ggm_change = False

classes = (
)

def register():
    load_icons()
    if bpy.app.version >= (2, 80, 0):
        from bpy.utils import register_class
        for cls in classes:
            register_class(cls)
        GearGenMaster.register()
        bpy.types.VIEW3D_MT_mesh_add.append(menu_func_gear)
    else:
        bpy.utils.register_module(__name__)
        bpy.types.INFO_MT_mesh_add.append(menu_func_gear)

def unregister():
    if bpy.app.version >= (2, 80, 0):
        bpy.types.VIEW3D_MT_mesh_add.remove(menu_func_gear)
        GearGenMaster.unregister()
        from bpy.utils import unregister_class
        for cls in reversed(classes):
            unregister_class(cls)
    else:
        bpy.types.INFO_MT_mesh_add.remove(menu_func_gear)
        bpy.utils.unregister_module(__name__)
    global custom_icons
    unload_icons()


if __name__ == "__main__":
    register()