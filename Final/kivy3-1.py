import threading
import sqlite3
import pandas as pd
import webbrowser
import time
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from random import sample
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from os import listdir

from kivy.uix.dropdown import DropDown
from kivy.factory import Factory

#kv_path = './kv/'
#for kv in listdir(kv_path):
#    Builder.load_file(kv_path + kv)

conn = sqlite3.connect('Youtube1.db')
c = conn.cursor()

#read_clients = pd.read_csv(r'C:\Users\aksha\OneDrive\Documents\Take A Break\Final\YoutubeList.csv')
#read_clients.to_sql('Youtube1', conn, if_exists='append',
#                   index=False)  # Insert the values from the csv file into the table 'CLIENTS'
#c.execute('''Select * from Youtube1''')
mainDF = pd.read_csv(r'C:\Users\User\Documents\PythonCode\YoutubeList1.csv')
#conn.commit()

kv = """
#:import Factory kivy.factory.Factory

<Row@BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Rectangle:
            size: self.size
            pos: self.pos
    value: ''
    Label:
        text: root.value
<CustomDropdown@DropDown>:
    id: dropdown
    on_select:
        app.root.ids.btn.text = '{}'.format(args[1])
        

    Button:
        id: btn1
        text: '10 minutes'
        size_hint_y: None
        height: '48dp'
        on_press: root.timing10()
        on_release:
            dropdown.select(btn1.text)

    Button:
        id: btn2
        text: '15 minutes'
        size_hint_y: None
        height: '48dp'
        on_press: root.timing15()
        on_release:
            dropdown.select(btn2.text)
    Button:
        id: btn3
        text: '30 minutes'
        size_hint_y: None
        height: '48dp'
        on_press: root.timing30()
        on_release:
            dropdown.select(btn3.text)
        
    Button:
        id: btn4
        text: '45 minutes'
        size_hint_y: None
        height: '48dp'
        on_press: root.timing45()
        on_release:
            dropdown.select(btn4.text)
        
    Button:
        id: btn5
        text: '60 minutes'
        size_hint_y: None
        height: '48dp'
        on_press: root.timing60()
        on_release:
            dropdown.select(btn5.text)
        
    
<CDropdown@DropDown>:
    id: ddown
    on_select:
        app.root.ids.btn.text = '{}'.format(args[1])
        

    Button:
        id: btn1
        text: 'Videos'
        size_hint_y: None
        height: '48dp'
        on_press: root.Genre_Video()
        on_release:
            ddown.select(btn1.text)
        

    Button:
        id: btn2
        text: 'Puzzles'
        size_hint_y: None
        height: '48dp'
        on_press: root.Genre_Puzzle()
        on_release:
            ddown.select(btn2.text)
        
    Button:
        id: btn3
        text: 'Jokes'
        size_hint_y: None
        height: '48dp'
        on_press: root.Genre_Joke()
        on_release:
            ddown.select(btn3.text)
        
<TBreak>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    orientation: 'vertical'
    GridLayout:
        cols: 3
        rows: 2
        size_hint_y: None
        height: dp(108)
        padding: dp(8)
        spacing: dp(16)
        Button:
            text: 'PlayList'
            on_press: root.playlist()
        Button:
            text: 'ReshuffleList'
            on_press: root.reshuff()
        Button:
            text: 'ClearList'
            on_press: root.clear()
        BoxLayout:
            spacing: dp(8)
            Button:
                text: "Start/Stop"
                on_press: root.play()
            
        BoxLayout:
            spacing: dp(8)
            Button:
                text: "Next"
                on_press: root.proceed()
        BoxLayout:
            spacing: dp(8)           
            Button:
                text: 'History'
                on_press: root.history()
    GridLayout:
        cols: 2
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(8)
        BoxLayout:
            spacing: dp(8)
            Button:
                id: btn
                text: 'Timing'
                on_release: Factory.CustomDropdown().open(self)
                size_hint_y: None
                height: '30dp'
        BoxLayout:
            spacing: dp(8)
            Button:
                id: btn
                text: 'Genre'
                on_release: Factory.CDropdown().open(self)
                size_hint_y: None
                height: '30dp'
    GridLayout:
        cols: 1
        rows: 1
        size_hint_y: None
        height: dp(40)
        padding: dp(8)
        spacing: dp(8)
        BoxLayout:
            spacing: dp(8)
            Label:
                text: ('[b]Add to Playlist[/b]')
                markup: True
                font_size:'15pt'
        
    GridLayout:
        cols: 4
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(16)
        BoxLayout:
            spacing: dp(8)
            TextInput:
                id: name_input
                size_hint_x: 0.6
                hint_text: 'Playlist name'
                padding: dp(10), dp(10), 0, 0
        BoxLayout:
            spacing: dp(8)
            TextInput:
                id: url_input
                size_hint_x: 0.6
                hint_text: 'url'
                padding: dp(10), dp(10), 0, 0
        BoxLayout:
            spacing: dp(8)
            TextInput:
                id: genre_input
                size_hint_x: 0.6
                hint_text: 'Genre'
                padding: dp(10), dp(10), 0, 0
        BoxLayout:
            spacing: dp(8)
            Button:
                text: 'Add'
                on_press: root.additem()
        
        
        
    GridLayout:
        cols: 1
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(16)
        BoxLayout:
            spacing: dp(8)
            Button:
                text: "Snooze"
                on_press: root.close()

            
        
        
        
        
        
        
    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(10)
        viewclass: 'Row'
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)
"""

Builder.load_string(kv)


def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}


class TBreak(BoxLayout):
    playFlag = False
    delay = 10
    
#first row buttons Playlist,reshuffle,clearlist
    
    def playlist(self):
        print(mainDF.shape)
        referenceDF = mainDF.loc[(mainDF.counter == 0)]
        print(referenceDF.head())
        self.rv.data = [{'value': referenceDF.iloc[i, 1]}
                        for i in range(0, len(referenceDF.index))]

    
    def reshuff(self):
        #code to be added
        print(mainDF)
    def clear(self):
        mainDF.counter = 0
        self.rv.data = []

    
    
    
    
#second row buttons Play,next,history

    def playForThread(self):
        currentWait = 0
        while TBreak.playFlag:
            if currentWait % TBreak.delay == 0 and currentWait != 0:
                jumpToRow = int(mainDF['counter'].sum())
                link = mainDF.loc[jumpToRow, 'url']
                mainDF.loc[jumpToRow, 'counter'] = 1
                webbrowser.open(link)  # <- Main Class
                if self.rv.data:
                    self.rv.data.pop(0)

                
            time.sleep(1)
            currentWait = currentWait + 1


    def play(self):
        t1 = threading.Thread(target=TBreak.playForThread, args=(self,))
        if TBreak.playFlag:
            TBreak.playFlag = False
        else:
            TBreak.playFlag = True
            t1.start()

    def proceed(self):
        print(mainDF.shape)
        j = int(mainDF['counter'].sum())
        '''
        j = j + 1
        for i in range(j, len(df.index)):
            gh = df.iloc[i, 2]
            df.loc[i, 'counter'] = 1
            time.sleep(5)
            webbrowser.open(gh)
        '''
        mainDF.loc[j, 'counter'] = 1
        
    def history(self):
        print(mainDF.shape)
        referenceDF = mainDF.loc[(mainDF.counter == 1)]
        print(referenceDF.head())
        self.rv.data = [{'value': referenceDF.iloc[i, 1]}
                        for i in range(0, len(referenceDF.index))]

    
    
        
#Genre area
    def Genre_Puzzle(Self):
        #code to be added
        print(mainDF)
    def Genre_Video(Self):
        #code to be added
        print(mainDF)
    def Genre_Joke(Self):
        #code to be added
        print(mainDF)     

#timing
        
    def timing10(self):
        #code to be added
        print(mainDF)
    def timing15(self):
        #code to be added
        print(mainDF)
    def timing30(self):
        #code to be added
        print(mainDF)
    
    def timing45(self):
        #code to be added
        print(mainDF)
    def timing60(self):
        #code to be added
        print(mainDF)
        
        
#add playlist
        
        
        
    def additem(self):
        if self.name_input.text != "" and self.url_input.text != "" and self.genre_input.text != "":         
            #db.add_user(self.email.text, self.password.text, self.namee.text)
            self.reset()
    #def insertname(self, value):
        #print(mainDF)
        #add value to csv file name
        #self.rv.data.insert(0, {'value': value or 'default value'})
        #self.rv.refresh_from_data()

    #def inserturl(self, value):
     #   print(mainDF)
        #add value url to csv file name
        #if self.rv.data:
         #   self.rv.data[0]['value'] = value or 'default new value'
          #  self.rv.refresh_from_data()
            
            
#Exit button
    def close(self):
        print(mainDF)
        mainDF.to_csv(r'C:\Users\User\Documents\PythonCode\YoutubeList1.csv', index=False)

        TBreak.playFlag = False
        App.get_running_app().stop()
        Window.close()



    

class TakebreakApp(App):
    def build(self):
        return TBreak()


reset()
if __name__ == '__main__':
    TakebreakApp().run()
