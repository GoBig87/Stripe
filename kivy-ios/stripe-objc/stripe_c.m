#import <Foundation/Foundation.h>
#import "Stripe/PublicHeaders/STPCardParams.h"
#import "Stripe/PublicHeaders/STPAPIClient.h"
#import "Stripe/PublicHeaders/STPToken.h"
#import <Foundation/NSError.h>
#import <Foundation/NSString.h>

#include "stripe_c.h"

@implementation retToken

- (void) retrieveTokenObjC:(char*)myKey andcardNumber:(char*)cardNumber andexpMonth:(int)expMonth andexpYear:(int)expYear andcvc:(char*)cvc anduser_func:(tokenfunc)user_func anduser_data:(void*)user_data {

    NSString* NScardNumber = [NSString stringWithUTF8String:cardNumber];
    NSString* NScvc = [NSString stringWithUTF8String:cvc];
    STPCardParams *cardParams = [[STPCardParams alloc] init];
    cardParams.number = NScardNumber;
    cardParams.expMonth = expMonth;
    cardParams.expYear = expYear;
    cardParams.cvc = NScvc;
    NSString *myPublishableKey = [NSString stringWithUTF8String:myKey];
    STPAPIClient *apiClient = [[STPAPIClient alloc] initWithPublishableKey:myPublishableKey];
    [apiClient createTokenWithCard:cardParams completion:^(STPToken *token,NSError *error) {
        if (token == nil || error != nil) {
            const char* errorChar = [error.localizedDescription UTF8String];
            user_func(errorChar,user_data);
        } else {
            const char* tokenChar = [token.tokenId UTF8String];
            user_func(tokenChar,user_data);
        }
    }];
}

@end

void retrieveToken(char* myKey, char* cardNumber, int expMonth, int expYear, char* cvc,tokenfunc user_func, void *user_data){

    retToken* retrieveToken = [[retToken alloc] init];
    [retrieveToken retrieveTokenObjC:myKey andcardNumber:cardNumber andexpMonth:expMonth andexpYear:expYear andcvc:cvc anduser_func:user_func anduser_data:user_data];
}