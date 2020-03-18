from kivy3 import TestApp
from kivy3 import TBreak
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


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
<Test>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    
    orientation: 'vertical'
    GridLayout:
        cols: 3
        rows: 2
        size_hint_y: None
        height: dp(108)
        padding: dp(8)
        spacing: dp(16)
        Button:
            text: 'Snooze'
            on_press: root.snooze()
        Button:
            text: 'Ok'
            on_press: root.ok()
        
"""

Builder.load_string(kv)


class Test(BoxLayout):

    def snooze(self):
        App.get_running_app().stop()
        Window.close()

    def ok(self):
        with open('kivy3.py') as f:
            code = compile(f.read(), 'TBreak', 'exec')
            exec(code)


class TestApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TestApp().run()