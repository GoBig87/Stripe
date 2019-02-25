from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.textfields import MDTextField
from kivymd.button import MDRaisedButton
from kivy.clock import Clock
from kivy.atlas import Atlas
from kivymd import images_path
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.atlas import Atlas
from kivymd import images_path
from kivy.uix.popup import Popup
from kivy.utils import platform
from kivy.app import App
from kivymd.label import MDLabel
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

if platform == 'android':
    import StripeAndroid as Stripe
if platform == 'ios':
    import StripeIOS as Stripe

class StripeMD(BoxLayout):
    def __init__(self,**kwargs):
        super(StripeMD, self).__init__(**kwargs)
        self.util = kwargs.get('util')
        key = kwargs.get('key')
        layout = self.layout()
        self.add_widget(layout)
        if platform in ["ios","android"]:
            self.stripe = Stripe.StripeToken()
            self.stripeUtil = Stripe.StripeUtil()
            self.stripeUtil.stripekey = key
        
    def layout(self):

        self.paymentDict = {}
        self.card = False
        self.year = False
        self.month = False
        self.cvc = False

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

        layout = BoxLayout(
            orientation='vertical',
            padding=(2 * dp(48), 2 * dp(48))
        )
        # Credit Card Input
        self.creditCardField = MDTextField()
        self.creditCardField.hint_text = "Credit Card Number"
        self.creditCardField.input_filter = 'int'
        self.creditCardField.max_text_length = 16
        self.creditCardField.bind(text=on_text_card)
        layout.add_widget(self.creditCardField)

        # Exp date input
        dateBox = BoxLayout()
        self.expMonth = MDTextField()  # This is the color used by the textfield
        self.expMonth.hint_text = "Exp Month"
        self.expMonth.input_filter = 'int'
        self.expMonth.max_text_length = 2
        self.expMonth.bind(text=on_text_month)
        self.expYear = MDTextField()
        self.expYear.hint_text = "Exp Year"
        self.expYear.input_filter = 'int'
        self.expYear.max_text_length = 4
        self.expYear.bind(text=on_text_year)
        dateBox.add_widget(self.expMonth)
        dateBox.add_widget(self.expYear)
        layout.add_widget(dateBox)
        # CVC
        cvcBox = BoxLayout()
        self.cvcTextField = MDTextField()
        self.cvcTextField.hint_text = "CVC"
        self.cvcTextField.helper_text = "3 digit number on back of card"
        self.cvcTextField.helper_text_mode = "on_focus"
        self.cvcTextField.input_filter = "int"
        self.cvcTextField.bind(text=on_text_cvc)
        blankWidget8 = MDLabel(text='')
        cvcBox.add_widget(self.cvcTextField)
        cvcBox.add_widget(blankWidget8)
        layout.add_widget(cvcBox)

        # Combined Boxes into
        proceedButton = MDRaisedButton(text='Enter Credit Card', size_hint=(None, None), size=(4 * dp(48), dp(48)))
        proceedButton.md_bg_color = [0.9, 0, 0, 0.9]
        # proceedButton.bind(on_press=lambda x: self.processInformation(paymentDict))
        self.app = App.get_running_app()

        def setButtonColor():
            if all([self.card, self.year, self.month, self.cvc]):
                proceedButton.md_bg_color = self.app.theme_cls.primary_color
                proceedButton.text = 'Proceed'
                proceedButton.bind(on_press=lambda x: self.processInformation())
            else:
                proceedButton.unbind

        # proceedButton.bind(on_press=lambda x: self.processInformation(paymentDict))
        proceedAnchor = AnchorLayout(anchor_x='center', anchor_y='bottom')
        proceedAnchor.add_widget(proceedButton)
        # #Combine all together
        layout.add_widget(proceedAnchor)
        # layout.add_widget(self.NavDrawer)

        content = Builder.load_string(spinner)
        self.authenPopup = Popup(title='Authenticating Card', title_align='center',
                                 size_hint=(None, None), size=(dp(200), dp(200)))
        self.authenPopup.add_widget(content)
        self.authenPopup.title_font = 'data/fonts/Roboto-Bold.ttf'
        self.authenPopup.title_color = App.get_running_app().theme_cls.primary_color
        self.authenPopup.separator_color = App.get_running_app().theme_cls.primary_color
        self.authenPopup.background = str(Atlas('{}round_shadow.atlas'.format(images_path)))

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
        self.authenPopup.open()

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
        self.authenPopup.titel ="Stripe only \nWorks in ios\n and Android"
        time.sleep(2)
        self.authenPopup.dismiss()
        self.event.cancel()

    def set_popup(self, dt):
        #This section acts as a callback for our stripe token
        #Once it is no longer empty, proceed to check the token
        #for authenticity
        if self.stripeUtil.token != "":
            #Error token "Your card's number is invalid"
            if 'invalid' in self.stripeUtil.token:
                self.authenPopup.title = "Invalid Card"
                time.sleep(1)
                self.authenPopup.dismiss()
                self.event.cancel()
            else:
                #Send the stripe token to your server and wait for your rsp
                status = self.util.sendTokenToServer(self.stripeUtil.token,self.util.user)
                if status == True:
                    self.authenPopup.content ="Created user succesfully"
                    time.sleep(1)
                    self.authenPopup.dismiss()
                    self.event.cancel()
                else:
                    self.authenPopup.content = "Authenticating Failed"
                    time.sleep(1)
                    self.authenPopup.dismiss()
                    self.event.cancel()

    def clearTextFields(self):
        self.securityCode.text = ''
        self.zipcode.text = ''
        self.experationMonth.text = ''
        self.experationYear.text = ''
        self.cardNumber.text = ''
        self.Name.text = ''