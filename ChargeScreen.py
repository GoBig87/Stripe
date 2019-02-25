#Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivymd.textfields import MDTextField
from kivymd.button import MDRaisedButton
from kivy.app import App
from kivy.atlas import Atlas
from kivymd import images_path
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.atlas import Atlas
from kivymd import images_path
from kivy.uix.popup import Popup
#base python
import time

spinner = ''' 
#:import MDSpinner kivymd.spinner.MDSpinner

AnchorLayout:
    anchor_x: 'center'
    anchor_y: 'center'
    MDSpinner:
        id: spinner                    
        size_hint: None, None
        size: dp(46), dp(46)

'''

class ChargeScreen(Screen):
    def __init__(self,**kwargs):
        super(ChargeScreen, self).__init__(**kwargs)
        self.util = kwargs.get('util')
        layout = self.layout()
        self.add_widget(layout)

    def layout(self):
        self.charge = False
        self.amount = ''
        self.ready  = False

        def on_text_charge(instance, value):
            self.amount = value
            if len(value) >= 1:
                self.ready = True
            else:
                self.ready = False
            setButtonColor()

        layout = BoxLayout(
                        orientation= 'vertical',
                        padding= (2*dp(48),2*dp(48))
                        )

        #Charge Box
        chargeField = MDTextField()
        chargeField.hint_text = "Enter Amount to Charge"
        chargeField.input_filter = "int"
        chargeField.bind(text=on_text_charge)
        layout.add_widget(chargeField)

        proceedButton = MDRaisedButton(text='Proceed',size_hint=(None, None),size= (4*dp(48),dp(48)))
        proceedButton.md_bg_color = [0.9, 0, 0, 0.9]

        app = App.get_running_app()
        def setButtonColor():
            if self.ready:
                proceedButton.md_bg_color = app.theme_cls.primary_color
                proceedButton.bind(on_press=lambda x: self.createCharge())

        proceedAnchor = AnchorLayout(anchor_x='center',anchor_y='bottom',padding=[60])
        proceedAnchor.add_widget(proceedButton)
        layout.add_widget(proceedAnchor)

        content = Builder.load_string(spinner)
        self.stripepopup = Popup(title='Charging Card', title_align='center',
                size_hint=(None, None), size=(dp(200), dp(200)))
        self.stripepopup.add_widget(content)
        self.stripepopup.title_font = 'data/fonts/Roboto-Bold.ttf'
        self.stripepopup.title_color = App.get_running_app().theme_cls.primary_color
        self.stripepopup.separator_color = App.get_running_app().theme_cls.primary_color
        self.stripepopup.background = str(Atlas('{}round_shadow.atlas'.format(images_path)))

        return layout

    def createCharge(self):
        self.stripepopup.open()
        time.sleep(1)
        msg = {}
        msg['function'] = 'Create_Charge'
        msg['email'] = self.util.email
        msg['amount'] = self.amount
        rsp = self.util.ConnectToServer(msg)
        if rsp['rsp'] == 'succeeded':
            self.stripepopup.title = "Charged Succeded"
            time.sleep(1)
            self.stripepopup.dismiss()
        else:
            self.stripepopup.title = "Charge  Failed"
            time.sleep(1)
            self.stripepopup.dismiss()