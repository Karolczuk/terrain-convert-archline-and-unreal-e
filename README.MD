# Terrain Converter
*File exe version download: https://serwerentazis.quickconnect.to/d/s/z4hpWRFozIXdlaGqxLmNmcn83hc9UwDh/cKQVD-AU__qI3Q_wE2_5GUfUHc_X5zwK-OrFAByRZeQs

*Tutorial - how to use terrain converter: https://youtu.be/xCaH5lte604

## Description

This application was created out of the need for efficient implementation of terrain models from the portal https://mapy.geoportal.gov.pl/imap/Imgp_2.html?gpmap=gp0 into BIM (Building Information Modeling) software and the Unreal Engine - graphics engine.
The program is used to convert ASCII GRID (.asc) files [DTM] downloaded from services such as https://mapy.geoportal.gov.pl/imap/Imgp_2.html?gpmap=gp0 and convert them into Archline XYZ (.csv) format and Unreal Engine height maps (.png). The converter allows for quick file conversion, enabling efficient use in BIM projects as well as photorealistic visualizations of construction objects. The usage method is presented in the following link: https://youtu.be/xCaH5lte604

### Application Functions

- Loading an ASCII GRID (.asc) file and checking whether the file structure contains the necessary data for proper file usage
- Modifying the density of terrain contour grids, allowing adjustment of the number of points according to project needs. This enables grid density customization so that it does not significantly burden the project
- Converting ASCII GRID (.asc) files to the XYZ format accepted by Archline.XP (BIM)
- Converting ASCII GRID (.asc) files to the height map (.png) format accepted by the Unreal Engine graphics engine

## Installation

The program is contained in a single file (`Terrain converter.exe`) and does not require installation.

## Usage

### Downloading an ASCII GRID - NMT File

1. Visit the [Geoportal](https://mapy.geoportal.gov.pl/imap/Imgp_2.html?gpmap=gp0).
2. Zoom into the area of interest.
3. Use one of the two methods to download the file:

#### Method 1

a) Use the tool located in the upper left corner [Dane do pobrania] (data download).  
b) Select the WCS service [Numeryczny Model Terenu]] (Digital Terrain Mode) - Arc/Info ASCII Grid].  
c) Choose the layer [DTM_PL-EVRF2007-NH], alternatively [DTM_PL-KRON86-NH].  
d) Select the tool [Rysuj obs...] to mark the area of interest.  
e) Click [Zapisz plik] (Save file).

#### Method 2

a) In the 'zawartość mapy' (map content) menu, expand the [Dane do pobrania] (Downloadable Data) directory.  
b) Expand the [Numeryczny Model Terenu]] (Digital Terrain Mode)  directory.  
c) Expand the [siatka <= 1m] (grid <= 1m) directory (it is recommended to choose a 1m grid density).  
d) Check the [NMT PL - EVRF2007-NH] item, alternatively [NMT PL-KRON86-NH].  
e) Left-click on the area of interest, from the appearing menu select the previously marked service.  
f) Select the resource and click [pobierz plik danych dla tej sekcji] (download data file for this section).

### Loading an ASCII GRID File

1. Open Terrain converter.
2. In the panel, click the button 'Wybierz plik [.asc] do konwersji' (Select [.asc] file to convert).
3. After successfully loading the file, a preview of the Digital Terrain Model will appear on the right side.

### Conversion to Archline.XP (BIM) - XYZ Format (.csv)

1. Choose the target file path using the button 'Podaj nazwę i ścieżkę zapisywanego pliku' (Enter the name and path of the file to be saved).
2. Click 'KONWERTUJ' (CONVERT).
3. Import the file into Archline using [Architecture] -> [Terrain] -> [Create] -> [Create by importing data].

### Conversion to Unreal Engine (Graphics Engine) - Height Map Format (.png)

1. Choose the target file path using the button 'Enter the name and path of the file to be saved'.
2. Click 'KONWERTUJ' (CONVERT).
3. Import the file into Unreal Engine using [Landscape] -> [Manage] -> [New] -> [Import from file].

* Usage link: https://youtu.be/xCaH5lte604

## Application Operation

### GUI Generation

The program's GUI was created using the PySide6 library. All GUI elements such as buttons, text fields, etc. were implemented in the file gui/converter_window.py. Besides the functions creating the interface in this file, there is also a function assigning functionalities to individual buttons. To maintain code clarity, GUI styling and geometry formatting of various elements were moved to the file utilis/styles.py.

### Fetching Data from ASCII GRID File and Updating Variables During Program Runtime

Fetching data from the ASCII GRID file is done using the module logic/get_ascii_grid_data.py. This module utilizes the module utilis/settings_and_data.py, where variables are implemented as an updating Variables class instance. The Variables class instance has two functions: update_variable and get_variable, which use 'setattr' and 'getattr' functions. This approach allows dynamic data exchange between different modules, facilitated by the instance of the Variables class created in this file as ActualVariablesInstance = Variables().

The first step involves retrieving the file path using the QFileDialog class. Then, using the function def is_ascii_grid_file, it checks if the file (asc.) is an NMT file or not an ASCII GRID file at all. This is done by comparing the header values in the first 6 lines of the imported text file with lists imported from utilis/settings_and_data.py, namely ascii_grid_data_set_dx_dy_variant and ascii_grid_data_set_dx_dy_variant. If the file matches any of the formats, the function saves the data to variables, updating them in the ActualVariablesInstance class. Subsequently, other modules gain access to header values such as "ncols," "nrows," "xllcorner," etc., and the data grid itself.

While fetching subsequent lines of data from the file, the application progress bar is updated. After fetching and saving the data into the variables of the ActualVariablesInstance class, GUI elements are updated, and functionalities of buttons like decrease and increase grid density, provide path to save png and csv files are unlocked. Additionally, a map is drawn using the draw_map function from the module logic/draw_map.py.

### Changing Grid Density

This is achieved through functions in the module logic/mesh_density_manipulator.py, assigned to the increase_grid_density_button and reduce_grid_density_button. 

These functions retrieve the grid density from the ActualVariablesInstance class instance imported earlier from the ASCII GRID file. The function operates in two alternative modes: increasing or decreasing the grid density. Depending on the option, the density value is incremented or decremented by 1 within the range of 1 to 100. Subsequently, the variable in the ActualVariablesInstance class is updated. After updating the values, a map is redrawn using the draw_map function from the logic/draw_map.py module.

### Drawing Terrain Model Preview Map

The map is drawn using the draw_map function located in the module logic/draw_map.py. Map drawing occurs during the import of the ASCII GRID file and after each manipulation of grid density.

The first step involves fetching all necessary variables from the ActualVariablesInstance class instance, such as header values (xllcorner, yllcorner, dx, dy), grid density (mesh_density), and terrain elevation values (data_grid). These values are used to create a chart depicting terrain elevations represented by colors on axes representing geodetic longitude and latitude (x and y). Additionally, canvas and figure values are fetched, initially set to None, which help identify whether the chart and canvas are being drawn for the first time or if the function is being called to overwrite existing canvas and chart.

After updating the variables in the ActualVariablesInstance class instance, the data_grid_filtered variable is determined. This variable holds the filtered data_grid based on the _mesh_density value. Subsequently, the ActualVariablesInstance class instance is updated with the created data_grid_filtered variable. GUI elements such as information_grid_density and information_amount_of_points are also updated, allowing precise checking of the number of points in the grid. This feature primarily facilitates importing large areas into Archline (BIM) with practically any number of points.

The next step involves checking if any charts already exist; if so, they are cleared, along with the canvas.

Next, a figure and canvas are created and updated in the ActualVariablesInstance class instance.

Drawing of the map for data_grid_filtered is initiated using the imshow function, taking into account the updated dx and dy values scaled by mesh_density.

### Conversion to Archline (csv.)

Conversion to a csv file is done using the module logic/convert_to_csv.py. The first step involves fetching data from the ActualVariablesInstance class instance. Once the data is initialized, the number of points prepared for conversion (amount_of_points) is calculated, and the variable actual_converted_amount_of_points is determined.

The function writes lines of text to a file at the path previously set by the logic/save_as_function.py module, which is linked to the save_as_xyz_button with the .csv variant. Each line in the csv file corresponding to each value of the filtered data_grid_filtered must appear as follows:

    com_x.value_x;com_y.value_y;com_z.value_z

        com_x - This is a comment for the x value. It appears in the grid generated by Archline (BIM). The program assigns to it the current value of actual_converted_amount_of_points and also numbers all points from 1 to the last point in the data_grid_filtered grid.

        value_x - This is the geodetic coordinate value calculated as (xllcorner + dx * (column number of the grid))

        com_y - This is a comment for the y value. It is not visible in Archline, so it is set to 0 in every case.

        value_y - This is the geodetic coordinate value calculated as (yllcorner + dy * (row number of the grid))

        com_z - This is a comment for the z value. It is not visible in Archline, so it is set to 0 in every case.

        value_z - This is the elevation value read from the data_grid_filtered grid.

    Since '.' is reserved in the notation as a connector between value and comment and ',' is equivalent to ';', which separates individual x, y, and z values, it is necessary to use the format function to split the number into an integer and decimal part, and then put them together in an equation that Archline executes when importing to get a floating point number. The operation is presented in the following example:

        142.26
        142 + (0.27 * 100) / 100
        142 + 26/100 - this form is received by Archline

        Example target line => 1.574405 + 98/100; 0.148516 + 26/100; 0.1819 + 70/100

    After creating all lines of the target csv file, the progress bar is updated to 100%, and then a message is displayed indicating successful completion of the operation.

### Conversion to Unreal Engine (.png)

Conversion to a (.png) file is handled by the module logic/convert_to_png.py. To properly prepare the (.png) file for import into the Unreal Engine graphics engine:

- The png file must be in 16-bit grayscale format.
- A 16-bit file allows for representing grayscale values from 0 (black) to 65535 (white).
- The width and height of the created landscape plane mimic the bitmap of the png file, where each pixel's grayscale value translates into a height level, deforming the plane to represent terrain elevations. White color (65535) represents the highest point of our landscape, while black color (0) represents the lowest point.

In Unreal Engine, each landscape can be scaled along x, y, and z coordinates:
- x and y dimensions in the basic version (scale x=1, y=1) create a plane of 1 pixel by 1 pixel, translating to 1cm by 1cm (0.01m by 0.01m).
- z elevation in the basic version (scale z=1) between black (0) and white (65535) corresponds to a height difference of 512 units, equivalent to 512cm (5.12m).

By default, when importing a png file, Unreal Engine creates a landscape with a scale of (x=100, y=100, z=100), resulting in a terrain where 1 pixel represents 1m² and a height difference between black (0) and white (65535) of 512m. However, to accurately represent all heights found in Poland, the import scale will be adjusted to (x=100, y=100, z=600), allowing 1 pixel to represent 1m² and a height difference between black (0) and white (65535) of 3072m. If a greater height difference needs to be represented, adjust the Unreal Engine values accordingly, along with the converter's unreal_engine_min_val and unreal_engine_max_val to cover that range.

Operation of the converter:
- It scales all received elevation values from the data_grid_filtered variable in the range from 0 to 1, assuming that 0 = unreal_engine_min_val = -512 and 1 = unreal_engine_max_val = 2560.
- Then, it multiplies all these values by 65535 to obtain a proportional distribution of elevations in the range from 0 to 65535, where 0 = -512 and 65535 = 2560.

Next, using the Image class from the PIL library, the resulting set of numbers is transformed into a 16-bit grayscale map. The map is then scaled to dimensions imgae_width = round(ncols) - 1 and imgae_height = round(nrows) - 1 to maintain consistent dimensions even if the number of points is reduced during filtering from data_grid to filtered_data_grid.

After this operation, the image is saved to a png file, and a message is displayed confirming the successful conversion along with a reminder to set the scale in Unreal Engine.

## Technologies Used

*Python 3.12.3* - Application framework, class and method creation.

*PySide6 Library* - GUI element creation such as widgets, buttons, etc.
                  - Organization of element positions using QVBoxLayout and QHBoxLayout.
                  - Implementation of icons for the program.
                  - Generation of dialog windows using QFileDialog.
                  - Creation of a new thread for time-consuming functions (inheritance from QThread) to prevent interface window blocking during execution of lengthy operations.

*NumPy Library* - Data set operations, rounding, extraction of values at regular intervals.

*PIL Library* - Drawing bitmap maps from data sets.

*Matplotlib* - Dynamic chart drawing showing the distribution of elevation values on geodetic coordinates x and y.

## Future Development

1. Addition of map generators (.dxf) depicting elements such as plot boundaries, terrain infrastructure, etc.
2. Integration of multiple asc files to create larger terrains (over 7km²).

## Authors

Karolczuk Kamil.



