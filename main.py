import sys
import pyglet
from math import *
import random

windowSize= 1000

#The length of one side of the square
#in percentage of the window
SIZE = 0.8

#Center of window
WINDOW_CENTER = windowSize/2

#Half the size of the square (Used for coordinates)
HALF_SIZE = WINDOW_CENTER*SIZE

#The length of the radius (used for pi calculation)
CIRCLE_RADIUS = (windowSize/2)*SIZE

#Number of Vertices used to draw the circle
NUM_OF_VERTICES = 80000

#Speed at which points are drawn
SPEED = 1

#List containing all the points drawn
allPoints = []

batchAllPoints = pyglet.graphics.Batch()

totalPoints = 0
pointsInCircle = 0

def getPi():
    return (4*pointsInCircle)/totalPoints

class Point:
    def __init__(self):
        #create new point at random position
        self.x = random.randint(abs(WINDOW_CENTER-HALF_SIZE), WINDOW_CENTER+HALF_SIZE)
        self.y = random.randint(abs(WINDOW_CENTER-HALF_SIZE), WINDOW_CENTER+HALF_SIZE)

        circleColor = ('c3B', [0, 0, 0])
        squareColor = ('c3B', [255, 255, 255])

        #Set up data for the vertex list
        vertexFormat = 'v2i'

        #Check if the point is in the circle
        if self.isInCirlce():
            global pointsInCircle
            pointsInCircle = pointsInCircle+ 1
            self.color = circleColor
        else: 
            self.color = squareColor

        #create a pyglet vertex list
        #self.vertices = pyglet.graphics.vertex_list(1, (vertexFormat, [self.x,self.y]), self.color)
    
    def draw(self):
        self.vertices.draw(pyglet.gl.GL_POINTS)

    def isInCirlce(self):
        #Check if it is in circle
        if ((self.x-WINDOW_CENTER)**2 + (self.y -WINDOW_CENTER)**2) < CIRCLE_RADIUS**2:
            return True
        else:
            return False

class Circle:
    def __init__(self):
        #Set up vertex list params
        vertexFormat = 'v2f'
        colorFormat = 'c3B'
        color = [255,255,255]*(NUM_OF_VERTICES)

        #Center the circle in the square
        center = windowSize/2

        #Radius based on size of length of a side of the square
        size = center * SIZE
        
        #Create vertex list for the vertices in a circle
        verts = []
        for i in range(NUM_OF_VERTICES):
            angle = radians(float(i)/NUM_OF_VERTICES * 360.0)
            x = size*cos(angle) + center
            y = size*sin(angle) + center
            verts += [x,y]
        
        self.vertices = pyglet.graphics.vertex_list(NUM_OF_VERTICES, (vertexFormat, verts), (colorFormat, color))

    def draw(self):
        self.vertices.draw(pyglet.gl.GL_POLYGON)

class Square:
    def __init__(self):
        #Set up format for vertex list params
        vertexFormat = 'v2i'
        colorFormat = 'c3B'

        #Color of the square
        color = [0, 0, 0] *4

        #Get the vertices based on size
        allVertices = self.get_vectors()
        allVertices = [abs(int(x)) for x in allVertices]

        #define the vertices as a pyglet vertex_list
        self.vertices = pyglet.graphics.vertex_list(4, (vertexFormat, allVertices), (colorFormat, color))

    def get_vectors(self):
        #TODO: Change these to use the global variables defined above
        centerX = windowSize/2        
        centerY = windowSize/2
        halfSizeX = (SIZE*windowSize)/2
        halfSizeY = (SIZE*windowSize)/2
        
        return [centerX-halfSizeX,centerY+halfSizeY, centerX+halfSizeX,centerY+halfSizeY, centerX+halfSizeX,centerY-halfSizeY, centerX-halfSizeX,centerY-halfSizeY]

    def draw(self):
        self.vertices.draw(pyglet.gl.GL_QUADS)

class View(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.square = Square()
        self.circle = Circle()
        self.piLabel = pyglet.text.Label('0', font_name='Times New Roman', font_size=50, x=20, y=20, color=(0,0,0,255))

    def on_draw(self):
        self.clear()
        self.square.draw()
        self.circle.draw()
        self.piLabel.draw()
        batchAllPoints.draw()

        # for point in allPoints:
            # point.draw()

    def update(self, dt):
        global totalPoints
        for i in range(SPEED):
            #Create a new point
            point = Point()

            #Add it to the batch
            batchAllPoints.add(1, pyglet.gl.GL_POINTS, None, ('v2i', [point.x, point.y]), point.color)
            # allPoints.append(Point())

            #Keep track of number of points
            totalPoints = totalPoints + 1

            #Calculate pi
            piFloat = getPi()

            #Convert pi to string
            piString = "{:.9f}".format(piFloat)

            #Update label
            # self.piLabel = pyglet.text.Label(piString, font_name='Times New Roman', font_size=50, x=20, y=20, color=(0,0,0,255))
            self.piLabel.text = piString

if __name__ == '__main__':
    #Create window
    window = View(width=windowSize, height=windowSize, caption="Estimating Pi", resizable=False)
    
    #Set Background
    pyglet.gl.glClearColor(220/255,220/255, 220/255,0)

    #Schedule update function
    pyglet.clock.schedule_interval(window.update, 1/60.0)

    pyglet.app.run()
