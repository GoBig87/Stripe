//
//  STPCard+Private.h
//  Stripe
//
//  Created by Ben Guo on 1/4/17.
//  Copyright © 2017 Stripe, Inc. All rights reserved.
//

#import "STPCard.h"
#import "STPInternalAPIResponseDecodable.h"

NS_ASSUME_NONNULL_BEGIN

@interface STPCard () <STPInternalAPIResponseDecodable>

+ (STPCardFundingType)fundingFromString:(NSString *)string;
+ (nullable NSString *)stringFromFunding:(STPCardFundingType)funding;
- (nullable STPAddress *)address;

@end

NS_ASSUME_NONNULL_END
