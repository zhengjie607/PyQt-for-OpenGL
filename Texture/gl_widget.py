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
from PIL import Image
import time
class GLWidget(QOpenGLWidget):
    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(10, 10,700, 700))#窗口位置和大小
        self.isMove=False
        self.isRotate=False
        self.model=[]#该列表需要存储一个一个的字典，字典形式为{'material':Materials,'data':numpy.array()}，每一个model[x]代表一个模型，包含材质和点的数据
        self.quadratic=gluNewQuadric()#创建一个二次曲面物体
        gluQuadricTexture(self.quadratic,GL_TRUE)#启用该二次曲面的纹理
    def changeGeometry(self,x,y,width,height):
        self.setGeometry(QtCore.QRect(x, y,width, height))
    def initdata(self,data):
        self.model=data
    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0,0,0,0)
        self.camera=camera()
        self.light=Light(Materials[0])
        self.loadTexture()
    def paintGL(self):
        self.camera.Update()
        self.drawTexture()
        #self.textureSphere()
        
        for i in range(len(self.model)):
            #print("Load")
            glPushMatrix()
            self.light.Update(self.model[i]['material'])
            self.VBO(self.model[i]['data'])
            glPopMatrix()
    #该函数用来截屏并保存为png图像，glReadPixels的参数以窗体左下角为坐标原点。
    def loadTexture(self):
        import os   
        file_dir="image/jpg"
        for root, dirs, imgFiles in os.walk(file_dir):  
            print(imgFiles)
        self.len_image=len(imgFiles)
        for i in range(self.len_image):
            img=Image.open(file_dir+"/"+imgFiles[i])
            width,height=img.size
            img=img.tobytes('raw','RGBX',0,-1)
            #print(str(i)+":"+str(img[0:100]))
            glGenTextures(1)#申请2个纹理对象
            glBindTexture(GL_TEXTURE_2D,i)#设置当前纹理对象
            glTexImage2D(GL_TEXTURE_2D,0,4,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,img)#将纹理从内存上传到显存。第一个0：原始级别，基本不变；4：在显卡的像素格式；第二个0： 参数 border 注明了纹理是否有边框。无边框取值为 0， 有边框取值为 1， 边框的颜色由 GL_TEXTURE_BORDER_COLOR 选项设置；GL_RGBA：在内存的像素格式；GL_UNSIGNED_BYTE：每一个像素分量的类型
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
            #glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_REPEAT)
            #glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE, GL_DECAL)#GL_DECAL为贴纸模式
    
    def textureSphere(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        gluSphere(self.quadratic,20,80,80)
        glTranslatef(50,0,0)
        glBindTexture(GL_TEXTURE_2D, 1)
        gluSphere(self.quadratic,20,80,80)
        glTranslatef(50,0,0)
        glBindTexture(GL_TEXTURE_2D, 2)
        gluSphere(self.quadratic,20,80,80)
        glTranslatef(0,50,0)
        glBindTexture(GL_TEXTURE_2D, 3)
        gluSphere(self.quadratic,20,80,80)
        glTranslatef(-50,0,0)
        glBindTexture(GL_TEXTURE_2D, 4)
        gluSphere(self.quadratic,20,80,80)
        glTranslatef(-50,0,0)
        glBindTexture(GL_TEXTURE_2D, 5)
        gluSphere(self.quadratic,20,80,80)
        
        glTranslatef(0,0,50)
        glBindTexture(GL_TEXTURE_2D, 6)
        gluSphere(self.quadratic,20,80,80)
        
        glTranslatef(50,0,0)
        glBindTexture(GL_TEXTURE_2D, 7)
        gluSphere(self.quadratic,20,80,80)
        glTranslatef(50,0,0)
        glBindTexture(GL_TEXTURE_2D, 8)
        gluSphere(self.quadratic,20,80,80)
        glTranslatef(0,-50,0)
        glBindTexture(GL_TEXTURE_2D, 9)
        gluSphere(self.quadratic,20,80,80)
        glTranslatef(-50,0,0)
        glBindTexture(GL_TEXTURE_2D, 10)
        gluSphere(self.quadratic,20,80,80)
        glTranslatef(-50,0,0)
        glBindTexture(GL_TEXTURE_2D, 11)
        gluSphere(self.quadratic,20,80,80)
    def drawTexture(self):
        #glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBegin(GL_QUADS)   
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-10.0, -10.0, -10.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-10.0, -10.0, 10.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-10.0, 10.0, 10.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-10.0, 10.0, -10.0)
        glEnd()
        

         #切换纹理
        glBindTexture(GL_TEXTURE_2D, 1)
        glBegin(GL_QUADS)        
       
        
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-10.0, -10.0, 10.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(10.0, -10.0, 10.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(10.0, 10.0, 10.0)
        glTexCoord2f(0.0,1.0)
        glVertex3f(-10.0, 10.0, 10.0)
        glEnd()
 #切换纹理

        glBindTexture(GL_TEXTURE_2D, 2)
        glBegin(GL_QUADS)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3f(10.0, -10.0, -10.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(10.0, 10.0, -10.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(10.0, 10.0, 10.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(10.0, -10.0, 10.0)
        glEnd()
 #切换纹理

        glBindTexture(GL_TEXTURE_2D, 3)
        glBegin(GL_QUADS)        
        
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-10.0, -10.0, -10.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-10.0, 10.0, -10.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(10.0, 10.0, -10.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(10.0, -10.0, -10.0)
        glEnd()
 #切换纹理

        glBindTexture(GL_TEXTURE_2D, 4)
        glBegin(GL_QUADS)        
        
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-10.0, -10.0, -10.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(10.0, -10.0, -10.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(10.0, -10.0, 10.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-10.0, -10.0, 10.0)
        glEnd()
 #切换纹理

        glBindTexture(GL_TEXTURE_2D, 5)
        glBegin(GL_QUADS)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-10.0, 10.0, -10.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-10.0, 10.0, 10.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(10.0, 10.0, 10.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(10.0, 10.0, -10.0)
        glEnd()
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
