from jnius import autoclass,PythonJavaClass,cast,java_method

Integer = autoclass('java.lang.Integer')
String  = autoclass('java.lang.String')

Stripe = autoclass('com.stripe.android.Stripe')
Card  = autoclass('com.stripe.android.model.Card')
Token  = autoclass('com.stripe.android.model.Token')

class PythonTokenCallback(PythonJavaClass):
    __javacontext__ = 'app'
    __javainterfaces__ = ['com.stripe.android.TokenCallback']

    def __init__(self,util):
        self.util = util

    @java_method('(Lcom/stripe/android/model/Token;)V')
    def onSuccess(self,token):
        tok = token.getId()
        self.util.token = str(tok)

    @java_method('[Ljava/lang/Exception;)V')
    def onError(self,error):
        self.util.token = str(error)

class StripeUtil():
    def __init__(self):
        self.token = ''
        self.stripekey = ''

class StripeToken():
    def __init__(self):
        pass

    def genToken(self,util,cardNum,expMon,expYear,cvc):
        jcardNum = cast('java.lang.String', String(cardNum))
        jexpMon = cast('java.lang.Integer', Integer(expMon))
        jexpYear = cast('java.lang.Integer', Integer(expYear))
        jcvc = cast('java.lang.String', String(cvc))
        card = Card(jcardNum,jexpMon,jexpYear,jcvc)
        if not card.validateCard():
            print 'Card Not Valid'
            return False
        stripe = Stripe(util.stripekey)
        token_cb = PythonTokenCallback(util)
        stripe.createToken(card,token_cb)

