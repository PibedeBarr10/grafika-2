import numpy as np
from math import sin, cos
from pygame import draw
from operator import itemgetter

# Wymiary okna programu
width = 1000
height = 600

# Kolor bryły
obj_color = (255, 255, 255)

# Wartość przesunięcia punktów
krok = 0.5

# Macierz do rzutowania
d = 500
projectionMatrix = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,1/d,0]
], dtype = float)

# Macierz do przesunięcia
moveMatrix = np.array([
    [width/2],
    [height/2],
    [0],
    [0]
], dtype = float)

# Rzutowanie
def projection(Matrix):
    # Transpozycja macierzy
    Matrix = Matrix.T

    wsp_z = Matrix[2]

    A = np.dot(projectionMatrix, Matrix)
    A = A/(wsp_z/d)

    #przesuniecie obiektu na środek ekranu
    A += moveMatrix

    return A[:-1,:]

# Zmienne do wyliczania cosinusa kąta padania światła w metodzie oblicz_cos
lightPoint = np.array([0,0,-100], dtype = float)
lightDirection = np.array([0,0,0], dtype = float)

# Wyliczenie cosinusa kąta padania koloru
def oblicz_cos(normalVector, lightDirection):

    # Wyliczenie długości wektorów
	normalVectorlLength = (normalVector[0]**2 + normalVector[1]**2 + normalVector[2]**2) ** 0.5
	lightDirectionlLength = (lightDirection[0]**2 + lightDirection[1]**2 + lightDirection[2]**2) ** 0.5

	normalVector = normalVector/normalVectorlLength
	lightDirection = lightDirection/lightDirectionlLength

	cosinus = np.dot(normalVector, lightDirection)
	return max(0, cosinus)

class Mesh:
    def __init__(self, vertices, faces, screen):
        self.screen = screen
        self.vertices = np.ones((len(vertices),4), dtype = float)
        self.vertices[:,:-1] = vertices
        self.faces = np.array(faces, dtype = int)
        self.cosinus = 0

        # Tablica, w której sortuje się ściany do algorytmu malarskiego
        self.depthArray = []
		
		# Początkowe oddalenie bryły
        for i in range(len(self.vertices)):
            self.vertices[i][2] -= 30

    # Generowanie sceny    
    def render(self):
        A = projection(self.vertices)
        Matrix = self.vertices.T

        for face in self.faces:
            # Wektory normalne
            normal_vector1 = np.array([Matrix[0][int(face[0])-1], Matrix[1][int(face[0])-1], Matrix[2][int(face[0])-1]])
            normal_vector2 = np.array([Matrix[0][int(face[1])-1], Matrix[1][int(face[1])-1], Matrix[2][int(face[1])-1]])
            normal_vector3 = np.array([Matrix[0][int(face[2])-1], Matrix[1][int(face[2])-1], Matrix[2][int(face[2])-1]])

            # Wyliczanie punktu środkowego trójkąta z wektorów normalnych trójkąta
            temp1 = normal_vector3 - normal_vector1
            temp2 = normal_vector2 - normal_vector1
            centerPoint = (normal_vector1 + normal_vector2 + normal_vector3)/3

            tempFace = np.cross(temp1, temp2)

            # Nieuwzględnianie w rysowaniu ścian zasłoniętych
            if (normal_vector1[0] * tempFace[0] + normal_vector1[1] * tempFace[1] + normal_vector1[2] * tempFace[2]) > 0:
                # Wektory ze współrzędnymi zrzutowanymi: x i y
                vector1 = [int(A[0][int(face[0])-1]), int(A[1][int(face[0])-1])]
                vector2 = [int(A[0][int(face[1])-1]), int(A[1][int(face[1])-1])]
                vector3 = [int(A[0][int(face[2])-1]), int(A[1][int(face[2])-1])]
                
                self.depthArray.append((centerPoint[2], tempFace, centerPoint, [vector1, vector2, vector3]))

        # Sortowanie całej tablicy po współrzędnej Z punktu centralnego ściany
        self.depthArray.sort(key=itemgetter(0))

        for i in self.depthArray:
            self.drawTriangle(i[1], i[2], i[3][0], i[3][1], i[3][2], obj_color)
        
        # Czyszczenie tablicy
        self.depthArray.clear()

    # Rysowanie trójkątów
    def drawTriangle(self, tempFace, centerPoint, point1, point2, point3, color):

        # Wyliczanie kąta
        lightDirection = lightPoint - centerPoint
        self.cosinus = oblicz_cos(tempFace, lightDirection)
        
        # Wyliczenie koloru po cieniowaniu
        final_color = (color[0] * self.cosinus, color[1] * self.cosinus, color[2] * self.cosinus)
        
        # Rysowanie trójkąta w pygame
        draw.polygon(self.screen, final_color, ((point1[0], point1[1]), (point2[0], point2[1]), (point3[0], point3[1])))
        
    def Right(self):
        for i in range(len(self.vertices)):
            self.vertices[i][0] += krok
    
    def Left(self):
        for i in range(len(self.vertices)):
            self.vertices[i][0] -= krok
    
    def Up(self):
        for i in range(len(self.vertices)):
            self.vertices[i][1] -= krok
    
    def Down(self):
        for i in range(len(self.vertices)):
            self.vertices[i][1] += krok
    
    def Forward(self):
        for i in range(len(self.vertices)):
            self.vertices[i][2] += krok
    
    def Back(self):
        for i in range(len(self.vertices)):
            self.vertices[i][2] -= krok
    
    def rotate(self, axis, angle):
        # Macierze obrotu
        rotateX = np.array([
            [1, 0, 0, 0],
            [0, cos(angle), sin(angle), 0],
            [0, -sin(angle), cos(angle), 0],
            [0, 0, 0, 1]
        ])

        rotateY = np.array([
            [cos(angle), 0, -sin(angle), 0],
            [0, 1, 0, 0],
            [sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])

        rotateZ = np.array([
            [cos(angle), sin(angle), 0, 0],
            [-sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        if axis == 'x':
            self.vertices = np.dot(self.vertices, rotateX)
        elif axis == 'y':
            self.vertices = np.dot(self.vertices, rotateY)
        else:
            self.vertices = np.dot(self.vertices, rotateZ)