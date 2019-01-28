from OpenGL.GL import *
Materials={
        'brass':{
            'ambient_light':[0.329412,0.223529,0.02745,1.000000],
            'diffuse':[0.780392,0.568627,0.113725,1.000000],
            'specular':[0.992157, 0.941176,0.807843,1.000000],
            'shininess':27.897400
        },#黄铜
        'bronze':{
            'ambient_light':[0.212500,0.127500,0.054000,1.000000],
            'diffuse':[0.714000,0.428400,0.181440,1.000000],
            'specular':[0.393548,0.271906,0.166721,1.000000],
            'shininess':25.600000
        },#青铜
        'brightbronze':{
            'ambient_light':[0.250000,0.148000,0.064750,1.000000],
            'diffuse':[0.400000,0.236800,0.103600,1.000000],
            'specular':[0.774597,0.458561,0.200621,1.000000],
            'shininess':76.800003
        },#亮青铜
        'chromium':{
            'ambient_light':[0.250000,0.250000,0.250000,1.000000],
            'diffuse':[0.400000,0.400000, 0.400000,1.000000],
            'specular':[0.774597,0.774597,0.774597,1.000000],
            'shininess':76.800003
        },#铬
        'copper':{
            'ambient_light':[0.191250, 0.073500, 0.022500, 1.000000],
            'diffuse':[0.703800, 0.270480, 0.082800, 1.000000],
            'specular':[0.256777, 0.137622, 0.086014, 1.000000],
            'shininess':12.800000
        },#铜
        'brightcopper':{
            'ambient_light':[0.229500, 0.088250, 0.027500, 1.000000],
            'diffuse':[0.550800, 0.211800, 0.066000, 1.000000],
            'specular':[0.580594, 0.223257, 0.069570, 1.000000],
            'shininess':51.200001
        },#亮铜
        'gold':{
            'ambient_light':[0.247250, 0.199500, 0.074500, 1.000000],
            'diffuse':[0.751640, 0.606480, 0.226480, 1.000000],
            'specular':[0.628281, 0.555802, 0.366065, 1.000000],
            'shininess':51.200001
        },#金
        'brightgold':{
            'ambient_light':[0.247250, 0.224500, 0.064500, 1.000000],
            'diffuse':[0.346150, 0.314300, 0.090300, 1.000000],
            'specular':[0.797357, 0.723991, 0.208006, 1.000000],
            'shininess':83.199997
        },#亮金
        'whitewax':{
            'ambient_light':[0.105882, 0.058824, 0.113725, 1.000000],
            'diffuse':[0.427451, 0.470588, 0.541176, 1.000000],
            'specular':[0.333333, 0.333333, 0.521569, 1.000000],
            'shininess':9.846150
        },#白蜡
        'silver':{
            'ambient_light':[0.192250, 0.192250, 0.192250, 1.000000],
            'diffuse':[0.507540, 0.507540, 0.507540, 1.000000],
            'specular':[0.508273, 0.508273, 0.508273, 1.000000],
            'shininess':51.200001
        },#银
        'brightsilver':{
            'ambient_light':[0.231250, 0.231250, 0.231250, 1.000000],
            'diffuse':[0.277500, 0.277500, 0.277500, 1.000000],
            'specular':[0.773911, 0.773911, 0.773911, 1.000000],
            'shininess':89.599998
        },
        'emerald':{
            'ambient_light':[0.021500, 0.174500,0.021500,0.550000],
            'diffuse':[0.075680,0.614240,0.075680,0.550000],
            'specular':[ 0.633000,0.727811,0.633000,0.550000],
            'shininess':76.800003
        },#翠绿
        'jasper':{
            'ambient_light':[0.135000, 0.222500, 0.157500, 0.950000],
            'diffuse':[0.540000, 0.890000, 0.630000, 0.950000],
            'specular':[0.316228, 0.316228, 0.316228, 0.950000],
            'shininess':12.800000
        },#墨绿
        'obsidian':{
            'ambient_light':[0.053750,0.050000,0.066250,0.820000],
            'diffuse':[0.182750,0.17000,0.225250,0.820000],
            'specular':[ 0.332741, 0.328634,0.346435,0.820000],
            'shininess':38.400002
        },#黑曜石
        'pearl':{
            'ambient_light':[0.250000, 0.207250, 0.207250, 0.922000],
            'diffuse':[1.000000, 0.829000, 0.829000, 0.922000],
            'specular':[ 0.296648, 0.296648, 0.296648, 0.922000],
            'shininess':11.264000
        },#珍珠
        'ruby':{
            'ambient_light':[0.174500, 0.011750, 0.011750, 0.550000],
            'diffuse':[0.614240, 0.041360, 0.041360, 0.550000],
            'specular':[0.727811, 0.626959, 0.626959, 0.550000],
            'shininess':76.800003
        },#红宝石
        'beryl':{
            'ambient_light':[0.100000, 0.187250, 0.174500, 0.800000],
            'diffuse':[0.396000, 0.741510, 0.691020, 0.800000],
            'specular':[0.297254, 0.308290, 0.306678, 0.800000],
            'shininess':12.800000
        },#绿宝石
        'blackplastic':{
            'ambient_light':[0.000000, 0.000000, 0.000000, 1.000000],
            'diffuse':[0.010000, 0.010000, 0.010000, 1.000000],
            'specular':[0.500000, 0.500000, 0.500000, 1.000000],
            'shininess':32.000000
        },#黑塑料
        'blackrubber':{
            'ambient_light':[0.020000, 0.020000, 0.020000, 1.000000],
            'diffuse':[0.010000, 0.010000, 0.010000, 1.000000],
            'specular':[0.400000, 0.400000, 0.400000, 1.000000],
            'shininess':10.000000
        },#黑橡胶
        'violet':{
            'ambient_light':[0.110000, 0.060000, 0.090000, 1.000000],
            'diffuse':[0.430000, 0.470000, 0.540000, 1.000000],
            'specular':[0.330000, 0.330000, 0.520000, 1.000000],
            'shininess':22.000000
        }#紫罗兰
}
class Light:
    def __init__(self,m):
        glShadeModel(GL_SMOOTH)
        self.lightpos=[0,0,1,0]
        whiltlitht=[1,1,1,1]
        glMaterial(GL_FRONT,GL_AMBIENT,m['ambient_light'])
        glMaterial(GL_FRONT,GL_SPECULAR, m['specular'])
        glMaterial(GL_FRONT,GL_SHININESS, m['shininess'])
        glMaterial(GL_FRONT,GL_DIFFUSE, m['diffuse'])
        
        #glLight(GL_LIGHT0,GL_POSITION, self.lightpos)
        #glLight(GL_LIGHT0,GL_DIFFUSE, whiltlitht)
       # glLight(GL_LIGHT0,GL_SPECULAR, whiltlitht)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)   
        glEnable(GL_DEPTH_TEST)
    def Update(self,m):
        glLight(GL_LIGHT0,GL_POSITION, self.lightpos)
        glMaterial(GL_FRONT,GL_AMBIENT,m['ambient_light'])
        glMaterial(GL_FRONT,GL_SPECULAR, m['specular'])
        glMaterial(GL_FRONT,GL_SHININESS, m['shininess'])
        glMaterial(GL_FRONT,GL_DIFFUSE, m['diffuse'])
        
    
        
