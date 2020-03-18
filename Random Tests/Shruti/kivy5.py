# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 17:27:30 2020

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 14:16:51 2020

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 01:13:54 2020

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 21:11:25 2020

@author: User
"""

import sqlite3
import pandas as pd
import webbrowser
import time
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from os import listdir
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


conn = sqlite3.connect('Youtube1.db')  
c = conn.cursor()

read_clients = pd.read_csv (r'C:\Users\aksha\OneDrive\Documents\Take A Break\Random Tests\Shruti\YoutubeList1.csv')
read_clients.to_sql('Youtube1', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'CLIENTS' 
c.execute('''Select * from Youtube1''')
df = pd.DataFrame(c.fetchall(), columns=['id','title','url','views','counter'])
conn.commit()

#Reset function
def reset():
 import kivy.core.window as window
 from kivy.base import EventLoop
 if not EventLoop.event_listeners:
    from kivy.cache import Cache
    window.Window = window.core_select_lib('window', window.window_impl, True)
    Cache.print_usage()
    for cat in Cache._categories:
        Cache._objects[cat] = {}
        
# Start function      
class Start(Button):
    pass


class Forward(Button):
    pass

class Close(Button):
    pass
     
     
class Container(GridLayout):
    display = ObjectProperty()
    def play(self): 
        for i in range(0,len(df.index)):
            gh=df.get_value(i,2,True)
            df.set_value(i, 'counter', 1) 
            df.head()
            print(df)
            time.sleep(30)
            webbrowser.open(gh)# <- Main Class
    def proceed(self):
       j=df['counter'].sum()
       j=j+1
       for i in range(j,len(df.index)):
           gh=df.get_value(i,2,True)
           df.set_value(i, 'counter', 1) 
           df.head()
           print(df)
           time.sleep(5)
           webbrowser.open(gh)
    def close(self):
       App.get_running_app().stop()
       Window.close()
    


class BreakApp(App): 
    def build(self):   
        return Container()
    
#Next Function
    
reset()

if __name__ == "__main__":
    app = BreakApp()
    app.run()
    
     
     
     
     
     
     
     
     
     
     
     
