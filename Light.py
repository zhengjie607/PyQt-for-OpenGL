from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from Vector3f import *
from Camera import camera
class Light:
    def __init__(self):
        glShadeModel(GL_SMOOTH)
        self.lightpos=[0,0,1,0]
        whiltlitht=[1,1,1,1]
        ambient_light=[0.329412,0.223529,0.027451,1.000000]
        diffuse=[0.780392,0.568627,0.113725,1.000000]
        specular=[0.992157,0.941176,0.807843,1.000000]
        shininess = 27.897400
        glMaterial(GL_FRONT,GL_SPECULAR, specular)
        glMaterial(GL_FRONT,GL_SHININESS, shininess)
        glMaterial(GL_FRONT,GL_DIFFUSE, diffuse)

        glLight(GL_LIGHT0,GL_POSITION, self.lightpos)
        glLight(GL_LIGHT0,GL_DIFFUSE, whiltlitht)
        glLight(GL_LIGHT0,GL_SPECULAR, whiltlitht)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)   
        glEnable(GL_DEPTH_TEST)
    def Update(self):
        cam=camera()
        self.lightpos=[-cam.forwardDir.X,-cam.forwardDir.Y,-cam.forwardDir.Z,0]
    def material(self):
        pass
    
        
