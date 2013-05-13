import flickrapi, os, urllib, argparse
from datetime import date
from _config import apikey, apisecret

ordinal = 734100
days_per_fetch=30

def retrieve(photo, filename):
	info = flickr.photos_getInfo(photo_id=photo.get('id'), secret=photo.get('secret'))
	originalsecret = info[0].get('originalsecret')

	#http://farm9.staticflickr.com/8518/8366707744_94cd8f8f01_o.jpg
	#http://farm9.staticflickr.com/8518/8366707744_94cd8f8f01_o.jpg
        if photo.get('originalsecret'):

		url = 'http://farm{farm}.staticflickr.com/{server}/{id}_{secret}_o.jpg'.format(
			farm=photo.get('farm'),
			server=photo.get('server'),
			id=photo.get('id'),
			secret=originalsecret)
	else:
		url = 'http://farm{farm}.staticflickr.com/{server}/{id}_{secret}_o.jpg'.format(
			farm=photo.get('farm'),
			server=photo.get('server'),
			id=photo.get('id'),
			secret=secret)
	print "\t" + url

	try:
		urllib.urlretrieve(url, filename)
	except Exception, e:
		print e



flickr = flickrapi.FlickrAPI(apikey, secret=apisecret)
while True:

	#work out the dates
	from_date = date.fromordinal(ordinal)
	to_date = date.fromordinal(ordinal + days_per_fetch)
	print "fetching {fromdate} to {todate}".format(
		fromdate=from_date.strftime("%Y-%m-%d"),
		todate=to_date.strftime("%Y-%m-%d"),
		privacy_filter=3)
	ordinal -= days_per_fetch

	#fetch the photos
	for photo in flickr.walk(user_id='36251685@N00',
	        min_taken_date=from_date.strftime("%Y-%m-%d"),
	        max_taken_date=to_date.strftime("%Y-%m-%d")):
	    
		#print "Getting info"
		photo_id = photo.get('id')
		secret = photo.get('secret')
		orig_secret = photo.get('originalsecret')

		folder = '{year}-{month}'.format(year=from_date.strftime("%Y"), month=from_date.strftime("%m"))
		if not os.path.exists(folder):
			os.mkdir(folder)

		filename = "{folder}/{photo_id}.jpg".format(folder=folder, photo_id=photo_id)
		old_filename = '{folder}/{photo_id}_{secret}_o.jpg'.format(folder=folder, secret=orig_secret, photo_id=photo_id)
		
		print "\t" + filename,
		if os.path.exists(filename) or os.path.exists(old_filename):
			print "\tskipping"

		else:
                	retrieve(photo, filename=filename)

	
