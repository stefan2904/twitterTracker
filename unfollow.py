import tweepy
from config import *
from array import array

# == Config== ================================================================

followerFile = "follower.dat"

# == OAuth Authentication == =================================================

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# == GET ids of all followers == =============================================

newFollowerList = array('i')

# == create array of current followers == ====================================

for follower in tweepy.Cursor(api.followers_ids).items():
	newFollowerList.append(follower)
	#print len(newFollowerList), "\t", follower

print "Loaded %d follower-ids from Twitter" % len(newFollowerList)

# == Load old follower-list == ===============================================

oldFollowerList = array('i')
f = file(followerFile,"rb")
try:
    oldFollowerList.fromfile(f, 20000)
except EOFError:
    pass
f.close()

print "Read %d follower-ids from file" % len(oldFollowerList)

# == Find (un)follows == =====================================================

unfollows = list(set(oldFollowerList) - set(newFollowerList))
follows = list(set(newFollowerList) - set(oldFollowerList))

print "there are", len(unfollows), "and", len(follows), "follows!"
print ""

# == identify (un)follows ====================================================

for follow in follows:
	print follow, "\t", api.get_user(id=follow).screen_name, "\t followed"

for unfollow in unfollows:
	print unfollow, "\t", api.get_user(id=unfollow).screen_name, "\t unfollowed"

# == Backup current follower-list == =========================================

f = file(followerFile,"wb")
newFollowerList.tofile(f)
f.close()


