"""
This module is responsible for the following functions:
- draw height map
- actualize gui with information about mesh density valuse and amount of height points
- actualize styles of reduce and increase mesh denisty button when they reached the limit value
"""
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import  QPushButton,  QLabel,  QVBoxLayout, QToolTip
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from utilis.settings_and_data import ActualVariablesInstance
from utilis.styles import style_button, style_blocked_button, style_hover_button

def draw_map(increase_grid_density_button=QPushButton,
            reduce_grid_density_button=QPushButton,
            information_grid_density=QLabel,
            information_amount_of_points=QLabel,
            map_window=QVBoxLayout):
    
    # TAKE DATA
    # input data        
    data_grid = ActualVariablesInstance.get_variable(9)
    mesh_density = round(ActualVariablesInstance.get_variable(10))
    xllcorner = ActualVariablesInstance.get_variable(5)
    yllcorner = ActualVariablesInstance.get_variable(6)
    dx = ActualVariablesInstance.get_variable(7)
    dy = ActualVariablesInstance.get_variable(8)
    canvas = ActualVariablesInstance.get_variable(12)
    figure = ActualVariablesInstance.get_variable(13)
    #filtration and update of data grid
    data_grid_filtered = data_grid[::mesh_density, ::mesh_density]
    ActualVariablesInstance.update_variable(11,data_grid_filtered)
    # mesh density information actualization        
    information_grid_density.setText(f"Gęstość siatki: {mesh_density} x {mesh_density}")
    information_amount_of_points.setText(f"Ilość punktów: {np.array(data_grid_filtered).size:,}".replace(',',' '))
    # reduce and increase button actualize styles - limit values
    if mesh_density == 1:
        increase_grid_density_button.setStyleSheet(style_blocked_button)
    else:
        increase_grid_density_button.setStyleSheet(style_button+style_hover_button)
    if mesh_density == 100:
        reduce_grid_density_button.setStyleSheet(style_blocked_button)
    else:
        reduce_grid_density_button.setStyleSheet(style_button+style_hover_button)    
    # DRAWING HEIGHT MAP
    # clean figure
    if len(plt.get_fignums())!=0:
        plt.close('all')
    # clean canvas
    if canvas is not None:            
        canvas.deleteLater()      

    # create figure
    figure = plt.figure(figsize=(2,2))
    figure = plt.figure(facecolor='#00000000')
    # update canvas to settings_and_data.py
    ActualVariablesInstance.update_variable(13,figure)
    # create new canvas
    canvas = FigureCanvas(figure)  
    map_window.addWidget(canvas)
    # update canvas to settings_and_data.py
    ActualVariablesInstance.update_variable(12,canvas)
    # create new scale bars
    ax = figure.add_subplot(111)
    #draw map
    im = ax.imshow(
        data_grid_filtered,
        cmap='terrain',
        extent=(
            xllcorner, 
            xllcorner + np.array(data_grid_filtered).shape[1] * (dx * mesh_density),
            yllcorner + np.array(data_grid_filtered).shape[0] * (dy * mesh_density), 
            yllcorner
        )
    )
    
    # set colorbar
    ax.figure.colorbar(im, ax=ax, label='Wysokość (m n.p.m.)')
    ax.set_xlabel('Długość')
    ax.set_ylabel('Szerokość')
    # read the value hover cursor
    def format_coord(x, y):
        col = int((x - xllcorner) / (dx * mesh_density))
        row = int((yllcorner + np.array(data_grid_filtered).shape[0] * (dy * mesh_density) - y) / (dy * mesh_density))
        if col >= 0 and col < data_grid_filtered.shape[1] and row >= 0 and row < data_grid_filtered.shape[0]:
            z = data_grid_filtered[row, col]
            return f'Długość: {x:.2f}\n Szerokość: {y:.2f}\n Wysokość: {z:.2f} (m n.p.m.)'
        else:
            return 'Poza zakresem danych'
    # view tooltip hover cursor
    def on_move(event):
        if event.inaxes:
            tooltip_text = format_coord(event.xdata, event.ydata)
            QToolTip.showText(event.guiEvent.globalPos(), tooltip_text, canvas)            

    # connect the function to the motion_notify_event
    canvas.mpl_connect('motion_notify_event', on_move)

    #draw canvas
    canvas.draw()
        