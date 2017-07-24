import pymongo
from pymongo import MongoClient
import datetime
import SAlphaScraper

def main():
	client = MongoClient('localhost', 27017)		#Connect to database
	db = client.StockTracker
	Count = db.Count
	Prices = db.Prices

	'''Get data from scraper'''
	dataToEnter = SAlphaScraper.getData()

	'''Update Count Collection'''
	bulk = Count.initialize_ordered_bulk_op()
	for dataPoint in dataToEnter:
		bulk.find({'name': dataPoint[0]}).upsert().update({'$inc': {'mentions': 1}, '$push': {'timestamps': dataPoint[1], 'authors': dataPoint[2]}})
	bulk.execute()

	
	look = Count.find({}, {'_id': False}).sort('name', pymongo.ASCENDING)

	for each in look:
		print(each)
	print(Count.count())

	

if __name__ == "__main__":
	main()


