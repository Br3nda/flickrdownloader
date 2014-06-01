import os
import urllib, urllib2
import argparse
from datetime import date
from _config import apikey, apisecret
import shutil
import flickr

# Derive from Request class and override get_method to allow a HEAD request.
class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


ordinal = 733400
days_per_fetch=60

while True:
    from_date = date.fromordinal(ordinal)
    to_date = date.fromordinal(ordinal + days_per_fetch)
        
    
    
    print "Retrieving videos from {date}".format(date=from_date.strftime("%Y-%m-%d"))
    try:
      for video in flickr.photos_search(auth=True,
		      user_id='36251685@N00',
		      min_taken_date=from_date.strftime("%Y-%m-%d"),
		      max_taken_date=to_date.strftime("%Y-%m-%d"),
		      media='videos'):
		      
	  print '{title} {url}'.format(title=video.title, url=video.url)
	  #print video
	  #fetch the photos
	  folder = '{year}-{month}'.format(year=from_date.strftime("%Y"), month=from_date.strftime("%m"))
	  if not os.path.exists(folder):
	      os.mkdir(folder)

	  
	  largest = video.getSizes()[-1]
	  url = largest['source']
	  print "\t Getting headers of {url}".format(url=url)

	  request = HeadRequest(url)
	  response = urllib2.urlopen(request)
	  headers = response.info()

	  cd = headers['Content-Disposition']
	  filename = cd.replace('attachment; filename=', '{folder}/'.format(folder=folder))        
	  print filename

	  if os.path.exists(filename):
	      print "\tskipping"
	      continue
	  print "\t Retrieving {url}".format(url=url)

	  (tmp_filename, headers) = urllib.urlretrieve(url)

	  #move to real filename
	  shutil.move(tmp_filename, filename)
    except Exception, e:
	print e
    else:
	ordinal += days_per_fetch
	    