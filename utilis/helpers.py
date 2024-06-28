import sys
import os

"""
This module is responsible for the following functions:
- storage helpers methods
"""
from PySide6.QtWidgets import  QPushButton, QMessageBox
import webbrowser

from utilis.styles import style_button, style_hover_button


def show_message(self, message: str, window_title: str, Type):
    """
    creates different types of messages
    """
    # ok button
    Ok_button = QPushButton('OK')
    Ok_button.setFixedSize(100, 30)
    Ok_button.setStyleSheet(style_button + style_hover_button)

    # ok message box
    msg_box = QMessageBox()
    msg_box.setIcon(Type)
    msg_box.setWindowTitle(window_title)
    msg_box.setText(message)
    msg_box.addButton(Ok_button, QMessageBox.AcceptRole)
    msg_box.exec()

def unblock_function(button: QPushButton, new_style):
    """
    unblock functions for buttons and change their styles
    """
    # unblock function for button
    button.setDisabled(False) 
           
    # change style
    if new_style:
        if isinstance(new_style, str):
            button.setStyleSheet(new_style)

def go_to_the_link(link=str):
    """
    open link
    """
    # go to the link
    webbrowser.open(link)

def resource_path(relative_path):
    """ Returns the path to the resource, whether it is a script or a frozen executable """
    try:
        # PyInstaller creates a 'sys._MEIPASS' variable that points to a temporary resource directory
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)