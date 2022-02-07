import numpy as np

class Navigation_System_HardInfo:

    #pythonでは、const(定数)をすべて大文字で表現するのが慣例
    MAG_STR = 0.00217
    MAG_LEN = 0.0142
    CORD_MIN = -0.0616
    CORD_MAX = 0.0616
    GRID_LEN = 64

    def __init__(self):

        #Sensor間距離
        dist_sens = (self.CORD_MAX - self.CORD_MIN )/(self.GRID_LEN - 1 )

        #等間隔の配列を生成 np.arange(始点,終点,間隔) ※要素数の場合は、np.listspaceを使用する
        self.X_Array = np.arange(self.CORD_MIN, self.CORD_MAX+(dist_sens/2), dist_sens)
        self.Y_Array = np.arange(self.CORD_MIN, self.CORD_MAX+(dist_sens/2), dist_sens)
        self.X_Mesh,self.Y_Mesh = np.meshgrid(self.X_Array,self.Y_Array)

    def get_X_Mesh_Grid(self):

        return self.X_Mesh

    def get_Y_Mesh_Grid(self):

        return self.Y_Mesh

    def get_mag_str(self):

        return self.MAG_STR

    def get_mag_len(self):

        return self.MAG_LEN

    def get_sen_grid_len(self):

        return self.GRID_LEN