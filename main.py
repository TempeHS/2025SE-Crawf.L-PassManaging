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
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, filename)


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.fileencryptor = encrypt.AESFileEncryptor()
        self.init_ui()
        self.show_error = message_utils.show_error
        self.show_warning = message_utils.show_warning
        self.show_info = message_utils.show_info

    def init_ui(self) -> None:
        """
        Initialise the user interface of the application.
        """
        self.setWindowTitle("Simple App")

        # Create layout
        layout = QVBoxLayout()

        # Add a label
        self.label = QLabel("Enter a memorable password:")
        layout.addWidget(self.label)

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.password_field.setTextMargins(0, 0, 0, 0)
        self.password_field.setPlaceholderText("Enter password for encryption:")
        layout.addWidget(self.password_field)

        # Add a confirm password field
        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_field.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.confirm_password_field.setTextMargins(0, 0, 0, 0)
        self.confirm_password_field.setPlaceholderText("Confirm password:")
        layout.addWidget(self.confirm_password_field)

        # Add a submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.show_dialog)
        layout.addWidget(self.submit_button)

        # Set the layout for the main window
        self.setLayout(layout)

    def show_dialog(self) -> None:
        """
        Shows a dialog with the time it takes to encrypt the file.
        """
        text = self.password_field.text()
        confirm_text = self.confirm_password_field.text()
        # Check if the passwords match and are not empty
        if text != confirm_text:
            self.show_error("Passwords do not match.")
            return
        if not text or not confirm_text:
            self.show_error("Password fields cannot be empty.")
            return
        # Encrypt the file and measure the time taken
        try:
            start_time = time.time()
            self.encode(password=text)
            end_time = time.time()
            elapsed = end_time - start_time
            self.show_info(
                f"File encrypted successfully!\n\nTime taken: {elapsed:.3f} seconds"
            )
        except Exception as exc:
            self.show_error(str(exc))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    app.exec()
