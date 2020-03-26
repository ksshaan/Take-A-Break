import threading
import sqlite3
import pandas as pd
import webbrowser
import time
import numpy as np
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
        app.root.ids.bt1.text = '{}'.format(args[1])
        

    Button:
        id: btn1
        text: '10 minutes'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select(btn1.text)

    Button:
        id: btn2
        text: '15 minutes'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select('15 minutes')
    Button:
        id: btn3
        text: '30 minutes'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select('30 minutes')
        
    Button:
        id: btn4
        text: '45 minutes'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select('45 minutes')
        
    Button:
        id: btn5
        text: '60 minutes'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select('60 minutes')
        
    
<CDropdown@DropDown>:
    id: ddown
    on_select:
        app.root.ids.btn.text = '{}'.format(args[1])
        

    Button:
        id: b1
        text: 'Videos'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('Videos')
        

    Button:
        id: b2
        text: 'Puzzles'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('Puzzles')
        
    Button:
        id: b3
        text: 'Jokes'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('Jokes')
        
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
            text: 'Queue'
            on_press: root.queue()
        Button:
            text: 'Shuffle'
            on_press: root.shuffle()
        Button:
            text: 'Reset'
            on_press: root.resetHistory()
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
                id: bt1
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
                hint_text: 'Playlist Name'
                padding: dp(10), dp(10), 0, 0
        BoxLayout:
            spacing: dp(8)
            TextInput:
                id: url_input
                size_hint_x: 0.6
                hint_text: 'Url'
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
                on_press: root.additem('Playlist added',name_input.text,url_input.text,btn.text)
    GridLayout:
        cols: 1
        rows: 1
        size_hint_y: None
        height: dp(40)
        padding: dp(8)
        spacing: dp(8)
        BoxLayout:
            spacing: dp(5)
            Label:
                id: updlbl
                text:'Please press add button to add to playlist' if name_input.text!='' and url_input.text!='' else 'Please all values'
                
                font_size:'8pt'
        
        
        
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
    mainDF = pd.read_csv(r'C:\Users\User\Documents\DataScience\Python\PythonCode\YoutubeList1.csv')
    historyDF = pd.read_csv(r'C:\Users\User\Documents\DataScience\Python\PythonCode\TakeABreak\History.csv')
    queueDF = pd.read_csv(r'C:\Users\User\Documents\DataScience\Python\PythonCode\TakeABreak\Queue.csv')
    playFlag = False
    delay = 10
    shuffleFlag = False
    timing = 30
    selectedGenre = 'NA'

    # first row buttons Queue,Shuffle,Reset
    def updateQueue(self):
        if TBreak.queueDF.shape[0] == 0:
            if TBreak.selectedGenre == 'NA':
                TBreak.queueDF = TBreak.queueDF.append(TBreak.mainDF)
            else:
                TBreak.queueDF = TBreak.queueDF.append(TBreak.mainDF.loc[(TBreak.mainDF.genre == TBreak.selectedGenre), :])

    def queue(self):
        TBreak.updateQueue(self)
        self.rv.data = [{'value': TBreak.queueDF.iloc[i, 1]}
                        for i in range(0, len(TBreak.queueDF.index))]

    def shuffle(self):
        TBreak.updateQueue(self)
        if TBreak.shuffleFlag:
            TBreak.queueDF = TBreak.queueDF.sort_values('id')
            TBreak.shuffleFlag = False
        else:
            TBreak.queueDF = TBreak.queueDF.sample(frac=1)
            TBreak.shuffleFlag = True

    def resetHistory(self):
        TBreak.historyDF = TBreak.historyDF.iloc[0:0]
        TBreak.queueDF = TBreak.queueDF.iloc[0:0]
        TBreak.updateQueue(self)
        #TBreak.mainDF.counter = 0
        self.rv.data = []

    # second row buttons Play,next,history
    def playForThread(self):
        TBreak.updateQueue(self)
        currentWait = 0
        while TBreak.playFlag:
            if currentWait % TBreak.delay == 0 and currentWait != 0:
                link = TBreak.queueDF.iloc[0, 2]
                webbrowser.open(link)  # <- Main Class
                TBreak.historyDF = TBreak.historyDF.append(TBreak.queueDF.iloc[0, :])
                TBreak.queueDF = TBreak.queueDF.drop(TBreak.queueDF.index[0])
                if self.rv.data:
                    self.rv.data.pop(0)
            time.sleep(0.5)
            currentWait = currentWait + 0.5


    def play(self):
        t1 = threading.Thread(target=TBreak.playForThread, args=(self,))
        if TBreak.playFlag:
            TBreak.playFlag = False
        else:
            TBreak.playFlag = True
            t1.start()

    def proceed(self):
        TBreak.queueDF = TBreak.queueDF.drop(TBreak.queueDF.index[0])
        print(TBreak.queueDF.head())

    def history(self):
        print(TBreak.historyDF.head())
        self.rv.data = [{'value': TBreak.historyDF.iloc[i, 1]}
                        for i in range(0, len(TBreak.historyDF.index))]

    '''Genre area
    def Genre_Puzzle(Self):
        # code to be added
        print(mainDF)

    def Genre_Video(Self):
        # code to be added
        print(mainDF)

    def Genre_Joke(Self):
        # code to be added
        print(mainDF)

        # timing

    def timing10(self):
        # code to be added
        print(mainDF)

    def timing15(self):
        # code to be added
        print(mainDF)

    def timing30(self):
        # code to be added
        print(mainDF)

    def timing45(self):
        # code to be added
        print(mainDF)

    def timing60(self):
        # code to be added
        print(mainDF)

    # add playlist
    def additem(self):
        if self.name_input.text != "" and self.url_input.text != "" and self.genre_input.text != "":
            # db.add_user(self.email.text, self.password.text, self.namee.text)
            self.reset()
    # def insertname(self, value):
    # print(mainDF)
    # add value to csv file name
    # self.rv.data.insert(0, {'value': value or 'default value'})
    # self.rv.refresh_from_data()

    # def inserturl(self, value):
    #   print(mainDF)
    # add value url to csv file name
    # if self.rv.data:
    #   self.rv.data[0]['value'] = value or 'default new value'
    #  self.rv.refresh_from_data()
    '''
    def additem(self,txt,a,b,c):
        self.ids.updlbl.text = txt
        print(a)
        print(b)
        print(c)
        #if self.name_input.text != "" and self.url_input.text != "" and self.genre_input.text != "":
            # db.add_user(self.email.text, self.password.text, self.namee.text)
        
    # Exit button
    def close(self):
        TBreak.mainDF.to_csv(r'C:\Users\User\Documents\DataScience\Python\PythonCode\YoutubeList1.csv', index=False)
        TBreak.historyDF.to_csv(r'C:\Users\User\Documents\DataScience\Python\PythonCode\TakeABreak\History.csv', index=False)
        TBreak.queueDF.to_csv(r'C:\Users\User\Documents\DataScience\Python\PythonCode\TakeABreak\Queue.csv', index=False)
        TBreak.playFlag = False
        time.sleep(0.5)
        App.get_running_app().stop()
        Window.close()


class TakebreakApp(App):
    def build(self):
        return TBreak()


reset()

if __name__ == '__main__':
    TakebreakApp().run()
