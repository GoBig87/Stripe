# Stripe
An implementation of Stripe payment processing designed for Kivy-ios and python-4-android

How to install:
  ANDROID
    For android applications in your buildozer.spec file add
    android.gradle_dependencies = com.stripe:stripe-android:2.1.0,com.android.support:support-v4:24.0.0
    and make sure your android api is set to equal or greater than the follow so your buildozer will use gradle to build your apk
      # (int) Android API to use
      android.api = 24
      # (int) Minimum API required
      android.minapi = 19
      # (int) Android SDK version to use
      android.sdk = 24
  IOS
    IOS apps will need to use the stripe recipe for Kivy-ios that can be located in the Kivy-ios directory of this project.  The kivy         stripe recipee also requires a patch for the host_setuptools recipee.  Move these two recipees into .buildozer/ios/platform/kivy-         ios/recipees. Add stripe to your requirements in your buildozer spec file or build them with ./toolchain.py.  Once your recipees have     been compiled, open up xcode and click file->add files to project and select Stripe.Framework found in this repository under kivy-ios     and click "copy files if needed".  Then click add files to project again and add Stripe.bundle and make sure "copy files if needed" is     checked again.
   Server
    Demo server will require python modules twisted and stripe and can be installed via pip.
    
How to use in your app:
    First import Stripe in your project
    if platform == 'android':
        import StripeAndroid as Stripe
    if platform == 'ios':
        import StripeIOS as Stripe
        
    if platform in ["ios","android"]:
        self.stripe = Stripe.StripeToken()
        self.stripeUtil = Stripe.StripeUtil()
        self.stripeUtil.stripekey = 'your token from stripe here'
     
     #Collect user credit card information and send to stripe
     #Use the genToken method of the StripeToken object to generate a stripe token
     self.stripe.genToken(self.stripeUtil, cardNum, expMonth, expYear, cvc)
     
     #Once the genToken function has been called wait for self.stripeUtil.token to be populated with a token
     #When self.stripeUtil.token is no longer empty, check the response for errors then send the token to your server
     #Error token response "Your card's number is invalid"
      if 'invalid' in self.stripeUtil.token:
        #alert app with error
      else:
          #Use the sendToken method of the StripeToken object to send the token to your server
          #in order to do this you will need to create a utitlity class to send the token to your server
          status = self.stripe.sendToken(self.util,self.stripeUtil.token,self.util.email)
          if status == True:
              #Return true from your server if everything is ok
          else:
              #If there is an error return false from your server
    
    #you will need to create a utility class to send your token to your server
    #When you send this object inside the sendToken method it will call the sendTokenToServer method
    class Utility():
        def __init__(self):
            self.address = ''
            self.socket = ''
            self.email  = ''

        def sendTokenToServer(self,token,email):
            #This method is where you format on how you want
            #to send your stripe token to your server.
            msg = ast.literal_eval(
             '{"function": "client_token", "token":"' + token + '", "email":"' + email + '"}')
            rsp = self.connectToServer(self.host, self.port, msg)
            if rsp['rsp'] == 'Created new user succesfully.':
                return True
            else:
                return False

          
