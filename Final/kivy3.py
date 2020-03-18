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
from string import ascii_lowercase

#kv_path = './kv/'
#for kv in listdir(kv_path):
#    Builder.load_file(kv_path + kv)

#conn = sqlite3.connect('Youtube1.db')
#c = conn.cursor()

#read_clients = pd.read_csv(r'C:\Users\aksha\OneDrive\Documents\Take A Break\Final\YoutubeList.csv')
#read_clients.to_sql('Youtube1', conn, if_exists='append',
#                   index=False)  # Insert the values from the csv file into the table 'CLIENTS'
#c.execute('''Select * from Youtube1''')

#conn.commit()

kv = """
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
            text: 'History'
            on_press: root.history()
        Button:
            text: 'Clear list'
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
            
        Button:
            text: "Exit"
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
    mainDF = pd.read_csv(r'C:\Users\aksha\OneDrive\Documents\Take A Break\Final\YoutubeList.csv')
    playFlag = False
    delay = 10
    shuffleFlag = False

    def playForThread(self):
        currentWait = 0
        while TBreak.playFlag:
            if currentWait % TBreak.delay == 0 and currentWait != 0:
                jumpToRow = int(TBreak.mainDF['counter'].sum())
                link = TBreak.mainDF.loc[jumpToRow, 'url']
                TBreak.mainDF.loc[jumpToRow, 'counter'] = 1
                webbrowser.open(link)  # <- Main Class
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
        j = int(TBreak.mainDF['counter'].sum())
        '''
        j = j + 1
        for i in range(j, len(df.index)):
            gh = df.iloc[i, 2]
            df.loc[i, 'counter'] = 1
            time.sleep(5)
            webbrowser.open(gh)
        '''
        TBreak.mainDF.loc[j, 'counter'] = 1

    def close(self):
        TBreak.mainDF.to_csv(r'C:\Users\aksha\OneDrive\Documents\Take A Break\Final\YoutubeList.csv', index=False)

        TBreak.playFlag = False
        App.get_running_app().stop()
        Window.close()

    def queue(self):
        referenceDF = TBreak.mainDF.loc[(TBreak.mainDF.counter == 0)]
        print(referenceDF.head())
        self.rv.data = [{'value': referenceDF.iloc[i, 1]}
                        for i in range(0, len(referenceDF.index))]

    def history(self):
        referenceDF = TBreak.mainDF.loc[(TBreak.mainDF.counter == 1)]
        print(referenceDF.head())
        self.rv.data = [{'value': referenceDF.iloc[i, 1]}
                        for i in range(0, len(referenceDF.index))]

    def clear(self):
        TBreak.mainDF.counter = 0
        self.rv.data = []

    def shuffle(self):
        if TBreak.shuffleFlag:
            TBreak.mainDF = TBreak.mainDF.sort_values('id')
            TBreak.shuffleFlag = False
        else:
            TBreak.mainDF = TBreak.mainDF.sample(frac=1)
            TBreak.shuffleFlag = True


class TestApp(App):
    def build(self):
        return TBreak()


reset()
if __name__ == '__main__':
    TestApp().run()
