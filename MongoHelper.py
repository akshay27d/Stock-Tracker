import pymongo
from pymongo import MongoClient
import sys

def main():
	client = MongoClient('localhost', 27017)		#Connect to database
	db = client.StockTracker
	Count = db.Count
	Prices = db.Prices
	Log = db.Log

	if sys.argv[1]== 'deletecl':
		Count.delete_many({})
		Log.delete_many({})
	elif sys.argv[1]== 'deletep':
		Prices.delete_many({})
	elif sys.argv[1]== 'show':
		if sys.argv[2] == 'Count':
			look = Count.find({}, {'name': 1, 'mentions':1, '_id':0}).sort('name', pymongo.DESCENDING)
			totalDataPoints=0
			for each in look:
				print(each)
				totalDataPoints+= int(each['mentions'])
			print('Stocks: '+ str(Count.count()))
			print('Data Points: ' + str(totalDataPoints))
		elif sys.argv[2] == 'Prices':
			look = Prices.find({}).sort('name', pymongo.ASCENDING)
			totalDataPoints=0
			for each in look:
				print(each)
				doc=Prices.find_one({},{'_id':0, 'name':0});
				count=0
				for key in doc:
					count +=1
				totalDataPoints+= count
			print('Stocks: '+ str(Prices.count()))
			print('Data Points: ' + str(totalDataPoints))

if __name__ == "__main__":
	main()