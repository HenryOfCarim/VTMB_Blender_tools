try:
	import bpy
except: ImportError

import os
# script based on Arben OMARI and DDLullu code
# probably works only with Vamped 0.92 and  PackFile Explorer 3.09


class xImport:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dir_path = os.path.dirname(file_path)
        self.f = open(file_path, 'r', encoding = 'utf-8')
        self.lines = self.f.readlines()
        self.f.close()
        print(file_path)
    
    def import_mesh(self):
        lines =self.lines
        mesh_name = os.path.basename(self.file_path)
        mesh = bpy.data.meshes.new(mesh_name)
        # Get UV
        for line_uv in lines:
            l = line_uv.strip()
            words = line_uv.split()																																																	
            if l and words[0] == "MeshTextureCoords":
                uv_line_idx = lines.index(line_uv)+1 #ve
                print("found UV")
        # Get materials
        mat_id = 0
        line_idx = -1
        materials = []
        textures = []
        for mat_line in lines:
            line_idx += 1
            l = mat_line.strip()
            words = mat_line.split()																																																	
            if l and words[0] == "Material" :
                mat_id += 1	
                self.write_materials(line_idx, mat_id, materials, textures)
                print("found material")	
                		
        #Get material indices for vertices
        num_mat_idx = 0
        num_vtx = 0
        material_vtx = []
        for mat_line in lines:
            l = mat_line.strip()
            words = mat_line.split()
            if l and words[0] == "MeshMaterialList" :
                num_mat_idx = self.lines.index(mat_line) + 3
                num_vtx = self.lines[num_mat_idx]
                num_vtx = self.clean_line(num_vtx)
                num_vtx = int(num_vtx)
                print("mat_vtx_idx {}".format(num_vtx))
        for i in range(num_vtx):
            lin = self.lines[num_mat_idx + 1 + i]
            lin_str = self.clean_line(lin)
            mat_id_vtx = int(lin_str)
            #lin_str = lin_str.strip()
            material_vtx.append(mat_id_vtx)
        print(len(material_vtx))   
 
        #Create The Mesh
        for line in lines:
            l = line.strip()
            words = line.split()																																																	
            if l and words[0] == "Mesh" :											
                mesh_line_idx = lines.index(line)
                print("mesh line idx {}".format(mesh_line_idx))																		
                self.write_vertices(mesh_line_idx, mesh, uv_line_idx, material_vtx, materials)
                
    def write_vertices(self, mesh_line_idx, mesh, uv_line_idx, material_vtx, materials):
        vertices = []
        faces = []
        edges = []
        normals = []
        uv = []
        print(mesh_line_idx)
        # find num vertices
        lin = self.lines[mesh_line_idx + 1]
        lin_str = self.clean_line(lin)
        lin_str = lin_str.strip()
        print(lin_str)          
        if lin_str:
            #print("True")                               
            num_vtx = int((lin_str.split()[0]))
            vtx_idx = self.lines.index(lin)
        else :
            #print("False")
            lin = self.lines[mesh_line_idx + 2]
            lin_str = self.clean_line(lin)
            num_vtx = int((lin_str.split()[0]))
            vtx_idx = self.lines.index(lin)
        print(num_vtx)
        vx_array = range(vtx_idx  + 1, (vtx_idx  + num_vtx +1))
        
        # find num faces
        lin = self.lines[vtx_idx + num_vtx +1]
        lin_str = self.clean_line(lin)             
        lin_str = lin_str.strip()                
        if lin_str :                                 
            num_face = int((lin_str.split()[0]))
            face_idx = self.lines.index(lin)
        else :
            lin = self.lines[vtx_idx + num_vtx +2]
            lin_str = self.clean_line(lin)
            num_face  = int((lin_str.split()[0]))
            face_idx = self.lines.index(lin)
        print("num faces is {}".format(num_face))
        fac_array = range(face_idx + 1, (face_idx + num_face + 1)) #face array

        # set vertices array
        i = 0
        for l in vx_array: 
            i += 1
            lin = self.lines[l]
            lin_str = self.clean_line(lin)
            words = lin_str.split()
            if len(words)==3:
                co_vert_x = float(words[0])
                co_vert_z = float(words[1])
                co_vert_y = float(words[2])
                v = (co_vert_x,co_vert_y,co_vert_z)
                #print(v)
                vertices.append(v)
        # set faces array
        i = 0
        ofs = 0
        #name_tex1 = ""
        for f in fac_array:
            i += 1
            lin = self.lines[f+ofs]
            lin_str = self.clean_line(lin)
            words = lin_str.split() # array with a face indices
            #print("words is{}".format(words))
            if not(words):#se  pass blank line
                ofs += 1                       # since i only see one
                lin = self.lines[f+ofs]     # blank i make a check
                lin_str = self.clean_line(lin) # for only one. May be
                words = lin_str.split()          # adjust if necessary.
            if len(words) == 5:
                print("quad")
            elif len(words) == 4:
                a = int(words[1])
                b = int(words[3])
                c = int(words[2])
                face =(a,b,c) 
                #print("face is {}".format(face))
                faces.append(face)        
        # set UV array
        if uv_line_idx:
            #print("UV is {}".format(self.lines[uv_line_idx]))
            num_uv = self.lines[uv_line_idx +1]
            num_uv = self.clean_line(num_uv)
            num_uv = int(num_uv)
            print(num_uv)
            for i in range(num_uv):
                v_uv = self.lines[uv_line_idx+2+i]
                v_uv = self.clean_line(v_uv)
                v_uv = v_uv.split()
                #print(v_uv)
                x = float(v_uv[0])
                y = ((float(v_uv[1]))* -1) + 1
                uv_tuple = (x, y)
                uv.append(uv_tuple)
                
        # create mesh
        mesh.from_pydata(vertices, edges, faces)
        uv_layer = mesh.uv_layers.new(name=mesh.name)
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        per_loop_list = []
        for loop in mesh.loops:
            offset = loop.vertex_index 
            per_loop_list.extend((uv[offset][0], uv[offset][1]))
        uv_layer.data.foreach_set('uv', per_loop_list)

        # set materials
        for mat in materials:
            mesh_obj.data.materials.append(mat)
        for face in mesh_obj.data.polygons:
            face_idx = face.index
            mat_idx = material_vtx[face_idx]
            face.material_index = mat_idx
            
        bpy.context.collection.objects.link(mesh_obj)

    def write_materials(self, nr_mat, idx, materials, textures):
        '''
        Create materials and set textures to a list
        '''
        name = "Material_" + str(idx)
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        link = mat.node_tree.links.new
        lin = self.lines[nr_mat + 2]   #ve
        fixed_line = self.clean_line(lin)
        words = fixed_line.split()	
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (float(words[0]),
                                                                                     float(words[1]),
                                                                                     float(words[2]),
                                                                                     float(words[3]))
        
        materials.append(mat)                                                                             
        lin = self.lines[nr_mat + 6]
        lin_str = self.clean_line(lin)
        tex_n = lin_str.split() # "TextureFilename" sting
        #for packfile explorer
        if not tex_n:		
            lin = self.lines[nr_mat + 7]  
            lin_str = self.clean_line(lin)
            tex_n = lin_str.split()
            print("tex_n is {}".format(tex_n))
            if tex_n and tex_n[0] == "TextureFilename" :
                #print("texture works")
                if len(tex_n) > 1:
                    print("tex_n is {}".format(tex_n))
                    textures.append(tex_n[1])
                if len(tex_n) <= 1 :
                    #print("dir path {}".format(self.dir_path))
                    is_tex_exist = True
                    lin_tex_name = self.lines[nr_mat + 9]
                    tex_name_str = self.clean_line(lin_tex_name)
                    tex_name_str = tex_name_str.split() # texture name "Missing.tga"
                    tex_path = os.path.join(self.dir_path, tex_name_str[0])
                    tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
                    tex_node.location =(-300, 350)
                    try:
                        tex_node.image = bpy.data.images.load(tex_path)
                    except:
                        is_tex_exist = False
                        print("Missing texture {}".format(tex_path))
                    if is_tex_exist:
                        link(tex_node.outputs['Color'], bsdf.inputs[0])
                        print("texture applied")
                    textures.append(tex_name_str[0])
            else:
                tex_name_str = None
                textures.append(tex_name_str)
        #for vamped 92
        else:				
            if tex_n and tex_n[0] == "TextureFilename" :
                if len(tex_n) > 1: # tex_n =['TextureFilename', 'tongue.tga']
                    is_tex_exist = True
                    tex_name_str = self.clean_line(tex_n[1])
                    tex_path = os.path.join(self.dir_path, tex_name_str)
                    tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
                    tex_node.location =(-300, 350)
                    try:
                        tex_node.image = bpy.data.images.load(tex_path)
                    except:
                        is_tex_exist = False
                        print("Missing texture {}".format(tex_path))
                    if is_tex_exist:
                        link(tex_node.outputs['Color'], bsdf.inputs[0])
                    textures.append(tex_n[1])
                if len(tex_n) <= 1 :
                    print("vamped")
                    is_tex_exist = True
                    lin_tex_name = self.lines[nr_mat + 7] #ve
                    tex_name_str = self.clean_line(lin_tex_name)
                    tex_name_str = tex_name_str.split()
                    textures.append(tex_name_str[0])
                    tex_path = os.path.join(self.dir_path, tex_name_str[0])
                    tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
                    tex_node.location =(-300, 350)
                    try:
                        tex_node.image = bpy.data.images.load(tex_path)
                    except:
                        is_tex_exist = False
                        print("Missing texture {}".format(tex_path))
                    if is_tex_exist:
                        link(tex_node.outputs['Color'], bsdf.inputs[0])
                        print("texture applied")
            else :
                tex_name_str = None
                textures.append(tex_name_str)
        return materials, textures
            
    def clean_line(self, line):
        fix_line = line.replace(";", " ")
        fix_1_line = fix_line.replace('"', ' ')
        fix_2_line = fix_1_line.replace("{", " ")
        fix_3_line = fix_2_line.replace("}", " ")
        fix_4_line = fix_3_line.replace(",", " ")
        fix_5_line = fix_4_line.replace("'", " ")
        return fix_5_line
    
        