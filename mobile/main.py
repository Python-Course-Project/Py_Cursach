from kivymd.app import MDApp

#from mobile.MainScreen import NavigationLayout
import json
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
# noinspection PyUnresolvedReferences
from mobile.MainScreen import MainScreen
from mobile.connection_controller.ConnectionController import ConnectionController
from requests.exceptions import HTTPError, ConnectionError
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import SwapTransition, SlideTransition
from kivymd.uix.list import TwoLineListItem
from mobile.note_field import NoteField

Window.size = (300, 500)


class LoginScreenManager(ScreenManager):
    pass


# class HiScreen(Screen):
#     def automatic_switch(self):
#         print("HI")
#         Clock.schedule_once(self.switch_to_auth, 2)
#
#     def switch_to_auth(self):
#         print("!!!!!!!!!!!!!!!!!!!!!!")
#         app = MDApp.get_running_app()
#         app.root.current = "AuthScreen"

class AuthScreen(Screen):
    login_input = ObjectProperty()
    password_input = ObjectProperty()

    # TODO: автозаполнение
    # def fill_on_enter(self):
    #     self.login_input.text = ConnectionController().username

    def verify_auth(self):
        if not self.login_input.text:
            dialog = MDDialog(title="Login", text="Empty login rejected", size_hint=(0.8, None))
            dialog.open()
            return False

        if not self.password_input.text:
            dialog = MDDialog(title="Login", text="Empty password rejected", size_hint=(0.8, None))
            dialog.open()
            return False

        return True

    def log_in(self):
        try:
            ConnectionController.login(self.login_input.text, self.password_input.text)
        except ConnectionError:
            dialog = MDDialog(title="Login", text="Network failed you(", size_hint=(0.8, None))
            dialog.open()

            return False
        except HTTPError:
            dialog = MDDialog(title="Login", text="Wrong username/password \n Forgot password? Bad.",
                              size_hint=(0.8, None))
            self.password_input.text = ""
            dialog.open()

            return False

        return True

    def login_button_behavior(self):
        if self.verify_auth():
            if self.log_in():
                ConnectionController.pull_notes()

                self.manager.transition = SlideTransition()
                self.manager.transition.direction = "up"
                self.manager.current = "MainScreen"




class RegisterScreen(Screen):
    login_input = ObjectProperty()
    password_input = ObjectProperty()
    password_confirm_input = ObjectProperty()

    def verify_fields(self):
        if not self.login_input.text:
            dialog = MDDialog(title="Register", text="Empty login rejected", size_hint=(0.8, 0.5))
            dialog.open()
            self.password_input.text = ""
            self.password_confirm_input.text = ""
            return False

        if not self.password_input.text:
            dialog = MDDialog(title="Register", text="Empty password rejected", size_hint=(0.8, 0.5))
            dialog.open()
            return False

        if self.password_input.text != self.password_confirm_input.text:
            dialog = MDDialog(title="Register", text="Passwords do not match", size_hint=(0.8, 0.5))
            dialog.open()
            self.password_input.text = ""
            self.password_confirm_input.text = ""
            return False

        return True

    def register(self):
        try:
            ConnectionController.register(self.login_input.text, self.password_input.text)
        except ConnectionError:
            dialog = MDDialog(title="Register", text="Network failed you(", size_hint=(0.8, 0.5))
            dialog.open()
            return False
        except HTTPError:
            dialog = MDDialog(title="Register", text="User already exist", size_hint=(0.8, 0.5))
            dialog.open()
            return False

        return True

    def register_button_behavior(self):
        if self.verify_fields():
            if self.register():
                self.manager.transition = SwapTransition()
                self.manager.current = "AuthScreen"


class MainApp(MDApp):

    def build(self):
        self.title = 'Cool Note App'


if __name__ == "__main__":
    MainApp().run()
