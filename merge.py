import bpy
import re
import os
import cv2

root = "D:\\Fynn\\Downloads\\Downloads\\w3\\"
            
            
def reduceVerts(filePath, objname):
    merge_thresholds = (0.0005, 0.001, 0.0015, 0.00005)

    for t in merge_thresholds:
        view_layer = bpy.context.view_layer

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        bpy.ops.outliner.orphans_purge()
        bpy.ops.outliner.orphans_purge()
        bpy.ops.outliner.orphans_purge()

        imported_object = bpy.ops.import_scene.obj(filepath=filePath + objname)

        obj_object = bpy.context.selected_objects[0]

        bpy.context.view_layer.objects.active = obj_object

        bpy.ops.object.convert(target='MESH')

        print(bpy.context.view_layer.objects.active.name)

        print(len(bpy.context.view_layer.objects.active.data.vertices))

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold = t)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose()
        bpy.ops.object.mode_set(mode='OBJECT')

        vertcount = len(bpy.context.view_layer.objects.active.data.vertices)

        print(vertcount)

        exported = bpy.ops.export_scene.obj(filepath=filePath + "new_vertcount_" + str(vertcount) + "_" + objname)
        
def resizeImage(filePath, objname):
    try:
        img=cv2.imread(filePath + objname)
        img_50 = cv2.resize(img, None, fx = 0.50, fy = 0.50, interpolation=cv2.INTER_LANCZOS4)
        img_25 = cv2.resize(img, None, fx = 0.25, fy = 0.25, interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(filePath + "new_size_" + str(50) + "_" + objname, img_50)
        cv2.imwrite(filePath + "new_size_" + str(25) + "_" + objname, img_25)
    except:
        pass
    



for root, dirs, files in os.walk(top = root ):
    for file in files:
        filePath = root + "\\"
        objname = file
        if re.search(r'.obj', objname) is not None and re.search(r'new_vert', objname) is None:
            print(filePath + objname)
            reduceVerts(filePath, objname)
        elif (re.search(r'.png', objname) is not None or re.search(r'.dds', objname) is not None) and re.search(r'new_size', objname) is None:
            resizeImage(filePath, objname)