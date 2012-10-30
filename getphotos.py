import flickrapi, os, urllib, argparse
from datetime import date
from _config import apikey, apisecret

#ordinal = 730000
ordinal = 734100
days_per_fetch=90

flickr = flickrapi.FlickrAPI(apikey, secret=apisecret)
while True:

	#work out the dates
	from_date = date.fromordinal(ordinal)
	to_date = date.fromordinal(ordinal + days_per_fetch)
	print "fetching {fromdate} to {todate}".format(
		fromdate=from_date.strftime("%Y-%m-%d"),
		todate=to_date.strftime("%Y-%m-%d"),
		privacy_filter=3)
	ordinal += days_per_fetch

	if (to_date.year < 2005):
		next

	#fetch the photos
	for photo in flickr.walk(user_id='36251685@N00',
	        min_taken_date=from_date.strftime("%Y-%m-%d"),
	        max_taken_date=to_date.strftime("%Y-%m-%d")):
	    
		try:	
			print '{id} "{title}"'.format(id=photo.get('id'), title=photo.get('title'))
		except:
			pass
		
		#print "Getting info"
		#info = flickr.photos_getInfo(photo_id=photo.get('id'), secret=photo.get('secret'))

		url = 'http://farm{farm}.staticflickr.com/{server}/{id}_{secret}_o.jpg'.format(
			farm=photo.get('farm'),
			server=photo.get('server'),
			id=photo.get('id'),
			secret=photo.get('secret'))
		filename = url.split('/')[-1]
		print url
		print filename
		
		folder = '{year}-{month}'.format(year=from_date.strftime("%Y"), month=from_date.strftime("%m"))
		if not os.path.exists(folder):
			os.mkdir(folder)

		filename = "{folder}/{filename}".format(folder=folder, filename=filename)
		if os.path.exists(filename):
			print "skipping"
		else:
			try:
				urllib.urlretrieve(url, filename)
			except Exception, e:
				print e


	if to_date.year > 2012:
		break	



	
