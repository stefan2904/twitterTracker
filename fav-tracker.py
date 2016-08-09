from __future__ import absolute_import, print_function
import config as settings

from tweepy import OAuthHandler
from tweepy import API

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.


auth = OAuthHandler(settings.consumer_key, settings.consumer_secret)
auth.secure = True
auth.set_access_token(settings.access_token, settings.access_token_secret)

api = API(auth)

# print('Hi, %s!' % api.me().name)

tweets = api.favorites(page=1)

print('Loaded %d tweets ... ' % len(tweets))

for tweet in tweets:
    print('%d by %s: %s' % (tweet.id, tweet.author.screen_name, tweet.text.replace('\n', ' ')))


