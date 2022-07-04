import bpy
import random
from mathutils import Matrix


def deselect_scene():
    return bpy.ops.object.select_all(action='DESELECT')


def dupe_move_ob(coll, ob, vec):
    copy = ob.copy()

    copy.matrix_world = Matrix.Translation(vec) @ copy.matrix_world

    coll.objects.link(copy)
    bpy.context.view_layer.objects.active = copy
    copy.data.make_local()
    ob.select_set(False)
    copy.data = copy.data.copy()

    copyMat = copy.data.materials[0]
    single_user_mat = copyMat.copy()
    copyMat = single_user_mat
    copy.data.materials[0] = copyMat

    #obj = bpy.context.scene.objects.get("Gala")
    copy.material_slots[0].material.node_tree.nodes[
        'AppleMatGroup'].node_tree = copy.material_slots[
            0].material.node_tree.nodes['AppleMatGroup'].node_tree.copy()
    #print(original_group)
    #original_group = original_group.copy()
    #print(original_group)
    #print(copy.material_slots[0].material.node_tree.nodes['AppleMatGroup'].node_tree)
    #original_group = single_user_group
    return copy


def subdiv_object(ob, sub_degree):
    bpy.ops.object.modifier_add(type="SUBSURF")
    subdivision_modifier = ob.modifiers["Subdivision"]
    subdivision_modifier.levels = sub_degree
    #ob.data = ob.data.copy()
    bpy.ops.object.modifier_apply(modifier=subdivision_modifier.name)


def bend_object(ob, bend_degree, vert_group):
    #bpy.ops.object.parent_clear(type='CLEAR')
    bpy.ops.object.modifier_add(type="SIMPLE_DEFORM")
    simple_deform_modifier = ob.modifiers["SimpleDeform"]
    simple_deform_modifier.vertex_group = vert_group
    simple_deform_modifier.deform_method = "BEND"
    simple_deform_modifier.angle = bend_degree
    simple_deform_modifier.deform_axis = random.choice(['X', 'Y'])

    #print(ob.data.users)
    #ob.data = ob.data.copy()
    bpy.ops.object.modifier_apply(modifier=simple_deform_modifier.name)


def change_ColorRamp(ob, ColorRampName):
    copyMat = ob.data.materials[0].copy()
    ob.data.materials[0] = copyMat
    ob.data.make_local()
    copyMat.node_tree.nodes.active
    cr = copyMat.node_tree.nodes['AppleMatGroup'].node_tree.nodes[
        ColorRampName].color_ramp
    for i in range(1, len(cr.elements)):
        cr.elements[i].position = cr.elements[i].position + random.uniform(
            -0.05, 0.15)
        print(cr.elements[i].position)

    #cr.elements[2].color = (0, 0, 0, 1)


def texture_modif(copy, StripeScale, PointScale, DentScale, DentStrength,
                  InjuryScale, SunSpotRotation, UpperSpotScale):

    #original_group = copy.material_slots['Material'].material.node_tree.nodes['AppleMatGroup'].node_tree
    #single_user_group = original_group.copy()
    #original_group = single_user_group

    copyMat = copy.data.materials[0]
    single_user_group = copyMat.copy()
    copyMat = single_user_group
    copy.data.materials[0] = copyMat
    #copy.data.make_local()
    copyMat.node_tree.nodes.active

    #copyNodeTree = copy.data.materials[0].node_tree

    copyMat.node_tree.nodes['AppleMatGroup'].inputs[
        'StripeScale'].default_value = StripeScale
    copyMat.node_tree.nodes['AppleMatGroup'].inputs[
        'PointScale'].default_value = PointScale
    copyMat.node_tree.nodes['AppleMatGroup'].inputs[
        'DentScale'].default_value = DentScale
    copyMat.node_tree.nodes['AppleMatGroup'].inputs[
        'DentStrength'].default_value = DentStrength
    copyMat.node_tree.nodes['AppleMatGroup'].inputs[
        'InjuryScale'].default_value = InjuryScale
    copyMat.node_tree.nodes['AppleMatGroup'].inputs[
        'SunSpotRotation'].default_value = SunSpotRotation
    copyMat.node_tree.nodes['AppleMatGroup'].inputs[
        'UpperSpotScale'].default_value = UpperSpotScale


def displace(ob, Midlevel, Strength, DisplaceSize, DisplaceNoiseDepth,
             vert_group):

    bpy.ops.texture.new()
    texture = bpy.data.textures[-1]
    texture.type = 'CLOUDS'
    bpy.data.textures[texture.name].noise_basis = 'ORIGINAL_PERLIN'
    bpy.data.textures[texture.name].noise_scale = DisplaceSize
    bpy.data.textures[texture.name].noise_depth = DisplaceNoiseDepth

    bpy.ops.object.modifier_add(type='DISPLACE')
    modif = ob.modifiers["Displace"]
    modif.mid_level = Midlevel
    modif.strength = Strength
    modif.vertex_group = vert_group

    bpy.context.active_object.modifiers[-1].texture = texture
    #ob.data = ob.data.copy()
    bpy.ops.object.modifier_apply(modifier=modif.name)


def gen_apple(ob, matrixSizeY, matrixSizeX, matrixShift):
    pose_x = 0
    for y in range(0, matrixSizeY):
        pose_x += matrixShift
        pose_y = 0
        for x in range(0, matrixSizeX):

            vec = (pose_x, pose_y, 0)

            Midlevel = random.uniform(0.45, 0.55)
            Strength = random.uniform(0, 0.05)
            DisplaceNoiseDepth = random.randint(0, 5)
            DisplaceSize = random.uniform(0.3, 1.0)
            BendScale = random.uniform(0, 0.523599)

            StripeScale = random.uniform(10, 30)
            InjuryScale = random.uniform(0, 10)
            PointScale = random.uniform(40, 50)
            DentScale = random.uniform(-2, 2)
            DentStrength = random.uniform(0, 0.3)
            SunSpotRotation = (0, random.uniform(-40,
                                                 40), random.uniform(0, 360))
            UpperSpotScale = random.uniform(2, 13)
            vert_group = 'fruit'
            sub_degree = 2

            C = bpy.context
            coll = C.collection
            copy = dupe_move_ob(coll, ob, vec)

            subdiv_object(copy, sub_degree)

            bend_object(copy, BendScale, vert_group)

            displace(copy, Midlevel, Strength, DisplaceSize,
                     DisplaceNoiseDepth, vert_group)

            #matName = 'Apple'
            ColorRampName = 'ColorRamp.003'
            '''
            texture_modif(copy, StripeScale, PointScale, DentScale,
                          DentStrength, InjuryScale, SunSpotRotation,
                          UpperSpotScale)'''

            #change_ColorRamp(copy, ColorRampName)
            #change_color(copy, copy.data.materials, brCont)

            t = random.uniform(0.8, 1.2)
            z = random.uniform(t * 0.95, t * 1.05)

            copy.scale = (t, t, t)
            copy.scale = (t, t, z)
            pose_y += matrixShift


deselect_scene()

ob_name = "Gala"
obTuber = bpy.context.scene.objects[ob_name]
matrixSizeY = 2
matrixSizeX = 1
matrixShift = obTuber.dimensions.x + obTuber.dimensions.x / 5

gen_apple(obTuber, matrixSizeY, matrixSizeX, matrixShift)
