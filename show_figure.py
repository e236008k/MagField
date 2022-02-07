import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

class Show_Figure:

    #Constructor
    def __init__(self,fig_num):

        #figure instanceを生成
        self.fig = plt.figure(fig_num)
        #self.fig = plt.figure(fig_num, figsize=(200, 200))

        #将来的にaxes数を引数で調整できるようにする
        self.ax = self.fig.add_subplot(1,1,1,projection='3d')

    #3次元座標情報をグラフ化(Surface)する関数
    def show_surface_fig(self, x_mesh, y_mesh, z):

        #Z軸方向の値のピーク値の絶対値を取得
        v_range = self._get_z_peak(z)

        #3次元プロット(Surface)
        #AxesにSurfaceを追加する
        self.surf = self.ax.plot_surface(x_mesh, y_mesh, z, cmap=plt.cm.get_cmap('coolwarm'), norm=Normalize(vmin=-v_range, vmax=v_range), linewidth=0, antialiased=False)
        # カラーバーの表示
        #self.fig.colorbar(self.surf, shrink=0.5, aspect=10)

        #plt.show()

    def clear(self):

        self.ax.cla()
        self._graph_setting_init()

    def _graph_setting_init(self):
        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.ax.set_zlabel("Z Axis")

    def get_fig_obj(self):

        return self.fig

    def _get_z_peak(self,z):

        max = abs(np.max(z))
        min = abs(np.min(z))

        if max > min:
            return max
        else:
            return min