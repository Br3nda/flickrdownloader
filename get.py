import os
import time
import urllib, urllib2
import argparse
from datetime import date
import datetime
from _config import apikey, apisecret
import shutil
import flickr
import sys



# Derive from Request class and override get_method to allow a HEAD request.
class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


def main():
  try:
    start_date = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d');
  except Exception, e:
    raise 
    start_date = date.today()

  ordinal =  start_date.toordinal()
  days_per_fetch=1

  while True:
    from_date = date.fromordinal(ordinal)
    to_date = date.fromordinal(ordinal + days_per_fetch)
    print "============= {from_date} ====================".format(from_date=from_date)
      
    try:
      get_photos(from_date, to_date)
      get_videos(from_date, to_date)
    except Exception, e:
      print e
    finally:
      ordinal -= days_per_fetch


def ensure_folder_exists(folder):
  for i in range(5, len(folder.split('/')) + 1):
      folder_to_check = '/'.join(folder.split('/')[:i])
      if not os.path.exists(folder_to_check):
        os.mkdir(folder_to_check)


def get_photos(from_date, to_date):
  print "\tRetrieving photos from {date}".format(date=from_date.strftime("%Y-%m-%d"))
  
  ##PHOTOS on this day
  for photo in flickr.photos_search(auth=True,
        user_id='36251685@N00',
        min_taken_date=from_date.strftime("%Y-%m-%d"),
        max_taken_date=to_date.strftime("%Y-%m-%d"),
        media='photos'):
        
    print "\t\t * Found a photo: {title} {url}".format(title=photo.title, url=photo.url)
    folder = '/home/brenda/Photos/{year}/{month}/{day}'.format(year=from_date.strftime("%Y"), month=from_date.strftime("%m"), day=from_date.strftime("%d"))
    
    ensure_folder_exists(folder)
    
    filename = '{folder}/{id}.jpg'.format(folder=folder, id=photo.id)
    
    if os.path.exists(filename):
        print "\t\t * skipping {filename}".format(filename=filename)
        return
    
    largest = photo.getSizes()[-1]
    url = largest['source']
    print "\t\t * Retrieving: {url}".format(url=url)
    print "\t\t * Saving to: {filename}".format(filename=filename)
    
    (filename, headers) = urllib.urlretrieve(url, filename)  

def get_videos(from_date, to_date):
  """
  VIDEOS on this day
  """
  print "\tRetrieving videos from {date}".format(date=from_date.strftime("%Y-%m-%d"))
  for video in flickr.photos_search(auth=True,
      user_id='36251685@N00',
      min_taken_date=from_date.strftime("%Y-%m-%d"),
      max_taken_date=to_date.strftime("%Y-%m-%d"),
      media='videos'):
        
    print "\t\t * Found a video: {title} {url}".format(title=video.title, url=video.url)
    #print video
    #fetch the photos
    folder = '{year}-{month}'.format(year=from_date.strftime("%Y"), month=from_date.strftime("%m"))
    
    ensure_folder_exists(folder)
    
    largest = video.getSizes()[-1]
    url = largest['source']
    print "\t\t * Getting headers of {url}".format(url=url)

    request = HeadRequest(url)
    response = urllib2.urlopen(request)
    headers = response.info()

    cd = headers['Content-Disposition']
    filename = cd.replace('attachment; filename=', '{folder}/'.format(folder=folder))        

    if os.path.exists(filename):
        print "\t\t * Skipping {filename}".format(filename=filename)
        continue
    print "\t Retrieving {url}".format(url=url)

    (tmp_filename, headers) = urllib.urlretrieve(url)

    #move to real filename
    shutil.move(tmp_filename, filename)
    
    
    
main()

  
