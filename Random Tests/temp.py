from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
import pandas as pd
import webbrowser, time, sqlite3
 
conn = sqlite3.connect('Youtube1.db')  
c = conn.cursor()

read_clients = pd.read_csv (r'C:\Users\aksha\OneDrive\Documents\Take A Break\Random Tests\Shruti\YoutubeList1.csv')
read_clients.to_sql('Youtube1', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'CLIENTS' 
c.execute('''Select * from Youtube1''')
df = pd.DataFrame(c.fetchall(), columns=['id','title','url','views','counter'])
conn.commit()

class FirstKivy(App):

    def build(self):
        lbl = Label()
        btnStrt = Button(text = "Start", pos = (150, 350), size_hint = (0.25,0.18))
        btnStrt.bind(on_press = lambda a: FirstKivy.start())
        btnCls = Button(text = "Close", pos = (300, 350), size_hint = (.25, .18))
        btnCls.bind(on_press = lambda b: FirstKivy.stop())
        btnNxt = Button(text = "Next", pos = (450, 350), size_hint = (.25, .18))
        btnNxt.bind(on_press = lambda b: FirstKivy.proceed())
        lbl.add_widget(btnCls)
        lbl.add_widget(btnStrt)
        lbl.add_widget(btnNxt)
        return lbl
    
    def start():
        for i in range(0,df.shape[0]): #len(df.index)
            gh=df.loc[i, 'url']
            df.loc[i, "counter"] = 1
            time.sleep(15)
            webbrowser.open(gh)
            
    def proceed():
        j=df['counter'].sum()
        j=j+1
        print(j)
        for i in range(j,df.shape[0]):
            gh=df.loc[i, 'url']
            df.loc[i, "counter"] = 1
            time.sleep(5)
            webbrowser.open(gh)
            
    def close():
        App.get_running_app().stop()
        Window.close()
        FirstKivy.reset()
    
    
    def reset():
        print("reset started")
        import kivy.core.window as window
        from kivy.base import EventLoop
        if not EventLoop.event_listeners:
            from kivy.cache import Cache
            window.Window = window.core_select_lib('window', window.window_impl, True)
            Cache.print_usage()
            for cat in Cache._categories:
                Cache._objects[cat] = {}
        print("reset done")

        
if __name__ == "__main__":
    app = FirstKivy()
    app.run()