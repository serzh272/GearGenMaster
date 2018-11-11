bl_info = {
    "name": "GearGenMaster",
    "author": "Sergey Drachev",
    "version": (0, 1, 2),
    "blender": (2, 79, 1),
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
    from GearGenMaster import GearGenMaster

    print("GearGen: Imported multifiles")
import bpy, os, sys


def load_icons():
    global custom_icons
    import bpy.utils.previews
    custom_icons = bpy.utils.previews.new()
    mod = sys.modules["GearGenMaster"]
    abspath = os.path.abspath(sys.modules["GearGenMaster"].__file__)
    path = os.path.join(os.path.dirname(abspath), "icons", "gears.png")
    custom_icons.load("geargen_icon", path, 'IMAGE')
    path = os.path.join(os.path.dirname(abspath), "icons", "spur.png")
    custom_icons.load("spur_icon", path, 'IMAGE')
    path = os.path.join(os.path.dirname(abspath), "icons", "internal.png")
    custom_icons.load("internal_icon", path, 'IMAGE')
    path = os.path.join(os.path.dirname(abspath), "icons", "bevel.png")
    custom_icons.load("bevel_icon", path, 'IMAGE')
    path = os.path.join(os.path.dirname(abspath), "icons", "worm.png")
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


def register():
    load_icons()
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_function)


def unregister():
    bpy.types.INFO_MT_mesh_add.remove(menu_function)
    bpy.utils.unregister_module(__name__)
    global custom_icons
    unload_icons()


if __name__ == "__main__":
    register()