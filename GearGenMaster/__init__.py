bl_info = {
    "name": "GearGenMaster",
    "author": "Sergey Drachev",
    "version": (0, 1, 0),
    "blender": (2, 78, 1),
    "location": "View3D > Add > Mesh",
    "description": "Add gears",
    "warning": "",
    "category": "Add Mesh",
}

if "bpy" in locals():
    import importlib
    importlib.reload(GearGen)
    print("GearGen: Reloaded multifiles")
else:
    from GearGen import GearGen
    print("GearGen: Imported multifiles")
import bpy
     
    #////////////////////////////////////////////////////////////////////////////////     
def menu_function(self, context):
    
    self.layout.menu(GearGen.Geargen_add.bl_idname, text="GearGenMaster", icon="SCRIPTWIN")    

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_function)


def unregister():    
    bpy.types.INFO_MT_mesh_add.remove(menu_function)
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
