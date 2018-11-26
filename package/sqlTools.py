# -*- coding: utf-8 -*-
"""

(终于解决)sqlite动态插入问题(wordmaya)


"""

import sqlite3
#import pandas as pd
from pandas import DataFrame
import itertools


#nameDataBase
def insertTable(name,name1):
    conn = sqlite3.connect('majia.db')
    cursor = conn.cursor()
    #a = '难受'
    #########################有value时，不能自己拼占位符，使用?。否则一个字符串会默认拆分成多项。
    cursor.execute('insert into {} values (?)'.format(name), (name1,))
    #CREATE TABLE {} (nameList text)
    cursor.close()
    conn.commit()
    conn.close()

    #新建一个表    
def createTable(nameD):
    conn = sqlite3.connect('majia.db')
    cursor = conn.cursor()
    cursor.execute('create table {} (nameList text)'.format(nameD))
    cursor.close()
    conn.commit()
    conn.close()

    
#输入参数为带引号字符串
def buildTable(name, num=1):
    conn = sqlite3.connect('majia.db')
    cursor = conn.cursor()
    cursor.execute('create table {} (nameList text)'.format(name)) 
    cursor.execute('insert into 数据总表 values (?)', (name,))
    for i in range(1, num+1):
        nameN = name + str(i)
        cursor.execute('create table {} (url text, title text, desc text)'.format(nameN))
        cursor.execute('insert into {} values (?)'.format(name), (nameN,))
        conn.commit()
    cursor.close()
    conn.commit()
    conn.close()

#遍历namelist
def selectNameList():
    conn = sqlite3.connect('majia.db')
    #得到数据总表list
    cursor = conn.cursor()
    cursor.execute('select * from 数据总表')
    nameAll = []    
    for x in cursor.fetchall():
        nameAll = nameAll + [x[0]]
    cursor.close()
    
    #得到数据总表中，每个名称对应的list，再组合为list[list，]
    cursor = conn.cursor()
    namePart = []
    for x in nameAll:
        name = []
        cursor.execute('select * from {}'.format(x))
        for y in cursor.fetchall():
            name = name + [y[0]]
        namePart.append(name)
    cursor.close()        
    
    conn.commit()
    conn.close()
    
    return nameAll, namePart
    
#tree被点击item的表，所有内容list
def selectNameClicked(name): 
    conn = sqlite3.connect('majia.db')
    #得到数据总表list
    cursor = conn.cursor()
    cursor.execute('select * from {}'.format(name))
    nameClickedList = cursor.fetchall()
    
    cursor.close()            
    conn.commit()
    conn.close()
    
    #print(nameClickedList)
    return nameClickedList
    
def updateDoubleClickedList(name, a, b, c, oldTitle):

    conn = sqlite3.connect('majia.db')
    conn.text_factory = str
    #得到数据总表list
    cursor = conn.cursor()

    cursor.execute("""UPDATE {} SET url=?, title=?, desc=? WHERE title= ? """.format(name), (a, b, c, oldTitle))
    
    cursor.close()            
    conn.commit()
    conn.close()
    
#获取数据总表,或各分库总表的内容
def selcetNameAll(name):
    conn = sqlite3.connect('majia.db')
    #得到数据总表list
    cursor = conn.cursor()
    cursor.execute('select * from {}'.format(name))
    nameAll = []    
    for x in cursor.fetchall():
        nameAll = nameAll + [x[0]]
    cursor.close()
    return nameAll
    
    
#在当前选中表中 添加数据
def insertNameClickedList(name, a, b, c):
    conn = sqlite3.connect('majia.db')
    conn.text_factory = str
    #得到数据总表list
    cursor = conn.cursor()

    cursor.execute('insert into {} values(?,?,?)'.format(name), (a, b, c))
    
    cursor.close()            
    conn.commit()
    conn.close()
    
    
def deleteNameClickedList(name, b):
    conn = sqlite3.connect('majia.db')
    conn.text_factory = str
    #得到数据总表list
    cursor = conn.cursor()

    cursor.execute('delete from {} where title= (?)'.format(name), (b,))
    
    cursor.close()            
    conn.commit()
    conn.close()
    
    
    
'''    
#生成excel 
def produceFinalData1():
    conn = sqlite3.connect('majia.db')    
    
        
    cursor = conn.cursor()
    cursor.execute('select * from duorou1')
    dataBase1 = cursor.fetchall()
    cursor.close()    
    dataComb1 = list(itertools.combinations(dataBase1, 3))
    #print(dataComb1)
    
    cursor = conn.cursor()
    cursor.execute('select * from duorou2')
    dataBase2 = cursor.fetchall()
    cursor.close()    
    dataComb2 = list(itertools.combinations(dataBase2, 2))
    
    cursor = conn.cursor()
    cursor.execute('select * from duorou3')
    dataBase3 = cursor.fetchall()
    cursor.close()   
    dataComb3 = list(itertools.combinations(dataBase3, 2))
    
    cursor = conn.cursor()
    cursor.execute('select * from duorou4')
    dataBase4 = cursor.fetchall()
    cursor.close()    
    dataComb4 = list(itertools.combinations(dataBase4, 1))
    #print(dataComb1)
    
    
    dataAll = []
    dataCombAll = list(itertools.product(dataComb1, dataComb2, dataComb3, dataComb4))
    #print(dataCombAll[0])
    for data in dataCombAll:
        dataTuple = data[0] + data[1] + data[2] + data[3]
        #print(dataTuple[0])
        dataAll = dataAll + list(dataTuple)+ [('','','')]
    dataFinal = pd.DataFrame(dataAll)
    dataFinal.to_excel('majia20.xls', header=False, index=False)
'''    
    
    
    
def produceFinalData(nameSelectDateBase, ratio, nameFileDataBase):
    conn = sqlite3.connect('majia.db')
    
    namelist = selcetNameAll(nameSelectDateBase)
    
    returnList = []
    for x in range(len(ratio)):
        num = int(ratio[x])
        name = namelist[x]
           
        cursor = conn.cursor()
        cursor.execute('select * from {}'.format(name))
        dataBaseX = cursor.fetchall()
        cursor.close()    
        dataCombX = list(itertools.combinations(dataBaseX, num))
        returnList.append(dataCombX)    
    
    dataAll = []
    dataCombAll = list(itertools.product(*returnList))
    for data in dataCombAll:
        dataTuple = ()
        for i in range(len(data)):
            dataTuple += data[i]

        dataAll = dataAll + list(dataTuple)+ [('','','')]
    dataFinal = DataFrame(dataAll)
    #dataFinal.to_excel('{}.xls'.format(nameFileDataBase), header=False, index=False)
    # 输出excel 保存到桌面
	 dataFinal.to_excel(os.path.join(os.path.expanduser("~"), 'Desktop') + '\\{}.xls'.format(nameFileDataBase), header=False, index=False)
    #dataFinal.to_excel(os.path.join(os.path.dirname(__file__) + '//output//{}.xls'.format(nameFileDataBase), header=False, index=False)
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    