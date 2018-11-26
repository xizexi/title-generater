# -*- coding: utf-8 -*-
"""


菜单栏逻辑实现
更新原则：操作对应更新数据库，重新读


"""

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import package.sqlTools
import package.dialogAdd
import package.dialogAddDataBase
import package.dialogOutput
import package.dialogInsert

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.resize(800,600)
        self.setWindowTitle('小马奔腾 1.0')
        #self.setWindowIcon(QIcon(’icons/myapp.ico’))
        #菜单栏
        menu_edit = self.menuBar().addMenu('编辑')
        act_add = menu_edit.addAction('添加库')
        act_add.triggered.connect(self.addDataBase)
        
        menu_output = self.menuBar().addMenu('输出')
        act_output = menu_output.addAction('输出 库组合 到Excel')
        act_output.triggered.connect(self.output)
        
        
        
        #数据初始化,常年维持两个list
        nameAll, namePart = package.sqlTools.selectNameList()
        self.nameDic = dict(zip(nameAll, namePart))

        #self.nameClicked = 'duorou1'
        #self.nameClickedList = sqlTools.selectNameClicked(self.nameClicked)
        self.nameClicked = ''
        self.nameClickedList = []
        self.clickedRow = 10
        
        
        
        
        
        
        #主界面布局
        self.homeWidget = QWidget()
        self.setCentralWidget(self.homeWidget)        
        self.hbox = QHBoxLayout()
        
           

            
        #左侧界面布局
        self.tree = QTreeWidget()
        #属性设置
        self.tree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tree.setHeaderLabels(['当前库'])
        #载入更新数据
        self.changeTreeUI()
        self.tree.expandAll()
        self.tree.itemClicked.connect(self.treeClickedEvent)   
        self.hbox.addWidget(self.tree, 1)
        
        
        
        #右侧界面布局         
        self.table = QTableWidget() 
        #表格属性设置
        self.table.horizontalHeader().setSectionResizeMode(1)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)        
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['链接','题目','描述'])

        
         # 右键菜单，如果不设为CustomContextMenu,无法使用customContextMenuRequested
        self.table.setContextMenuPolicy(Qt.CustomContextMenu) 
        self.table.customContextMenuRequested.connect(self.showRightMenu)
        
                
        #载入更新数据
        self.changeTableUI()
        self.table.itemDoubleClicked.connect(self.tableDoubleClickedEvent)
        
        
        
        self.table.itemPressed.connect(self.tableClickedEvent)
        self.hbox.addWidget(self.table, 4)
        
        
        
        self.homeWidget.setLayout(self.hbox)
        self.statusBar().showMessage(' 程序已就绪...')
        self.show()



        
        
    def changeTreeUI(self):
        self.tree.clear()
        #self.table.clearContents()
        
        
        nameAll, namePart = package.sqlTools.selectNameList()
        self.nameDic = dict(zip(nameAll, namePart))
        #self.table.clearContents()
        for v,k in self.nameDic.items():
            root= QTreeWidgetItem(self.tree)
            root.setText(0, v)
            for x in k:
                child = QTreeWidgetItem(root)
                child.setText(0, x)
            self.tree.addTopLevelItem(root)
        
        self.tree.expandAll()

        
        

    def changeTableUI(self):

        self.table.clearContents()
        
        if not self.nameClicked == '':
            self.nameClickedList = package.sqlTools.selectNameClicked(self.nameClicked)
        else:
            self.nameClickedList = []
        self.table.setRowCount(len(self.nameClickedList))    

        if self.nameClicked not in self.nameDic.keys():
        
            row = 0
            for x in self.nameClickedList:
                for i in range(3):
                    newItem = QTableWidgetItem("{}".format(x[i]))
                    self.table.setItem(row, i, newItem)
                row = row + 1

        

            
            
        
    #终于终于终于实现了动态获取点击内容
    def treeClickedEvent(self, item, column):

        self.nameClicked = item.text(column)

        self.changeTableUI()
              
        #print(self.nameClicked)
        


    #动态获取双击行号    
    def tableDoubleClickedEvent(self, item):
        self.clickedRow = item.row()
        self.list = self.nameClickedList[self.clickedRow]
        #print(list)
        #dialog所需值传递
        dialog = dialogAdd.Example()

        dialog.urlEdit.setText(self.list[0])
        dialog.titleEdit.setText(self.list[1])
        dialog.descEdit.setText(self.list[2])
        dialog.titleValue = self.list[1] #保存更新前的键值，选取title
        dialog.nameClicked = self.nameClicked
        
        #dialog.show()
        #dialog.exec_()                
        value = dialog.exec_()
        if value:
            self.changeTableUI()
    #获取单击行号        
    def tableClickedEvent(self, item):
        self.clickedRow = item.row()
        
        
    def addDataBase(self):
        
        dialog = dialogAddDataBase.Example()

        #dialog.show()
        #dialog.exec_()
        value = dialog.exec_()
        if value:
            self.changeTreeUI()
            self.table.clearContents()

    

    def output(self):
        
        dialog = dialogOutput.Example()
        value = dialog.exec_()
        if value:
            self.statusBar().showMessage('文件已成功输出 在应用根目录下...')

			
    def showRightMenu(self, pos):  # 创建右键菜单
        self.table.contextMenu = QMenu(self)
        self.actionAdd = self.table.contextMenu.addAction('添加 数据到当前数据表')
        self.actionDelete = self.table.contextMenu.addAction('删除 当前选中数据')
        self.table.contextMenu.popup(QCursor.pos())  # 2菜单显示的位置
        self.actionAdd.triggered.connect(self.actionHandlerAdd)
        self.actionDelete.triggered.connect(self.actionHandlerDelete)
        # self.view.contextMenu.move(self.pos())  # 3
        self.table.contextMenu.show()
        
        
    def actionHandlerAdd(self):
        #print(self.nameClicked)
        
        dialog = dialogInsert.Example()
        dialog.nameClicked = self.nameClicked
        
        value = dialog.exec_()
        if value:
            self.changeTableUI()
    
    def actionHandlerDelete(self):

        title = self.nameClickedList[self.clickedRow][1]
        #print(title)
        package.sqlTools.deleteNameClickedList(self.nameClicked, title)
        self.changeTableUI()
            
            
            
            
            
            
myapp = QApplication(sys.argv)
myapp.aboutToQuit.connect(myapp.deleteLater)
mainwindow = MainWindow()
sys.exit(myapp.exec_())