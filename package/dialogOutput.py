# -*- coding: utf-8 -*-
"""
Created on Fri May 12 02:49:35 2017

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


        
        name = QLabel('选择输出类库：')
        ratio = QLabel('设置子库比例(默认)：')
        nameFile = QLabel('设置输出文件名(必填)：')

        
        
        self.nameEdit = QComboBox()
        for x in package.sqlTools.selcetNameAll('数据总表'):
            self.nameEdit.addItem(x)
        
        self.ratioEdit = QLineEdit()
        self.ratioEdit.setText('3221')
        
        self.nameFileEdit = QLineEdit()
        


        


        
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
        grid.addWidget(name, 1, 0)
        grid.addWidget(self.nameEdit, 1, 1)
        grid.addWidget(ratio, 2, 0)
        grid.addWidget(self.ratioEdit, 2, 1)
        grid.addWidget(nameFile, 3, 0)
        grid.addWidget(self.nameFileEdit, 3, 1)

     
        vbox = QVBoxLayout()   
        vbox.addLayout(grid)
        vbox.addLayout(hbox)
               
        self.setLayout(vbox)
        
        self.resize(600,400)
        self.setWindowTitle('输出排列组合') 

        
        
    
    def save(self):
        #sqlTools.buildTable(self.nameEdit.text(), int(self.numEdit.text()))
        #print(self.nameEdit.currentText(), self.ratioEdit.text(), self.nameFileEdit.text())
        package.sqlTools.produceFinalData(self.nameEdit.currentText(), self.ratioEdit.text(), self.nameFileEdit.text())
        #sqlTools.produceFinalData()
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
