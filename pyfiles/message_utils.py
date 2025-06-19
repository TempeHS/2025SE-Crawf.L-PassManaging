from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt


def show_error(self, message: str) -> None:
    """Display errors in a message box that allows copying text.
    Args:
        message (str): The error message to display.
    """
    box = QMessageBox()
    box.setIcon(QMessageBox.Icon.Critical)
    box.setWindowTitle("Error")
    box.setText(message)
    box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    box.exec()


def show_warning(self, message: str) -> None:
    """Display warnings in a message box that allows copying text.
    Args:
        message (str): The warning message to display.
    """
    box = QMessageBox()
    box.setIcon(QMessageBox.Icon.Warning)
    box.setWindowTitle("Warning")
    box.setText(message)
    box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    box.exec()


def show_info(self, message: str) -> None:
    """Display information in a message box that allows copying text.
    Args:
        message (str): The information message to display.
    """
    box = QMessageBox()
    box.setIcon(QMessageBox.Icon.Information)
    box.setWindowTitle("Information")
    box.setText(message)
    box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    box.exec()
