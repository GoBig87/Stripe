#Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivymd.textfields import MDTextField
from kivymd.button import MDRaisedButton
from kivymd.label import MDLabel
from kivy.app import App

#base python
import socket

class ConnectionScreen(Screen):
    def __init__(self,**kwargs):
        super(ConnectionScreen, self).__init__(**kwargs)
        self.util = kwargs.get('util')
        layout = self.layout()
        self.add_widget(layout)

    def layout(self):
        self.address = False
        self.port = False

        def on_text_address(instance, value):
            try:
                socket.inet_aton(value)
                # legal socket value
                self.address = True
                self.util = value
            except socket.error:
                self.address = False
            setButtonColor()

        def on_text_port(instance, value):
            self.port = True
            self.util.port = value
            setButtonColor()

        layout = FloatLayout()

        #IP address
        addressBox = BoxLayout()
        addressField = MDTextField(size_hint_x=.9)
        addressField.hint_text = "IP Address"
        addressField.bind(text=on_text_address)
        addressBox.add_widget(addressField)

        #Port
        portBox = BoxLayout()
        portField = MDTextField(password=True,size_hint_x=.9)
        portField.hint_text = "Port"
        portField.input_filter = "int"
        portField.bind(text=on_text_port)
        portBox.add_widget(portField)


        #Combine fields
        combinedBox = BoxLayout(orientation='vertical',size_hint_y=.3)
        combinedBox.add_widget(addressBox)
        combinedBox.add_widget(portBox)
        networkAnchor = AnchorLayout(anchor_x='center',anchor_y='top',padding=[100])
        networkAnchor.add_widget(combinedBox)

        proceedBox = BoxLayout()
        blankWidget13 = MDLabel(text='')
        proceedButton = MDRaisedButton(text='Proceed')
        blankWidget14 = MDLabel(text='')
        proceedButton.md_bg_color = [0.9, 0, 0, 0.9]

        app = App.get_running_app()
        def setButtonColor():
            if all([self.port,self.address]):
                proceedButton.md_bg_color = app.theme_cls.primary_color
                proceedButton.bind(on_press=lambda x: self.returnhome())

        proceedBox.add_widget(blankWidget13)
        proceedBox.add_widget(proceedButton)
        proceedBox.add_widget(blankWidget14)
        proceedAnchor = AnchorLayout(anchor_x='center',anchor_y='center',padding=[60])
        proceedAnchor.add_widget(proceedBox)
        # #Combine all together
        layout.add_widget(networkAnchor)
        layout.add_widget(proceedAnchor)

        return layout

    def returnHome(self):
        self.manager.current = 'card'


