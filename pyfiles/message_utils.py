from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt


class MessageBox(QMessageBox):
    """Custom boxes that allows copying text."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    def show_error(self, message: str) -> None:
        """
        Show an error message box with the given title and message.
        Args:
            message (str): The error message to display.
        """
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle("Error")
        self.setText(message)
        self.exec()

    def show_warning(self, message: str) -> None:
        """
        Show a warning message box with the given title and message.
        Args:
            message (str): The warning message to display.
        """
        self.setIcon(QMessageBox.Icon.Warning)
        self.setWindowTitle("Warning")
        self.setText(message)
        self.exec()

    def show_info(self, message: str) -> None:
        """
        Show an information message box with the given title and message.
        Args:
            message (str): The information message to display.
        """
        self.setIcon(QMessageBox.Icon.Information)
        self.setWindowTitle("Information")
        self.setText(message)
        self.exec()
