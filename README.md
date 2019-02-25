# Stripe
An implementation of Stripe payment processing designed for Kivy-ios and python-4-android

## How to install:  

  ###   ANDROID
      For android applications in your buildozer.spec file add
      android.gradle_dependencies = com.stripe:stripe-android:2.1.0,com.android.support:support-v4:24.0.0
      and make sure your android api is set to equal or greater than the follow so your buildozer will use 
      gradle to build your apk
        # (int) Android API to use
        android.api = 24
        # (int) Minimum API required
        android.minapi = 19
        # (int) Android SDK version to use
        android.sdk = 24
  ###   IOS
        IOS apps will need to use the stripe recipe for Kivy-ios that can be located in the Kivy-ios directory of this 
        project. The kivy stripe recipee also requires a patch for the host_setuptools recipee.  Move these two recipees into
        .buildozer/ios/platform/kivy-ios/recipees. Add stripe to your requirements in your buildozer spec file or build 
        them with ./toolchain.py.  Once your recipees have been compiled, open up xcode and click file->add files to project
        and select Stripe.Framework found in this repository under kivy-ios and click "copy files if needed".  Then click 
        add files to project again and add Stripe.bundle and make sure "copy files if needed" is checked again.
   ###  Server
        Demo server will require python modules twisted and stripe and can be installed via pip.
  
## How to use in your app:  
### Create Payment Screen and generate token
    from stripe.StripeMD import StripeMD
    .
    .
    #Then Create a StripeMD instance
    #util needs an object with class variable user and a method sendTokenToServer(token,object.user)
    #This method will send your token to your server to be stored in your database with your token and user tied together
    CreditCardLayout = StripeMD(util=<your server instance>,key=_key)
    layout.add_widget(CreditCardLayout)
    
## How to use in your server:  
    In order to fully implement stripe you will need a server that will store user information in a database
    along with their token.  All charges must be created from your server.
  
  ### Install the Stripe pyton package with pip and import
    import stripe
    #Then add your api key
    _stripe_api_key = "your key here"
    stripe.api_key = _stripe_api_key
  
  ### Charge customer
  stripe.Charge.create(amount=amountCharged, currency='usd', description='Add info here', customer=customerToken, capture=False)
  
