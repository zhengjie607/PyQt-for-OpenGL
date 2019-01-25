
# coding: utf-8

# In[1]:


from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QPoint,QLineF
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import math
import form
from form import Ui_Form
from Camera import camera
from Vector3f import *
from Light import Light
from Optimizermaster.FileHandler import FileHandler
import sys
from ctypes import sizeof, c_float, c_void_p, c_uint
data=array([],'f')#导入文件
normal=array([],'f')
float_size = sizeof(c_float)
record_len       = 12 * float_size
vertex_offset    = c_void_p(0 * float_size)
class GLWidget(QOpenGLWidget):
    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(10, 10,700, 700))#窗口位置和大小
        self.isMove=False
        self.isRotate=False
    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        self.camera=camera()
        self.light=Light()
    def paintGL(self):
        self.camera.Update()
        self.light.Update()
        #glutWireTeapot(0.5)
        if data.any()==False:
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
        '''print(1)
        glEnableClientState(GL_VERTEX_ARRAY)
        print(2)
        data_buffer = (c_float*len(data))(*data)#地址和所在长度
        print(3)
        glBindBuffer(GL_ARRAY_BUFFER,glGenBuffers(1))
        print(4)
        glBufferData(GL_ARRAY_BUFFER,data_buffer,GL_STATIC_DRAW)
        del data_buffer
        print(5)
        glVertexPointer(3, GL_FLOAT,record_len , vertex_offset)
        print(6)
        print(len(data))
        #glDrawArrays(GL_TRIANGLES,0,2001)
        #offset=0
        #glDrawElements(GL_TRIANGLES,3,GL_UNSIGNED_INT, c_void_p(offset))
        glDrawArrays(GL_TRIANGLES,0,len(data))
        print(7)
        glDisableClientState(GL_VERTEX_ARRAY)
        '''
       
        #self.vnor=vbo.VBO(normal)
        self.vb=vbo.VBO(data)
        
        #self.vnor.bind()
        self.vb.bind()
        
        self.vertex=data.take([0,1,2],axis=1)
        #self.normal=data.take([3,4,5],axis=1)
        #glEnableVertexAttribArray(self.vertex)
        #glEnableVertexAttribArray(self.normal)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        #glEnableClientState(GL_COLOR_ARRAY)
        #glVertexAttribPointer(self.vertex,3, GL_FLOAT,False, 24, self.vb)
        #glVertexAttribPointer(self.normal, 3, GL_FLOAT,False, 24, self.vb+12)
        
        glNormalPointer(GL_FLOAT, 24, self.vb+12)
        #glVertexPointerf(self.vb)
        
        glVertexPointer(3, GL_FLOAT, 24, self.vb )
        #glColorPointer(3, GL_FLOAT, 24, self.vb+12 )
        #glDrawArrays(GL_TRIANGLES, 0, len(data)*3)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertex))
        #self.vnor.unbind()
        self.vb.unbind()
        #glDisableVertexAttribArray(self.vertex)
        #glDisableVertexAttribArray(self.normal)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        #glDisableClientState(GL_COLOR_ARRAY)
    def mousePressEvent(self,event):
        self.myMousePosition=event.pos()
        if event.button()==Qt.LeftButton:
            self.isMove=True
        if event.button()==Qt.RightButton:
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
        if event.button()==Qt.LeftButton:
            self.isMove=False
        if event.button()==Qt.RightButton:
            self.isRotate=False
        #print('mPos:(X:'+str(self.camera.mPos.X)+',Y:'+str(self.camera.mPos.Y)+',Z:'+str(self.camera.mPos.Z)+')')
        #print('mViewCenter:(X:'+str(self.camera.mViewCenter.X)+',Y:'+str(self.camera.mViewCenter.Y)+',Z:'+str(self.camera.mViewCenter.Z)+')')
    def mouseMoveEvent(self,event):
        if self.isMove:
            moveX=event.pos().x()-self.myMousePosition.x()
            moveY=event.pos().y()-self.myMousePosition.y()
            self.camera.Move(moveX,moveY)
            self.myMousePosition=event.pos()
        if self.isRotate:
            moveX=event.pos().x()-self.myMousePosition.x()
            moveY=event.pos().y()-self.myMousePosition.y()
            self.camera.Yaw(-moveX)
            self.camera.Pitch(-moveY)
            self.myMousePosition=event.pos()
        self.update()

class myform(QtWidgets.QWidget,Ui_Form):
    
    def __init__(self):
        super(myform,self).__init__()
        self.setupUi(self)
        self.graphicsView1=GLWidget(self)
        self.btn=QtWidgets.QPushButton(self)
        self.btn.setGeometry(QtCore.QRect(710, 40, 75, 23))
        self.btn.setObjectName("pushButton")
        self.btn.setText("打开文件")
        self.btn.clicked.connect(self.getfile)
        self.vertex=array([],'f')
    def getfile(self):
        global data
        global normal
        dlg=QtWidgets.QFileDialog()
        f=dlg.getOpenFileName(self,'Open File','.\\Optimizermaster','STL File (*.stl)')
        file=FileHandler().load_mesh(f[0])
        data=array(file[0]['mesh'],'f')
        normal=array(file[0]['normal'],'f')
        #print(data.take([1,2,3],axis=1))
        
        print(len(data))
        #print(data)
        #print(len(normal))
    def flatten(self,*lll):
        return [u for ll in lll for l in ll for u in l]
app=QtWidgets.QApplication(sys.argv)
mywindow=myform()
mywindow.show()
app.exec_()
sys.exit()


# In[ ]:


dir(QtWidgets.QWidget)


# In[ ]:


help(QOpenGLWidget.resizeGL)


# In[ ]:


print(cos(60*math.pi/180))


# In[ ]:


i=10.0
print(sys.getsizeof(i))
print(type(i))


# In[ ]:


import logging


# In[ ]:


log=logging.getLogger(__name__)


# In[ ]:


print(log)


# In[ ]:


dir(glBufferData)


# In[ ]:


dir(vbo)

