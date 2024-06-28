"""
Module is asign to save as png and save as xyz buttons in gui(gui.converter_window.py)
This module is responsible for the following functions:
- set up new file path
- update new file path to utilis.settings_and_data.py ActualVariablesInstance
"""
from PySide6.QtWidgets import QPushButton, QFileDialog, QLabel
from typing import Literal, Union

from utilis.settings_and_data import ActualVariablesInstance
from utilis.styles import style_button, style_hover_button, style_active_button, style_label
from utilis.helpers import unblock_function

def save_new_file_as(file_extension: Literal['csv', 'png'], #choose if it is csv or png variant
                    index_path_to_update: Union[int],       #choose if it is csv or png variant
                    path_button =QPushButton, 
                    convert_button=QPushButton,
                    convert_title=QLabel):
    
    #OPEN FILE DIALOG
    options = QFileDialog.Option()
    #take path
    path, _ = QFileDialog.getSaveFileName(None, "Zapisz plik jako", "",
                                            f"Pliki {file_extension.upper()} (*.{file_extension})",
                                            options=options)
    if path != "":
        #try path
        if not path.endswith('.'+file_extension):
            path += '.'+file_extension
        path_button_text = path if len(path) < 43 else path[:15] +" (...) "+ path[-20:]
        #data actualization
        ActualVariablesInstance.update_variable(index_path_to_update, path)        
        #change formating path button
        path_button.setText(path_button_text)
        path_button.setStyleSheet(style_active_button)
        #unblock convert function
        unblock_function(convert_button, style_button+style_hover_button)
        #format style convert title
        convert_title.setStyleSheet(style_label)        