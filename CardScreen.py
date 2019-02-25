#Kivy
from kivy.uix.screenmanager import Screen
from stripe.StripeMD import StripeMD

_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

class CardScreen(Screen):
    def __init__(self,**kwargs):
        super(CardScreen, self).__init__(**kwargs)
        self.util = kwargs.get('util')
        layout = self.layout()
        self.add_widget(layout)

    def layout(self):
        return StripeMD(util=self.util,key=_key)








