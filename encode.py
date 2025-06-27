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
import sqlite3 as sql
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
    """
    home_dir = os.path.expanduser("~")
    app_dir = os.path.join(home_dir, ".simple_app_data")
    os.makedirs(app_dir, exist_ok=True)
    # Hide the folder and file on Windows
    if os.name == "nt":
        import ctypes

        FILE_ATTRIBUTE_HIDDEN = 0x02
        try:
            ctypes.windll.kernel32.SetFileAttributesW(app_dir, FILE_ATTRIBUTE_HIDDEN)
            ctypes.windll.kernel32.SetFileAttributesW(
                os.path.join(app_dir, filename), FILE_ATTRIBUTE_HIDDEN
            )
        except Exception:
            pass  # Ignore if fails (e.g., file doesn't exist yet)
    return os.path.join(app_dir, filename)


class EncodeApp(QWidget):
    """
    A simple application that allows users to encrypt a file with a password.
    This application provides a user interface for entering a password,
    confirming it, and encrypting a file using the AES encryption algorithm.
    The encrypted file is saved in the user's home directory under a hidden
    directory named ".simple_app_data". The application also provides feedback
    to the user through message boxes for successful encryption, warnings, and errors.
    """

    def __init__(self):
        super().__init__()
        self.fileencryptor = encrypt.AESFileEncryptor(self)
        self.message_box = message_utils.MessageBox(self)
        self.init_ui()

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

    def encode(self, password: str) -> None:
        """Encrypt a file using the provided password.
        Args:
            password (str): The password to use for encryption.
        """
        if not password:
            self.message_box.show_warning("Password cannot be empty.")
            return
        if not os.path.exists(resource_path("template.db")):
            # create a template database if it does not exist
            conn = sql.connect(resource_path("template.db"))
            cur = conn.cursor()

            # Create a SQLite3 database the structure `name,url,username,password,note`
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    note TEXT
                )
                """
            )
            conn.commit()
            conn.close()

        input_path = resource_path("template.db")
        encrypted_path = user_data_path("passes.db.enc")
        # decrypted_path = user_data_path("passes_de.db")
        try:
            self.fileencryptor.encrypt_file(
                password=password,
                input_path=input_path,
                output_path=encrypted_path,
            )

        except Exception as exc:
            self.message_box.show_error(f"Encryption failed: {str(exc)}")
            return

    def show_dialog(self) -> None:
        """
        Shows a dialog with the time it takes to encrypt the file.
        """
        text = self.password_field.text()
        confirm_text = self.confirm_password_field.text()
        # Check if the passwords match and are not empty
        if text != confirm_text:
            self.message_box.show_warning("Passwords do not match.")
            return
        if not text or not confirm_text:
            self.message_box.show_warning("Password fields cannot be empty.")
            return
        # Encrypt the file and measure the time taken
        try:
            start_time = time.perf_counter()
            self.encode(password=text)
            end_time = time.perf_counter()
            elapsed = end_time - start_time
            if elapsed < 1:
                self.message_box.show_info(
                    f"File encrypted successfully! Time taken: {elapsed * 1000:.0f} milliseconds"
                )
            else:
                self.message_box.show_info(
                    f"File encrypted successfully! Time taken: {elapsed:.3f} seconds"
                )
        except Exception as exc:
            self.message_box.show_error(str(exc))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EncodeApp()
    window.show()
    app.exec()
