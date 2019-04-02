from PyQt5 import QtCore, QtGui, QtWidgets
from numpy import *
import math
from Optimizermaster.FileHandler import FileHandler
import sys
from gl_widget import GLWidget
from Light import Materials
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from OpenGL.GLUT import *
import matrix
import time
model=[]
class myform(QtWidgets.QWidget):
    
    def __init__(self):
        super(myform,self).__init__()
        #窗口
        self.setObjectName("Form")
        self.resize(900, 900)
        self.setWindowTitle(QtCore.QCoreApplication.translate("Form", "Form"))
        
        #直接引用自定义opengl类
        self.opengl_widget=GLWidget(self)
        
        #self.btn 打开文件
        self.btn=QtWidgets.QPushButton(self)
        self.btn.setGeometry(QtCore.QRect(710, 40, 75, 23))
        self.btn.setObjectName("pushButton")
        self.btn.setText("打开文件")
        self.btn.clicked.connect(self.getfile)
        
        #self.cb  选择材质
        self.cb=QtWidgets.QComboBox(self)
        self.cb.setGeometry(QtCore.QRect(710,70,100,20))
        self.cb.addItems(['黄铜','青铜','亮青铜','铬','铜','亮铜','金','亮金',
                          '白蜡','银','亮银','祖母绿',
                          '碧玉','黑曜石','珍珠','红宝石','绿宝石','黑塑料','黑橡胶','紫罗兰'])
        self.cb.currentIndexChanged.connect(self.selectionChange)
        
        self.btn_image=QtWidgets.QPushButton(self)
        self.btn_image.setGeometry(QtCore.QRect(710, 100, 75, 23))
        self.btn_image.setObjectName("pushButton_image")
        self.btn_image.setText("截图")
        self.btn_image.clicked.connect(self.getimage)
        
        self.btn_rotate=QtWidgets.QPushButton(self)
        self.btn_rotate.setGeometry(QtCore.QRect(710, 360, 75, 23))
        self.btn_rotate.setObjectName("pushButton_rotate")
        self.btn_rotate.setText("旋转")
        self.btn_rotate.clicked.connect(self.rote)
        
        self.btn_rotate=QtWidgets.QPushButton(self)
        self.btn_rotate.setGeometry(QtCore.QRect(710, 390, 75, 23))
        self.btn_rotate.setObjectName("pushButton_translate")
        self.btn_rotate.setText("平移")
        self.btn_rotate.clicked.connect(self.translate)
        
        self.btn_rotate=QtWidgets.QPushButton(self)
        self.btn_rotate.setGeometry(QtCore.QRect(710, 430, 75, 23))
        self.btn_rotate.setObjectName("pushButton_rotate_camera")
        self.btn_rotate.setText("旋转相机")
        self.btn_rotate.clicked.connect(self.rotate_camera)
        self.isrotatecamera=False
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.ro)
        
        self.qlistwidget=QtWidgets.QListWidget(self)
        self.qlistwidget.setGeometry(QtCore.QRect(720,140,100,200))
        self.qlistwidget.setObjectName('Object Name')
    def getfile(self):
        dlg=QtWidgets.QFileDialog()
        f=dlg.getOpenFileName(self,'Open File','.','STL File (*.stl)')
        file=FileHandler().load_mesh(f[0])#f[0]是路径，f[1]是类型
        data=array(file['mesh'],'f')
        print(data)
        model.append({'material':Materials[0],'data':data})
        self.qlistwidget.addItem(f[0].split('/')[-1].split('.')[0])
        self.qlistwidget.setCurrentItem(self.qlistwidget.item(0))
        self.opengl_widget.initdata(model)
        #print(data)
        self.opengl_widget.update()
    def selectionChange(self):
        print(self.cb.currentIndex())
        self.opengl_widget.model[self.qlistwidget.currentIndex().row()]['material']=Materials[self.cb.currentIndex()]
        self.opengl_widget.update()
    def getimage(self):
        #glutSwapBuffers()
        self.opengl_widget.geti()
    def rote(self):
        matrix.rotate(model[self.qlistwidget.currentIndex().row()]['data'],45,45,45)
        self.opengl_widget.update()
    def translate(self):
        matrix.translate(model[self.qlistwidget.currentIndex().row()]['data'],10,0,0)
        self.opengl_widget.update()
    def rotate_camera(self):
        if self.isrotatecamera==False:
            self.isrotatecamera=True
            self.timer.start(100)
        else:
            self.isrotatecamera=False
            self.timer.stop()
    def ro(self):
        self.opengl_widget.camera.Yaw(5)
        self.opengl_widget.light.lightpos=[-self.opengl_widget.camera.forwardDir.X,-self.opengl_widget.camera.forwardDir.Y,-self.opengl_widget.camera.forwardDir.Z,0]
        self.opengl_widget.update()
app=QtWidgets.QApplication(sys.argv)
mywindow=myform()
mywindow.show()
app.exec_()
sys.exit()
