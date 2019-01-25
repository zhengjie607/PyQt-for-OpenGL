
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


# In[2]:


class stlfile:
    originalname = ''
    tweakedname = ''

# Get a list of stl files
path = r"""C:\Users\singers\Documents\buildplateoptimization\TooManySTLs"""
listOfSTLfiles = []
for root, dirs, files in os.walk(path):
        for file_ in files:
            filename, file_extension = os.path.splitext(file_)
            if(file_extension=='.stl'):
                completepath = os.path.join(root, file_)
                print(completepath)
                listOfSTLfiles.append(completepath)



# In[3]:


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
           
# Write to CSV    
# print('Write the list to a file')

# d = {'stlfiles':validSTLfiles}
# df = pd.DataFrame(data=d)
# df.to_csv('stlfiles.csv')

# print('reading the csv file')
# df = pd.read_csv('stlfiles.csv')
# validSTLfiles  = df['stlfiles'].values.tolist()

# print(listOfSTLfiles)
# with open('validSTLfiles.csv', 'wb') as myfile:
#     writer = csv.writer(myfile)
#     writer.writerows(listOfSTLfiles)
   # for rowtext in listOfSTLfiles:
   #     print(rowtext)
   #     wr.writerow(rowtext)

       


# In[4]:


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


# In[5]:



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


# In[6]:


def copy_obj(obj, dims, num_rows, num_cols, num_layers):
    w, l, h = dims
    copies = []
    for layer in range(num_layers):
        for row in range(num_rows):
            for col in range(num_cols):
                # skip the position where original being copied is
                if row == 0 and col == 0 and layer == 0:
                    continue
                _copy = mesh.Mesh(obj.data.copy())
                # pad the space between objects by 10% of the dimension being
                # translated
                if col != 0:
                    translate(_copy, w, w / 10., col, 'x')
                if row != 0:
                    translate(_copy, l, l / 10., row, 'y')
                if layer != 0:
                    translate(_copy, h, h / 10., layer, 'z')
                copies.append(_copy)
    return copies


# In[7]:


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
        
            


# In[8]:


# Define Files as STL class and pull geometry & data
AllFiles = []
for thing in Tweaked:
    model = STLattributes(thing)
    AllFiles.append(model)


# In[9]:


# Define Build Plate Space
# width = input('What is the width of the buildplate? ')
# length = input('What is the length of the buildplate? ')
# height = input('What is the height of the buildplate? ')

width = 200
length = 250
height = 300
volume = width*length*height


# In[10]:


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


# In[11]:


# Sort files
FitFiles.sort(key = lambda file: file.zdif, reverse = True)
#print(''),
#print(FitFiles)
print('Sorting Files')


# In[12]:


# Make all objects flush

for thing in FitFiles:
    thing.flush()


# In[16]:


# Order them on plate
origin = [0,0]
row = []
combined = None
wsum = 0
group = 1
batch = []
margin = 2
for thing in FitFiles:
    wsum += thing.xdif+margin
    print('This is the wsum: '+str(wsum))
    if thing.xdif+origin[0] >= width:
        max_y_in_row = max([x for x in row])
        origin[0] = wsum = 0
        origin[1] += max_y_in_row
        print('This is the lsum: ' +str(origin[1]))
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
    origin[0] = thing.maxx
    batch.append(thing)
# Concatenate and Save   
if batch:
    #[print(x) for x in batch]
    combined = mesh.Mesh(np.concatenate([x.geo.data for x in batch]))
    combined.save(path+'\\new_combined_group_' +str(group)+'.stl', mode=stl.Mode.ASCII)
    #print('If Statement Triggered!')

