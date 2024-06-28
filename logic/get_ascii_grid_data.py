"""
Module is asign to original file path button in gui(gui.converter_window.py)
This module is responsible for the following functions:
- get original file path with using QFileDialog
- try data in .asc file and make decision is this, a file ASCII GRID - if is not a ASCII GRID module inform about that with using show_message function
- try is it ASCII GRID xyz or cellsize
- organize data form file and overites valuse from utilis.settings_and_data.py ActualVariablesInstance
- draw height map with using logic.draw_map.py
- updates the progress bar and when every operation is done change format styles gui elements and unblock functions like manipulate mesh density or setting up path for convert files.

!!! data from mapy.geoportal.pl uses a EPSG:2180 - ETRF2000-PL/CS92 (ID:EPSG:2180) coordinate system !!!
"""
import os
import numpy as np
from PySide6.QtWidgets import  QPushButton, QFileDialog, QLabel, QMessageBox, QVBoxLayout, QProgressBar
from PySide6.QtCore import QThread, Signal

from logic.draw_map import draw_map
from utilis.helpers import show_message, unblock_function
from utilis.settings_and_data import ActualVariablesInstance, ascii_grid_data_set_dx_dy_wariant, ascii_grid_data_set_cellsize_wariant
from utilis.styles import style_active_button, style_label, style_button, style_hover_button, style_progress_bar

class GetAsciiGridData(QThread):    
    progress_updated = Signal(int)

    def __init__(self, original_file_path_button=QPushButton,
                 increase_grid_density_button=QPushButton,
                 reduce_grid_density_button=QPushButton,
                 save_as_xyz_button=QPushButton,
                 save_as_png_button=QPushButton,
                 grid_density_file_title=QLabel,
                 information_amount_of_points=QLabel,
                 information_grid_density=QLabel,
                 save_as_xyz_title=QLabel,
                 save_as_png_title=QLabel,
                 original_file_progress_bar=QProgressBar,
                 map_window=QVBoxLayout):        
        super().__init__()
        
        self.original_file_path_button = original_file_path_button
        self.increase_grid_density_button = increase_grid_density_button
        self.reduce_grid_density_button = reduce_grid_density_button
        self.save_as_xyz_button = save_as_xyz_button
        self.save_as_png_button = save_as_png_button
        self.grid_density_file_title = grid_density_file_title
        self.information_amount_of_points = information_amount_of_points
        self.information_grid_density = information_grid_density
        self.save_as_xyz_title = save_as_xyz_title
        self.save_as_png_title = save_as_png_title
        self.original_file_progress_bar = original_file_progress_bar
        self.map_window = map_window

        self.progress_updated.connect(self.update_progress_bar)

    def update_progress_bar(self, value):
        self.original_file_progress_bar.setValue(value)

    def get_original_file_path(self):
        def is_ascii_grid_file(path):
            try:
                # INITIALIZATION VARIABLES
                values = {}
                keys = []
                file_size = os.path.getsize(path) # take file size
                bytes_read = 0

                with open(path, 'r') as file:
                    # TAKE HEADERS
                    for key_dx_dy, key_cellsize in zip(ascii_grid_data_set_dx_dy_wariant, ascii_grid_data_set_cellsize_wariant):
                        # update progress bar
                        line = file.readline().strip()                     
                        bytes_read += len(line.encode('utf-8'))
                        self.progress_updated.emit(int((bytes_read / file_size) * 100))

                        # try is it is dx_dy ASCII GRID                       
                        if line.startswith(key_dx_dy):
                            values[key_dx_dy] = float(line.split()[1]) 
                            keys.append(key_dx_dy)

                        # try is it is cellsize ASCII GRID    
                        elif line.startswith(key_cellsize):
                            values[key_cellsize] = float(line.split()[1])
                            keys.append(key_cellsize)

                        # if it isnt ASCII GRID dx_dy and ASCII GRID cellsize
                        else:                            
                            return False
                        
                    # TAKE DATA GRID
                    data_grid = []                    
                    for line in file:
                        # read row
                        row = [float(value) for value in line.split()]
                        bytes_read += len(line.encode('utf-8'))
                        # update progress bar
                        self.progress_updated.emit(int((bytes_read / file_size) * 100))                        
                        data_grid.append(row)
                    # replace with array
                    data_grid = np.array(data_grid)
                    # if it is cellsize include nodata value - nodatavalue is change to 0 n.p.m.
                    if keys[4] == ascii_grid_data_set_cellsize_wariant[4]:
                        data_grid[data_grid==values[keys[5]]]=0
                        values["data_grid"] = data_grid 
                    else:
                        values["data_grid"] = data_grid     
                return True, values, keys
            
            except Exception as e:
                return False
            
        #OPEN FILE DIALOG
        options = QFileDialog.Options()
        #take path
        path, _ = QFileDialog.getOpenFileName(None, "Wybierz plik ASCII GRID", "", "(*.asc)", options=options)      

        if path:
            # show progress bar
            self.original_file_progress_bar.setStyleSheet(style_progress_bar)
            # set up progress bar value on 0            
            self.original_file_progress_bar.setValue(0)            
            result = is_ascii_grid_file(path)
            if result:
                success, values, keys = result
                if success:
                    #UPDATE DATA
                    # update original file path                    
                    ActualVariablesInstance.update_variable(0, path)

                    # set button text
                    button_text = path if len(path) < 43 else path[:15] + " (...) " + path[-20:]

                    # data actualization                    
                    ActualVariablesInstance.update_variable(3, values[keys[0]])         # ncols        
                    ActualVariablesInstance.update_variable(4, values[keys[1]])         # nrows           
                    ActualVariablesInstance.update_variable(5, values[keys[2]])         # xllcorner             
                    ActualVariablesInstance.update_variable(6, values[keys[3]])         # yllcorner             
                    ActualVariablesInstance.update_variable(7, values[keys[4]])         # dx 
                    if keys[4] == ascii_grid_data_set_cellsize_wariant[4]:
                        ActualVariablesInstance.update_variable(8, values[keys[4]])     # dy if it's cellsize ASCII GRID 
                    else:
                        ActualVariablesInstance.update_variable(8, values[keys[5]])     # dy if it's dx_dy ASCII GRID
                    ActualVariablesInstance.update_variable(10, values[keys[4]])        # mesh_density
                    ActualVariablesInstance.update_variable(9, values["data_grid"])     # data_grid                   

                    # change formating original file path button - style active button
                    self.original_file_path_button.setText(button_text)
                    self.original_file_path_button.setStyleSheet(style_active_button)

                    # UNBLOCK FUNCTION
                    # grid density manipulation                                      
                    unblock_function(self.increase_grid_density_button, False)
                    unblock_function(self.reduce_grid_density_button, style_button+style_hover_button)
                    # archline converter - save as xyz
                    if ActualVariablesInstance.get_variable(1) == '':                  
                        unblock_function(self.save_as_xyz_button, style_button+style_hover_button)
                    # unreal engine converter - save as png
                    if ActualVariablesInstance.get_variable(2) == '':                    
                        unblock_function(self.save_as_png_button, style_button+style_hover_button) 

                    # CHANGE STYLES GUI ELEMENTS
                    # grid density manipulation 
                    self.grid_density_file_title.setStyleSheet(style_label)                
                    self.information_amount_of_points.setStyleSheet(style_label)                
                    self.information_grid_density.setStyleSheet(style_label)
                    # archline converter - save as xyz
                    self.save_as_xyz_title.setStyleSheet(style_label)
                    # unreal engine converter - save as png
                    self.save_as_png_title.setStyleSheet(style_label)                                    

                    # DRAW HEIGHT MAP
                    draw_map(self.increase_grid_density_button,
                            self.reduce_grid_density_button,
                            self.information_grid_density,
                            self.information_amount_of_points,
                            self.map_window)
                    # update original file progress bar to 100%
                    self.original_file_progress_bar.setValue(100)                                        
                else:
                    show_message(None, 'Wybrany plik nie jest plikiem ASCII GRID', "bład", QMessageBox.Critical)                    
            else:
                show_message(None,'Wybrany plik nie jest plikiem ASCII GRID', "bład", QMessageBox.Critical)