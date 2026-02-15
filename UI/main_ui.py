import PySide6
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

#===============================================================================
app_name = "Qyrou-Pulse"
app_icon = "C:\\Users\\USER\\Qyrou-Pulse\\media\\image\\icon_app.png"

class MainWindow(QMainWindow):
     def __init__(self):
          super().__init__()
          self.setWindowTitle(app_name)
          self.setMinimumSize(850, 800)
          self.setWindowIcon(PySide6.QtGui.QIcon(app_icon))
          self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
          self.init_ui()

     def init_ui(self):
          central_widget = QWidget()
          self.setCentralWidget(central_widget)
          
          self.main_layout = QVBoxLayout()
          self.main_layout.setContentsMargins(15,0,15,15)
          self.main_layout.addStretch(1)
          self.prompt_box = QTextEdit()
          self.prompt_box.setPlaceholderText("Say hi to Qyrou-Pulse...") 
          self.prompt_box.setFixedHeight(150)
          self.prompt_box.setStyleSheet("""
               background-color: #f0f0f0;
               border: 1px solid #ccc;
               border-radius: 10px;
               padding: 10px;
               """)    
         

          self.main_layout.addWidget(self.prompt_box)
          central_widget.setLayout(self.main_layout)

#_______________________________________________________________________________

if __name__ == "__main__":
     app = QApplication([])
     window = MainWindow()
     window.show()
     app.exec()
