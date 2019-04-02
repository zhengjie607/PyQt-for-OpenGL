from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from Vector3f import *
import math

class camera:
    def __init__(self):
        self.mPos=Vector3f(0.0,0.0,0.0)
        self.mViewCenter=Vector3f(0.0,0.0,-1.0)
        self.mUp=Vector3f(0.0,1.0,0.0)
        self.right=100
        self.top=100
        self.forwardDir=self.mViewCenter-self.mPos
        self.rithtDir=self.forwardDir.cross(self.mUp)
    def Update(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.right,self.right,-self.top,self.top,-200,200)
        gluLookAt(self.mPos.X,self.mPos.Y,self.mPos.Z,self.mViewCenter.X,self.mViewCenter.Y,self.mViewCenter.Z,self.mUp.X,self.mUp.Y,self.mUp.Z)
    def Move(self,deltax,deltay):
        self.forwardDir.Normalize()
        self.rithtDir.Normalize()
        self.mUp.Normalize()
        dx=self.rithtDir*deltax
        dy=self.mUp*deltay
        self.mPos=self.mPos-dx+dy
        self.mViewCenter=self.mPos+self.forwardDir
    def Rotate(self,viewDirection,angle,x,y,z):
        #x，y，z组成旋转轴
        C=math.cos(angle*math.pi/180)
        S=math.sin(angle*math.pi/180)
        newX=viewDirection.X * (x * x + (1 - x * x) * C) + viewDirection.Y * (x * y * (1 - C) - z * S) + viewDirection.Z * (x * z * (1 - C) + y * S)
        newY=viewDirection.X * (x * y * (1 - C) + z * S) + viewDirection.Y * (y * y + (1 - y * y) * C) + viewDirection.Z * (y * z * (1 - C) - x * S)
        newZ=viewDirection.X * (x * z * (1 - C) - y * S) + viewDirection.Y * (y * z * (1 - C) + x * S) + viewDirection.Z * (z * z + (1 - z * z) * C)
        newdir=Vector3f(newX,newY,newZ)
        #newdir.Normalize()
        return newdir
    def Yaw(self,angle):
        self.forwardDir=self.Rotate(self.forwardDir,angle,self.mUp.X,self.mUp.Y,self.mUp.Z)
        self.rithtDir=self.Rotate(self.rithtDir,angle,self.mUp.X,self.mUp.Y,self.mUp.Z)
        self.mPos = self.mViewCenter-self.forwardDir
    def Pitch(self,angle):
        self.forwardDir=self.Rotate(self.forwardDir,angle,self.rithtDir.X,self.rithtDir.Y,self.rithtDir.Z)
        self.mUp=self.Rotate(self.mUp,angle,self.rithtDir.X,self.rithtDir.Y,self.rithtDir.Z)
        self.mPos = self.mViewCenter-self.forwardDir
