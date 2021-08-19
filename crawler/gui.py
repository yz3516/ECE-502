'''from tkinter import *

def gui():
	global url_input,text
	#创建空白窗口,作为主载体
	root = Tk()
	root.title('test')
	#窗口的大小，后面的加号是窗口在整个屏幕的位置
	root.geometry('550x400+398+279')
	#标签控件，窗口中放置文本组件
	Label(root,text='Input the Website Address :',font=("arial",20),fg='black').grid()
	#定位 pack包 place位置 grid是网格式的布局
	
	#Entry是可输入文本框
	url_input=Entry(root,font=("arial",15))
	url_input.grid(row=0,column=1)
	#列表控件
	text=Listbox(root,font=('arial',15),width=45,height=10)
	#columnspan 组件所跨越的列数
	text.grid(row=1,columnspan=2)
	#设置按钮 sticky对齐方式，N S W E
	button =Button(root,text='Download',font=("arial",15)).grid(row=2,column=0,sticky=W)
	button =Button(root,text='Exit',font=("arial",15),command=root.quit).grid(row=2,column=1,sticky=E)
	#使得窗口一直存在
	mainloop()
