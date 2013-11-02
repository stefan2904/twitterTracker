
from config import *
from array import array

## TODO: Use more functions. ;-)
## TODO: more elegant way to append content at the begining of the file (logBuffer)

# == Config== ================================================================

followerFile = "follower.dat"


# == Load  follower-list == ===============================================

oldFollowerList = array('L')
try:
	f = file(followerFile,"rb")
except IOError:
	init = True

try:
    oldFollowerList.fromfile(f, 20000)
except EOFError:
    pass
f.close()

print "Read %d follower-ids from file" % len(oldFollowerList)

# == convert ====================================================
newFollowerList = array('L')

for follow in oldFollowerList:
	newFollowerList.append(long(follow))
	print "was", type(follow), "is now", type(long(follow))

f = file(followerFile,"wb")
newFollowerList.tofile(f)
f.close()
