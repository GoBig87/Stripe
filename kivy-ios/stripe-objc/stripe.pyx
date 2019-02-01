STUFF = "Hi"

cdef extern from "stripe_c.h":
    ctypedef void (*tokenfunc)(const char *name, void *user_data)
    void retrieveToken(char* myKey, char* cardNumber, int expMonth, int expYear, char* cvc,tokenfunc user_func, void *user_data)

def getToken(tokenCallback,myKey,cardNumber,expMonth,expYear,cvc):

    cdef bytes myKey_bytes = myKey.encode('utf-8')
    cdef char* myKey_string = myKey_bytes
    cdef bytes cardNumber_bytes = cardNumber.encode('utf-8')
    cdef char* cardNumber_string = cardNumber_bytes
    cdef bytes cvc_bytes = cvc.encode('utf-8')
    cdef char* cvc_string = cvc_bytes

    retrieveToken(myKey_bytes, cardNumber_bytes, expMonth, expYear, cvc_bytes, callback, <void*>tokenCallback)

cdef void callback(const char *name, void *tokenCallback):
    (<object> tokenCallback).token = (name.decode('utf-8'))