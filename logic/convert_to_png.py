"""
Module is asign to convert to png button in gui(gui.converter_window.py)
This module is responsible for the following functions:
- take actual data from utilis.settings_and_data.py ActualVariablesInstance
- convert data_grid_filtered values to 18bit gray scale height map
- set image size
- if everything is done, show message that action is complete and save file as .png
"""
import os
import numpy as np
from PIL import Image
from PySide6.QtWidgets import QMessageBox, QProgressBar
from PySide6.QtCore import QThread, Signal

from utilis.settings_and_data import ActualVariablesInstance
from utilis.styles import style_progress_bar
from utilis.helpers import show_message

class ConvertToPng(QThread):
    progress_updated = Signal(int)
    def __init__(self, convert_png_progress_bar=QProgressBar): 

        super().__init__()

        self.convert_png_progress_bar = convert_png_progress_bar 
        self.progress_updated.connect(self.update_progress_bar)

    def update_progress_bar(self, value):
        self.convert_png_progress_bar.setValue(value)

    def convert(self):
        """
        Unreal engine using imported png height map to create landscape object.
        It works like that every pixel make plane and grayscale of this pixel set height:
        PLANE: in basic veriosn 1px create plane with dimensions (1 game unit) x (1 game unit) which which corresponds to the equivalent 0,01m x 0,01cm
                thats why we need to scale landscape object in x and y coordinate by 100 what give us 1m x 1m plane = 1 square meter
                Scaled by 100 is set default
        HEIGHTS: Unreal engine interpes height map in the following way:
                0(black color) - lowest point
                65535 (white color) - highest point
                in basic version the difference berween lowest and highest point is equvalent 512 game unit that is equivalent 5,12m
                which means the height difference between 0 and 1 grayscale is 5,12/65535 ≈ 0,00007812619211
                when we use landscape scale on z coordinate by 600 that give us height diference with a value of 3072m which will allow mapping all heights in Poland
        Module operation:
        set mnimum value of meters Above Mean Sea Level at -512 (AMSL)
        set maximum value of meters Above Mean Sea Level at 2560 (AMSL)
        load data_grid_filtered and scaled every value assuming that -512 (AMSL) is 0 and 2560 (AMSL) is 1
        tramsform every value multiplay by 65535
        make image with using created array
        scale image to meters
        save image as png
        """

        # INPUT DATA
        # constant        
        unreal_engline_min_val = -512   # set minimum value of meters Above Mean Sea Level (AMSL) which corresponds to 0 (black color) in 16bit png greyscale  
        unreal_engline_max_val = 2560   # set maximum value of meters Above Mean Sea Level (AMSL) which corresponds to 65535 (white color) in 16bit png greyscale  
        # input data              
        path = ActualVariablesInstance.get_variable(2)
        ncols = ActualVariablesInstance.get_variable(3)
        nrows = ActualVariablesInstance.get_variable(4)
        data_grid_filtered = ActualVariablesInstance.get_variable(11)

        # SET VARIABLES
        imgae_width = round(ncols) -1
        imgae_height = round(nrows) -1
        image_size = (imgae_width, imgae_height)

        #FORMATING ASCII GRID FILE TO PNG UNREAL ENGINE FILE
        # show convert progress bar
        self.convert_png_progress_bar.setStyleSheet(style_progress_bar)
        # set convert progress bar value on 0               
        self.convert_png_progress_bar.setValue(0) 
        # convert data from meters Above Mean Sea Level (AMSL) to 16bit png greyscale        
        scaled_data = np.clip((data_grid_filtered - unreal_engline_min_val) / (unreal_engline_max_val - unreal_engline_min_val) * 65535, 0, 65535)
        # round scaled data
        scaled_data = np.round(scaled_data, 2)
        def save_as_png(data, output_path):            
            img = Image.fromarray(data, mode='I;16')
            # set convert xyz progress bar value on 10
            self.convert_png_progress_bar.setValue(10)

            # resize image 1px = 1meter          
            img = img.resize(image_size,)
            # set convert xyz progress bar value on 20
            self.convert_png_progress_bar.setValue(20) 

            # save created image to output path        
            img.save(output_path)
            # set convert xyz progress bar value on 100
            self.convert_png_progress_bar.setValue(100)            
        # save png
        save_as_png(scaled_data.astype(np.uint16), path)        
        show_message(None, f'Pomyślnie utworzono plik: {os.path.basename(path)}!\n\nWskazówka: \nPrzy imporcie pliku do Unreal Engine ustaw skalę:         \n   x=100 \n   y=100 \n   z=600 \nPowodzenia!', "Utworzono plik", QMessageBox.Information)