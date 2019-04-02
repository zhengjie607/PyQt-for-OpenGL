import math
import numpy
def _rotate_free(angle,initx,inity,initz,axlex,axley,axlez,cenx,ceny,cenz):
    C=math.cos(angle*math.pi/180)
    S=math.sin(angle*math.pi/180)
    M0=axlex*axlex+(1-axlex*axlex)*C
    M1=axlex*axley*(1-C)-axlez*S
    M2=axlex*axlez*(1-C)+axley*S
    M3=(1-C)*(1-axlex*axlex)*cenx-(axlex*axley-axlex*axley*C-axlez*S)*ceny-(axlex*axlez-axlex*axlez*C+axley*S)*cenz
    M4=axlex*axley*(1-C)+axlez*S
    M5=axley*axley+(1-axley*axley)*C
    M6=axley*axlez*(1-C)-axlex*S
    M7=(1-C)*(1-axley*axley)*ceny-(axlex*axley-axlex*axley*C+axlez*S)*cenx-(axley*axlez-axley*axlez*C-axlex*S)*cenz
    M8=axlex*axlez*(1-C)-axley*S
    M9=axlez*axley*(1-C)+axlex*S
    M10=axlez*axlez+(1-axlez*axlez)*C
    M11=(1-C)*(1-axlez*axlez)*cenz-(axlex*axlez-axlex*axlez*C-axley*S)*cenx-(axley*axlez-axley*axlez*C+axlex*S)*ceny
    newx=M0*initx+M1*inity+M2*initz+M3
    newy=M4*initx+M5*inity+M6*initz+M7
    newz=M8*initx+M9*inity+M10*initz+M11
    return newx,newy,newz
def rotate(data,angle,x=0,y=0,z=0):
    Xmax,Ymax,Zmax,_,_,_=data.max(axis=0)
    Xmin,Ymin,Zmin,_,_,_=data.min(axis=0)
    cenx=(Xmax+Xmin)/2
    ceny=(Ymax+Ymin)/2
    cenz=(Zmax+Zmin)/2
    h=math.sqrt(x**2+y**2+z**2)
    x=x/h
    y=y/h
    z=z/h
    for i in range(len(data)):
        data[i][0],data[i][1],data[i][2]=_rotate_free(angle,data[i][0],data[i][1],data[i][2],x,y,z,cenx,ceny,cenz)
        #data[i][3],data[i][4],data[i][5]=_rotate_free(-angle,data[i][3],data[i][4],data[i][5],x,y,z,cenx,ceny,cenz)
def translate(data,mx,my,mz):
    for i in range(len(data)):
        data[i][0],data[i][1],data[i][2]=data[i][0]+mx,data[i][1]+my,data[i][2]+mz