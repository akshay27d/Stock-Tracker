import pymongo
from pymongo import MongoClient
import datetime

from pandas_datareader import data
import pandas as pd

def getStockData(ticker, start_date, Prices, end_date=datetime.datetime.now().strftime("%Y-%m-%d")):
	''' 
	ticker should be turned to a list
	dates format is YYYY-MM-DD
	'''
	start_date = start_date.split(' ')[0]
	data_source = 'google'

	entryData={}
	try:
		panel_data = data.DataReader([ticker], data_source, start_date, end_date)
		all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
		close = panel_data.ix['Close'].reindex(all_weekdays).fillna(method='ffill')
	
		rows = close.index

		entryData={'name':ticker}
		for date in rows:
			fdate = date.strftime('%Y-%m-%d')
			pval = close[ticker][date]
			entryData[fdate] = pval
	except Exception:
		print(ticker+"-------"+start_date+'------'+end_date)

	return entryData

def insertToPrices(tickers, Prices):
	bulk = Prices.initialize_ordered_bulk_op()
	for i in tickers:
		exist = Prices.find_one({'name': i[0]})
		if exist == None:
			newInsert = getStockData(i[0], i[1], Prices)
			bulk.insert(newInsert)
		else:
			print('Unfinished Code')
			return None
			newInsert = getStockData(i[0], '''find last date tested''', Prices)
			bulk.insert(newInsert)
	try:
		bulk.execute()
	except Exception:
		None

def main():
	client = MongoClient('localhost', 27017)		#Connect to database
	db = client.StockTracker
	Prices = db.Prices
	Count = db.Count

	dbData = Count.find({}, {'_id':0, 'name': 1, 'timestamps':1}).sort('name', pymongo.ASCENDING)	#Get stocks and times to look for
	tickers = []
	for stock in dbData:
		tickers.append([stock['name'], stock['timestamps'][0]])

	# insertToPrices(tickers, Prices)



	'''Resetter'''
	# Prices.delete_many({})			
	# post= {"name": stock_to_enter, datetime.datetime.utcnow().strftime("%Y-%m-%d"): "39.44"}}
	# Prices.insert_one(post)

	# print(db.collection_names(include_system_collections=False))

	Prices.delete_many({'name':{ "$exists" : False }})
	look = Prices.find({}).sort('name',pymongo.DESCENDING)

	for each in look:
		print(each)
	print(Count.count())

if __name__ == "__main__":
	main()










