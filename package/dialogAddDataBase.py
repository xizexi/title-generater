# -*- coding: utf-8 -*-
"""
Created on Fri May 12 00:58:37 2017

@author: C
"""
import sys
from PyQt5.QtGui import *  
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
import package.sqlTools 


class Example(QDialog):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):


        url = QLabel('添加库名(必填)：')
        title = QLabel('子库个数(必填)：')

        self.nameEdit = QLineEdit()
        self.numEdit = QLineEdit()

        
        self.okButton = QPushButton('确认')
        self.noButton = QPushButton('取消')
        self.okButton.clicked.connect(self.save)
        self.noButton.clicked.connect(self.noSave)
        
        hbox = QHBoxLayout()  
        hbox.addStretch(1)  
        hbox.addWidget(self.okButton)
        hbox.addStretch(1) 
        hbox.addWidget(self.noButton)
        hbox.addStretch(1) 

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(url, 1, 0)
        grid.addWidget(self.nameEdit, 1, 1)
        grid.addWidget(title, 2, 0)
        grid.addWidget(self.numEdit, 2, 1)

     
        vbox = QVBoxLayout()   
        vbox.addLayout(grid)
        vbox.addLayout(hbox)
               
        self.setLayout(vbox)
        
        self.resize(600,400)
        self.setWindowTitle('添加数据库')   
        
        
    
    def save(self):
        package.sqlTools.buildTable(self.nameEdit.text(), int(self.numEdit.text()))
        self.accept()
    
    
    def noSave(self, event):
        reply = QMessageBox.question(self, ' 信息', ' 你确定要不保存退出吗？ ', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.accept()
        else:
            event.ignore()
     
    def closeEvent(self, event):
        #重新定义 colseEvent
        reply = QMessageBox.question(self, ' 信息', ' 你确定要不保存退出吗？ ', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
   
        
     
if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
