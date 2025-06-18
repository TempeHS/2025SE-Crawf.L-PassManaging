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
import sys
import time
import os

import pyfiles.arg2id as arg2id
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
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, filename)


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.hasher = arg2id.Argon2IDHasher()
        self.encryptor = encrypt.AESFileEncryptor()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("Simple App")

        # Create layout
        layout = QVBoxLayout()

        # Add a label
        self.label = QLabel("Enter some text:")
        layout.addWidget(self.label)

        # Add an input field
        self.input_field = QLineEdit()
        self.input_field.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.input_field.setTextMargins(
            0, 0, 0, 0
        )  # Optional: Adjust margins if needed
        layout.addWidget(self.input_field)

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
            self.show_error("Password cannot be empty.")
            return
        input_path = resource_path("help.txt")
        encrypted_path = user_data_path("help.txt.enc")
        # decrypted_path = user_data_path("help_de.txt")
        try:
            self.encryptor.encrypt_file(
                password=password,
                input_path=input_path,
                output_path=encrypted_path,
            )
            # self.encryptor.decrypt_file(
            #     password=password,
            #     input_path=encrypted_path,
            #     output_path=decrypted_path,
            # )
            QMessageBox.information(
                self, "Success", "Encryption and decryption completed successfully."
            )
        except Exception as exc:
            self.show_error(str(exc))

    def show_error(self, message) -> None:
        """Display errors in a message box.
        Args:
            message (str): The error message to display.
        """
        QMessageBox.critical(self, "Error", message)

    def show_dialog(self) -> None:
        """
        Show a dialog with the submitted text and its hashed version (using Argon2ID).
        """
        text = self.input_field.text()
        self.raw_password = text
        self.encode(password=text)
        try:
            start_time = time.time()
            hashed = self.hasher.hash(text)
            end_time = time.time()
            elapsed = end_time - start_time
            QMessageBox.information(
                self,
                "Submitted",
                f"Submitted text: {text}\n\nHashed password: {hashed}\n\nHashing took {elapsed:.3f} seconds",
            )
        except Exception as exc:
            self.show_error(str(exc))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    app.exec()
