# qpy:kivy
import kivy

kivy.require('1.10.1')
from kivy.app import App
from kivy.utils import platform

if platform == "ios":
    from os.path import join, dirname
    import kivy.garden

    kivy.garden.garden_app_dir = join(dirname(__file__), "libs", "garden")
if platform == "android":
    import androidPermissions

from kivy.uix.screenmanager import ScreenManager

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivymd.theming import ThemeManager
from kivymd.label import MDLabel


from CardScreen import CardScreen
from ChargeScreen import ChargeScreen
from ConnectionScreen import ConnectionScreen
from UserScreen import UserScreen

import utility

main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout

NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        canvas:
            Rectangle:
                size: root.size
                pos: root.pos
        NavigationDrawerToolbar:
            title: "Welcome!"
        NavigationDrawerIconButton:
            id: user
            icon: 'account-settings'
            text: "Set User"
            on_press: app.root.content.current = 'user'
            on_release: [[ 'menu' , lambda x:  app.root.nav_drawer.toggle()]]
        NavigationDrawerIconButton:
            id: network
            icon: 'ethernet'
            text: "Setup Network"
            on_press: app.root.content.current = 'network'
            on_release: [[ 'menu' , lambda x:  app.root.nav_drawer.toggle()]]
        NavigationDrawerIconButton:
            id: card
            icon: 'credit-card'
            text: "Credit Card"
            on_press: app.root.content.current = 'card'
            on_release: [[ 'menu' , lambda x:  app.root.nav_drawer.toggle()]]
        NavigationDrawerIconButton:
            id: charge
            icon: 'cash-usd'
            text: "Create Charge"
            on_press: app.root.content.current = 'charge'
            on_release: [[ 'menu' , lambda x: app.root.nav_drawer.toggle()]]  
        NavigationDrawerIconButton:
            id: exit
            icon: 'exit-to-app'
            text: "Return"
            on_press: [[ 'menu' , lambda x:  app.root.nav_drawer.toggle()]]                   

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        Toolbar:
            id: toolbar
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [[ 'menu' , lambda x: root.toggle_nav_drawer()]]

        Image:
            id: 'stripe'
            source: 'stripe_imgs/Stripe_logo.png'
            allow_stretch: True
            keep_ratio: True
            valign: 'center'
            halign: 'center'
            size_hint: None,None
            size: 2*dp(60),root.theme_cls.standard_increment

    '''


class MainBox(FloatLayout):
    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        self.util = kwargs.get('util')

        self.navbar = AnchorLayout(anchor_x='center', anchor_y='top')
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')

        self.toolbar = Builder.load_string(main_widget_kv)

        self.content = ScreenManager()
        self.content.add_widget(UserScreen(name='user',util =self.util))
        self.content.add_widget(CardScreen(name='card',util =self.util))
        self.content.add_widget(ChargeScreen(name='charge',util =self.util))
        self.content.add_widget(ConnectionScreen(name='network',util =self.util))
        self.screens.add_widget(self.content)

        self.add_widget(self.screens)
        self.add_widget(self.toolbar)


class MainApp(App):
    theme_cls = ThemeManager()
    # theme_cls.primary_palette = 'Teal'
    # theme_cls.primary_hue = '300'
    nav_drawer = ObjectProperty()

    def build(self):
        util = utility.Utility()
        if platform is 'android':
            perms = ["android.permission.INTERNET"]
            androidPermissions.acquire_permissions(perms)
        return MainBox(util=util)


if __name__ == "__main__":
    MainApp().run()







