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
    ob.select_set(False)
    return copy

def bend_object(ob, bend_degree):
    #bpy.ops.object.parent_clear(type='CLEAR')
    bpy.ops.object.modifier_add(type = "SIMPLE_DEFORM") 
    simple_deform_modifier = ob.modifiers["SimpleDeform"]
    simple_deform_modifier.deform_method = "BEND"
    simple_deform_modifier.angle = bend_degree
    simple_deform_modifier.deform_axis = random.choice(['X','Y'])
    #print(ob.data.users)
    ob.data = ob.data.copy()
    bpy.ops.object.modifier_apply(modifier=simple_deform_modifier.name)

def taper_object(ob, taper_factor):
    bpy.ops.object.modifier_add(type = "SIMPLE_DEFORM") 
    simple_deform_modifier = ob.modifiers["SimpleDeform"]
    simple_deform_modifier.deform_method = "TAPER"
    simple_deform_modifier.factor = taper_factor
    simple_deform_modifier.deform_axis = random.choice(['X','Y','Z'])
    ob.data = ob.data.copy()
    bpy.ops.object.modifier_apply(modifier=simple_deform_modifier.name)
    
def wave_object(ob, wave_narrowness_degree):
    bpy.ops.object.modifier_add(type = "WAVE") 
    simple_deform_modifier = ob.modifiers["Wave"]
    simple_deform_modifier.height = 0.1
    simple_deform_modifier.width = 1 
    simple_deform_modifier.narrowness = wave_narrowness_degree
    ob.data = ob.data.copy()
    bpy.ops.object.modifier_apply(modifier=simple_deform_modifier.name)

def change_noise(ob,mat , noise_scale):
    copyMat = mat.copy()
    copyMat.use_nodes = True
    copyMat.node_tree.nodes.active
    copyMat.node_tree.nodes['NoiseScale'].inputs["Scale"].default_value = noise_scale
    ob.data.materials[0] = copyMat
    
def change_color(ob,mat , brCont):
    for i in range(len(mat)):
        copyMat = mat[i].copy()
        copyMat.use_nodes = True
        copyMat.node_tree.nodes.active
        copyMat.node_tree.nodes['Bright/Contrast'].inputs["Bright"].default_value = brCont
        
        ob.data.materials[i] = copyMat
    


def gen_matrix(ob,matrixSize,matrixShift,bend_div,taper_div, scale_factor):
    pose_x = 0
    for y in range(0, matrixSize):
        pose_x += matrixShift
        pose_y = 0
        for x in range(0,matrixSize):
                                   
            vec = (-pose_x,pose_y,0)
            bend_degree = (random.random()*random.choice([-1,1]))/bend_div
            wave_narrowness_degree = (random.random() + random.randint(0, 4))
            taper_factor = random.random()/taper_div
            noise_scale = random.uniform(-2, 2)
            brCont = random.uniform(-0.15, 0.02)
            
            C = bpy.context
            coll = C.collection
            copy = dupe_move_ob(coll, ob, vec)
            newV = random.random()

            bend_object(copy, bend_degree)
            taper_object(copy, taper_factor)
            #wave_object(copy, wave_narrowness_degree)
            change_noise(copy, copy.data.materials[0], noise_scale)
            change_color(copy,copy.data.materials , brCont)
            
            x = 1 + random.uniform(-copy.dimensions.x*scale_factor, copy.dimensions.x*scale_factor)
            #y = 1 + random.uniform(-copy.dimensions.y*scale_factor, copy.dimensions.y*scale_factor)
            z = random.uniform(copy.dimensions.z-0.2, copy.dimensions.z+0.3)
            copy.dimensions.z = z
            #copy.scale = (x, x, z)
            pose_y += matrixShift


deselect_scene()

obLeaf = bpy.context.scene.objects["Leaf"]     
obTuber = bpy.context.scene.objects["Tuber"]  
obCucumber = bpy.context.scene.objects["Cucumber"] 
matrixSize = 5
matrixShift = 2

gen_matrix(obTuber,matrixSize,matrixShift,5,4,0.02)
#gen_matrix(obCucumber,matrixSize,matrixShift,3,2,0.1)