from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
import sys
import time
import os

import pyfiles.encrypt as encrypt


def resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller bundle.
    This function checks if the application is running as a PyInstaller bundle
    and adjusts the path accordingly. If not, it uses the current file's directory.
    """
    if hasattr(sys, "_MEIPASS"):
        # If running as a PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def user_data_path(filename):
    """
    Get a path for user data files in the user's home directory.
    This function creates a directory named ".simple_app_data" in the user's home
    directory if it does not exist, and returns the full path to the specified filename.
    """
    home_dir = os.path.expanduser("~")
    app_dir = os.path.join(home_dir, ".simple_app_data")
    os.makedirs(name=app_dir, exist_ok=True)
    return os.path.join(app_dir, filename)


class DecodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.fileencryptor = encrypt.AESFileEncryptor()
        self.init_ui()

    def show_error(self, message: str) -> None:
        """Display errors in a message box that allows copying text.
        Args:
            message (str): The error message to display.
        """
        box = QMessageBox(self)
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
        box = QMessageBox(self)
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
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle("Information")
        box.setText(message)
        box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        box.exec()

    def init_ui(self) -> None:
        """
        Initialise the user interface for the decoder application.
        """
        pass

    def decode(self, password: str) -> None:
        """Decrypt a file using the provided password.
        Args:
            password (str): The password to use for decryption.
        """
        if not password:
            self.show_error("Password cannot be empty.")
            return
        input_path = user_data_path("help.txt.enc")
        decrypted_path = user_data_path("help_de.txt")
        try:
            self.fileencryptor.decrypt_file(
                password=password,
                input_path=input_path,
                output_path=decrypted_path,
            )
            self.show_info(f"File decrypted successfully to {decrypted_path}")
        except Exception as e:
            self.show_error(f"Decryption failed: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DecodeApp()
    window.show()
    app.exec()
