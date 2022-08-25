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
        self.windowHeight = 450
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
        self.menubar = QtWidgets.QMenuBar(self)
        self.toolbar = QtWidgets.QToolBar()
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setSizeGripEnabled(False)
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setMenuBar(self.menubar)
        mainLayout.addWidget(self.toolbar)

        #self.createMenuActions()
        #searchLayout = QtWidgets.QHBoxLayout()
        self.line_search = QtWidgets.QLineEdit(self)
        self.line_search.setPlaceholderText("Search here")
        self.button_search = QtWidgets.QPushButton("Search")
        
        # self.label_doc_count = QtWidgets.QLabel("DOC Count:")
        # self.label_open_docs = QtWidgets.QLabel("Open - ")
        # self.label_wait_docs = QtWidgets.QLabel("Waiting - ")
        # self.label_complete_docs = QtWidgets.QLabel("Completed - ")
        self.dropdown_type = QtWidgets.QComboBox(self)
        self.dropdown_type.setFixedWidth(100)
        self.dropdown_type.addItems(["Ongoing","Canceled","Completed"])
        self.button_refresh = QtWidgets.QPushButton("Refresh")
        
        self.button_open = QtWidgets.QPushButton("Open")
        self.button_open.setEnabled(False)
        self.button_add = QtWidgets.QPushButton("New Project")

        # self.statusbar.addPermanentWidget(self.label_doc_count)
        # self.statusbar.addPermanentWidget(self.label_open_docs)
        # self.statusbar.addPermanentWidget(self.label_complete_docs)
        # self.statusbar.addPermanentWidget(self.label_wait_docs)

        self.toolbar.addWidget(self.line_search)
        self.toolbar.addWidget(self.button_search)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.button_add)
        self.toolbar.addWidget(self.button_open)
        self.toolbar.addWidget(self.button_refresh)
        self.toolbar.addWidget(self.dropdown_type)
        
        self.docs = QtWidgets.QListView()
        self.docs.setStyleSheet("QListView{background-color:#f0f0f0}")
        self.docs.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.docs.setResizeMode(QtWidgets.QListView.Adjust)
        self.docs.setItemDelegate(ProjectDelegate())
        #self.docs.doubleClicked.connect(self.openDoc)
        
        
        self.model = ProjectModel()
        self.docs.setModel(self.model)
        
        #self.docs.selectionModel().selectionChanged.connect(self.onRowSelect)
        
        mainLayout.addWidget(self.docs)
        
        #mainLayout.addWidget(self.statusbar)
        
        #self.dropdown_type.currentIndexChanged.connect(self.repopulateTable)
        
        #self.docs.verticalScrollBar().valueChanged.connect(self.loadMoreTable)
        
        mainLayout.setMenuBar(self.menubar)
        
        #self.repopulateTable()
        
class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
        
PADDING = QtCore.QMargins(15, 2, 15, 2)

class ProjectDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()
        
        doc_id, title, doc_type, status, last_modified, stage, waiting_on, elapsed_days, comment_count = index.model().data(index, QtCore.Qt.DisplayRole)
        
        lineMarkedPen = QtGui.QPen(QtGui.QColor("#f0f0f0"),1,QtCore.Qt.SolidLine)
        
        r = option.rect.marginsRemoved(PADDING)
        painter.setPen(QtCore.Qt.NoPen)
        if option.state & QtWidgets.QStyle.State_Selected:
            color = QtGui.QColor("#A0C4FF")
        elif option.state & QtWidgets.QStyle.State_MouseOver:
            color = QtGui.QColor("#BDB2FF")
        else:
            color = QtGui.QColor("#FFFFFC")
        painter.setBrush(color)
        painter.drawRoundedRect(r, 5, 5)
        
        
        if status !="Completed":
            rect = QtCore.QRect(r.topRight()+QtCore.QPoint(-150,2),QtCore.QSize(125,20))
            if status =="Out For Approval":
                color = QtGui.QColor("#CAFFBF")
            elif status =="Rejected":
                color = QtGui.QColor("#FFADAD")
            else:
                color = QtGui.QColor("#FDFFB6")
            painter.setBrush(color)
            painter.drawRoundedRect(rect, 5, 5)
            font = painter.font()
            font.setPointSize(8)
            painter.setFont(font)
            painter.setPen(QtCore.Qt.black)
            painter.drawText(r.topRight()+QtCore.QPoint(-145,16),status)
        
        painter.setPen(lineMarkedPen)
        painter.drawLine(r.topLeft()+QtCore.QPoint(0,25),r.topRight()+QtCore.QPoint(0,25))

        
        text_offsetx1 = 15
        text_offsetx2 = r.width()/2+10
        
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QtCore.Qt.black)
        painter.drawText(r.topLeft()+QtCore.QPoint(text_offsetx1,20),doc_id)
        if len(title)>75:
            title = title[:75] + "..."
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(r.topLeft()+QtCore.QPoint(175,20),title)
        font.setPointSize(10)
        font.setBold(False)
        painter.setFont(font)
        #ecn_id, title, ecn_type, status, last_modified, stage, waiting_on, elapsed_days, comment_count
        painter.drawText(r.topLeft()+QtCore.QPoint(text_offsetx1,45),f"Type: {doc_type}")
        painter.drawText(r.topLeft()+QtCore.QPoint(175,45),f"Last Modified: {last_modified}")
        painter.drawText(r.topLeft()+QtCore.QPoint(text_offsetx1+375,45),f"Stage: {stage}")
        painter.drawText(r.topLeft()+QtCore.QPoint(text_offsetx1+450,45),f"Elapsed: {elapsed_days}")
        painter.drawText(r.topLeft()+QtCore.QPoint(text_offsetx1+550,45),f"💬: {comment_count}")
        if len(waiting_on)>25:
            waiting_on = waiting_on[:25] + "..."
        painter.drawText(r.topLeft()+QtCore.QPoint(text_offsetx1+610,45),f"Waiting On: {waiting_on}")
        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(option.rect.width()-50,55)

class ProjectModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(ProjectModel, self).__init__(*args, **kwargs)
        self.docs = []

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.docs[index.row()]

    def setData(self, index, role, value):
        self._size[index.row()]
        
    def rowCount(self, index):
        return len(self.docs)
    
    def removeRow(self, row):
        del self.docs[row]
        self.layoutChanged.emit()
        
    def get_doc_data(self,row):
        return self.docs[row]

    def clear_docs(self):
        self.docs = []
    
    def add_doc(self, doc_id, title, doc_type, status, last_modified, stage, waiting_on, elapsed_days, comment_count):
        # Access the list via the model.
        self.docs.append((doc_id, title, doc_type, status, last_modified, stage, waiting_on, elapsed_days, comment_count))
        # Trigger refresh.
        self.layoutChanged.emit()
        
        
# execute the program
def main():
    print(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    manager = ProjectManager()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()