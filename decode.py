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
    Args:
        relative_path (str): The relative path to the resource.
    Returns:
        str: The absolute path to the resource.
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
    directory. If it does not exist, and returns the full path to the specified filename.

    ### For Windows:

        "C:\\Users\\<username>\\.simple_app_data\\<filename>"

    ### For Linux/Mac:

        "/home/<username>/.simple_app_data/<filename>"

    Args:
        filename (str): The name of the file to be stored in the user data directory.
    Returns:
        str: The full path to the specified file in the user data directory.
    """
    home_dir = os.path.expanduser("~")
    app_dir = os.path.join(home_dir, ".simple_app_data")
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, filename)


class DecodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.file_encryptor = encrypt.AESFileEncryptor(self)
        self.message_box = message_utils.MessageBox(self)
        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialise the user interface for the decoder application.
        """
        self.setWindowTitle("File Decryptor")

        # Create layout
        layout = QVBoxLayout()

        # label
        self.label = QLabel("Enter the password to decrypt the file:")
        layout.addWidget(self.label)

        # password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.password_input.setTextMargins(0, 0, 0, 0)
        self.password_input.setPlaceholderText("Enter password for decryption:")
        layout.addWidget(self.password_input)

        # submit button
        self.submit_button = QPushButton("Decrypt File")
        self.submit_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.submit_button.clicked.connect(self.on_submit)
        layout.addWidget(self.submit_button)

    def on_submit(self) -> None:
        """
        Handle the submit button click event.

        This method retrieves the password from the input field, validates it,
        and attempts to decrypt the file. It also measures the time taken for decryption
        and displays appropriate messages based on the outcome.
        """
        password = self.password_input.text()
        if not password:
            self.message_box.show_warning("Password cannot be empty.")
            return
        try:
            start_time = time.perf_counter()
            result = self.decode(password)
            end_time = time.perf_counter()
            if result is None:
                elapsed_time = end_time - start_time
                if elapsed_time < 1:
                    self.message_box.show_info(
                        f"Decryption completed in {elapsed_time * 1000:.0f} milliseconds."
                    )
                else:
                    self.message_box.show_info(
                        f"Decryption completed in {elapsed_time:.3f} seconds."
                    )
        except FileNotFoundError:
            self.message_box.show_error(
                rf"The encrypted file does not exist. The file should exist at {user_data_path(result)}."
            )
            return
        except Exception as e:
            self.message_box.show_error(f"An error occurred: {str(e)}")
            return

    def decode(self, password: str) -> None:
        """Decrypt a file using the provided password.
        Args:
            password (str): The password to use for decryption.
        """
        input_path = user_data_path("passes.db.enc")
        decrypted_path = user_data_path("passes_de.db")
        try:
            self.file_encryptor.decrypt_file(
                password=password,
                input_path=input_path,
                output_path=decrypted_path,
            )
            return None
        except Exception as e:
            self.message_box.show_error(f"Decryption failed: {str(e)}")
            return input_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DecodeApp()
    window.show()
    app.exec()
