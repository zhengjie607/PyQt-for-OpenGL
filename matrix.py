import math
import numpy
def Matrix_rotate(angle,axlex,axley,axlez,cenx,ceny,cenz):
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
    return numpy.matrix([[M0,M1,M2,M3],[M4,M5,M6,M7],[M8,M9,M10,M11],[0,0,0,1]])
def Matrix_scale(scale_x,scale_y,scale_z,cenx,ceny,cenz):
    M00=scale_x
    M03=(1-scale_x)*cenx
    M11=scale_y
    M13=(1-scale_y)*ceny
    M22=scale_z
    M23=(1-scale_z)*cenz
    return numpy.matrix([[M00,0,0,M03],[0,M11,0,M13],[0,0,M22,M23],[0,0,0,1]])
def Matrix_translate(move_x,move_y,move_z):
    return numpy.matrix([[1,0,0,move_x],[0,1,0,move_y],[0,0,1,move_z],[0,0,0,1]])
def getCenter(data):
    Xmax,Ymax,Zmax,_,_,_=data.max(axis=0)
    Xmin,Ymin,Zmin,_,_,_=data.min(axis=0)
    cenx=(Xmax+Xmin)/2
    ceny=(Ymax+Ymin)/2
    cenz=(Zmax+Zmin)/2
    return cenx,ceny,cenz
def M_dot_data(data,M):
    point=numpy.matrix(data[:,0:3])
    point=numpy.insert(point,3,1,axis=1)
    b=numpy.dot(point,M.T)
    data[:,0:3]=b[:,0:3]
def rotate(data,angle,x=0,y=0,z=0):
    cenx,ceny,cenz=getCenter(data)
    h=math.sqrt(x**2+y**2+z**2)
    x=x/h
    y=y/h
    z=z/h
    M=Matrix_rotate(angle,x,y,z,cenx,ceny,cenz)
    M_dot_data(data,M)
    M_normal=Matrix_rotate(angle,x,y,z,0,0,0)
    normal=numpy.matrix(data[:,3:])
    normal=numpy.insert(normal,3,1,axis=1)
    c=numpy.dot(normal,M_normal.T)
    data[:,3:]=c[:,0:3]
def scale(data,scale_x,scale_y,scale_z):
    cenx,ceny,cenz=getCenter(data)
    M=Matrix_scale(scale_x.scale_y,scale_z,cenx,ceny,cenz)
    M_dot_data(data,M)
def translate(data,movex,movey,movez):
    M=Matrix_translate(movex,movey,movez)
    M_dot_data(data,M)