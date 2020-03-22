import sys
import pyglet
from math import *
import random

windowSize= 800

#The length of one side of the square
#in percentage of the window
SIZE = 0.8
WINDOW_CENTER = windowSize/2
HALF_SIZE = WINDOW_CENTER*SIZE
CIRCLE_RADIUS = (windowSize/2)*SIZE

#Number of Vertices used to draw the circle
NUM_OF_VERTICES = 50000

#Speed at which points are drawn
SPEED = 1

allPoints = []

class Point:
    def __init__(self):
        vertexFormat = 'v2i'
        color = ('c3B', [100,500,300])

        #create new point at random position
        x = random.randint(abs(WINDOW_CENTER-HALF_SIZE), WINDOW_CENTER+HALF_SIZE)
        y = random.randint(abs(WINDOW_CENTER-HALF_SIZE), WINDOW_CENTER+HALF_SIZE)

        self.vertices = pyglet.graphics.vertex_list(1, (vertexFormat, [x,y]), color)
    
    def draw(self):
        self.vertices.draw(pyglet.gl.GL_POINTS)

class Circle:
    def __init__(self):
        vertexFormat = 'v2f'
        colorFormat = 'c3B'
        color = [0,0,0]*(NUM_OF_VERTICES)

        #Center the circle in the square
        center = windowSize/2

        #Radius based on size of length of a side of the square
        size = center * SIZE
        
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
        vertexFormat = 'v2i'
        colorFormat = 'c3B'

        #Color of the square
        color = [100, 100, 100] *4

        #Get the vertices based on size
        allVertices = self.get_vectors()
        allVertices = [abs(int(x)) for x in allVertices]

        #define the vertices as a pyglet vertex_list
        self.vertices = pyglet.graphics.vertex_list(4, (vertexFormat, allVertices), (colorFormat, color))

    def get_vectors(self):
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

    def on_draw(self):
        self.clear()
        self.square.draw()
        self.circle.draw()
        for point in allPoints:
            point.draw()
    
    def update(self, dt):
        for i in range(SPEED):
            allPoints.append(Point())

if __name__ == '__main__':
    #Create window
    window = View(width=windowSize, height=windowSize, caption="Estimating Pi", resizable=False)

    #Set Background
    pyglet.gl.glClearColor(1,1,1,0.5)

    pyglet.clock.schedule_interval(window.update, 1/30.0)
    pyglet.app.run()
