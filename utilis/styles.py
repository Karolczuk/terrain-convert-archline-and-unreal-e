"""
This module is responsible for the following functions:
- storage converter window geometry setting
- storage converter window geometry text
- storage widgets styles
"""
#CONSTANS - GEOMETRY
# main window
main_window_width = 1300
main_window_height = 755
main_window_margin = 5

# containers
left_cointainers_width = int(round(main_window_width/2.8)-1.5*main_window_margin)
right_cointainers_width = main_window_width-left_cointainers_width-3*main_window_margin

# buttons
button_height = 40

# labels
label_height = 20

# progress bar
progress_bar_height = 5

# title container
container_title_window_height = 50

# input data container    
input_data_container_height = 258

# convert data container
convert_container_height = 210

# data visualization container
data_visualization_container_height = 688

#CONSTANS - TEXT
main_title = "Konwerter plików ASCII Grid [.asc]"

#CONSTANS - STYLES
style_widget_main_window = """
    QWidget {
        background: #f3f3f7;
        color: black;
    }
"""
style_widget_container = """
    QWidget {
        background: #f0f0f0;
        border-radius: 1px;
        border: 1.5px solid #828790;                     
        color: black;
    }
"""
style_button = """
    QPushButton {
        background: #e1e1e1;
        color: black;
        border-radius: 2px;
        border: 0.5px solid #adadad;
        font-size: 15px;
    }

"""
style_hover_button = """
    QPushButton:hover {
        background: qlineargradient(
            spread:pad, x1:0, y1:0, x2:0, y2:1,
            stop:0 #fffbeb, stop:0.5 #ffe587, stop:1 #fffbeb
        );
        border: 1px solid #f9da4d;
    }
"""
style_active_button = """
    QPushButton {
        background: qlineargradient(
            spread:pad, x1:0, y1:0, x2:0, y2:1,
            stop:0 #f6ffeb, stop:0.5 #bdff87, stop:1 #f6ffeb
        );
        border-radius: 2px;
        border: 0.5px solid #84d145;
        color: black;
    }
"""
style_blocked_button = """
    QPushButton {
        background: #e1e1e1;
        color: grey;
        border-radius: 2px;
        border: 0.5px solid #adadad;
        font-size: 15px;
    }
    QPushButton:hover {
        background: #e1e1e1;
        color: grey;
        border-radius: 2px;
        border: 0.5px solid #adadad;
        font-size: 15px
    }
"""
style_label = """
    QLabel {
        background: #00000000;
        color: black;
        font-size: 15px;
        border: none;
    }
"""
style_messagebox = """
    QMessageBox {
        background: #f0f0f0;
        color: black;
        font-size: 15px;
    }
"""
style_title_label = """
    QLabel {
        background: #00000000;                  
        color: black;
        font-size: 20px;
        qproperty-alignment: 'AlignCenter';
    }
"""
style_subtitle_label = """
    QLabel {
        background: #00000000;                  
        color: black;
        font-size: 18px;
        qproperty-alignment: 'AlignCenter';
    }
"""
style_blocked_label = """
    QLabel {                  
        color: grey;
    }
"""

style_tooltip = """
    QToolTip {        
        color: black;
        font-size: 15px;
        border: none;
    }
"""
style_progress_bar = """
    QProgressBar {
        border: none;
        background: #e1e1e1;
        border-radius: 2px;         
        font-size: 20px;
        qproperty-alignment: 'AlignCenter';
      
    }
    QProgressBar::chunk {
        background-color: #71bc34;
        border-radius: 2px;
    }
"""
style_hide_progress_bar = """
    QProgressBar {
        border: none;
        background: #00000000; 
        font-size: 20px;
        qproperty-alignment: 'AlignCenter';
      
    }
    QProgressBar::chunk {
        background-color: #00000000;
    }
"""