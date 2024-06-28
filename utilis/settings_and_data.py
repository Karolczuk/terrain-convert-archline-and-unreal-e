"""
This module is responsible for the following functions:
- storage constant values
- storage variables value for aplication
- updating values while using the program 
"""
import numpy as np

#CONSTANT

ascii_grid_data_set_dx_dy_wariant = ["ncols", "nrows", "xllcorner", "yllcorner", "dx", "dy"]
ascii_grid_data_set_cellsize_wariant = ["ncols", "nrows", "xllcenter", "yllcenter", "cellsize", "nodata_value"]

# Index mapping
VARIABLES_INDEX = {
    0: 'original_file_path',
    1: 'new_file_xyz_path',
    2: 'new_file_png_path',
    3: 'ncols',
    4: 'nrows',
    5: 'xllcorner',
    6: 'yllcorner',
    7: 'dx',
    8: 'dy',
    9: 'data_grid',
    10: 'mesh_density',
    11: 'data_grid_filtered',
    12: 'canvas',
    13: 'figure'
}

#VARIABLES
class Variables():
    """
    storage variable start values
    update variable values between modules
    send variables values between modules
    """
    # variables
    def __init__(self):  
        self.original_file_path = ''
        self.new_file_xyz_path = ''
        self.new_file_png_path = ''
        self.ncols = 0
        self.nrows = 0
        self.xllcorner = 0
        self.yllcorner = 0
        self.dx = 0
        self.dy = 0
        self.data_grid = np.array([[0]])
        self.mesh_density = False
        self.data_grid_filtered = False
        self.canvas = None
        self.figure = None
    # set variable
    def update_variable(self, index, value):
        var_name = VARIABLES_INDEX.get(index)
        setattr(self, var_name, value)
    # get variable
    def get_variable(self, index):
        var_name = VARIABLES_INDEX.get(index)        
        return getattr(self, var_name)
#INSTANCE
ActualVariablesInstance = Variables()