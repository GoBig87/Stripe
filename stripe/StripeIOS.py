from stripe.stripe import getToken

class StripeUtil():
    def __init__(self):
        self.token = ''
        self.stripekey = ''

class StripeToken():
    def __init__(self):
        pass

    def genToken(self,util,cardNum,expMon,expYear,cvc):
        getToken(util,util.stripekey, cardNum, expMon, expYear, cvc)

    def sendToken(self,util,token,email):
        return util.sendTokenToServer(token,email)



