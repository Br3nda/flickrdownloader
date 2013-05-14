import flickrapi, os, urllib, argparse
from datetime import date
from _config import apikey, apisecret
import shutil

ordinal = 734100
days_per_fetch=365


print apikey
print apisecret

import logging
flickrapi.set_log_level(logging.DEBUG)
flickr = flickrapi.FlickrAPI(apikey, secret=apisecret)

(token, frob) = flickr.get_token_part_one(perms='read')
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

print "token = %s"%(token)

while True:

    #work out the dates
##    from_date = date.fromordinal(ordinal)
##    to_date = date.fromordinal(ordinal + days_per_fetch)
##    print "fetching {fromdate} to {todate}".format(
##        fromdate=from_date.strftime("%Y-%m-%d"),
##        todate=to_date.strftime("%Y-%m-%d"),
##        privacy_filter=3)
        
    ordinal += days_per_fetch

    #fetch the photos
##    for photo in flickr.walk(user_id='36251685@N00',
##        min_taken_date=from_date.strftime("%Y-%m-%d"),
##        max_taken_date=to_date.strftime("%Y-%m-%d"),
##        media='videos',
##        privacy_filter=3):
    for photo in flickr.photos_search(
            user_id='36251685@N00',
##        min_taken_date=from_date.strftime("%Y-%m-%d"),
##        max_taken_date=to_date.strftime("%Y-%m-%d"),
            media='videos',
            privacy_filter='3',
            per_page=10)[0]:
            
##    min_taken_date=2010-11-24&max_taken_date=2011-11-24&privacy_filter=3&media=videos&format=rest
#&auth_token=72157633468807171-867d9080b670bd57&api_sig=3119ccff4d38e61f55b89880c2693bc0
        
        if photo.get('ispublic'):
            print "Public!"
        else:
            print "Private"
        
    

##        #print "Getting info"
##        photo_id = photo.get('id')
##        secret = photo.get('secret')
##        orig_secret = photo.get('originalsecret')
##
##        folder = '{year}-{month}'.format(year=from_date.strftime("%Y"), month=from_date.strftime("%m"))
##        if not os.path.exists(folder):
##            os.mkdir(folder)
##
##        filename = "{folder}/{photo_id}.jpg".format(folder=folder, photo_id=photo_id)
##        old_filename = '{folder}/{photo_id}_{secret}_o.jpg'.format(folder=folder, secret=orig_secret, photo_id=photo_id)
##
##        if os.path.exists(filename) or os.path.exists(old_filename):
##            print "\tskipping"
##
##        else:
##            sizes = flickr.photos_getSizes(photo_id=photo.get('id'), secret=photo.get('secret'))[0]
##            url = sizes[-1].get('source')
##            media = sizes[-1].get('media')
##            
##            
##            print "\t" + url
##            if media == 'video':
##                (tmp_filename, headers) = urllib.urlretrieve(url)
##                
##                #touch the jpeg filename, so this video isn't re-fetched
##                f = open(filename, 'w')
##                f.write('.')                
##                
##                #read the original filenamefrom the http headers
##                cd =headers['Content-Disposition']
##                filename = cd.replace('attachment; filename=', '{folder}/'.format(folder=folder))
##                
##                #move to real filename
##                shutil.move(tmp_filename, filename)
##                
##
##            else:
##                (filename, headers) = urllib.urlretrieve(url, filename)
##            print headers
    assert False
