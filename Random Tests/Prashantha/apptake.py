import webbrowser
import time
import os


from tkinter import *
from tkinter import ttk
import pandas as pd
df = pd.read_csv("write_forcsvted.csv")
df.head()
sf=pd.read_csv("statquest.csv")
sf.head()

dict1 = df.set_index('title')['url'].to_dict()
dict2 = sf.set_index('title')['url'].to_dict()


root =Tk()

root.title('Take Break')
root.geometry('600x400')
root.configure(bg='Dodgerblue4')

def comboclick(event):

    return

def youtube():
    print(" You rang the Doorbell !")
    time.sleep(3)
    webbrowser.open(mycombo.get())

def youtube2():
    print(" You rang the Doorbell combo !")
    time.sleep(3)
    webbrowser.open(dict1[mycombo3.get()])


def statquest():
    print(" You rang the Doorbell combo !")
    time.sleep(3)
    webbrowser.open(dict2[mycombo4.get()])





def playme(event):

    webbrowser.open(mycombo.get())


option2 = ["https://techurls.com/",
"https://www.zdnet.com",
           "www.google.com",
           "www.ndtv.com",
           "www.msn.com",


]


mycombo = ttk.Combobox(root,value=option2,height=30,width=60)
mycombo.current(0)
mycombo.bind("<<Combobocselected>>",comboclick)
mycombo.pack()





youtubebtn = Button(root, text="Bookmarks",bg='lightblue',font=7,pady=15)
youtubebtn.pack()
youtubebtn['command'] = lambda :youtube()





mycombo3 = ttk.Combobox(root,value=list(dict1.keys()),height=30,width=60)
mycombo3.current(0)
mycombo3.bind("<<Combobocselected>>",comboclick)
mycombo3.pack()




youtubelistbtn = Button(root, text="Play-TED - Ex",bg='lightblue',font=7,pady=15)
youtubelistbtn.pack()
youtubelistbtn['command'] = lambda :youtube2()



mycombo4 = ttk.Combobox(root,value=list(dict2.keys()),height=30,width=60)
mycombo4.current(0)
mycombo4.bind("<<Combobocselected>>",comboclick)
mycombo4.pack()


statquestbtn = Button(root, text="Play Stat - Quest",bg='lightblue',font=7,pady=15)
statquestbtn.pack()
statquestbtn['command'] = lambda :statquest()

button_quit =Button(root,text="Exit Program",command=root.quit,bg='lightblue',font=12)
button_quit.pack()
root.mainloop()