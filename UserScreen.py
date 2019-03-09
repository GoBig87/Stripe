#Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivymd.textfields import MDTextField
from kivymd.button import MDRaisedButton
from kivy.metrics import dp

class UserScreen(Screen):
    def __init__(self,**kwargs):
        super(UserScreen, self).__init__(**kwargs)
        self.util = kwargs.get('util')
        layout = self.layout()
        self.add_widget(layout)

    def layout(self):
        self.user = ''

        def on_text_email(instance, value):
            self.user = str(value)
            setButtonColor()

        layout = BoxLayout(
                        orientation= 'vertical',
                        padding= (dp(48),2*dp(48)),
                        spacing= dp(48),
                        )

        userField = MDTextField()
        userField.hint_text = "Enter user ID"
        userField.bind(text=on_text_email)
        layout.add_widget(userField)

        proceedButton = MDRaisedButton(text='Enter Information', size_hint=(None, None),size= (4*dp(48),dp(48)))
        proceedButton.md_bg_color = [0.9, 0, 0, 0.9]
        app = App.get_running_app()

        def setButtonColor():
            if self.user != '':
                proceedButton.text = 'Proceed'
                proceedButton.md_bg_color = app.theme_cls.primary_color
                proceedButton.bind(on_press=lambda x: self.processInformation())

        proceedAnchor = AnchorLayout(anchor_x='center',anchor_y='center')
        proceedAnchor.add_widget(proceedButton)
        layout.add_widget(proceedAnchor)

        return layout

    def processInformation(self):
        self.util.user = self.user
        self.changeScreen()

    def changeScreen(self):
        self.manager.current = 'network'