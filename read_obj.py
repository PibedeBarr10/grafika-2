class ObjLoader(object):
    def __init__(self, fileName):
        self.vertices = []
        self.faces = []
        try:
            f = open(fileName)
            for line in f:
                if line[0] == "v":
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)
                    vertex = (round(float(line[index1:index2]), 2), round(float(line[index2:index3]), 2), round(float(line[index3:-1]), 2))
                    self.vertices.append(vertex)
                elif line[0] == "f":
                    i = line.find(" ") + 1
                    face = []
                    for item in range(line.count(" ")):
                        if line.find(" ", i) == -1:
                            face.append(line[i:-1])
                            break
                        face.append(line[i:line.find(" ", i)])
                        i = line.find(" ", i) + 1
                    self.faces.append(face)
            f.close()
        except IOError:
            print(".obj file not found.")
