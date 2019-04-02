
# coding: utf-8

# In[42]:


import struct
import numpy as np
path=r"F:\艾德威尔\软件\上位机\选区\喷杆cli\yp.cli"
class CLI():
    def __init__(self,path):
        self.UsePoint=[]
        self.read(path)
    def read(self,path):
        with open(path,'rb') as f:
            file=f.read()
            head=str(file).split('$$HEADEREND')
            head=head[0].split('\\n')
            print(head)
            for line in head:
                if '$$UNITS' in line:
                    self.unit=float(line.split('/')[1])
                if '$$DIMENSION' in line:
                    bound=line.split('/')[1]
                    Xmin,Ymin,Zmin,Xmax,Ymax,Zmax=bound.split(',')
                    self.Xmin=float(Xmin)
                    self.Ymin=float(Ymin)
                    self.Zmin=float(Zmin)
                    self.Xmax=float(Xmax)
                    self.Ymax=float(Ymax)
                    self.Zmax=float(Zmax)
                if '$$LAYERS' in line:
                    self.layer=int(line.split('/')[1])
            #print(head[0])
            f.seek(226,0)
            ty=struct.unpack('<H',f.read(2))
            #print("type:",ty)
            try:
                while True:
                    layer=struct.unpack('<H',f.read(2))
                    #print("layer:",layer)
                    Mypoint=[]
                    while True:
                        mypoint=[]
                        readtpye=struct.unpack('<H',f.read(2))
                        #print("readtype:",readtpye)
                        if readtpye[0]==128:
                            break
                        ID,Direction,Point_Num=struct.unpack('<HHH',f.read(6))
                        '''print("ID:",ID)
                        print("Direction:",Direction)
                        print("Point_Num:",Point_Num)'''
                        for i in range(Point_Num):
                            x,y=struct.unpack('<HH',f.read(4))
                            mypoint.append((x*self.unit,y*self.unit))
                        Mypoint.append(mypoint)
                    self.UsePoint.append(Mypoint)
            except:
                self.UsePoint.append(Mypoint)
                print('Finish!')
if __name__=='__main__':
    w=CLI(path)
    print(len(w.UsePoint))
    print(w.layer)
    print(w.Xmin)

