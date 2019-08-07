
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


#######################################################################################################################


class Panel(QtGuiWidgets):
	def __init__(self):
		super(Panel, self).__init__()

		group1 = QgroupBox("Checkbox")
		group1_layaout = QHBoxLayaout()

		for i in range(5):
			c = Qcheckbox()
			group1_layout.addWidget(c)
		group1.setLayout(group1_layout)

		group2 = QgroupBox("Line edit")
		group2_layout = QHBoxLayaout()

		for i in range (5):
			line = QLineEdit()
			group2_layout.addWidget(line)
		group2.setLayout(group2_layout)


		master_layout = QVBoxLayout()
		master_layout.addWidget(group1)
		master_layout.addWidget(group2)
		self.setLayout(master_layout)


app = QApplication(sys.arg)
panel = Panel()
panel.show()
app.exec_() 

 
#######################################################################################################################


from PySide2.QtWidgets import QWidget,QApplication 
from PySide2.QtWidgets import QListWidget, QHBoxLayout
from PySide2.QtGui import QIcon, QColor


class Panel(QWidget):
    def __init__(self):
        super(Panel,self).__init__()

        list_widget = QListWidget()
        items = ["world","hello","dear","butterfly"]

        for item in items:
            i = QListWidgetItem(item)
            i.setToolTip("hello toolptip")
            i.setIcon(QIcon("nuke.png"))
            i.setBackground(QColor(255,175,0))
            list_widget.addItem(i)
            

        master_layout = QHBoxLayout()
        master_layout.addWidget(list_widget)
        self.setLayout(master_layout)

panel = Panel()
panel.show()    


#######################################################################################################################


  class Panel(QWidget):
  	def __init__(self):
  		super(Panel,self).__init__()

  		table = QTableWidget()

  		layout1 = QHBoxLayout() 
  		layout2 = QHBoxLayout()
  		layout3 = QHBoxLayout()

  		for i in range(5):
  			layout1.addWidget(QCheckbox())

  		for i in range(5):
  			layout1.addWidget(QPushButton())

  		for i in range(5):
  			layout1.addWidget(QLineEdit())

  		tab1 = QtGuiWidget()
  		tab2 = QtGuiWidget()
  			