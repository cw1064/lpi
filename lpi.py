class Label:
	def __init__(self, object, parent):
		self.object = object
		self.text = object.text
		attrs = object.attrib
		for attrib in attrs:
			setattr(self, attrib, attrs[attrib])
		self.x = float(self.x)
		self.y = float(self.y)
		temp = parent.find("{http://www.w3.org/2000/svg}path")
		d = temp.attrib["d"]
		d = d[1:]
		d = d.replace("C", " ")
		d = d.split(" ")
		for i in range(0, len(d)):
			d[i] = d[i].split(",")
			d[i][0] = float(d[i][0])
			d[i][1] = float(d[i][1])
		self.paths = []
		for i in range(0, int((len(d)-1)/3)):
			self.paths.append([[d[i*3][0], d[i*3][1]],[d[(i+1)*3][0], d[(i+1)*3][1]]])
		labfont = object.attrib["font-family"].split(",")[0]
		newFont = ImageFont.truetype(labfont + ".ttf", int(float(object.attrib["font-size"])))
		self.dimsy = newFont.getsize(self.text)
		self.dims = [float(self.dimsy[0]), float(self.dimsy[1])]
		self.locs = []
		self.minx = self.x - self.dims[0]/2
		self.maxx = self.x + self.dims[0]/2
		self.miny = self.y
		self.maxy = self.y + self.dims[1]
		self.scale = 1
		self.peak = 0
		
	def __str__(self):
		output = "Text: " + self.text + "\nX: " + str(self.x) + "\nY: " + str(self.y) + "\nPaths are:"
		for i in self.paths:
			output = output + "\n(" + str(i[0][0]) + ", " + str(i[0][1]) + ") to (" + str(i[1][0]) + ", " + str(i[1][1]) + ")"
		output = output + "\nDimensions are " + str(self.dims) + " and text size is " + self.object.attrib["font-size"]
		return output
	
	def setx(self, val):
		self.x = val
		self.object.attrib["x"] = str(val)
		
	def sety(self, val):
		self.y = val
		self.object.attrib["y"] = str(val)
		
	def setalign(self, val):
		if val == "r":
			self.object.attrib["text-anchor"] = "start"
			self.sety(self.y + self.scale*self.dims[1]/2)
			self.setx(self.x - 2 + 2*self.scale)
			self.minx = self.x
			self.maxx = self.x + self.scale*self.dims[0]
			self.miny = self.y - self.scale*self.dims[1]
			self.maxy = self.y
		elif val == "l": 
			self.object.attrib["text-anchor"] = "end"
			self.sety(self.y + self.scale*self.dims[1]/2)
			self.setx(self.x + 2 - 2*self.scale)
			self.minx = self.x - self.scale*self.dims[0]
			self.maxx = self.x
			self.miny = self.y - self.scale*self.dims[1]
			self.maxy = self.y
		elif val == "u":
			self.object.attrib["text-anchor"] = "middle"
			self.minx = self.x - self.scale*self.dims[0]/2
			self.maxx = self.x + self.scale*self.dims[0]/2
			self.miny = self.y - self.scale*self.dims[1]
			self.maxy = self.y 
		elif val == "d":
			self.object.attrib["text-anchor"] = "middle"
			self.sety(self.y + self.scale*self.dims[1]*0.8 - 2 + 2*self.scale)
			self.minx = self.x - self.scale*self.dims[0]/2
			self.maxx = self.x + self.scale*self.dims[0]/2
			self.miny = self.y 
			self.maxy = self.y + self.scale*self.dims[1]
		
class Block:
	def __init__(self, object, isEdge):
		self.object = object
		if isEdge:
			if object[2] == "x":
				self.minx = object[0][0]
				self.maxx = object[0][0]
				if object[1][1] > object[0][1]:
					self.maxy = object[1][1]
					self.miny = object[0][1]
				else:
					self.maxy = object[0][1]
					self.miny = object[1][1]
			else:
				self.miny = object[0][1]
				self.maxy = object[0][1]
				if object[1][0] > object[0][0]:
					self.maxx = object[1][0]
					self.minx = object[0][0]
				else:
					self.maxx = object[0][0]
					self.minx = object[1][0]
		else:
			dims = object.attrib["points"]
			dims = dims.split(" ")
			for i in range(0, len(dims)):
				dims[i] = dims[i].split(",")
				dims[i][0] = float(dims[i][0])
				dims[i][1] = float(dims[i][1])
			minx = maxx = dims[0][0]
			miny = maxy = dims[0][1]
			for i in range(1, len(dims)):
				if minx > dims[i][0]:
					minx = dims[i][0]
				elif maxx < dims[i][0]:
					maxx = dims[i][0]
				if miny > dims[i][1]:
					miny = dims[i][1]
				elif maxy < dims[i][1]:
					maxy = dims[i][1]
			self.minx = minx
			self.maxx = maxx
			self.miny = miny
			self.maxy = maxy
		
	def __str__(self):
		output = "X is all of " + str(self.minx) + " to " + str(self.maxx) + "\nY is all of " + str(self.miny) + " to " + str(self.maxy)
		return output
		
def edgeHandle(object):
	d = object.attrib["d"]
	d = d[1:]
	d = d.replace("C", " ")
	d = d.split(" ")
	for i in range(0, len(d)):
		d[i] = d[i].split(",")
		d[i][0] = float(d[i][0])
		d[i][1] = float(d[i][1])
	paths = []
	for i in range(0, int((len(d)-1)/3)):
		paths.append([[d[i*3][0], d[i*3][1]],[d[(i+1)*3][0], d[(i+1)*3][1]]])
	for path in paths:
		if path[0][0] == path[1][0]:
			path.append("x")
			newBlock = Block(path, True)
			blocks.append(newBlock)
		else:
			path.append("y")
			newBlock = Block(path, True)
			blocks.append(newBlock)
			
def locgen(label):
	for path in label.paths:
		if path[0][0] == path[1][0]:
			lng = lngwgh*max(0, lngmax-abs(path[1][1] - path[0][1]))/lngmax
			exp = expwgh*min(0, path[0][0]-2-label.dims[0]-vminx)
			penalty = lng - exp - lpref
			label.locs.append([[path[0][0]-2, (path[0][1] + path[1][1])/2, cntwgh-penalty], [path[0][0]-2, path[0][1], 0-penalty], ["l", 1]])
			label.locs.append([[path[0][0]-2, (path[0][1] + path[1][1])/2, cntwgh-penalty], [path[0][0]-2, path[1][1], 0-penalty], ["l", 1]])
			exp = expwgh*min(0, vmaxx-(path[0][0]+2+label.dims[0]))
			penalty = lng - exp - rpref
			label.locs.append([[path[0][0]+2, (path[0][1] + path[1][1])/2, cntwgh-penalty], [path[0][0]+2, path[0][1], 0-penalty], ["r", 1]])
			label.locs.append([[path[0][0]+2, (path[0][1] + path[1][1])/2, cntwgh-penalty], [path[0][0]+2, path[1][1], 0-penalty], ["r", 1]])
		else:                                                                                                                   
			lng = lngwgh*max(0, lngmax-abs(path[1][0] - path[0][0]))/lngmax                                                                    
			exp = expwgh*min(0, path[0][1]-2-label.dims[1]-vminy)            
			penalty = lng - exp - upref
			label.locs.append([[(path[0][0] + path[1][0])/2, path[0][1]-2, cntwgh-penalty], [path[0][0], path[0][1]-2, 0-penalty], ["u", 1]])
			label.locs.append([[(path[0][0] + path[1][0])/2, path[0][1]-2, cntwgh-penalty], [path[1][0], path[0][1]-2, 0-penalty], ["u", 1]])
			exp = expwgh*min(0, vmaxy-(path[0][1]+2+label.dims[1]))      
			penalty = lng - exp - dpref
			label.locs.append([[(path[0][0] + path[1][0])/2, path[0][1]+1, cntwgh-penalty], [path[0][0], path[0][1]+2, 0-penalty], ["d", 1]])
			label.locs.append([[(path[0][0] + path[1][0])/2, path[0][1]+1, cntwgh-penalty], [path[1][0], path[0][1]+2, 0-penalty], ["d", 1]])
	label.locs.sort(key=lambda loc: loc[0][2], reverse=True)
	
def loccollide(i, loc, block):
	breaknow = False
	if loc[2][0] == "l":
		if block.maxx > (loc[0][0] - loc[2][1]*(labels[i].dims[0]+4)) and block.minx < loc[0][0] and block.miny < (max(loc[0][1], loc[1][1]) + loc[2][1]*labels[i].dims[1]/2) and block.maxy > (min(loc[0][1], loc[1][1]) - loc[2][1]*labels[i].dims[1]/2): #if there is any obstruction at all
			if block.maxy > (loc[0][1] - loc[2][1]*labels[i].dims[1]/2) and block.miny < (loc[0][1] + loc[2][1]*labels[i].dims[1]/2): #if the [0] edge of the range is obstructed
				if block.maxy > (loc[1][1] - loc[2][1]*labels[i].dims[1]/2) and block.miny < (loc[1][1] + loc[2][1]*labels[i].dims[1]/2): #if the [1] edge of the range is obstructed (ie, both are and so the whole range is)
					if block.maxx > loc[0][0]: #if the obstruction is total
						loc[0][0] = "No" #this removes it from the list, but afterwards so as not to mess up the order
						breaknow = True
					else:	#the obstruction is not total, ie it's partial
						loc[2][1] = (loc[0][0] - block.maxx)/(labels[i].dims[0]+4) #shrink the label to fit
				else:	#if the [1] edge is unobstructed (but the [0] edge still is)
					if loc[0][1] > loc[1][1]:	#for knowing which edge is the high edge
						if block.maxx > loc[0][0]:
							newy = block.miny-loc[2][1]*labels[i].dims[1]/2
							loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
							loc[0][1] = newy
						else:
							newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01 #you'll see this +-0.01 a lot. it's to deal with the small rounding errors on floats
							neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
							labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
							loc[2][1] = (loc[0][0] - block.maxx)/(labels[i].dims[0]+4)
							loc[1][1] = newy
							loc[1][2] = neww
					else:
						if block.maxx > loc[0][0]:
							newy = block.maxy+loc[2][1]*labels[i].dims[1]/2
							loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
							loc[0][1] = newy
						else:
							newy = block.maxy+loc[2][1]*labels[i].dims[1]/2+0.01
							neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
							labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
							loc[2][1] = (loc[0][0] - block.maxx)/(labels[i].dims[0]+4)
							loc[1][1] = newy
							loc[1][2] = neww
			elif block.maxy > (loc[1][1] - loc[2][1]*labels[i].dims[1]/2) and block.miny < (loc[1][1] + loc[2][1]*labels[i].dims[1]/2):
				if loc[1][1] > loc[0][1]:
					if block.maxx > loc[0][0]:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						loc[1][1] = newy
					else:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
						loc[2][1] = (loc[0][0] - block.maxx)/(labels[i].dims[0]+4)
						loc[0][1] = newy
						loc[0][2] = neww
				else:
					if block.maxx > loc[0][0]:
						newy = block.maxy+loc[2][1]*labels[i].dims[1]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						loc[1][1] = newy
					else:
						newy = block.maxy+loc[2][1]*labels[i].dims[1]/2+0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
						loc[2][1] = (loc[0][0] - block.maxx)/(labels[i].dims[0]+4)
						loc[0][1] = newy
						loc[0][2] = neww
			else:
				if loc[0][1] < loc[1][1]:
					if block.maxx > loc[0][0]:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
						newy = block.maxy+loc[2][1]*labels[i].dims[1]/2
						loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						loc[0][1] = newy
					else:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
						newy2 = block.maxy+loc[2][1]*labels[i].dims[1]/2+0.01
						neww2 = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy2)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy2, neww2], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[0][1] = newy2
						loc[0][2] = neww2
						loc[1][1] = newy
						loc[1][2] = neww
						loc[2][1] = (loc[0][0] - block.maxx)/(labels[i].dims[0]+4)
				else:
					if block.maxx > loc[0][0]:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						newy = block.maxy+loc[2][1]*labels[i].dims[1]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						loc[1][1] = newy
					else:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						newy2 = block.maxy+loc[2][1]*labels[i].dims[1]/2+0.01
						neww2 = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy2)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy2, neww2], [loc[2][0], loc[2][1]]])
						loc[0][1] = newy
						loc[0][2] = neww
						loc[1][1] = newy2
						loc[1][2] = neww2
						loc[2][1] = (loc[0][0] - block.maxx)/(labels[i].dims[0]+4)
	elif loc[2][0] == "r":
		if block.maxx > loc[0][0] and block.minx < (loc[0][0] + loc[2][1]*(labels[i].dims[0]+4)) and block.miny < (max(loc[0][1], loc[1][1]) + loc[2][1]*labels[i].dims[1]/2) and block.maxy > (min(loc[0][1], loc[1][1]) - loc[2][1]*labels[i].dims[1]/2):
			if block.maxy > (loc[0][1] - loc[2][1]*labels[i].dims[1]/2) and block.miny < (loc[0][1] + loc[2][1]*labels[i].dims[1]/2):
				if block.maxy > (loc[1][1] - loc[2][1]*labels[i].dims[1]/2) and block.miny < (loc[1][1] + loc[2][1]*labels[i].dims[1]/2):
					if block.minx < loc[0][0]:
						loc[0][0] = "No"
						breaknow = True
					else:
						loc[2][1] = (block.minx-loc[0][0])/(labels[i].dims[0]+4)
				else:
					if loc[0][1] > loc[1][1]:
						if block.minx < loc[0][0]:
							newy = block.miny-loc[2][1]*labels[i].dims[1]/2
							loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
							loc[0][1] = newy
						else:
							newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
							neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
							labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
							loc[2][1] = (block.minx-loc[0][0])/(labels[i].dims[0]+4)
							loc[1][1] = newy
							loc[1][2] = neww
					else:
						if block.minx < loc[0][0]:
							newy = block.maxy+loc[2][1]*labels[i].dims[1]/2
							loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
							loc[0][1] = newy
						else:
							newy = block.maxy+loc[2][1]*labels[i].dims[1]/2+0.01
							neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
							labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
							loc[2][1] = (block.minx-loc[0][0])/(labels[i].dims[0]+4)
							loc[1][1] = newy
							loc[1][2] = neww
			elif block.maxy > (loc[1][1] - loc[2][1]*labels[i].dims[1]/2) and block.miny < (loc[1][1] + loc[2][1]*labels[i].dims[1]/2):
				if loc[1][1] > loc[0][1]:
					if block.minx < loc[0][0]:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						loc[1][1] = newy
					else:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
						loc[2][1] = (block.minx-loc[0][0])/(labels[i].dims[0]+4)
						loc[0][1] = newy
						loc[0][2] = neww
				else:
					if block.minx < loc[0][0]:
						newy = block.maxy+loc[2][1]*labels[i].dims[1]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						loc[1][1] = newy
					else:
						newy = block.maxy+loc[2][1]*labels[i].dims[1]/2+0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
						loc[2][1] = (block.minx-loc[0][0])/(labels[i].dims[0]+4)
						loc[0][1] = newy
						loc[0][2] = neww
			else:
				if loc[0][1] < loc[1][1]:
					if block.minx < loc[0][0]:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[1][2]*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
						newy = block.maxy+loc[2][1]*labels[i].dims[1]/2
						loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						loc[0][1] = newy
					else:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[1][2]*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
						newy2 = block.maxy+loc[2][1]*labels[i].dims[1]/2+0.01
						neww2 = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy2)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy2, neww2], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[2][1] = (block.minx-loc[0][0])/(labels[i].dims[0]+4)
						loc[0][1] = newy2
						loc[0][2] = neww2
						loc[1][1] = newy
						loc[1][2] = neww
				else:
					if block.minx < loc[0][0]:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						newy = block.maxy+loc[2][1]*labels[i].dims[1]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
						loc[1][1] = newy
					else:
						newy = block.miny-loc[2][1]*labels[i].dims[1]/2-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						newy2 = block.maxy+loc[2][1]*labels[i].dims[1]/2+0.01
						neww2 = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy2)/(loc[0][1]-loc[1][1])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy2, neww2], [loc[2][0], loc[2][1]]])
						loc[0][1] = newy
						loc[0][2] = neww
						loc[1][1] = newy2
						loc[1][2] = neww2
	elif loc[2][0] == "u":
		if block.maxx > (min(loc[0][0], loc[1][0]) - loc[2][1]*labels[i].dims[0]/2) and block.minx < (max(loc[0][0], loc[1][0]) + loc[2][1]*labels[i].dims[0]/2) and block.miny < loc[0][1] and block.maxy > loc[0][1] - loc[2][1]*(labels[i].dims[1]+2):
			if block.maxx > (loc[0][0] - loc[2][1]*labels[i].dims[0]/2) and block.minx < (loc[0][0] + loc[2][1]*labels[i].dims[0]/2):
				if block.maxx > (loc[1][0] - loc[2][1]*labels[i].dims[0]/2) and block.minx < (loc[1][0] + loc[2][1]*labels[i].dims[0]/2):
					if block.maxy > loc[0][1]:
						loc[0][0] = "No"
						breaknow = True
					else:
						loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
				else:
					if loc[0][0] > loc[1][0]:
						if block.maxy > loc[0][1]:
							newx = block.minx-loc[2][1]*labels[i].dims[0]/2
							loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
							loc[0][0] = newx
						else:
							newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
							neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
							labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
							loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
							loc[1][0] = newx
							loc[1][2] = neww
					else:
						if block.maxy > loc[0][1]:
							newx = block.maxx+loc[2][1]*labels[i].dims[0]/2
							loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
							loc[0][0] = newx
						else:
							newx = block.maxx+loc[2][1]*labels[i].dims[0]/2+0.01
							neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
							labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
							loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
							loc[1][0] = newx
							loc[1][2] = neww
			elif block.maxx > (loc[1][0] - loc[2][1]*labels[i].dims[0]/2) and block.minx < (loc[1][0] + loc[2][1]*labels[i].dims[0]/2):
				if loc[1][0] > loc[0][0]:
					if block.maxy > loc[0][1]:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						loc[1][0] = newx
					else:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
						loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
						loc[0][0] = newx
						loc[0][2] = neww
				else:
					if block.maxy > loc[0][1]:
						newx = block.maxx+loc[2][1]*labels[i].dims[0]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						loc[1][0] = newx
					else:
						newx = block.maxx+loc[2][1]*labels[i].dims[0]/2+0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
						loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
						loc[0][0] = newx
						loc[0][2] = neww
			else:
				if loc[0][0] < loc[1][0]:
					if block.maxy > loc[0][1]:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[1][2]*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
						newx = block.maxx+labels[i].dims[0]/2
						loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						loc[0][0] = newx
					else:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[1][2]*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
						newx2 = block.maxx+labels[i].dims[0]/2+0.01
						neww2 = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx2)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx2, loc[0][1], neww2], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
						loc[0][0] = newx2
						loc[0][2] = neww2
						loc[1][0] = newx
						loc[1][2] = neww
				else:
					if block.maxy > loc[0][1]:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						newx = block.maxx+labels[i].dims[0]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						loc[1][0] = newx
					else:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						newx2 = block.maxx+labels[i].dims[0]/2+0.01
						neww2 = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx2)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx2, loc[1][1], neww2], [loc[2][0], loc[2][1]]])
						loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
						loc[0][0] = newx
						loc[0][2] = neww
						loc[1][0] = newx2
						loc[1][2] = neww2
	elif loc[2][0] == "d":
		if block.maxx > (min(loc[0][0], loc[1][0]) - loc[2][1]*labels[i].dims[0]/2) and block.minx < (max(loc[0][0], loc[1][0]) + loc[2][1]*labels[i].dims[0]/2) and block.miny < loc[0][1] + loc[2][1]*(labels[i].dims[1]+4) and block.maxy > loc[0][1]:
			if block.maxx > (loc[0][0] - loc[2][1]*labels[i].dims[0]/2) and block.minx < (loc[0][0] + loc[2][1]*labels[i].dims[0]/2):
				if block.maxx > (loc[1][0] - loc[2][1]*labels[i].dims[0]/2) and block.minx < (loc[1][0] + loc[2][1]*labels[i].dims[0]/2):
					if block.miny < loc[0][1]:
						loc[0][0] = "No"
						breaknow = True
					else:
						loc[2][1] = (block.miny - loc[0][1])/(labels[i].dims[1]+4)
				else:
					if loc[0][0] > loc[1][0]:
						if block.miny < loc[0][1]:
							newx = block.minx-loc[2][1]*labels[i].dims[0]/2
							loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
							loc[0][0] = newx
						else:
							newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
							neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
							labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
							loc[2][1] = (block.miny - loc[0][1])/(labels[i].dims[1]+4)
							loc[1][0] = newx
							loc[1][2] = neww
					else:
						if block.miny < loc[0][1]:
							newx = block.maxx+loc[2][1]*labels[i].dims[0]/2
							loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
							loc[0][0] = newx
						else:
							newx = block.maxx+loc[2][1]*labels[i].dims[0]/2+0.01
							neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
							labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
							loc[2][1] = (block.miny - loc[0][1])/(labels[i].dims[1]+4)
							loc[1][0] = newx
							loc[1][2] = neww
			elif block.maxx > (loc[1][0] - loc[2][1]*labels[i].dims[0]/2) and block.minx < (loc[1][0] + loc[2][1]*labels[i].dims[0]/2):
				if loc[1][0] > loc[0][0]:
					if block.miny < loc[0][1]:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						loc[1][0] = newx
					else:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
						loc[2][1] = (block.miny - loc[0][1])/(labels[i].dims[1]+4)
						loc[0][0] = newx
						loc[0][2] = neww
				else:
					if block.miny < loc[0][1]:
						newx = block.maxx+loc[2][1]*labels[i].dims[0]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						loc[1][0] = newx
					else:
						newx = block.maxx+loc[2][1]*labels[i].dims[0]/2+0.01
						neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
						loc[2][1] = (block.miny - loc[0][1])/(labels[i].dims[1]+4)
						loc[0][0] = newx
						loc[0][2] = neww
			else:
				if loc[0][0] < loc[1][0]:
					if block.miny < loc[0][1]:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[1][2]*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
						newx = block.maxx+loc[2][1]*labels[i].dims[0]/2+0.01
						loc[0][2] = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						loc[0][0] = newx
					else:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[1][2]*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
						newx2 = block.maxx+loc[2][1]*labels[i].dims[0]/2+0.01
						neww2 = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx2)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx2, loc[0][1], neww2], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
						loc[0][0] = newx2
						loc[0][2] = neww2
						loc[1][0] = newx
						loc[1][2] = neww
				else:
					if block.miny < loc[0][1]:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						newx = block.maxx+loc[2][1]*labels[i].dims[0]/2
						loc[1][2] = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
						loc[1][0] = newx
					else:
						newx = block.minx-loc[2][1]*labels[i].dims[0]/2-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						newx2 = block.maxx+loc[2][1]*labels[i].dims[0]/2+0.01
						neww2 = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx2)/(loc[0][0]-loc[1][0])
						labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx2, loc[1][1], neww2], [loc[2][0], loc[2][1]]])
						loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
						loc[0][0] = newx2
						loc[0][2] = neww2
						loc[1][0] = newx
						loc[1][2] = neww
	return breaknow
	
def locprox(i, loc, block):
	if loc[2][0] == "l":
		if block.maxx > (loc[0][0] - loc[2][1]*(labels[i].dims[0])) and block.minx < loc[0][0] and block.miny < (max(loc[0][1], loc[1][1]) + loc[2][1]*(prxmax+labels[i].dims[1]/2)) and block.maxy > (min(loc[0][1], loc[1][1]) -  loc[2][1]*(prxmax+labels[i].dims[1]/2)):
			if block.maxy > (loc[0][1] - loc[2][1]*(prxmax+labels[i].dims[1]/2)) and block.miny < (loc[0][1] + loc[2][1]*(prxmax+labels[i].dims[1]/2)): #if the [0] edge of the range is obstructed
				if block.maxy > (loc[1][1] - loc[2][1]*(prxmax+labels[i].dims[1]/2)) and block.miny < (loc[1][1] + loc[2][1]*(prxmax+labels[i].dims[1]/2)): #if the [1] edge of the range is obstructed (ie, both are and so the whole range is)
					if loc[0][1] > block.maxy:
						if loc[0][2]-abs(loc[0][1]-block.maxy) > loc[1][2]-abs(loc[1][1]-block.maxy):
							loc[0][2] = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
					else:
						if loc[0][2]-abs(loc[0][1]-block.miny) > loc[1][2]-abs(loc[1][1]-block.miny):
							loc[0][2] = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
				else:	#if the [1] edge is unobstructed (but the [0] edge still is)
					if loc[0][1] > loc[1][1]:	#for knowing which edge is the high edge
						newy = block.miny-loc[2][1]*(prxmax+labels[i].dims[1]/2)-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[1][1] = newy
						loc[1][2] = neww
						if loc[0][2]-abs(loc[0][1]-block.miny) > loc[1][2]-abs(loc[1][1]-block.miny):
							loc[0][2] = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
					else:
						newy = block.maxy+loc[2][1]*(prxmax+labels[i].dims[1]/2)+0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[1][1] = newy
						loc[1][2] = neww
						if loc[0][2]-abs(loc[0][1]-block.maxy) > loc[1][2]-abs(loc[1][1]-block.maxy):
							loc[0][2] = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
			elif block.maxy > (loc[1][1] - loc[2][1]*(prxmax+labels[i].dims[1]/2)) and block.miny < (loc[1][1] + loc[2][1]*(prxmax+labels[i].dims[1]/2)):
				if loc[1][1] > loc[0][1]:
					newy = block.miny-loc[2][1]*(prxmax+labels[i].dims[1]/2)-0.01
					neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
					labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
					loc[0][1] = newy
					loc[0][2] = neww
					if loc[0][2]-abs(loc[0][1]-block.miny) > loc[1][2]-abs(loc[1][1]-block.miny):
						loc[0][2] = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
						loc[1][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
					else:
						tempx = loc[0][0]
						tempy = loc[0][1]
						tempw = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
						loc[0][0] = loc[1][0]
						loc[0][1] = loc[1][1]
						loc[0][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
						loc[1][0] = tempx
						loc[1][1] = tempy
						loc[1][2] = tempw
				else:
					newy = block.maxy+loc[2][1]*(prxmax+labels[i].dims[1]/2)+0.01
					neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
					labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
					loc[0][1] = newy
					loc[0][2] = neww
					if loc[0][2]-abs(loc[0][1]-block.maxy) > loc[1][2]-abs(loc[1][1]-block.maxy):
						loc[0][2] = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
						loc[1][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
					else:
						tempx = loc[0][0]
						tempy = loc[0][1]
						tempw = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
						loc[0][0] = loc[1][0]
						loc[0][1] = loc[1][1]
						loc[0][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
						loc[1][0] = tempx
						loc[1][1] = tempy
						loc[1][2] = tempw
	elif loc[2][0] == "r":
		if block.maxx > loc[0][0] and block.minx < (loc[0][0] + loc[2][1]*(labels[i].dims[0])) and block.miny < (max(loc[0][1], loc[1][1]) + loc[2][1]*(prxmax+labels[i].dims[1]/2)) and block.maxy > (min(loc[0][1], loc[1][1]) - loc[2][1]*(prxmax+labels[i].dims[1]/2)):
			if block.maxy > (loc[0][1] - loc[2][1]*(prxmax+labels[i].dims[1]/2)) and block.miny < (loc[0][1] + loc[2][1]*(prxmax+labels[i].dims[1]/2)):
				if block.maxy > (loc[1][1] - loc[2][1]*(prxmax+labels[i].dims[1]/2)) and block.miny < (loc[1][1] + loc[2][1]*(prxmax+labels[i].dims[1]/2)):
					if loc[0][1] > block.maxy:
						if loc[0][2]-abs(loc[0][1]-block.maxy) > loc[1][2]-abs(loc[1][1]-block.maxy):
							loc[0][2] = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
					else:
						if loc[0][2]-abs(loc[0][1]-block.miny) > loc[1][2]-abs(loc[1][1]-block.miny):
							loc[0][2] = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
				else:
					if loc[0][1] > loc[1][1]:
						newy = block.miny-loc[2][1]*(prxmax+labels[i].dims[1]/2)-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[1][1] = newy
						loc[1][2] = neww
						if loc[0][2]-abs(loc[0][1]-block.miny) > loc[1][2]-abs(loc[1][1]-block.miny):
							loc[0][2] = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
					else:
						newy = block.maxy+loc[2][1]*(prxmax+labels[i].dims[1]/2)+0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][1]-newy)/(loc[1][1]-loc[0][1])
						labels[i].locs.append([[loc[0][0], newy, neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[1][1] = newy
						loc[1][2] = neww
						if loc[0][2]-abs(loc[0][1]-block.maxy) > loc[1][2]-abs(loc[1][1]-block.maxy):
							loc[0][2] = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
			elif block.maxy > (loc[1][1] - loc[2][1]*(prxmax+labels[i].dims[1]/2)) and block.miny < (loc[1][1] + loc[2][1]*(prxmax+labels[i].dims[1]/2)):
				if loc[1][1] > loc[0][1]:
					newy = block.miny-loc[2][1]*(prxmax+labels[i].dims[1]/2)-0.01
					neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
					labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
					loc[0][1] = newy
					loc[0][2] = neww
					if loc[0][2]-abs(loc[0][1]-block.miny) > loc[1][2]-abs(loc[1][1]-block.miny):
						loc[0][2] = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
						loc[1][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
					else:
						tempx = loc[0][0]
						tempy = loc[0][1]
						tempw = loc[0][2]-abs(loc[0][1]-block.miny)*prxwgh
						loc[0][0] = loc[1][0]
						loc[0][1] = loc[1][1]
						loc[0][2] = loc[1][2]-abs(loc[1][1]-block.miny)*prxwgh
						loc[1][0] = tempx
						loc[1][1] = tempy
						loc[1][2] = tempw
				else:
					newy = block.maxy+loc[2][1]*(prxmax+labels[i].dims[1]/2)+0.01
					neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][1]-newy)/(loc[0][1]-loc[1][1])
					labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [loc[1][0], newy, neww], [loc[2][0], loc[2][1]]])
					loc[0][1] = newy
					loc[0][2] = neww
					if loc[0][2]-abs(loc[0][1]-block.maxy) > loc[1][2]-abs(loc[1][1]-block.maxy):
						loc[0][2] = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
						loc[1][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
					else:
						tempx = loc[0][0]
						tempy = loc[0][1]
						tempw = loc[0][2]-abs(loc[0][1]-block.maxy)*prxwgh
						loc[0][0] = loc[1][0]
						loc[0][1] = loc[1][1]
						loc[0][2] = loc[1][2]-abs(loc[1][1]-block.maxy)*prxwgh
						loc[1][0] = tempx
						loc[1][1] = tempy
						loc[1][2] = tempw
	elif loc[2][0] == "u":
		if block.maxx > (min(loc[0][0], loc[1][0]) - loc[2][1]*(prxmax+labels[i].dims[0]/2)) and block.minx < (max(loc[0][0], loc[1][0]) + loc[2][1]*(prxmax+labels[i].dims[0]/2)) and block.miny < loc[0][1] and block.maxy > loc[0][1] - loc[2][1]*(labels[i].dims[1]+2):
			if block.maxx > (loc[0][0] - loc[2][1]*(prxmax+labels[i].dims[0]/2)) and block.minx < (loc[0][0] + loc[2][1]*(prxmax+labels[i].dims[0]/2)):
				if block.maxx > (loc[1][0] - loc[2][1]*(prxmax+labels[i].dims[0]/2)) and block.minx < (loc[1][0] + loc[2][1]*(prxmax+labels[i].dims[0]/2)):
					if loc[0][0] > block.maxx:
						if loc[0][2]-abs(loc[0][0]-block.maxx) > loc[1][2]-abs(loc[1][0]-block.maxx):
							loc[0][2] = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
					else:
						if loc[0][2]-abs(loc[0][0]-block.minx) > loc[1][2]-abs(loc[1][0]-block.minx):
							loc[0][2] = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
				else:
					if loc[0][0] > loc[1][0]:
						newx = block.minx-loc[2][1]*(prxmax+labels[i].dims[0]/2)-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[1][0] = newx
						loc[1][2] = neww
						if loc[0][2]-abs(loc[0][0]-block.minx) > loc[1][2]-abs(loc[1][0]-block.minx):
							loc[0][2] = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
					else:
						newx = block.maxx+loc[2][1]*(prxmax+labels[i].dims[0]/2)+0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[1][0] = newx
						loc[1][2] = neww
						if loc[0][2]-abs(loc[0][0]-block.maxx) > loc[1][2]-abs(loc[1][0]-block.maxx):
							loc[0][2] = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
			elif block.maxx > (loc[1][0] - loc[2][1]*(prxmax+labels[i].dims[0]/2)) and block.minx < (loc[1][0] + loc[2][1]*(prxmax+labels[i].dims[0]/2)):
				if loc[1][0] > loc[0][0]:
					newx = block.minx-loc[2][1]*(prxmax+labels[i].dims[0]/2)-0.01
					neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
					labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
					loc[0][0] = newx
					loc[0][2] = neww
					if loc[0][2]-abs(loc[0][0]-block.minx) > loc[1][2]-abs(loc[1][0]-block.minx):
						loc[0][2] = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
						loc[1][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
					else:
						tempx = loc[0][0]
						tempy = loc[0][1]
						tempw = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
						loc[0][0] = loc[1][0]
						loc[0][1] = loc[1][1]
						loc[0][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
						loc[1][0] = tempx
						loc[1][1] = tempy
						loc[1][2] = tempw
				else:
					newx = block.maxx+loc[2][1]*(prxmax+labels[i].dims[0]/2)+0.01
					neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
					labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
					loc[2][1] = (loc[0][1] - block.maxy)/(labels[i].dims[1]+4)
					loc[0][0] = newx
					loc[0][2] = neww
					if loc[0][2]-abs(loc[0][0]-block.maxx) > loc[1][2]-abs(loc[1][0]-block.maxx):
						loc[0][2] = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
						loc[1][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
					else:
						tempx = loc[0][0]
						tempy = loc[0][1]
						tempw = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
						loc[0][0] = loc[1][0]
						loc[0][1] = loc[1][1]
						loc[0][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
						loc[1][0] = tempx
						loc[1][1] = tempy
						loc[1][2] = tempw
	elif loc[2][0] == "d":
		if block.maxx > (min(loc[0][0], loc[1][0]) - loc[2][1]*(prxmax+labels[i].dims[0]/2)) and block.minx < (max(loc[0][0], loc[1][0]) + loc[2][1]*(prxmax+labels[i].dims[0]/2)) and block.miny < loc[0][1] + loc[2][1]*(labels[i].dims[1]) and block.maxy > loc[0][1]:
			if block.maxx > (loc[0][0] - loc[2][1]*(prxmax+labels[i].dims[0]/2)) and block.minx < (loc[0][0] + loc[2][1]*(prxmax+labels[i].dims[0]/2)):
				if block.maxx > (loc[1][0] - loc[2][1]*(prxmax+labels[i].dims[0]/2)) and block.minx < (loc[1][0] + loc[2][1]*(prxmax+labels[i].dims[0]/2)):
					if loc[0][0] > block.maxx:
						if loc[0][2]-abs(loc[0][0]-block.maxx) > loc[1][2]-abs(loc[1][0]-block.maxx):
							loc[0][2] = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
					else:
						if loc[0][2]-abs(loc[0][0]-block.minx) > loc[1][2]-abs(loc[1][0]-block.minx):
							loc[0][2] = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
				else:
					if loc[0][0] > loc[1][0]:
						newx = block.minx-loc[2][1]*(prxmax+labels[i].dims[0]/2)-0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[1][0] = newx
						loc[1][2] = neww
						if loc[0][2]-abs(loc[0][0]-block.minx) > loc[1][2]-abs(loc[1][0]-block.minx):
							loc[0][2] = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
					else:
						newx = block.maxx+loc[2][1]*(prxmax+labels[i].dims[0]/2)+0.01
						neww = loc[1][2] + (loc[0][2]-loc[1][2])*(loc[1][0]-newx)/(loc[1][0]-loc[0][0])
						labels[i].locs.append([[newx, loc[0][1], neww], [loc[1][0], loc[1][1], loc[1][2]], [loc[2][0], loc[2][1]]])
						loc[1][0] = newx
						loc[1][2] = neww
						if loc[0][2]-abs(loc[0][0]-block.maxx) > loc[1][2]-abs(loc[1][0]-block.maxx):
							loc[0][2] = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
							loc[1][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
						else:
							tempx = loc[0][0]
							tempy = loc[0][1]
							tempw = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
							loc[0][0] = loc[1][0]
							loc[0][1] = loc[1][1]
							loc[0][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
							loc[1][0] = tempx
							loc[1][1] = tempy
							loc[1][2] = tempw
			elif block.maxx > (loc[1][0] - loc[2][1]*labels[i].dims[0]/2) and block.minx < (loc[1][0] + loc[2][1]*labels[i].dims[0]/2):
				if loc[1][0] > loc[0][0]:
					newx = block.minx-loc[2][1]*(prxmax+labels[i].dims[0]/2)-0.01
					neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
					labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
					loc[0][0] = newx
					loc[0][2] = neww
					if loc[0][2]-abs(loc[0][0]-block.minx) > loc[1][2]-abs(loc[1][0]-block.minx):
						loc[0][2] = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
						loc[1][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
					else:
						tempx = loc[0][0]
						tempy = loc[0][1]
						tempw = loc[0][2]-abs(loc[0][0]-block.minx)*prxwgh
						loc[0][0] = loc[1][0]
						loc[0][1] = loc[1][1]
						loc[0][2] = loc[1][2]-abs(loc[1][0]-block.minx)*prxwgh
						loc[1][0] = tempx
						loc[1][1] = tempy
						loc[1][2] = tempw
				else:
					newx = block.maxx+loc[2][1]*(prxmax+labels[i].dims[0]/2)+0.01
					neww = loc[0][2] + (loc[1][2]-loc[0][2])*(loc[0][0]-newx)/(loc[0][0]-loc[1][0])
					labels[i].locs.append([[loc[0][0], loc[0][1], loc[0][2]], [newx, loc[1][1], neww], [loc[2][0], loc[2][1]]])
					loc[0][0] = newx
					loc[0][2] = neww
					if loc[0][2]-abs(loc[0][0]-block.maxx) > loc[1][2]-abs(loc[1][0]-block.maxx):
						loc[0][2] = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
						loc[1][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
					else:
						tempx = loc[0][0]
						tempy = loc[0][1]
						tempw = loc[0][2]-abs(loc[0][0]-block.maxx)*prxwgh
						loc[0][0] = loc[1][0]
						loc[0][1] = loc[1][1]
						loc[0][2] = loc[1][2]-abs(loc[1][0]-block.maxx)*prxwgh
						loc[1][0] = tempx
						loc[1][1] = tempy
						loc[1][2] = tempw


#init
import xml.etree.ElementTree as ET
from PIL import ImageFont
import math
import sys
svg = ET.parse(sys.argv[1])
root = svg.getroot()
labels = []
blocks = []
cols = []

#variables for preferences
lngmax = 50		#edge length where there is no longer a benefit
lngwgh = 0.5	#how much short length is an issue
cntwgh = 0.5	#how much centre of the edge is an issue
expwgh = 0.1		#the cost of each pixel of expansion
sclwgh = 100	#the cost of shrinking the label
prxmax = 4		#how far from an object is free
prxwgh = 1		#how much each pixel too close costs
upref =  0.1	#preference for labels on top of edges
dpref = -0.1	#preference for labels on bottom of edges
lpref =  0		#preference for labels on left of edges
rpref =  0		#preference for labels on right of edges

#viewbox reading
viewbox = root.attrib["viewBox"]
vbox = viewbox.split(" ")
for i in range(0, 4):
	vbox[i] = float(vbox[i])

#label + block finding
for child in root:
	for gchild in child:
		if gchild.get("class") == "edge":
			foundlabel = gchild.find("{http://www.w3.org/2000/svg}text")
			if foundlabel != None:
				newlabel = Label(foundlabel, gchild)
				labels.append(newlabel)
			foundlabel = gchild.find("{http://www.w3.org/2000/svg}path")
			if foundlabel != None:
				edgeHandle(foundlabel) 
		foundlabel = gchild.find("{http://www.w3.org/2000/svg}polygon")
		if foundlabel != None:
			newBlock = Block(foundlabel, False)
			blocks.append(newBlock)

#calculate new vbox
vminx = blocks[0].minx
vmaxx = blocks[0].maxx
vminy = blocks[0].miny
vmaxy = blocks[0].maxy
for block in blocks:
	vminx = min(vminx, block.minx)
	vminy = min(vminy, block.miny)
	vmaxx = max(vmaxx, block.maxx)
	vmaxy = max(vmaxy, block.maxy)
			
#prints
print("Viewbox is " + str(vbox))
print("but it could be " + str([vminx, vmaxy, vmaxx-vminx+8, vmaxy-vminy+8]))
	
print("\nlabels")
for label in labels:
	print(label)
	
print("\nblocks")
for block in blocks:
	print(block)
	
#gen locations + prelim heurs
for label in labels:
	locgen(label)

for i in range(0, len(labels)):
	for loc in labels[i].locs: #first pass, for removing intersections and scaling down partial obstructions
		for block in blocks:
			breaknow = loccollide(i, loc, block)
			if breaknow:
				break
	
	for k in range(len(labels[i].locs)-1, -1, -1):
		if labels[i].locs[k][0][0] == "No":
			labels[i].locs.remove(labels[i].locs[k])
								
	for loc in labels[i].locs: #second pass, for detecting things that are too close to edges
		for block in blocks:
			locprox(i, loc, block)
			
			
	for k in range(0, len(labels[i].locs)):
		if labels[i].locs[k][2][1] != 1:
			labels[i].locs[k][0][2] = labels[i].locs[k][0][2] - sclwgh*(1-labels[i].locs[k][2][1])
			labels[i].locs[k][1][2] = labels[i].locs[k][1][2] - sclwgh*(1-labels[i].locs[k][2][1])
	labels[i].locs.sort(key=lambda loc: loc[0][2], reverse=True)
	temp = "Locations: "
	for k in labels[i].locs:
		temp = temp + "\n(" + str(k[0][0]) + ", " + str(k[0][1]) + "), " + '%.2f' % k[0][2] + " to (" + str(k[1][0]) + ", " + str(k[1][1]) + "), " + '%.2f' % k[1][2] + ", " + k[2][0] + ", " + str(k[2][1])
	print(labels[i].text)
	print(temp)
	labelcollide = False
	labels[i].setx(labels[i].locs[0][0][0])
	labels[i].sety(labels[i].locs[0][0][1])
	labels[i].scale = labels[i].locs[0][2][1]
	labels[i].setalign(labels[i].locs[0][2][0])
	for j in range(0, i):
		if labels[i].minx < labels[j].maxx and labels[i].maxx > labels[j].minx and labels[i].miny < labels[j].maxy and labels[i].maxy > labels[j].miny:
			labelcollide = True
			break
	if labelcollide:
		labels[i].peak = labels[i].locs[0][0][2]
		cols.append([labels[i].text, labels[i].minx, labels[i].maxx, labels[i].miny, labels[i].maxy, labels[j].text, labels[j].minx, labels[j].maxx, labels[j].miny, labels[j].maxy])
		for loc in labels[i].locs:
			loc[0][2] = loc[0][2] + sclwgh*(1-loc[2][1])
			loc[1][2] = loc[1][2] + sclwgh*(1-loc[2][1])
			loccollide(i, loc, labels[j])
			loc[0][2] = loc[0][2] - sclwgh*(1-loc[2][1])
			loc[1][2] = loc[1][2] - sclwgh*(1-loc[2][1])
			for k in range(len(labels[i].locs)-1, -1, -1):
				if labels[i].locs[k][0][0] == "No":
					labels[i].locs.remove(labels[i].locs[k])
		labels[i].locs.sort(key=lambda loc: loc[0][2], reverse=True)
		if labels[i].locs[0][0][2] == labels[i].peak:
			labels[i].setx(labels[i].locs[0][0][0])
			labels[i].sety(labels[i].locs[0][0][1])
			labels[i].scale = labels[i].locs[0][2][1]
			labels[i].setalign(labels[i].locs[0][2][0])
		else:
			heurloss = labels[i].peak - labels[i].locs[0][0][2]
			labels[j].peak = labels[j].locs[0][0][2]
			for loc in labels[j].locs:
				loc[0][2] = loc[0][2] + sclwgh*(1-loc[2][1])
				loc[1][2] = loc[1][2] + sclwgh*(1-loc[2][1])
				loccollide(j, loc, labels[i])
				loc[0][2] = loc[0][2] - sclwgh*(1-loc[2][1])
				loc[1][2] = loc[1][2] - sclwgh*(1-loc[2][1])
				for k in range(len(labels[j].locs)-1, -1, -1):
					if labels[j].locs[k][0][0] == "No":
						labels[j].locs.remove(labels[j].locs[k])
			labels[j].locs.sort(key=lambda loc: loc[0][2], reverse=True)
			if labels[j].locs[0][0][2] + heurloss > labels[j].peak:
				labels[j].setx(labels[j].locs[0][0][0])
				labels[j].sety(labels[j].locs[0][0][1])
				labels[j].scale = labels[j].locs[0][2][1]
				labels[j].setalign(labels[j].locs[0][2][0])
			else:
				labels[i].setx(labels[i].locs[0][0][0])
				labels[i].sety(labels[i].locs[0][0][1])
				labels[i].scale = labels[i].locs[0][2][1]
				labels[i].setalign(labels[i].locs[0][2][0])
			

	
for label in labels:
	vminx = min(vminx, label.minx)
	vminy = min(vminy, label.miny)
	vmaxx = max(vmaxx, label.maxx)
	vmaxy = max(vmaxy, label.maxy)
	if label.scale != 1:
		label.object.attrib["font-size"] = '%.2f' % ((float(label.object.attrib["font-size"]))*label.scale) #maybe find out why the +7 is needed
	

#convert stuff back and output to file
vbox = [vminx, vmaxy, vmaxx-vminx+8, vmaxy-vminy+8]
root.attrib["width"] = str(int(math.ceil(vbox[2]))) + "pt"
root.attrib["height"] = str(int(math.ceil(vbox[3]))) + "pt"
for i in range(0, 4):
	vbox[i] = '%.2f' % vbox[i]
viewbox = vbox[0] + " " + vbox[1] + " " + vbox[2] + " " + vbox[3]
root.attrib["viewBox"] = viewbox
svg.write(sys.argv[2])