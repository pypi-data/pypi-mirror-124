import tkinter as tk

global textList
textList=locals()#自动生成变量名字典集
class biao():
    def __init__(self,maxr,maxc):
        ''':param maxr:设置总行数
           :param maxc:设置字段数量'''
        self.maxr=maxr
        self.maxc=maxc
    def auto_Create_Text(self,father,namelist=None,valueList=None):
        ''':param father:父组件的名称
           :param namelist:表格的字段名称
           :param valuelist:字段名的值'''
        name=0
        for r in range(self.maxr):
            for c in range(self.maxc):
                name+=1 #设置表格编号如text00，text01
                textList[name]=tk.Text(father,bd='1',width=8,height=1,
                                        relief='solid')
                textList[name].tag_configure('center',justify='center')
                
##                textList[name].place(relx=c/7.1,rely=r/6,relwidth=0.15,relheight=0.17)
                textList[name].grid(column=c,row=r)
                if c%2 == 0:
                    textList[name].insert(tk.END, u"")
                    textList[name].tag_add('center',1.0,'end')
                    textList[name].configure(bg='Gainsboro')
                else:
                    #设置字段值
                    textList[name].insert(tk.END, u"")
                    textList[name].tag_add('center',1.0,'end')
