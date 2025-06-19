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
import pyfiles.message_utils as message_utils


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
        self.message_box = message_utils.MessageBox(self)
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
        self.setWindowTitle("File Decryptor")

        # Create layout
        layout = QVBoxLayout()

        self.label = QLabel("Enter the password to decrypt the file:")
        layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.password_input.setTextMargins(0, 0, 0, 0)
        self.password_input.setPlaceholderText("Enter password for decryption:")

        layout.addWidget(self.password_input)

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
            self.message_box.show_info(
                f"File decrypted successfully to {decrypted_path}"
            )
        except Exception as e:
            self.message_box.show_error(f"Decryption failed: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DecodeApp()
    window.show()
    app.exec()
