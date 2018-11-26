# -*- coding: utf-8 -*-
"""
双击  数据库内容更新对话框

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


        url = QLabel('链接：')
        title = QLabel('题目：')
        desc = QLabel('描述：')
        self.urlEdit = QLineEdit()
        self.titleEdit = QLineEdit()
        self.descEdit = QTextEdit()
        #来自主窗体的值传递
        self.titleValue = 'a'
        self.nameClicked = 'b'
        
        self.okButton = QPushButton('确认')
        self.noButton = QPushButton('取消')
        self.okButton.clicked.connect(self.save)
        self.noButton.clicked.connect(self.noSave)
        
        hbox = QHBoxLayout()  
        hbox.addStretch(1)  
        hbox.addWidget(self.okButton)  
        hbox.addWidget(self.noButton)  

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(url, 1, 0)
        grid.addWidget(self.urlEdit, 1, 1)
        grid.addWidget(title, 2, 0)
        grid.addWidget(self.titleEdit, 2, 1)
        grid.addWidget(desc, 3, 0)
        grid.addWidget(self.descEdit, 3, 1, 5, 1)

     
        vbox = QVBoxLayout()   
        vbox.addLayout(grid)
        vbox.addLayout(hbox)
               
        self.setLayout(vbox)
        
        self.resize(600,400)
        self.setWindowTitle('更新数据')   
        
        
    
    def save(self):

        
        package.sqlTools.updateDoubleClickedList(self.nameClicked, self.urlEdit.text(), self.titleEdit.text(), self.descEdit.toPlainText(), self.titleValue)
        #sqlTools.updateDoubleClickedList(self.nameClicked, self.urlEdit.text(), self.titleEdit.text(), self.descEdit.toPlainText(), self.titleValue)
        #self.accept()
        #print([self.nameClicked, self.urlEdit.text(), self.titleEdit.text(), self.descEdit.toPlainText(), self.titleValue])
        self.accept()
        #print(self.nameClicked)
 
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
