try:
	import bpy
except: ImportError

import os
import struct
# script based on Arben OMARI and DDLullu code
# probably works only with Vamped 0.92 and  PackFile Explorer 3.09

class xExport:
	def __init__(self, filename):
		#global my_path
		self.file = open(filename, "rb")
		self.my_path = filename
		print("filename is {}".format(filename))
		#my_path = Blender.sys.dirname(filename)
		#filename += 'x'
		export_filename = filename[:-4] + '_x.mdl'
		#print ("filename1: {}".format(filename1))
		self.export_file = open(export_filename, "wb" )
		#my_path += '\\'	  #ve
		#print "my_path:", my_path

	def export_mdl(self):
		#editmode = Window.EditMode()	# are we in edit mode?	If so ...
		#if editmode: Window.EditMode(0) # leave edit mode before getting the mesh
		#bpy.ops.object.mode_set(mode='EDIT', toggle=False)

		print ("modifying MDL...")
		'''		
		EXPORT_VERT = Draw.Create(1)
		EXPORT_UV = Draw.Create(1)
		EXPORT_NORMAL = Draw.Create(0)
		pup_block = [\
		('Export Options'),\
		('Vertices' ,EXPORT_VERT , 'Export the Vertice?'),\
		('UV' ,EXPORT_UV , 'Export the UV?'),\
		('Normals' ,EXPORT_NORMAL , 'Export the Normal?')
		]
		if not Draw.PupBlock('Darken = check option...', pup_block):
			self.file.close()
			self.file1.close()
			return
		'''
		export_vert = True
		export_uv = True
		export_normal = True

		#object = Blender.Object.GetSelected()[0]
		#mesh = object.getData()
		object = bpy.context.active_object
		mesh = object.data
		
		texcoord = []
		vtx_UV = (float('0.0'),float('0.0'))
		num_vtx_exported = 0
		for vtx in mesh.vertices:
			num_vtx_exported += 1
			texcoord.append(vtx_UV)
			
       # seek the offset of vertices number and position

		self.file.seek(324)
		temp_data = self.file.read(4)           #offset for smd
		data=struct.unpack('<i', temp_data)
		print ("model offset is {}: ".format(data[0]))
		off_vert = data[0]+16
		self.file.seek(off_vert+144)             #offset for number and position of the vertices in model
		temp_data = self.file.read(8)
		data = struct.unpack('<ii',temp_data)
		num_vtx_og = data[0]
		vtx_ofs = data[1] + off_vert    #find start of verts in file ### -12 for bone's weight
		print ("vert mdl:  {}". format(num_vtx_og))
		print ("vert exported:   {}". format(num_vtx_exported))
		print ("address vert: {}". format(vtx_ofs))
		#print "filename1: ", filename1

		#  check number of vertices against the mdl if no match exit
		#if num_vtx_og != num_vtx_exported :
		if True:
			print("Wrong count of vertice exiting...")
			#result=Blender.Draw.PupMenu("Model vertices dont match Blender vertices %t|OK")
		else:
		#	write list for vertice UV
			if mesh.hasFaceUV():

				for face in mesh.faces:
					texcoord[face.v[0].index] = (face.uv[0][0], 1 -face.uv[0][1])
					texcoord[face.v[1].index] = (face.uv[1][0], 1 -face.uv[1][1])
					texcoord[face.v[2].index] = (face.uv[2][0], 1 -face.uv[2][1])

		#	start writing new mdl file

			self.file.seek(0) 			     #return pointer to start of file
			self.export_file.write(self.file.read(vtx_ofs))  #read and write until first vertex position

			ii = 0
			for vert in mesh.verts:

				temp_data = self.file.read(44)	     #get vertices information, normals, UVs
				data = struct.unpack('<3BB4h3f3f2f',temp_data)

				if texcoord[ii][0] != 0.0:
					if not ((vert.co.x == 0.0) and (vert.co.y == 0.0) and (vert.co.z == 0.0)):
						temp_data = struct.pack('<3BB4h3f',data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]) #no vertices
						if export_vert: temp_data = struct.pack('<3BB4h3f',data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],vert.co.x,vert.co.y,vert.co.z) #with vertices
						temp_data1 = struct.pack('<3f',data[11],data[12],data[13]) #no normals
						if export_normal: temp_data1 = struct.pack('<3f',vert.no.x,vert.no.y,vert.no.z) # with normals
						temp_data2 = struct.pack('<2f',data[14],data[15]) #no UV
						if export_uv: temp_data2 = struct.pack('<2f',texcoord[ii][0],texcoord[ii][1]) #with uv
						#temp_data = struct.pack('<3BB4h3f3f2f',data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],texcoord[ii][0],texcoord[ii][1]) #only uv
						#                                        w1      w2      w3      n+?     b1     b2      b3        0       x      y        z       nx       ny       nz             u            v           #
				else:
					if not ((vert.co.x == 0.0) and (vert.co.y == 0.0) and (vert.co.z == 0.0)):
						temp_data = struct.pack('<3BB4h3f',data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]) #no vertices
						if export_vert: temp_data = struct.pack('<3BB4h3f',data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],vert.co.x,vert.co.y,vert.co.z) #with vertices
						temp_data1 = struct.pack('<3f',data[11],data[12],data[13]) #no normals
						if export_normal: temp_data1 = struct.pack('<3f',vert.no.x,vert.no.y,vert.no.z) # with normals
						temp_data2 = struct.pack('<2f',data[14],data[15]) #no UV
				self.export_file.write(temp_data) #overwite verts with blender value
				self.export_file.write(temp_data1) #overwite normals with blender value
				self.export_file.write(temp_data2) #overwite UV with blender value
				ii += 1

			self.export_file.write(self.file.read()) #finishing writing the mdl
			#result=Blender.Draw.PupMenu("The ..._x.MDL was created successfully %t|OK")


		self.file.close()
		self.export_file.close()
		#if editmode: Window.EditMode(1)  # optional, just being nice
		print ("... finished")