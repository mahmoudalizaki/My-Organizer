import sys
import os
import shutil
import winreg
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QMessageBox, QVBoxLayout, QWidget, QHBoxLayout, QCheckBox
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QPixmap, QIcon
from qt_material import apply_stylesheet
class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('My Organizer')
        self.setGeometry(600, 300, 600, 400)
        self.setFixedSize(600, 400)
        self.setWindowIcon(QIcon('logo.png'))
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                border: 2px solid #4CAF50;
            }
        """)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout()
        # Logo
        self.logoLabel = QLabel(self)
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap('logo.png')
        self.logoLabel.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(self.logoLabel)
        # Title label
        self.label = QLabel('Select a directory to organize files by their categories'.upper(), self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        # Checkbox to enable/disable creating subfolders
        self.createSubfoldersCheckBox = QCheckBox('Create subfolders for file types', self)
        self.createSubfoldersCheckBox.setChecked(True)
        layout.addWidget(self.createSubfoldersCheckBox, alignment=Qt.AlignmentFlag.AlignCenter)
        # Buttons layout
        buttonLayout = QHBoxLayout()
        self.buttonSelect = QPushButton('Select Directory', self)
        self.buttonSelect.clicked.connect(self.selectDirectory)
        buttonLayout.addWidget(self.buttonSelect, alignment=Qt.AlignmentFlag.AlignCenter)
        self.buttonOrganize = QPushButton('Organize Files', self)
        self.buttonOrganize.clicked.connect(self.organizeFiles)
        self.buttonOrganize.setEnabled(False)
        buttonLayout.addWidget(self.buttonOrganize, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(buttonLayout)
        # Selected directory label
        self.selectedDirLabel = QLabel('', self)
        self.selectedDirLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.selectedDirLabel)
        # Footer
        self.footer = QLabel('© 2024 Made with ♥ by Mahmoud A.Zaki. All rights reserved.\n♥ Free Palestine ♥', self)
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.footer)
        centralWidget.setLayout(layout)
        self.show()
    def selectDirectory(self):
        self.selectedDir = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if self.selectedDir:
            self.selectedDirLabel.setText(f'Selected Directory: {self.selectedDir}')
            self.buttonOrganize.setEnabled(True)
            self.animateButton(self.buttonOrganize)
                
    def organizeFiles(self):
        if not self.selectedDir:
            QMessageBox.warning(self, 'Warning', 'No directory selected!')
            return
        print(f"Selected Directory: {self.selectedDir}")
        # Define file categories and their extensions
        file_categories = {
            'Documents': [
                'pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odp', 'csv', 'rtf', 'tex', 'log'
            ],
            'Images': [
                'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg', 'webp', 'ico', 'psd', 'heic', 'raw', 'nef', 'cr2', 'orf'
            ],
            'Music': [
                'mp3', 'wav', 'aac', 'flac', 'ogg', 'm4a', 'wma', 'aiff', 'alac', 'pcm'
            ],
            'Videos': [
                'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm', 'mpeg', 'mpg', 'm4v', '3gp', '3g2'
            ],
            'Compressed': [
                'zip', 'rar', 'tar', 'gz', '7z', 'bz2', 'xz', 'iso', 'cab', 'tgz'
            ],
            'Executables': [
                'exe', 'msi', 'bat', 'cmd', 'com', 'ps1', 'vbs', 'jar', 'scr', 'wsf', 'lnk', 'gadget', 'inf1', 'msc', 'cpl', 'dll', 'ocx', 'sys', 'drv', 'vb', 'vbe', 'pif', 'scf', 'shs', 'hta'
            ],
            'Android': ['apk'],
            'Others': []
        }
        # Reverse the dictionary to map extensions to categories
        ext_to_category = {ext: category for category, exts in file_categories.items() for ext in exts}
        for root, _, files in os.walk(self.selectedDir):
            for file in files:
                ext = file.split('.')[-1].lower()
                category = ext_to_category.get(ext, 'Others')
                if self.createSubfoldersCheckBox.isChecked():
                    # Create the parent folder based on the file category, not the extension category
                    parent_folder = os.path.join(self.selectedDir, category)
                    folder_path = os.path.join(parent_folder, f"{ext.upper()}")  # Use the extension as the folder name
                    os.makedirs(folder_path, exist_ok=True)
                    shutil.move(os.path.join(root, file), os.path.join(folder_path, file))
                    print(f"Moved file '{file}' to '{os.path.join(folder_path, file)}'")
                else:
                    # Create the parent folder based on the category
                    parent_folder = os.path.join(self.selectedDir, category)
                    os.makedirs(parent_folder, exist_ok=True)
                    shutil.move(os.path.join(root, file), os.path.join(parent_folder, file))
                    print(f"Moved file '{file}' to '{os.path.join(parent_folder, file)}'")
        QMessageBox.information(self, 'Success', 'Files organized successfully!')
    def animateButton(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(QRect(button.x(), button.y() - 20, button.width(), button.height()))
        animation.setEndValue(QRect(button.x(), button.y(), button.width(), button.height()))
        animation.start()
def is_windows_dark_mode():
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        registry_key = winreg.OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        value, regtype = winreg.QueryValueEx(registry_key, 'AppsUseLightTheme')
        return value == 0
    except Exception as e:
        print(f"Error checking Windows theme: {e}")
        return False
if __name__ == '__main__':
    app = QApplication(sys.argv)
    if is_windows_dark_mode():
        # Apply the complete dark theme to your Qt App.
        apply_stylesheet(app, theme= 'light_blue.xml')
    else:
        apply_stylesheet(app, theme= 'dark_lightgreen.xml')
    ex = FileOrganizer()
    sys.exit(app.exec())
