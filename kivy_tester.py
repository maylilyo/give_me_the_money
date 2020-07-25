import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock


class PongApp(App):

    def print_it(self, instance, value):
        print('User clicked on', value)
        value = "!"
        return value

    def build(self):
        widget = Label(text='Hello [ref=world]World[/ref]', markup=True)
        widget.bind(on_ref_press=self.print_it)
        
        return widget


if __name__ == '__main__':
    PongApp().run()

def print_it(instance, value):
    print('User clicked on', value)
widget = Label(text='Hello [ref=world]World[/ref]', markup=True)
widget.bind(on_ref_press=print_it)