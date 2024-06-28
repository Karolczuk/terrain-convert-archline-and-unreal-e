"""
Module is asign to increase grid and reduce grid buttons in gui(gui.converter_window.py)
This module is responsible for the following functions:
- take actual mesh density from utilis.settings_and_data.py ActualVariablesInstance
- updtae new mesh density to utilis.settings_and_data.py ActualVariablesInstance
- draw height map with using logic.draw_map.py
"""
from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout
from typing import Literal

from logic.draw_map import draw_map
from utilis.settings_and_data import ActualVariablesInstance

def mesh_density_manipulator(action: Literal['increase', 'reduce'], #choose if it is increase or reduce variant
                          increase_grid_density_button=QPushButton, 
                          reduce_grid_density_button=QPushButton,
                          information_grid_density=QLabel,
                          information_amount_of_points=QLabel,
                          map_window=QVBoxLayout):
                          
    
    # input data - mesh density
    mesh_density = round(ActualVariablesInstance.get_variable(10))
    # mesh density manipulator
    if action == 'reduce':
        if mesh_density<=99:
            mesh_density+=1
            # update data - mesh density
            ActualVariablesInstance.update_variable(10,mesh_density)
            # draw height map
            draw_map(increase_grid_density_button,
                    reduce_grid_density_button,
                    information_grid_density,
                    information_amount_of_points,
                    map_window)
    elif action == 'increase':
        if mesh_density>1:
            mesh_density-=1
            # update data - mesh density
            ActualVariablesInstance.update_variable(10,mesh_density)
            # draw height map            
            draw_map(increase_grid_density_button,
                    reduce_grid_density_button,
                    information_grid_density,
                    information_amount_of_points,
                    map_window)  
    else:
        print('please select an action')