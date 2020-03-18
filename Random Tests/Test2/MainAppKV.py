from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.app import App


class MyGrid(Widget):
    name = ObjectProperty(None)
    email = ObjectProperty(None)

    def submit(self):
        print('Name:', self.name.text, '\nEmail:', self.email.text)
        self.name.text = ''
        self.email.text = ''

class DesignApp(App):
    def build(self):
        return MyGrid()


if __name__ == '__main__':
    DesignApp().run()
