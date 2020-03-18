from kivy.uix.floatlayout import FloatLayout
from kivy.app import App


class MyGrid(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MainApp().run()