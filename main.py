import sys
import os
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class MetadataEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.exiftool_path = self.get_exiftool_path()  # Correctly get path based on execution environment
    
    def get_exiftool_path(self):
        """Finds the correct path to exiftool.exe based on script or .exe execution."""
        if getattr(sys, 'frozen', False):  # Running as a PyInstaller .exe
            base_path = sys._MEIPASS  # PyInstaller extracts files here
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))  # Running as script
        
        return os.path.join(base_path, "Exiftool", "exiftool.exe")

    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Select a file to view or remove metadata:")
        self.label.setFont(QFont("Arial", 12))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        btn_layout = QHBoxLayout()
        self.btn_select = QPushButton("Select File")
        self.btn_select.setFont(QFont("Arial", 10))
        self.btn_select.clicked.connect(self.load_file)
        btn_layout.addWidget(self.btn_select)
        
        self.btn_remove_metadata = QPushButton("Remove Metadata")
        self.btn_remove_metadata.setFont(QFont("Arial", 10))
        self.btn_remove_metadata.clicked.connect(self.remove_metadata)
        btn_layout.addWidget(self.btn_remove_metadata)
        
        layout.addLayout(btn_layout)
        
        self.metadata_display = QTextEdit()
        self.metadata_display.setReadOnly(True)
        self.metadata_display.setFont(QFont("Courier", 10))
        layout.addWidget(self.metadata_display)
        
        self.setLayout(layout)
        self.setWindowTitle("Metadata Editor")
        self.resize(600, 450)
    
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        if file_path:
            self.display_metadata(file_path)
            self.current_file = file_path
    
    def display_metadata(self, file_path):
        try:
            print(f"Using ExifTool from: {self.exiftool_path}")  # Debugging
            result = subprocess.run([self.exiftool_path, file_path], capture_output=True, text=True)
            metadata_text = result.stdout if result.stdout else "No metadata found."
        except Exception as e:
            metadata_text = f"Error reading metadata: {e}"
        
        self.metadata_display.setText(metadata_text)
    
    def remove_metadata(self):
        if hasattr(self, 'current_file'):
            file_path = self.current_file
            confirm = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to remove metadata?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    subprocess.run([self.exiftool_path, "-all=", "-overwrite_original", file_path])
                    self.metadata_display.setText("Metadata removed successfully.")
                except Exception as e:
                    self.metadata_display.setText(f"Error removing metadata: {e}")
        else:
            QMessageBox.warning(self, "No File Selected", "Please select a file first.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MetadataEditor()
    window.show()
    sys.exit(app.exec())
