from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
Window.size = (300, 500)


class LoginScreenManager(ScreenManager):
    pass


class AuthScreen(Screen):
    login_input = ObjectProperty()
    password_input = ObjectProperty()

    def verify_auth(self):
        print(self.login_input.text, self.password_input.text)


class RegisterScreen(Screen):
    pass


class MainApp(MDApp):

    def build(self):
        pass


if __name__ == "__main__":
    MainApp().run()
