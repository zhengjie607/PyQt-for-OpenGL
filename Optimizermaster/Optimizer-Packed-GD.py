
# coding: utf-8

# In[1]:


# import Tweaker
import numpy as np
# the stl library is inside of numpy, so import it second
from stl import mesh
import stl
import os
import RunTweakerFromProgram
from RunTweakerFromProgram import Configuration
from RunTweakerFromProgram import RunTweakerFromProgram
import csv
import pandas as pd

from mpl_toolkits import mplot3d
from matplotlib import pyplot
import subprocess


# In[2]:


# Import PyQt
import PyQt5


# In[3]:


class stlfile:
    originalname = ''
    tweakedname = ''

# Get a list of stl files
path = r"""C:\Users\singers\Documents\buildplateoptimization\SmallTest"""
listOfSTLfiles = []
for root, dirs, files in os.walk(path):
        for file_ in files:
            filename, file_extension = os.path.splitext(file_)
            if(file_extension=='.stl'):
                completepath = os.path.join(root, file_)
                #print(completepath)
                listOfSTLfiles.append(completepath)



# In[4]:


# Test to see if they are valid by trying to process them with the numpystl library
numfiles = len(listOfSTLfiles)
volumeArray =np.empty( shape=(numfiles,1) )
count = 0
validSTLfiles = []
   
for filepath in listOfSTLfiles:
   print(filepath)
   volume=0
   
   try:
       your_mesh = mesh.Mesh.from_file(filepath)
       volume, cog, inertia = your_mesh.get_mass_properties()
       validSTLfiles.append(filepath)
   except:
       print('error occured')
   finally:
       if(np.isnan(volume)):

           volume =0
           np.insert(volumeArray,count,volume)
           count+=1


       


# In[5]:


# Loop over the files and run in tweaker
        
print('Rename Files')
Tweaked =[]
for currentFile in validSTLfiles:
    config = Configuration()
    config.inputfile = currentFile
    print(currentFile)
    folder, filename = os.path.split(str(currentFile))
    first = filename[0:4]
    second = filename[0:12]
    print(filename)
    if first != 'new_' and second != 'new_combined':
        newfilename = 'new_'+filename
        print(newfilename)
        newFullPath = os.path.join(folder,newfilename)
        print(newFullPath)
        config.outputfile  = newFullPath

        RunTweakerFromProgram(config)
        print(config.outputfile)
        Tweaked.append(newFullPath)


# In[6]:


copier = False
if len(Tweaked) == 1:
    choice = input('We noticed there is only one file. Would you like to make copies? (Y/N) ')
    if choice[0] == 'Y':
        copier = True
        num_of_copies = int(input('How many copies would you like? '))
    else:
        copier = False


# In[7]:



def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
    # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    #print(str(minx), str(maxx), str(miny), str(maxy), str(minz), str(maxz))
    
    return minx, maxx, miny, maxy, minz, maxz


# In[8]:


# Define STL Class and Functions
class STLattributes:

#     filepath = None
#     maxx = None
#     minx = None
#     maxy = None
#     miny = None
#     maxz = None
#     minz = None
#     xdif = None
#     ydif = None
#     zdif = None
        
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = ''
        self.geo = mesh.Mesh.from_file(self.filepath)
        self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz = find_mins_maxs(self.geo)
        self.xdif = abs(self.maxx-self.minx)
        self.ydif = abs(self.maxy-self.miny)
        self.zdif = abs(self.maxz-self.minz)
        
        self.volume = self.xdif*self.ydif*self.zdif
    def __repr__(self):
        return self.filepath
    
    def translate(self, step, padding, multiplier, axis):
        while multiplier == 0:
            print("A multiplier of 0 will result in no translation.")
            multiplier = input("Enter a modifier: ")
        if axis == 'x':
            items = [0, 3, 6]
        elif axis == 'y':
            items = [1, 4, 7]
        elif axis == 'z':
            items = [2, 5, 8]
        newList = list()
        for p in self.geo.points:
            #point items are ((x, y, z), (x, y, z), (x, y, z))
            for i in range(3):
                p[items[i]] += (step * multiplier) + (padding * multiplier)
                
            newList.append(p)
        self.geo.points = newList
                
        #print("--"*20)
        #print("About to call the find_mins_max function!")
        #print(str(self.minx),str(self.maxx),str(self.miny),str(self.maxy),str(self.minz),str(self.maxz))        
        self.minx,self.maxx,self.miny,self.maxy,self.minz,self.maxz = find_mins_maxs(self.geo)
        #print("After the find_mins_max function")
        #print("--"*20)
    
    def flush(self):
        self.translate(-self.minz, 0, 1,'z')
        self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz = find_mins_maxs(self.geo)
    def center(self,center, offset):
        self.translate(center[0]-self.minx+self.xdif/2+offset[0],0,1,'x')
        self.translate(center[1]-self.miny+self.ydif/2+offset[1],0,1,'y')
        self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz = find_mins_maxs(self.geo)
    def copy_obj(self, dims, num_rows, num_cols, num_layers):
        w, l, h = dims
        copies = []
        for layer in range(num_layers):
            for row in range(num_rows):
                for col in range(num_cols):
                    # skip the position where original being copied is
                    if row == 0 and col == 0 and layer == 0:
                        continue
                    _copy = mesh.Mesh(self.geo.data.copy())
                    # pad the space between objects by 10% of the dimension being
                    # translated
                    if col != 0:
                        self.translate(w, w / 10., col, 'x')
                    if row != 0:
                        self.translate(l, l / 10., row, 'y')
                    if layer != 0:
                        self.translate(h, h / 10., layer, 'z')
                    copies.append(_copy)
        return copies


# In[9]:


# Define Files as STL class and pull geometry & data
AllFiles = []
for thing in Tweaked:
    model = STLattributes(thing)
    AllFiles.append(model)


# In[10]:


# Define Build Plate Space
# width = input('What is the width of the buildplate? ')
# length = input('What is the length of the buildplate? ')
# height = input('What is the height of the buildplate? ')

width = 200
length = 250
height = 300
volume = width*length*height


# In[11]:


# Check if any files are too big
FitFiles = []
for thing in AllFiles:
    if thing.volume > volume:
        print("Warning: " + str(thing.filepath) + "is too big for the buildplate"),
        answer = input('Do you wish to continue? (Y/N) ')
        if answer == 'Y':
            choice = input('Would you like to resize (R) or exclude the model (E)? ')
            if choice[0] == 'R' or 'r':
                print('Work on this resizing thing later!!!')
            elif choice[0] == 'E' or 'e':
                print('')
        elif answer == 'N':
            print('')
    else:
        FitFiles.append(thing)
        
#print(FitFiles)
print('File fitting verified')


# In[12]:


# Sort files

print('Sorting Files')
FitFiles.sort(key = lambda file: file.zdif, reverse = True)
#print(''),
#print(FitFiles)


# In[13]:


# Make all objects flush and save to CSV
d = []
i = 0
df = pd.DataFrame(data=d, columns = ['Filepath', 'Min X', 'Max X', 'Min Y','Max Y','Min Z','Max Z'])
xyarray = []
bounds = []
bound = [(0,width),(0,length)]
for thing in FitFiles:
    thing.flush()
    thing.center([width/2,length/2],[width,length])
    df.loc[i] = [thing.filepath, thing.minx, thing.maxx,thing.miny,thing.maxy,thing.minz,thing.maxz]
    i+=1
    xyarray.append([thing.xdif,thing.ydif,thing.minx,thing.maxx, thing.miny,thing.maxy, thing.zdif])
    bounds += bound
#xyarray = [item for sublist in xyarray for item in sublist]
#print(df)
savepath = path+'\data.csv'
print(savepath)     
#Write to CSV
df.to_csv(savepath,sep = ',',mode = 'w',line_terminator = '\n')
#print(xyarray)
print(len(xyarray))
population_scope = len(xyarray)*4.5 % 2
print(bounds)
print(len(bounds))


# In[14]:


if copier == True:
    w1 = original.xdif
    l1 = original.ydif
    h1 = original.zdif
    for x in range(num_of_copies):
        new = FitFiles[0]
        new.geo.save(path+' - '+str(x))
        FitFiles.append(new)


# In[15]:


origin = [0,0]
center = [width/2,length/2]
row = []
combined = None
wsum = 0
group = 1
batch = []
coords = []
margin = 3
for thing in FitFiles:
    wsum += thing.xdif+margin
    #print('This is the wsum: '+str(wsum))
    if thing.xdif+origin[0] >= width:
        max_y_in_row = max([x for x in row])
        origin[0] = wsum = 0
        origin[1] += max_y_in_row+margin
        #print('This is the lsum: ' +str(origin[1]))
        row = []
        if thing.ydif+origin[1] >= length:
            print('batch#' + str(group))
            origin = [0,0]
            wsum = 0
            combined = mesh.Mesh(np.concatenate([x.geo.data for x in batch]))
            combined.save(path+'\\new_combined_group_' +str(group)+'.stl', mode=stl.Mode.ASCII)
            group+=1
            batch = []
            
    row.append(thing.ydif)
    thing.translate(origin[0]-thing.minx+margin,0,1,'x')
    thing.translate(origin[1]-thing.miny+margin,0,1,'y')
    coords.append([thing.minx+thing.xdif/2, thing.miny+thing.ydif/2])
    origin[0] = thing.maxx
    batch.append(thing)
# Concatenate and Save   
if batch:
    #[print(x) for x in batch]
    combined = mesh.Mesh(np.concatenate([x.geo.data for x in batch]))
    combined.save(path+'\\new_combined_group_' +str(group)+'.stl', mode=stl.Mode.ASCII)
    #print('If Statement Triggered!')


# In[16]:


print(coords)


# In[17]:


def evalfunction(xys,listofmodels):
    i = totalW = 0
    center = [100,125]
    #print(xys)
    for j,model in enumerate(listofmodels):
        #print(model)
        individual_w = 0
        x_local = xys[i]
        y_local = xys[i+1]
        #[thing.xdif,thing.ydif,thing.minx,thing.maxx, thing.miny,thing.maxy, thing.zdif]
        #        0          1          2          3           4          5           6
        xtranslation = x_local-model[2]-(model[0])/2
        ytranslation = y_local-model[4]-(model[1])/2
        model[2:4]+=xtranslation
        model[4:6]+=ytranslation
        xdist = center[0]-model[0]/2-model[2]
        ydist = center[1]-model[1]/2-model[4]
        dist = ((xdist**2+ydist**2)**.5)
        
        if x_local >= 200 - model[0] or y_local >= 250 - model[1] or x_local<0 or y_local<0:
            weight = (dist**2)*model[6]*20
            individual_w += weight
            #print('Model is out of bounds')
        else:
            
            for thing in listofmodels:
                if not (model[0] == thing[0] and model[1] == thing[1] and model[6] == thing[6]):
                    #if not (thing.minx<model.maxx<thing.maxx or thing.minx<model.minx<thing.maxx) and not(thing.miny<model.maxy<thing.maxy or thing.miny<model.miny<thing.maxy):
                    if(thing[2]<model[3]<thing[3] or thing[2]<model[2]<thing[3]):
                        #print("intersecting x range")
                        if(thing[4]<model[5]<thing[5] or thing[4]<model[4]<thing[5]):
                            x_left = max(model[2], thing[2])
                            y_top = max(model[5], thing[5])
                            x_right = min(model[3], thing[3])
                            y_bottom = min(model[4], thing[4])
                            
                            area = abs(x_left-x_right)*abs(y_top-y_bottom)
                            #print(area)
                            weight = (dist**2)*model[6]*area*10
                            individual_w+=weight
                            #print("and intersecting y range - COLLISION")
                            break
                            #print('Two models hit each other :(')
                        
            weight = (dist**2)*model[6]
            individual_w+=weight
        
        i += 2
        #if(j % 5 ==1):
        #    print('Checking model {0}'.format(j))
                #rint(i)
        totalW+=individual_w  
        #if i == len(listofmodels):
    #print('The end with weight  = {}'.format(totalW))
    #print('---'*40)
    return totalW


# ### not in use
# def eval2(listofmodels):
#     i = totalW = 0
#     center = [100,125]
#     for model in listofmodels:
#         #print(model)
#         x_local = xys[i]
#         y_local = xys[i+1]
#         xtranslation = x_local-model[2]
#         ytranslation = y_local-model[4]
#         xdist = center[0]-model[0]/2-model[2]
#         ydist = center[1]-model[1]/2-model[4]
#         dist = ((xdist**2+ydist**2)**.5)
#         
#         if x_local >= 200 - model[0] or y_local >= 250 - model[1] or x_local<0 or y_local<0:
#             weight = (dist**2)*model.zdif*20
#             totalW += weight
#         else:
#             
#             for thing in listofmodels:
#                 #if not (thing.minx<model.maxx<thing.maxx or thing.minx<model.minx<thing.maxx) and not(thing.miny<model.maxy<thing.maxy or thing.miny<model.miny<thing.maxy):
#                 if not (thing[2]<model[3]<thing[3] or thing[2]<model[2]<thing[3]) and not (thing[4]<model[5]<thing[5] or thing[4]<model[4]<thing[5]):
#                     weight = (dist**2)*model[6]
#                 else:
#                     weight = (dist**2)*model[6]*10
#     
#         i += 2
#         #rint(i)
#         totalW+=weight  
#         if i == len(listofmodels)-1:
#             print('The end with weight  = {}'.format(totalW))
#             print('---'*40)
#             return totalW

# In[18]:


from scipy.optimize import fmin_tnc
result = fmin_tnc(evalfunction,x0 = coords, args = (xyarray,),approx_grad = True, bounds = bounds, epsilon = 0.1, maxfun = 1000000, stepmx = 0.1, eta = .1)


# In[19]:


best_coords = result[0]
coord = []

print(best_coords)
print(coords)
# same = dif = 0
# for x in range(len(coords)):
#     if best_coords[x] == coords[x]:
#         same += 1
#     else:
#         dif +=1
# print(same,dif)


# In[20]:


i = 0
for thing in FitFiles:
    thing.translate(best_coords[i]-thing.minx-thing.xdif/2,0,1,'x')
    i += 1
    thing.translate(best_coords[i]-thing.miny-thing.miny/2,0,1,'y')
    i += 1


# In[21]:


combined = mesh.Mesh(np.concatenate([x.geo.data for x in FitFiles]))
savepath = path+'\\new_combined_group_'+'.stl'
combined.save(savepath, mode=stl.Mode.ASCII)


# In[22]:


# Plot Group of Files

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file(savepath)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

# Auto scale to the mesh size
scale = your_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()

