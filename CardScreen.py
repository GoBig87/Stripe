#Kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.textfields import MDTextField
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivymd.button import MDRaisedButton
from kivymd.label import MDLabel
from kivy.app import App
from kivy.atlas import Atlas
from kivymd import images_path
from kivy.utils import platform
#python base modules
import time
#My modules

if platform == 'android':
    import StripeAndroid as Stripe
if platform == 'ios':
    import StripeIOS as Stripe

_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

class CardScreen(Screen):
    def __init__(self,**kwargs):
        super(CardScreen, self).__init__(**kwargs)
        self.util = kwargs.get('util')
        layout = self.layout()
        self.add_widget(layout)
        if platform in ["ios","android"]:
            self.stripe = Stripe.StripeToken()
            self.stripeUtil = Stripe.StripeUtil()
            self.stripeUtil.stripekey = _key

    def layout(self):
        self.paymentDict = {}
        self.card  = False
        self.year  = False
        self.month = False
        self.cvc   = False

        def on_text_email(instance, value):
            var1 = str(value).find('.') +2
            var2 = len(str(value))
            if (str(value).find('.')+2 < len(value)) and (len(value) > 4) and (str(value).find('@')>0):
                self.email = True
                self.util.email = value
            else:
                self.email = False
            setButtonColor()

        def on_text_card(instance, value):
            if len(value) == 16:
                self.card = True
                self.paymentDict['card'] = str(value)
            else:
                self.card = False
            setButtonColor()

        def on_text_month(instance, value):
            if len(value) == 2:
                self.month = True
                self.paymentDict['month'] = str(value)
            else:
                self.month = False
            setButtonColor()

        def on_text_year(instance, value):
            if len(value) == 4:
                self.year = True
                self.paymentDict['year'] = str(value)
            else:
                self.year = False
            setButtonColor()

        def on_text_cvc(instance, value):
            if len(value) == 3:
                self.cvc = True
                self.paymentDict['cvc'] = str(value)
            else:
                self.cvc = False
            setButtonColor()

        layout = FloatLayout()

        #Email Address
        emailBox = BoxLayout()
        emailField = MDTextField(size_hint_x=.9)
        emailField.hint_text = "Email Address"
        emailField.bind(text=on_text_email)
        emailBox.add_widget(emailField)

        #Credit Card Input
        cardNumberBox = BoxLayout()
        blankWidget1  = MDLabel(text='',size_hint_x=.1)
        blankWidget2  = MDLabel(text='',size_hint_x=.1)
        self.creditCardField = MDTextField(size_hint_x=.8)
        self.creditCardField.hint_text = "Credit Card Number"
        self.creditCardField.input_filter = 'int'
        self.creditCardField.max_text_length = 16
        self.creditCardField.bind(text=on_text_card)
        cardNumberBox.add_widget(blankWidget1)
        cardNumberBox.add_widget(self.creditCardField)
        cardNumberBox.add_widget(blankWidget2)

        #Exp date input
        expDateBox = BoxLayout()
        blankWidget3 = MDLabel(text='',size_hint_x=.1)
        blankWidget5 = MDLabel(text='',size_hint_x=.1)
        self.expMonth = MDTextField(size_hint_x=.4) # This is the color used by the textfield
        self.expMonth.hint_text = "Exp Month"
        self.expMonth.input_filter = 'int'
        self.expMonth.max_text_length = 2
        self.expMonth.bind(text=on_text_month)
        self.expYear  = MDTextField(size_hint_x=.4)
        self.expYear.hint_text = "Exp Year"
        self.expYear.input_filter = 'int'
        self.expYear.max_text_length = 4
        self.expYear.bind(text=on_text_year)

        expDateBox.add_widget(blankWidget3)
        expDateBox.add_widget(self.expMonth)
        expDateBox.add_widget(self.expYear)
        expDateBox.add_widget(blankWidget5)

        #CVC
        cvcBox = BoxLayout()
        blankWidget7 = MDLabel(text='',size_hint_x=.1)
        self.cvcTextField = MDTextField(size_hint_x=.4)
        self.cvcTextField.hint_text   = "CVC"
        self.cvcTextField.helper_text = "3 digit number on back of card"
        self.cvcTextField.helper_text_mode = "on_focus"
        self.cvcTextField.input_filter = "int"
        self.cvcTextField.bind(text=on_text_cvc)
        blankWidget8 = MDLabel(text='',size_hint_x=.5)
        cvcBox.add_widget(blankWidget7)
        cvcBox.add_widget(self.cvcTextField)
        cvcBox.add_widget(blankWidget8)

        #Combined Boxes into
        combinedBox = BoxLayout(orientation='vertical',size_hint_y=.5)
        combinedBox.add_widget(emailBox)
        combinedBox.add_widget(cardNumberBox)
        combinedBox.add_widget(expDateBox)
        combinedBox.add_widget(cvcBox)
        paymentAnchor = AnchorLayout(anchor_x='center',anchor_y='top',padding=[100])
        paymentAnchor.add_widget(combinedBox)

        proceedBox = BoxLayout()
        blankWidget13 = MDLabel(text='')
        proceedButton = MDRaisedButton(text='Proceed')
        proceedButton.md_bg_color = [0.9, 0, 0, 0.9]

        self.app = App.get_running_app()
        def setButtonColor():
            if all([self.email,self.card,self.year,self.month,self.cvc]):
                proceedButton.md_bg_color = self.app.theme_cls.primary_color
                proceedButton.bind(on_press=lambda x: self.processInformation())
            else:
                proceedButton.unbind

        blankWidget14 = MDLabel(text='')
        proceedBox.add_widget(blankWidget13)
        proceedBox.add_widget(proceedButton)
        proceedBox.add_widget(blankWidget14)
        proceedAnchor = AnchorLayout(anchor_x='center',anchor_y='center',padding=[60])
        proceedAnchor.add_widget(proceedBox)
        # #Combine all together
        layout.add_widget(paymentAnchor)
        layout.add_widget(proceedAnchor)

        return layout

    def processInformation(self):
        self.card  = False
        self.year  = False
        self.month = False
        self.cvc   = False

        self.creditCardField.text = ''
        self.expYear.text = ''
        self.expMonth.text = ''
        self.cvcTextField.text = ''

        #Create pop up for process delay
        stripelabel = MDLabel(text='Authenticating', halign='center', valign='center')
        stripelabel.color = App.get_running_app().theme_cls.primary_color
        stripelabel.font_style = 'Body2'
        self.stripepopup = Popup(title='',
                                 content=stripelabel,
                                 size_hint=(None, None), size=(400, 400))
        self.stripepopup.separator_color = App.get_running_app().theme_cls.primary_color
        self.stripepopup.background = str(Atlas('{}round_shadow.atlas'.format(images_path)))
        self.stripepopup.open()

        if platform in ["ios", "android"]:
            #THIS IS WHERE STRIP STARTS
            #send all the card info to stripe
            #to generate a token
            self.stripe.genToken(self.stripeUtil,self.paymentDict['card'], int(self.paymentDict['month']), int(self.paymentDict['year']), self.paymentDict['cvc'])
            self.paymentDict = {}
            #Now we wait for stripe to generate our token
            self.event = Clock.schedule_interval(self.set_popup, 0.1)
        else:
            self.event = Clock.schedule_interval(self.os_error_popup, 0.1)

    def os_error_popup(self,dt):
        self.stripepopup.content = MDLabel(text="Stripe only \nWorks in ios\n and Android")
        time.sleep(2)
        self.stripepopup.dismiss()
        self.event.cancel()

    def set_popup(self, dt):
        #This section acts as a callback for our stripe token
        #Once it is no longer empty, proceed to check the token
        #for authenticity
        if self.stripeUtil.token != "":
            #Error token "Your card's number is invalid"
            if 'invalid' in self.stripeUtil.token:
                self.stripepopup.content = MDLabel(text="Invalid \nCard")
                time.sleep(1)
                self.stripepopup.dismiss()
                self.event.cancel()
            else:
                #Send the stripe token to your server and wait for your rsp
                status = self.stripe.sendToken(self.util,self.stripeUtil.token,self.util.email)
                if status == True:
                    self.stripepopup.content = MDLabel(text="Created user \nsuccesfully")
                    time.sleep(1)
                    self.stripepopup.dismiss()
                    self.event.cancel()
                else:
                    self.stripepopup.content = MDLabel(text="Authenticating \nFailed")
                    time.sleep(1)
                    self.stripepopup.dismiss()
                    self.event.cancel()

    def clearTextFields(self):
        self.securityCode.text = ''
        self.zipcode.text = ''
        self.experationMonth.text = ''
        self.experationYear.text = ''
        self.cardNumber.text = ''
        self.Name.text = ''




