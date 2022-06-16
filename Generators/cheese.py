import bpy
import sys
import random
from mathutils import Matrix

#print(os.path.abspath(__file__))

if not 'D:\\ВКР\\Project\\Generators' in sys.path:
    sys.path.append('D:\\ВКР\\Project\\Generators')

import radish
#from radish import change_noise


def change_noise(ob, mat, NoiseName, noise_scale):
    mat.use_nodes = True
    mat.node_tree.nodes.active
    mat.node_tree.nodes[NoiseName].inputs["Scale"].default_value = noise_scale
    ob.data.materials[0] = mat


def dupe_move_ob(coll, ob, vec):
    copy = ob.copy()
    copy.matrix_world = Matrix.Translation(vec) @ copy.matrix_world
    coll.objects.link(copy)
    bpy.context.view_layer.objects.active = copy
    copy.data.make_local()
    ob.select_set(False)
    copy.data = copy.data.copy()
    return copy


def gen_cheese(ob, matrixSizeY, matrixSizeX, matrixShift):
    pose_x = 0
    for y in range(0, matrixSizeY):
        pose_x += matrixShift
        pose_y = 0
        for x in range(0, matrixSizeX):

            vec = (-pose_x, pose_y, 0)

            C = bpy.context
            coll = C.collection
            copy = dupe_move_ob(coll, ob, vec)

            brCont = random.uniform(-0.05, 0.05)
            SmallSpot = random.uniform(-5, 5)

            NoiseName2 = "Voronoi Texture"
            brightName = "Bright/Contrast"

            ob.data.materials[0] = radish.change_bright(
                copy, copy.data.materials[0], brightName, brCont)

            radish.change_noise(copy, copy.data.materials[0], NoiseName2,
                                SmallSpot)

            z = random.uniform(0.9, 1)
            x = random.uniform(0.9, 1)
            y = random.uniform(0.9, 1)

            ob.scale = (x, z, y)
            pose_y += matrixShift


radish.deselect_scene()

ob_name = "CheeseSlice"
obTuber = bpy.context.scene.objects[ob_name]
matrixSizeY = 5
matrixSizeX = 1
matrixShift = obTuber.dimensions.x + obTuber.dimensions.x / 5

gen_cheese(obTuber, matrixSizeY, matrixSizeX, matrixShift)
