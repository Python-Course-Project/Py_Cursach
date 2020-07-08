from kivy.properties import ObjectProperty
from kivymd.uix.navigationdrawer import NavigationLayout
from kivymd.uix.screen import Screen
from kivymd.uix.toolbar import MDToolbar

from mobile.connection_controller.ConnectionController import ConnectionController


class MainScreen(Screen):
    MainScreen = ObjectProperty()
    pass


class BaseToolbar(MDToolbar):
    pass


class MainNavigationLayout(NavigationLayout):
    username_field = ObjectProperty()

    def pull_name(self):
        return "Username: " + ConnectionController().username
