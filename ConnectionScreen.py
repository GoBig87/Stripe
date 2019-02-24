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
from kivy.metrics import dp

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

        layout = BoxLayout(
                        orientation= 'vertical',
                        padding= (2*dp(48),2*dp(48))
                        )

        #IP address
        addressField = MDTextField()
        addressField.hint_text = "IP Address"
        addressField.bind(text=on_text_address)
        layout.add_widget(addressField)

        #Port
        portField = MDTextField(password=True)
        portField.hint_text = "Port"
        portField.input_filter = "int"
        portField.bind(text=on_text_port)
        layout.add_widget(portField)

        proceedButton = MDRaisedButton(text='Proceed',size_hint=(None, None),size= (4*dp(48),dp(48)))
        proceedButton.md_bg_color = [0.9, 0, 0, 0.9]

        app = App.get_running_app()
        def setButtonColor():
            if all([self.port,self.address]):
                proceedButton.md_bg_color = app.theme_cls.primary_color
                proceedButton.bind(on_press=lambda x: self.returnhome())

        proceedAnchor = AnchorLayout(anchor_x='center',anchor_y='center',padding=[60])
        proceedAnchor.add_widget(proceedButton)
        # #Combine all together
        layout.add_widget(proceedAnchor)

        return layout

    def returnHome(self):
        self.manager.current = 'card'


