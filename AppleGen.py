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
    return copy


def bend_object(ob, bend_degree):
    #bpy.ops.object.parent_clear(type='CLEAR')
    bpy.ops.object.modifier_add(type="SIMPLE_DEFORM")
    simple_deform_modifier = ob.modifiers["SimpleDeform"]
    simple_deform_modifier.deform_method = "BEND"
    simple_deform_modifier.angle = bend_degree
    simple_deform_modifier.deform_axis = random.choice(['X', 'Y'])
    #print(ob.data.users)
    ob.data = ob.data.copy()
    bpy.ops.object.modifier_apply(modifier=simple_deform_modifier.name)


def change_noise(ob, mat, NoiseName, noise_scale):
    copyMat = mat.copy()
    copyMat.use_nodes = True
    copyMat.node_tree.nodes.active
    copyMat.node_tree.nodes[NoiseName].inputs[
        "Scale"].default_value = noise_scale
    print(copyMat.node_tree.nodes[NoiseName].inputs["Scale"].default_value)
    ob.data.materials[0] = copyMat


def change_ColorRamp(ob, matName, ColorRampName):
    copyMat = bpy.data.materials[matName].copy()
    copyMat.use_nodes = True
    copyMat.node_tree.nodes.active
    cr = copyMat.node_tree.nodes[ColorRampName].color_ramp
    for i in range(1, len(cr.elements)):
        cr.elements[i].position = cr.elements[i].position + random.uniform(
            -0.1, 0.15)
    ob.data.materials[0] = copyMat
    #cr.elements[2].color = (0, 0, 0, 1)


def displace(ob, Midlevel, Strength, DisplaceSize, DisplaceNoiseDepth):

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

    bpy.context.active_object.modifiers[-1].texture = texture
    ob.data = ob.data.copy()
    #bpy.ops.object.modifier_apply(modifier=modif.name)


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

            Stripes = random.uniform(20, 30)
            BigSpot = random.uniform(5, 10)
            SmallSpot = random.uniform(800, 1000)
            injuty = random.uniform(30, 250)

            C = bpy.context
            coll = C.collection
            #copy = ob
            #copy.matrix_world = Matrix.Translation(vec) @ copy.matrix_world
            copy = dupe_move_ob(coll, ob, vec)

            displace(copy, Midlevel, Strength, DisplaceSize,
                     DisplaceNoiseDepth)

            NoiseName = 'Noise Texture'
            NoiseName1 = 'Noise Texture.001'
            NoiseName2 = 'Noise Texture.002'
            NoiseName3 = 'Noise Texture.003'

            matName = 'Apple'
            ColorRampName = 'ColorRamp.001'
            change_ColorRamp(copy, matName, ColorRampName)

            change_noise(copy, copy.data.materials[0], NoiseName, Stripes)
            change_noise(copy, copy.data.materials[0], NoiseName1, BigSpot)
            change_noise(copy, copy.data.materials[0], NoiseName2, SmallSpot)
            change_noise(copy, copy.data.materials[0], NoiseName3, injuty)
            #change_color(copy, copy.data.materials, brCont)

            z = random.uniform(0.9, 1)
            x = random.uniform(0.9, 1)

            print(x)
            print(z)
            copy.scale = (x, z, x)
            pose_y += matrixShift


deselect_scene()

ob_name = "Apple2"
obTuber = bpy.context.scene.objects[ob_name]
matrixSizeY = 3
matrixSizeX = 2
matrixShift = obTuber.dimensions.x + obTuber.dimensions.x / 5

gen_apple(obTuber, matrixSizeY, matrixSizeX, matrixShift)
