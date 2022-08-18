from PySide6 import QtWidgets, QtGui, QtCore
import sys, os


if getattr(sys, 'frozen', False):
    # frozen
    program_location = os.path.dirname(sys.executable)
else:
    # unfrozen
    program_location = os.path.dirname(os.path.realpath(__file__))
    
    
class ProjectManager(QtWidgets.QWidget):
    def __init__(self):
        super(ProjectManager, self).__init__()
        self.windowWidth = 800
        self.windowHeight = 900
        self.initAtt()
        self.initUI()
        self.center()
        self.show()
    
    
    def center(self):
        window = self.window()
        window.setGeometry(
            QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight,
            QtCore.Qt.AlignCenter,
            window.size(),
            QtGui.QGuiApplication.primaryScreen().availableGeometry(),
        ),
    )
        
    def initAtt(self):
        self.setGeometry(100, 50, self.windowWidth, self.windowHeight)
        title = "Project Manager"
        # self.setWindowIcon(self.ico)
        self.setWindowTitle(title)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        
    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)
        self.setLayout(layout)
        
        
# execute the program
def main():
    print(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    manager = ProjectManager()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()