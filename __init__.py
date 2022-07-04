from ntpath import join
import os
import bpy
from bpy.props import EnumProperty
#import AppleGen

bpr = bpy.props
data_for_enum = []
#Путь до папки с аддоном
path = os.getcwd(
) + '/' + bpy.app.version_string[0:4] + '/scripts/addons/fruit_gen/'
path = path.replace('\\', '/')

bl_info = {
    "name": "Apples generator",
    "author": "Alisa Fedorova",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "Viev3D > N panel > Apples",
    "description": "Apples variations generator",
    "category": "Object",
}


def add_items_from_collection(self, context):
    coll_name = "Apples"
    enum_items = []
    if coll_name not in bpy.data.collections:
        with bpy.data.libraries.load(path + 'Apple.blend', False,
                                     True) as (data_from, data_to):
            print(data_from.collections)
            data_to.collections = data_from.collections
    col_obj = bpy.data.collections[coll_name].objects
    #print(bpy.data.collections[coll_name].objects)
    for e, obj in enumerate(col_obj):

        enum_items.append((col_obj[e].name, col_obj[e].name, '', e))

    #print(enum_items)
    return enum_items


class GenerateShader(bpy.types.Operator):

    def execute(self, context):

        return {'FINISHED'}


PROPS = [
    ('apple_kind',
     bpy.props.EnumProperty(name='Kind of apple',
                            items=add_items_from_collection,
                            default=None)),
    ('location',
     bpy.props.EnumProperty(name='Location',
                            items=[('horizontally', 'Horizontally', '', 0),
                                   ('vertically', 'Vertically', '', 1)])),
    ('apple_number',
     bpy.props.IntProperty(name='Apple number:', default=2, min=1)),
    ('subdiv_level',
     bpy.props.IntProperty(name='Subdivision level:', default=2, min=0,
                           max=6)),
]


class ObjGeneratorOperator(bpy.types.Operator):
    bl_idname = 'opr.apples_generator_operator'
    bl_label = 'Object Generator Operator'
    bl_description = 'Generate apples variations'

    def execute(self, context):
        print()
        '''
        AppleGen.deselect_scene()

        ob_name = "Apple2"
        obTuber = bpy.context.scene.objects[ob_name]
        matrixSizeY = 3
        matrixSizeX = 2
        matrixShift = obTuber.dimensions.x + obTuber.dimensions.x / 5
        '''
        #gen_apple(obTuber, matrixSizeY, matrixSizeX, matrixShift)

        return {'FINISHED'}


class ObjGeneratorPanel(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_example_panel'
    bl_label = 'Apples generator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Apples"

    def draw(self, context):
        l = self.layout
        col = l.column()

        for (prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
        l.split()
        l.operator('opr.apples_generator_operator', text='Generate')  # OK


class ObjGetter(bpy.types.PropertyGroup):

    apple_kind: EnumProperty(name='Kind of apple',
                             items=add_items_from_collection)


CLASSES = [
    ObjGeneratorOperator,
    ObjGetter,
    ObjGeneratorPanel,
]


def register():

    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    for klass in CLASSES:
        bpy.utils.register_class(klass)

    #bpy.types.Scene.apple_props = bpy.props.PointerProperty(type=ObjGetter)


def unregister():

    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

    #del bpy.types.Scene.apple_props


if __name__ == '__main__':
    register()

# with numerous objects selected, if you want to prevent their selection 'en masse'
#for i in bpy.context.selected_objects:
#    i.hide_select = True