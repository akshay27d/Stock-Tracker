import pymongo
from pymongo import MongoClient
import datetime
from pytz import timezone
import SAlphaScraper
from pymongo.errors import BulkWriteError


def main():
	client = MongoClient('localhost', 27017)		#Connect to database
	db = client.StockTracker
	Count = db.Count
	Prices = db.Prices
	Log = db.Log

	'''Get data from scraper'''
	try:
		lastSearch = Log.find().sort('searchTimes', pymongo.DESCENDING).limit(1)[0]['searchTimes']
	except Exception:
		lastSearch = '2000-01-01 00:00'
	
	dataToEnter = SAlphaScraper.getData(lastSearch)

	tz = timezone('EST')
	formattedTime = tz.localize(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M")
	Log.insert_one({'searchTimes': formattedTime})

	'''Update Count Collection'''
	bulk = Count.initialize_ordered_bulk_op()
	newEntries=0
	for dataPoint in dataToEnter:
		bulk.find({'name': dataPoint[0]}).upsert().update({'$inc': {'mentions': 1}, '$push': {'timestamps': dataPoint[1], 'authors': dataPoint[2]}})
		newEntries+=1
	try:
		bulk.execute()
	except Exception:
		None
	
	look = Count.find({}, {'_id': False}).sort('mentions', pymongo.DESCENDING)

	for each in look:
		print(each)
	print(Count.count())

	print('New Entries: ' + str(newEntries))

	

if __name__ == "__main__":
	main()


