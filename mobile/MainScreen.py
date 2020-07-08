from kivymd.uix.screen import Screen
from mobile.connection_controller.ConnectionController import ConnectionController
from kivy.properties import ObjectProperty
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.navigationdrawer import NavigationLayout

class MainScreen(Screen):
    MainScreen = ObjectProperty()
    pass


class BaseToolbar(MDToolbar):
    pass


class MainNavigationLayout(NavigationLayout):
    username_field = ObjectProperty()

    def pull_name(self):
        return "Username: " + ConnectionController().username
