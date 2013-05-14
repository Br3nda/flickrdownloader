import os
import urllib, urllib2
import argparse
from datetime import date
from _config import apikey, apisecret
import shutil
import flickr

##permission = "read"
##
##
#### The following line links the class Auth() into a variable
#### so that the methods within can be used.
##
##myAuth = flickr.Auth()
##
##
#### The following line gets a "frob". The frob will change
#### each time you call it, and it needs to be the same
#### throughout the authentication process, so once it is
#### put into a variable, that variable will be used in future.
##
##frob = myAuth.getFrob()
##
##
#### The following line generates a link that the user needs
#### to be sent to. The user must be logged into Flickr in the
#### browser that is opened, and it will ask if it wishes to
#### allow your program to access it. Your API KEY must be
#### setup correctly within Flickr for this to work. See
#### below if you have any problems.
####
#### The permissions and frob variable are passed onto
#### the link method.
##
##link = myAuth.loginLink(permission,frob)
##
##
#### The following line just lets the user know they need
#### to be logged in, and gives them a chance to before
#### the rest of the script is processed.
##
##raw_input("Please make sure you are logged into Flickr in Firefox")
##
##
#### The following opens the link in Firefox under a Linux installation
#### There is a better way, but this way is fine for now.
##
##firefox=os.popen( 'firefox \"' + link + '\"' )
##
##
#### A firefox window will open asking the user if they wish to allow
#### your program/api key to access their account. Once they have
#### allowed it, the program can continue, so you need to ask
#### the user if they have.
##
##raw_input("A Firefox window should have opened. Press enter when you have authorized this program to access your account")
##
##
#### A token is needed, which can now be generated with the
#### following line of code.
##
##token = myAuth.getToken(frob)
##
##
#### This token cannot be got again, so the program will
#### need to store it somewhere. The following lines
#### of code will save it to token.txt in the current
#### working directory.
##
##f = file('token.txt','w')
##f.write(token)
##f.close()


# Derive from Request class and override get_method to allow a HEAD request.
class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


ordinal = 733400
days_per_fetch=1

while True:
    from_date = date.fromordinal(ordinal)
    to_date = date.fromordinal(ordinal + days_per_fetch)
        
    ordinal += days_per_fetch
    
    print "Retrieving photos from {date}".format(date=from_date.strftime("%Y-%m-%d"))
    for photo in flickr.photos_search(auth=True,
                        user_id='36251685@N00',
                        min_taken_date=from_date.strftime("%Y-%m-%d"),
                        max_taken_date=to_date.strftime("%Y-%m-%d"),
                        media='photos'):
                        
        print '{title} {url}'.format(title=photo.title, url=photo.url)
        #print video
        #fetch the photos
        

        folder = '{year}-{month}'.format(year=from_date.strftime("%Y"), month=from_date.strftime("%m"))
        if not os.path.exists(folder):
            os.mkdir(folder)

        filename = '{folder}/{id}.jpg'.format(folder=folder, id=photo.id)
        
        if os.path.exists(filename):
            print "\tskipping"
        else:
            largest = photo.getSizes()[-1]
            url = largest['source']
            print "\t Retrieving {url}".format(url=url)
            
            (filename, headers) = urllib.urlretrieve(url, filename)


