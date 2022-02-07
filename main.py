from typing import Any

import PySimpleGUI as sg
import numpy as np
from numpy import ndarray

import Navigation_System_HardInfo as nsh
import show_figure as sf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

def calc_mag_moment(x, y, z, theta, phi, xmesh, ymesh, grid_len, nav_hard_info ):

    ret_mag_field = []

    mag_len = nav_hard_info.get_mag_len()
    mag_str = nav_hard_info.get_mag_str()

    #センサ座標系->磁石座標系変換用
    #reshape(行,列) -> 配列から列ベクトルへの変換
    pole_axis_vec = np.array([np.cos(np.radians(phi))*np.cos(np.radians(theta)),
                              np.cos(np.radians(phi))*np.sin(np.radians(theta)),
                              np.sin(np.radians(phi))]).reshape(3,1)

    mag_center_pos = np.array([x, y, z]).reshape(3,1)

    mag_plus_pos = mag_center_pos + (mag_len/2)*pole_axis_vec
    mag_minus_pos = mag_center_pos - (mag_len/2)*pole_axis_vec

    #要素がすべて1の行列生成
    one_mat = np.ones((grid_len,grid_len))

    # センサと磁石距離ベクトルの計算(行列)
    x_diff_plus = mag_plus_pos[0] * one_mat - xmesh
    x_diff_minus = mag_minus_pos[0] * one_mat - xmesh

    y_diff_plus = mag_plus_pos[1] * one_mat - ymesh
    y_diff_minus = mag_minus_pos[1] * one_mat - ymesh

    z_diff_plus = mag_plus_pos[2] * one_mat
    z_diff_minus = mag_minus_pos[2] * one_mat

    # センサと磁石の距離(r^3)の導出
    # np.multiply(m1,m2) -> 2つの行列の要素ごとの積
    r_3_plus = calc_dist_matrix(x_diff_plus, y_diff_plus, z_diff_plus, 3)
    r_3_minus = calc_dist_matrix(x_diff_minus, y_diff_minus, z_diff_minus, 3)

    x_mag_field = mag_str * ((x_diff_plus / r_3_plus) - (x_diff_minus / r_3_minus))
    y_mag_field = mag_str * ((y_diff_plus / r_3_plus) - (y_diff_minus / r_3_minus))
    z_mag_field = mag_str * ((z_diff_plus / r_3_plus) - (z_diff_minus / r_3_minus))

    ret_mag_field.append(x_mag_field)
    ret_mag_field.append(y_mag_field)
    ret_mag_field.append(z_mag_field)

    return ret_mag_field

def calc_matrix_power_of_n(mat, n):
    ans = mat
    for i in range(n - 1):
        ans = np.multiply(ans, mat)

    # 計算結果を戻り値に格納
    ret = ans
    return ret


def calc_dist_matrix(xmat, ymat, zmat, n):

    x_power_2 = calc_matrix_power_of_n(xmat, 2)
    y_power_2 = calc_matrix_power_of_n(ymat, 2)
    z_power_2 = calc_matrix_power_of_n(zmat, 2)

    r_power_2 = x_power_2 + y_power_2 + z_power_2
    r_power_3 = r_power_2 * np.sqrt(r_power_2)
    ret = r_power_3

    return ret

if __name__ == '__main__':

    #figure Object List
    fig_obj = []
    fag_obj = []
    cv = []
    mag_fields = []
    key_canvas = ['X_Axis','Y_Axis','Z_Axis']

    #GUI Layout
    sg.theme('Dark Amber')

    #MagField計算のための値取得処理(Grid長の取得、X,Y MeshGrid行列の生成)
    nav_hard_info = nsh.Navigation_System_HardInfo()
    grid_len = nav_hard_info.get_sen_grid_len()
    x_mesh = nav_hard_info.get_X_Mesh_Grid()
    y_mesh = nav_hard_info.get_Y_Mesh_Grid()

    for i in range(3):
        #Generate Figure Instance
        tmp_obj = sf.Show_Figure(i)
        cv_tmp = sg.Canvas(key=key_canvas[i], size=(700, 600))

        #Listへの要素追加
        fig_obj.append(tmp_obj)
        cv.append(cv_tmp)

    frame1 = sg.Frame('',[[sg.Text('X[m]'),sg.Input('0.0',size=(7,1),key='X_IN')]
                        ,[sg.Text('Y[m]'),sg.Input('0.0',size=(7,1),key='Y_IN')]
                        ,[sg.Text('Z[m]'),sg.Input('0.04',size=(7,1),key='Z_IN')]
                        ,[sg.Text('Theta[deg]'),sg.Input('0.0',size=(7,1),key='THETA_IN')]
                        ,[sg.Text('Phi[deg]'),sg.Input('0.0',size=(7,1),key='PHI_IN')]
                        ,[sg.Button('Calc', key='Calc')]]
                        ,size=(150,600))

    frame2 = sg.Frame('',[[sg.Text('X Axis MagField')],[cv[0]]],size=(700, 600))

    frame3 = sg.Frame('',[[sg.Text('Y Axis MagField')],[cv[1]]],size=(700, 600))

    frame4 = sg.Frame('',[[sg.Text('Z Axis MagField')],[cv[2]]], size=(700, 600))

    layout = [ [frame1,frame2,frame3,frame4] ]

    #Generate GUI Window
    window = sg.Window('Sample Program',layout,resizable=True,finalize=True)

    #Connect Canvas with Figure Instance
    #tcv = [cv[0].TKCanvas, cv[1].TKCanvas, cv[2].TKCanvas]

    for i in range(3):
        tmp_obj = FigureCanvasTkAgg(fig_obj[i].get_fig_obj(), window[key_canvas[i]].TKCanvas)  # figのグラフを Tkinter の Canvas に関連付け
        fag_obj.append(tmp_obj)
        fag_obj[i].draw()
        fag_obj[i].get_tk_widget().pack()

    while True:

        #eventにkey名(ex: 'Calc'), valueに{'X_IN': '0.0'...}といったdict形式でデータが残る
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Calc':
            #座標情報の読み取り(Valueからの値の抽出) ->dtypeで文字列 or 数値の判断をした方がよさそう
            x = float(values['X_IN'])
            y = float(values['Y_IN'])
            z = float(values['Z_IN'])
            theta = float(values['THETA_IN'])
            phi = float(values['PHI_IN'])

            #磁束分布の計算
            mag_fields = calc_mag_moment(x, y, z, theta, phi, x_mesh, y_mesh, grid_len, nav_hard_info)

            #リスト長(len(リスト名))回数分の処理を実行
            for i in range(len(fig_obj)):
                fig_obj[i].clear()
                fig_obj[i].show_surface_fig(x_mesh, y_mesh, mag_fields[i])
                fag_obj[i].draw()

    #GUIを閉じたら処理を終える
    window.close()