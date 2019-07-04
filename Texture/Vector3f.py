import math
class Vector3f:
    def __init__(self,x,y,z):
        self.X=x
        self.Y=y
        self.Z=z
    def __add__(self,other):
        return Vector3f(self.X+other.X,self.Y+other.Y,self.Z+other.Z)
    def __sub__(self,other):
        return Vector3f(self.X-other.X,self.Y-other.Y,self.Z-other.Z)
    def __mul__(self,other):
        return Vector3f(self.X*other,self.Y*other,self.Z*other)
    def dot(self,other):
        return self.X*other.X+self.Y*other.Y+self.Z*other.Z
    def cross(self,other):
        return Vector3f(self.Y*other.Z-self.Z*other.Y,self.Z*other.X-self.X*other.Z,self.X*other.Y-self.Y*other.X)
    def magnitude(self):
        return math.sqrt(self.X*self.X+self.Y*self.Y+self.Z*self.Z)
    def Normalize(self):
        len=self.magnitude()
        self.X=self.X/len
        self.Y=self.Y/len
        self.Z=self.Z/len
