"""
This module is used for creating and inicialization gui elements: main window, containers, buttons, progress bar etc.
Also serves for assign main functions to buttons.
"""

from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QProgressBar
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from logic.get_ascii_grid_data import GetAsciiGridData
from logic.convert_to_csv import ConvertToCsv
from logic.convert_to_png import ConvertToPng
from logic.mesh_density_manipulator import mesh_density_manipulator
from logic.save_as_function import save_new_file_as
from utilis.styles import *
from utilis.helpers import go_to_the_link, resource_path

class ConverterWindow(QWidget):
    """
    It is used to create an gui object with assigned functionality.
    """
    def __init__(self):
        # Calls the constructor of the base class - QWidget
        super().__init__()
        # Set up gui elements             
        self.setup_gui()
        # show window         
        self.show() 

    # GUI INICJALIZATION 
    def setup_gui(self):
        # add gui elements - main window
        self.set_main_window()
        #add function to buttons
        self.functions_assignment() 

    # GUI MAIN WINDOW
    def set_main_window(self):
        """
        It is used to create main window, left and right containers and assign the remaining widgets to them.
        """
        # MAIN WINDOW CONTAINER
        self.move(250, 250)
        self.setFixedSize(main_window_width, main_window_height)
        self.setWindowTitle(main_title)
        # icon get from https://pl.freepik.com/ikona/gora_2510410#fromView=search&page=6&position=5&uuid=9c145f3a-ca9c-4651-8c1d-ac1ebb439fd3
        self.setWindowIcon(QIcon(resource_path(r'resources\icon2.ico'))) 
        self.setStyleSheet(style_widget_main_window
                           +style_button
                           +style_hover_button
                           +style_label
                           +style_messagebox)
        # MAIN LAYOUT               
        main_window_layout = QHBoxLayout(self)
        main_window_layout.setContentsMargins(0,0,0,0)
        main_window_layout.setSpacing(main_window_margin)
        main_window_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # LEFT CONTAINER LAYOUT
        left_container_layout = QVBoxLayout()
        left_container_layout.setContentsMargins(main_window_margin,main_window_margin,0,main_window_margin)
        left_container_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # RIGHT CONTAINER LAYOUT
        right_container_layout = QVBoxLayout()
        right_container_layout.setContentsMargins(0,main_window_margin,main_window_margin,main_window_margin)
        right_container_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # ADD ITEMS TO MAIN WINDOW LAYOUT
        main_window_layout.addLayout(left_container_layout)
        main_window_layout.addLayout(right_container_layout)

        # ADD ITEMS TO LEFT WINDOW LAYOUT
        left_container_layout.addWidget(self.create_title_container())
        left_container_layout.addWidget(self.create_input_data_container())  
        left_container_layout.addWidget(self.create_archline_converter_container())
        left_container_layout.addWidget(self.create_unreal_converter_container())

        # ADD ITEMS TO RIGHT WINDOW LAYOUT
        right_container_layout.addWidget(self.create_title_data_visualization_container())
        right_container_layout.addWidget(self.create_data_visualization_container())

    def create_title_container(self):
        """
        It is used to create main title container. It is just a main title window.
        """
        # TITLE CONTAINER
        # container
        container = QWidget(self)        
        container.setStyleSheet(style_widget_container
                            +style_button
                            +style_hover_button
                            +style_label
                            +style_messagebox)
        container.setFixedSize(left_cointainers_width,container_title_window_height)
        # layout
        layout = QHBoxLayout(container)
        # title
        title = QLabel(main_title,container)        
        title.setStyleSheet(style_title_label)

        #help
        self.help_button = QPushButton('')
        # icon get from https://pl.freepik.com/ikona/gora_2510410#fromView=search&page=6&position=5&uuid=9c145f3a-ca9c-4651-8c1d-ac1ebb439fd3
        self.help_button.setIcon(QIcon(resource_path(r'resources\youtube.png')))
        self.help_button.setFixedSize(40,30) 
        self.help_button.setIconSize(QSize(35,35))        

        #spacers
        spacer_left =QSpacerItem(60, label_height)
        spacer_middle =QSpacerItem(15, label_height)

        # ADD CONTENT TO LAYOUT
        layout.addItem(spacer_left)
        layout.addWidget(title)
        layout.addItem(spacer_middle)
        layout.addWidget(self.help_button)
        return container
        
    def create_input_data_container(self):
        """
        It is used to create main title container.
        """
        # INPUT DATA CONTAINER
        # container
        container = QWidget(self)        
        container.setStyleSheet(style_widget_container
                            +style_button
                            +style_hover_button
                            +style_label
                            +style_messagebox)
        container.setFixedSize(left_cointainers_width,input_data_container_height)
        # layout
        layout = QVBoxLayout(container)
        layout.setContentsMargins(main_window_margin,main_window_margin,main_window_margin,main_window_margin)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setSpacing(main_window_margin)       
        # title
        title = QLabel('WYBIERZ PLIK DO KONWERSJI [.asc]',container)
        title.setStyleSheet(style_subtitle_label)

        # ORIGINAL FILE - WIDGETS
        # original file title
        self.original_file_title = QLabel("Wybrany plik do konwersji:",container)
        # original file button
        self.original_file_path_button = QPushButton("Wybierz plik [.asc] do konwersji", container)
        self.original_file_path_button.setFixedSize(left_cointainers_width-4*main_window_margin,button_height)
        # original file progress bar
        self.original_file_progress_bar = QProgressBar(container)
        self.original_file_progress_bar.setTextVisible(False)
        self.original_file_progress_bar.setFixedSize(left_cointainers_width-4*main_window_margin,progress_bar_height)
        self.original_file_progress_bar.setStyleSheet(style_hide_progress_bar)

        # GRID_DENSITY - WIDGETS
        # grid density title
        self.grid_density_file_title = QLabel("Ustawienia gęstości siatki:",container)
        self.grid_density_file_title.setStyleSheet(style_blocked_label)
        # increase button
        self.increase_grid_density_button = QPushButton("ZWIĘKSZ ▲", container)
        self.increase_grid_density_button.setFixedSize((left_cointainers_width/2)-3*main_window_margin,button_height)
        self.increase_grid_density_button.setStyleSheet(style_blocked_button)        
        self.increase_grid_density_button.setDisabled(True)
        # reduce button
        self.reduce_grid_density_button = QPushButton("ZMNIEJSZ ▼", container)
        self.reduce_grid_density_button.setFixedSize((left_cointainers_width/2)-3*main_window_margin,button_height)
        self.reduce_grid_density_button.setStyleSheet(style_blocked_button)        
        self.reduce_grid_density_button.setDisabled(True)
        # information - grid density
        self.information_grid_density = QLabel("Gęstość siatki: ",container)
        self.information_grid_density.setStyleSheet(style_blocked_label)
        spacer = QSpacerItem(20, 20)
        # information - amount of points
        self.information_amount_of_points= QLabel("Ilość punktów: ",container)
        self.information_amount_of_points.setStyleSheet(style_blocked_label)
        # layout grid density     
        grid_density_main_panel_layout = QHBoxLayout()
        grid_density_left_panel_layout = QVBoxLayout()
        grid_density_left_panel_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        grid_density_right_panel_layout = QVBoxLayout()
        grid_density_right_panel_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # ADD CONTENT - GRID DENSITY SEGMENT
        # main grid density panel
        grid_density_main_panel_layout.addLayout(grid_density_left_panel_layout)
        grid_density_main_panel_layout.addLayout(grid_density_right_panel_layout)
        # left grid density panel
        grid_density_left_panel_layout.addWidget(self.increase_grid_density_button)
        grid_density_left_panel_layout.addWidget(self.reduce_grid_density_button)
        # right grid density panel
        grid_density_right_panel_layout.addWidget(self.information_grid_density)
        grid_density_right_panel_layout.addItem(spacer)
        grid_density_right_panel_layout.addWidget(self.information_amount_of_points)

        # ADD CONTENT - INPUT DATA CONTAINER
        layout.addWidget(title)
        layout.addWidget(self.original_file_title)
        layout.addWidget(self.original_file_path_button)
        layout.addWidget(self.original_file_progress_bar)
        layout.addWidget(self.grid_density_file_title)        
        layout.addLayout(grid_density_main_panel_layout)
        
        return container

    def create_archline_converter_container(self):
        """
        It is used to create archline container.
        """
        # INPUT ARCHLINE CONVERTER CONTAINER
        # container
        container = QWidget(self)        
        container.setStyleSheet(style_widget_container
                            +style_button
                            +style_blocked_button
                            +style_label
                            +style_blocked_label
                            +style_messagebox)
        container.setFixedSize(left_cointainers_width,convert_container_height)
        # layout       
        layout = QVBoxLayout(container)
        layout.setContentsMargins(main_window_margin,main_window_margin,main_window_margin,main_window_margin)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setSpacing(main_window_margin)
        # title
        title = QLabel('KONWERTUJ PLIK DO ARCHLINE [.csv]',container)
        title.setStyleSheet(style_subtitle_label)

        # ARCHLINE CONVERTER - WIDGETS
        # save as xyz title
        self.save_as_xyz_title = QLabel("Zapisz plik jako:",container)
        # save as xyz button
        self.save_as_xyz_button = QPushButton("Podaj nazwę i ścieżkę zapisywanego pliku", container)
        self.save_as_xyz_button.setFixedSize(left_cointainers_width-4*main_window_margin,button_height)        
        self.save_as_xyz_button.setDisabled(True) 
               
        # convert to xyz title
        self.convert_xyz_title = QLabel("Konwertuj:",container)
        self.convert_xyz_button = QPushButton("KONWERTUJ", container)
        # convert to xyz button
        self.convert_xyz_button.setFixedSize(left_cointainers_width-4*main_window_margin,button_height)        
        self.convert_xyz_button.setDisabled(True)
        # convert to xyz progress bar
        self.convert_xyz_progress_bar = QProgressBar(container)
        self.convert_xyz_progress_bar.setTextVisible(False)
        self.convert_xyz_progress_bar.setFixedSize(left_cointainers_width-4*main_window_margin,progress_bar_height)
        self.convert_xyz_progress_bar.setStyleSheet(style_hide_progress_bar)            

        # ADD CONTENT
        layout.addWidget(title)
        layout.addWidget(self.save_as_xyz_title)
        layout.addWidget(self.save_as_xyz_button)
        layout.addWidget(self.convert_xyz_title)
        layout.addWidget(self.convert_xyz_button) 
        layout.addWidget(self.convert_xyz_progress_bar) 

        return container

    def create_unreal_converter_container(self):
        """
        It is used to create unreal engine container.
        """
        # INPUT UNREAL ENGINE CONVERTER CONTAINER
        # container
        container = QWidget(self)        
        container.setStyleSheet(style_widget_container
                            +style_button
                            +style_blocked_button
                            +style_label
                            +style_blocked_label
                            +style_messagebox)
        container.setFixedSize(left_cointainers_width,convert_container_height)
        # layout        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(main_window_margin,main_window_margin,main_window_margin,main_window_margin)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setSpacing(main_window_margin)
        # title
        title = QLabel('KONWERTUJ PLIK DO UNREAL ENGINE [.png]',container)
        title.setStyleSheet(style_subtitle_label)

        # UNREAL ENGINE CONVERTER - WIDGETS
        # save as png title
        self.save_as_png_title = QLabel("Zapisz plik jako:",container)
        # save as png button
        self.save_as_png_button = QPushButton("Podaj nazwę i ścieżkę zapisywanego pliku", container)
        self.save_as_png_button.setFixedSize(left_cointainers_width-4*main_window_margin,button_height)
        self.save_as_png_button.setDisabled(True)

        # convert to png title
        self.convert_png_title = QLabel("Konwertuj:",container)
        self.convert_png_button = QPushButton("KONWERTUJ", container)
        # convert to png button
        self.convert_png_button.setFixedSize(left_cointainers_width-4*main_window_margin,button_height)      
        self.convert_png_button.setDisabled(True)
        # convert to png progress bar
        self.convert_png_progress_bar = QProgressBar(container)
        self.convert_png_progress_bar.setTextVisible(False)
        self.convert_png_progress_bar.setFixedSize(left_cointainers_width-4*main_window_margin,progress_bar_height)
        self.convert_png_progress_bar.setStyleSheet(style_hide_progress_bar)  

        # ADD CONTENT
        layout.addWidget(title)
        layout.addWidget(self.save_as_png_title)
        layout.addWidget(self.save_as_png_button)
        layout.addWidget(self.convert_png_title)
        layout.addWidget(self.convert_png_button) 
        layout.addWidget(self.convert_png_progress_bar) 

        return container

    def create_title_data_visualization_container(self):
        """
        It is used to create title data visualization container. It is just title of data visualization segment.
        """
        # INPUT DATA VISUALIZATION TITLE CONTAINER
        # container
        container = QWidget(self)        
        container.setStyleSheet(style_widget_container
                            +style_button
                            +style_hover_button
                            +style_label
                            +style_messagebox)
        container.setFixedSize(right_cointainers_width,container_title_window_height)
        # layout
        layout = QVBoxLayout(container)
        # title
        title = QLabel("Podgląd Numerycznego Modelu Terenu",container)
        title.setStyleSheet(style_title_label)

        # ADD CONTENT
        layout.addWidget(title)

        return container

    def create_data_visualization_container(self):
        """
        It is used to create data visualization container. This container is used to make space for drawing map from ASCII GRID file - logic.draw_map.py
        """
        # INPUT DATA VISUALIZATION CONTAINER
        # container
        container = QWidget(self)        
        container.setStyleSheet(style_widget_container
                            +style_button
                            +style_hover_button
                            +style_label
                            +style_messagebox
                            +style_tooltip)
        container.setFixedSize(right_cointainers_width,data_visualization_container_height)        
        # layout
        self.map_window = QVBoxLayout(container)               
        
        return container
    
    def functions_assignment(self):
        """
        It is used to assign functionality as methods or class to buttons. In this section in depending on the function, there are also assigned gui elements which styles is changed while using converter.
        This procedure makes the program more readable for the user.
        """
        # help_button
        self.help_button.clicked.connect(lambda: go_to_the_link(link='https://youtu.be/xCaH5lte604'))
        
        # original_file_path_button
        self.original_file_path_button.clicked.connect(lambda: GetAsciiGridData(self.original_file_path_button,
                                                                                self.increase_grid_density_button,
                                                                                self.reduce_grid_density_button,
                                                                                self.save_as_xyz_button,
                                                                                self.save_as_png_button,
                                                                                self.grid_density_file_title,
                                                                                self.information_amount_of_points,
                                                                                self.information_grid_density,
                                                                                self.save_as_xyz_title,
                                                                                self.save_as_png_title,
                                                                                self.original_file_progress_bar,
                                                                                self.map_window).get_original_file_path())
        
        # increase_grid_density_button
        self.increase_grid_density_button.clicked.connect(lambda: mesh_density_manipulator('increase',
                                                                                            self.increase_grid_density_button, 
                                                                                            self.reduce_grid_density_button,
                                                                                            self.information_grid_density,
                                                                                            self.information_amount_of_points,
                                                                                            self.map_window))

        # reduce_grid_density_button
        self.reduce_grid_density_button.clicked.connect(lambda: mesh_density_manipulator('reduce',
                                                                                            self.increase_grid_density_button, 
                                                                                            self.reduce_grid_density_button,
                                                                                            self.information_grid_density,
                                                                                            self.information_amount_of_points,
                                                                                            self.map_window))
        
        # save_as_xyz_button
        self.save_as_xyz_button.clicked.connect(lambda: save_new_file_as('csv',
                                                                            1,
                                                                            self.save_as_xyz_button,
                                                                            self.convert_xyz_button,
                                                                            self.convert_xyz_title))
        
        # convert_xyz_button
        self.convert_xyz_button.clicked.connect(lambda: ConvertToCsv(self.convert_xyz_progress_bar).convert())
        
        # save_as_png_button
        self.save_as_png_button.clicked.connect(lambda: save_new_file_as('png',
                                                                            2,
                                                                            self.save_as_png_button,
                                                                            self.convert_png_button,
                                                                            self.convert_png_title))

        # convert_png_button
        self.convert_png_button.clicked.connect(lambda: ConvertToPng(self.convert_png_progress_bar).convert())      