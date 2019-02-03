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
from kivy.atlas import Atlas
from kivymd import images_path

#base python
import time

class ChargeScreen(Screen):
    def __init__(self,**kwargs):
        super(ChargeScreen, self).__init__(**kwargs)
        self.util = kwargs.get('util')
        layout = self.layout()
        self.add_widget(layout)

    def layout(self):
        self.charge = False
        self.amount = ''

        def on_text_charge(instance, value):
            self.port = True
            self.util.port = value
            self.amount = value
            setButtonColor()

        layout = FloatLayout()

        #Port
        chargeBox = BoxLayout()
        chargeField = MDTextField(password=True,size_hint_x=.9)
        chargeField.hint_text = "Enter Amount to Charge"
        chargeField.input_filter = "int"
        chargeField.bind(text=on_text_charge)
        chargeBox.add_widget(chargeField)

        chargeAnchor = AnchorLayout(anchor_x='center',anchor_y='top',padding=[100])
        chargeAnchor.add_widget(chargeBox)

        proceedBox = BoxLayout()
        blankWidget1 = MDLabel(text='')
        proceedButton = MDRaisedButton(text='Proceed')
        blankWidget2 = MDLabel(text='')
        proceedButton.md_bg_color = [0.9, 0, 0, 0.9]

        app = App.get_running_app()
        def setButtonColor():
            if all([self.value]):
                proceedButton.md_bg_color = app.theme_cls.primary_color
                proceedButton.bind(on_press=lambda x: self.createCharge())

        proceedBox.add_widget(blankWidget1)
        proceedBox.add_widget(proceedButton)
        proceedBox.add_widget(blankWidget2)
        proceedAnchor = AnchorLayout(anchor_x='center',anchor_y='center',padding=[60])
        proceedAnchor.add_widget(proceedBox)
        # #Combine all together
        layout.add_widget(chargeAnchor)
        layout.add_widget(proceedAnchor)

        return layout

    def createCharge(self):
        #Create pop up for charge
        stripelabel = MDLabel(text='Creating Charge', halign='center', valign='center')
        stripelabel.color = App.get_running_app().theme_cls.primary_color
        stripelabel.font_style = 'Body2'
        self.stripepopup = Popup(title='',
                                 content=stripelabel,
                                 size_hint=(None, None), size=(400, 400))
        self.stripepopup.separator_color = App.get_running_app().theme_cls.primary_color
        self.stripepopup.background = str(Atlas('{}round_shadow.atlas'.format(images_path)))
        self.stripepopup.open()
        time.sleep(1)
        msg = {}
        msg['function'] = 'Create_Charge'
        msg['email'] = self.util.email
        msg['amount'] = self.amount
        rsp = self.util.ConnectToServer(msg)
        if rsp['rsp'] == 'succeeded':
            self.stripepopup.content = MDLabel(text="Charged\n Succeded")
            time.sleep(1)
            self.stripepopup.dismiss()
        else:
            self.stripepopup.content = MDLabel(text="Charge \n Failed")
            time.sleep(1)
            self.stripepopup.dismiss()