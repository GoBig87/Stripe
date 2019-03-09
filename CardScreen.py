#Kivy
from kivy.uix.screenmanager import Screen
from stripewidget.StripeMD import StripeMD

_key = 'your_stripe_key_here'

class CardScreen(Screen):
    def __init__(self,**kwargs):
        super(CardScreen, self).__init__(**kwargs)
        self.util = kwargs.get('util')
        layout = self.layout()
        self.add_widget(layout)

    def layout(self):
        return StripeMD(util=self.util,key=_key)








