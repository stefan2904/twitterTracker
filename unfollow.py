import tweepy
from config import *
from array import array
from datetime import datetime

## TODO: Use more functions. ;-)
## TODO: more elegant way to append content at the begining of the file (logBuffer)

# == Config== ================================================================

followerFile = "follower.dat"

logFile = "unfollow.html"

logLine = "<div class='%s'><a href='https://twitter.com/%s'><strong>%s</strong></a> %s at %s, now at %d followers</div>"

timestamp = "%d-%02d-%02d %02d:%02d" % (datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute)

DEBUG = True # Debug Output?

# == Helper Methods == =========================================

logBuffer = " " # logFile Cache 

def writeFollow(name, followerCnt):
	writeLog(name, followerCnt, "followed")

def writeUnfollow(name, followerCnt):
	writeLog(name, followerCnt, "unfollowed")

def writeSuspended(name, followerCnt):
	writeLog(name, followerCnt, "suspended")

def writeLog(name, followerCnt, action):
	mydebug(name + " " + action)
	global logBuffer
	ll = (logLine % (action, name, name, action, timestamp, followerCnt)) + '\n'
	logBuffer = ll + logBuffer

def saveLog():
	f = file(logFile, "r")
	oldLog = f.read()
	f.close()

	f = file(logFile, "w")
	f.write(logBuffer)
	f.write(oldLog)
	f.close()

def mydebug(txt):
	if(DEBUG == True):
		print txt

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

mydebug("Loaded %d follower-ids from Twitter" % len(newFollowerList))

# == Load old follower-list == ===============================================
init = False

oldFollowerList = array('i')
try:
	f = file(followerFile,"rb")
except IOError:
	init = True

if not init:
	try:
	    oldFollowerList.fromfile(f, 20000)
	except EOFError:
	    pass
	f.close()

	mydebug("Read %d follower-ids from file" % len(oldFollowerList))

# == Find (un)follows == =====================================================
if not init:
	unfollows = list(set(oldFollowerList) - set(newFollowerList))
	follows = list(set(newFollowerList) - set(oldFollowerList))

	mydebug("there are " + str(len(unfollows)) + " unfollows and " + str(len(follows)) + " follows!")
	mydebug("-")

# == identify (un)follows ====================================================
if not init:
	followerCnt = len(newFollowerList)

	for follow in follows:
		try:
			writeFollow(api.get_user(id=follow).screen_name, followerCnt)
		except tweepy.error.TweepError:
			writeSuspended(str(follow), followerCnt)

	for unfollow in unfollows:
		try:
			writeUnfollow(api.get_user(id=unfollow).screen_name, followerCnt)
		except tweepy.error.TweepError:
			writeSuspended(str(unfollow), followerCnt)

	saveLog()

# == Backup current follower-list == =========================================

f = file(followerFile,"wb")
newFollowerList.tofile(f)
f.close()


