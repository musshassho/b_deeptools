
import nuke
import os
import json
from nukescripts import panels
import sys


if nuke.NUKE_VERSION_MAJOR < 11: # < nuke11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets
else: # > nuke11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets



class Panel(QtGuiWidgets.QComboBox):
    def __init__(self):

        super(Panel,self).__init__()
        self.defaultSize = [400,200]

        self.set_panel()


    def set_panel(self):

        self.resize(self.defaultSize[0],self.defaultSize[1])
        #self.setGeometry(300, 300, 200, 150)
        self.setWindowTitle("Deep with it")
        
        self.move(QtGui.QCursor().pos() - QtCore.QPoint(32,74))

        self.edit = QtGuiWidgets.QLineEdit("Write my name here..")
        self.button = QtGuiWidgets.QPushButton("Show Greetings")
        self.pushbutton = QtGuiWidgets.QPushButton('Quit', self)
        
        self.pushbutton.move(50,100)
        self.pushbutton.clicked.connect(self.quitApp)


        layout = QtGuiWidgets.QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        layout.addWidget(self.button)
        layout.addWidget(self.pushbutton)
        
        

        self.setLayout(layout)



if __name__ == '__main__':
    #myApp = QtGuiWidgets.QApplication(sys.argv)
    myPanel = Panel()
    myPanel.show()
    #sys.exit(app.exec_())


