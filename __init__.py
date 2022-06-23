from ntpath import join
import os
import bpy

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
    "location": "Object context menu",
    "description": "Apples variations generator",
    "category": "Object",
}


def add_items_from_collection(self, context):
    enum_items = []

    coll_name = "Apples"
    with bpy.data.libraries.load(path + 'Apple.blend', False,
                                 True) as (data_from, data_to):
        data_to.collections = data_from.collections[0]
        #data_to.meshes = data_from.meshes
        '''
        for i in range(len(coll_obj[0])):
            enum_items.append(
                (coll_obj.objects[i].name, coll_obj.objects[i].name, '', i))'''

        #object_names = [obj for obj in data_from.collections[coll_name].objects]
    print(enum_items)
    return enum_items


'''
def add_items_from_collection_callback(self, context):
    items = []
    scene = context.scene
    for item in scene.my_items.values():
        items.append((item.some_str, item.some_str, ""))
    return items
'''

PROPS = [
    ('apple_kind',
     bpy.props.EnumProperty(name='Kind of apple',
                            items=[('a1', 'a1', '', 0), ('a2', 'a2', '', 1)])),
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


CLASSES = [
    ObjGeneratorOperator,
    ObjGeneratorPanel,
]


def register():

    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    for klass in CLASSES:
        bpy.utils.register_class(klass)


def unregister():

    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)


if __name__ == '__main__':
    register()

# with numerous objects selected, if you want to prevent their selection 'en masse'
#for i in bpy.context.selected_objects:
#    i.hide_select = True