from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
import webbrowser, time
 
class FirstKivy(App):
 
    def build(self):
        lbl = Label()
        btnStrt = Button(text = "Start", pos = (150, 350), size_hint = (0.25,0.18))
        btnStrt.bind(on_press = lambda a: FirstKivy.start())
        btnCls = Button(text = "Close", pos = (300, 350), size_hint = (.25, .18))
        btnCls.bind(on_press = lambda b: app.stop())
        lbl.add_widget(btnCls)
        lbl.add_widget(btnStrt)
        return lbl
    
    def start():
            webbrowser.open_new_tab("https://www.youtube.com/watch?v=0lRinhhlpzM")
 
if __name__ == "__main__":
    app = FirstKivy()
    app.run()