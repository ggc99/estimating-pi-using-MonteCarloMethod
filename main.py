import sys
import pyglet
from math import *

windowWidth = 800
windowHeight = 800

#The length of one side of the square
#in percentage of the window
SIZE = 0.8

NUM_OF_VERTICES = 10000

class Circle:
    def __init__(self):
        vertexFormat = 'v2f'
        colorFormat = 'c3B'
        color = [0,0,0]*(NUM_OF_VERTICES)

        #Center the circle in the square
        centerX = windowWidth/2
        centerY = windowHeight/2

        #Radius based on size of length of a side of the square
        size = centerX * SIZE

        verts = []
        for i in range(NUM_OF_VERTICES):
            angle = radians(float(i)/NUM_OF_VERTICES * 360.0)
            x = size*cos(angle) + centerX
            y = size*sin(angle) + centerX
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
        centerX = windowHeight/2        
        centerY = windowWidth/2
        halfSizeX = (SIZE*windowWidth)/2
        halfSizeY = (SIZE*windowHeight)/2
        
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

if __name__ == '__main__':
    #Create window
    window = View(width=windowWidth, height=windowHeight, caption="Estimating Pi", resizable=False)

    #Set Background
    pyglet.gl.glClearColor(1,1,1,0.5)

    #pyglet.clock.schedule_interval(window.update, 1/10.0)
    pyglet.app.run()
