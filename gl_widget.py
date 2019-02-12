from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Camera import camera
from Vector3f import *
from Light import Light,Materials
from numpy import array
class GLWidget(QOpenGLWidget):
    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(10, 10,700, 700))#窗口位置和大小
        self.isMove=False
        self.isRotate=False
        self.material=Materials['brass']
        self.data=array([],'f')
    def initdata(self,data):
        self.data=data
    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        self.camera=camera()
        self.light=Light(self.material)
    def paintGL(self):
        self.camera.Update()
        self.light.Update(self.material)
        #glutWireTeapot(0.5)
        if self.data.any()==False:
            print('mesh is none')
        else:
            #pass
            #self.testdraw()
            self.VBO()
    def testdraw(self):
        glBegin(GL_TRIANGLES)
        i=0
        for i in range(0,len(data),3):
            glNormal3f(normal[i],normal[i+1],normal[i+2])
            glVertex3f(data[i],data[i+1],data[i+2])
        glEnd()
    def VBO(self):
        #glPushMatrix()
        vb=vbo.VBO(self.data)
        vb.bind()
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glNormalPointer(GL_FLOAT, 24, vb+12)
        glVertexPointer(3, GL_FLOAT, 24, vb )
        glDrawArrays(GL_TRIANGLES, 0, len(self.data))
        vb.unbind()
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        #glPopMatrix()
    def mousePressEvent(self,event):
        self.myMousePosition=event.pos()
        if event.button()==QtCore.Qt.LeftButton:
            self.isMove=True
        if event.button()==QtCore.Qt.RightButton:
            self.isRotate=True
        #self.update()
    def wheelEvent(self,event):
        if event.angleDelta().y()>0:
            self.camera.right*=0.95
            self.camera.top*=0.95
        if event.angleDelta().y()<0:
            self.camera.right/=0.95
            self.camera.top/=0.95
        self.update()
    def mouseReleaseEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.isMove=False
        if event.button()==QtCore.Qt.RightButton:
            self.isRotate=False
    def mouseMoveEvent(self,event):
        if self.isMove:
            moveX=event.pos().x()-self.myMousePosition.x()
            moveY=event.pos().y()-self.myMousePosition.y()
            self.camera.Move(moveX*self.camera.right/200,moveY*self.camera.right/200)
            self.myMousePosition=event.pos()
        if self.isRotate:
            moveX=event.pos().x()-self.myMousePosition.x()
            moveY=event.pos().y()-self.myMousePosition.y()
            self.camera.Yaw(-moveX)
            self.camera.Pitch(-moveY)
            self.light.lightpos=[-self.camera.forwardDir.X,-self.camera.forwardDir.Y,-self.camera.forwardDir.Z,0]
            self.myMousePosition=event.pos()
        self.update()
