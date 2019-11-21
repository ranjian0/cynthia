import bpy
from .generic import PANEL_PT_test_tools
from .test_floorplan import BTOOLS_OT_test_floorplan

classes = (
    PANEL_PT_test_tools,
    BTOOLS_OT_test_floorplan
)


def register_tests():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister_tests():
    for cls in classes:
        bpy.utils.unregister_class(cls)