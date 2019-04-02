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
        self.model=[]#该列表需要存储一个一个的字典，字典形式为{'material':Materials,'data':numpy.array()}，每一个model[x]代表一个模型，包含材质和点的数据
    def initdata(self,data):
        self.model=data
    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1,1,1,0)
        self.camera=camera()
        self.light=Light(Materials[0])
    def paintGL(self):
        self.camera.Update()
        for i in range(len(self.model)):
            #print("Load")
            glPushMatrix()
            self.light.Update(self.model[i]['material'])
            self.VBO(self.model[i]['data'])
            glPopMatrix()
    #该函数用来截屏并保存为png图像，glReadPixels的参数以窗体左下角为坐标原点。
    def geti(self):
        data = glReadPixels(10, 190, 700, 700, GL_RGBA, GL_UNSIGNED_BYTE)
        import png
        png.write(open("screen_shot.png", "wb"), 700, 700, 4, data)
    def VBO(self,data):
        #glPushMatrix()
        vb=vbo.VBO(data)
        vb.bind()
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glNormalPointer(GL_FLOAT, 24, vb+12)
        glVertexPointer(3, GL_FLOAT, 24, vb )#在每一个周期里，都有6个32-bit浮点数据，总共4*6=24     3代表数量
        glDrawArrays(GL_TRIANGLES, 0, len(data))
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
