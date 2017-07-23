import pymongo
from pymongo import MongoClient
import datetime

from pandas_datareader import data
import pandas as pd

def getStockData(tickers, start_date, end_date):
	''' 
	tickers is a list
	dates format is YYYY-MM-DD
	'''
	data_source = 'google'

	panel_data = data.DataReader(tickers, data_source, start_date, end_date)
	all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
	close = panel_data.ix['Close'].reindex(all_weekdays).fillna(method='ffill')

	return close

def main():
	client = MongoClient('localhost', 27017)		#Connect to database
	db = client.StockTracker
	Prices = db.Prices

	stock_to_enter = input('Stock to enter: ')


	'''Resetter'''
	# Prices.delete_many({})			
	# post= {"name": stock_to_enter, datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"): "39.44"}}
	# Prices.insert_one(post)

	post= {"name": stock_to_enter, datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"): "39.44"}
	Prices.insert_one(post)

	print(db.collection_names(include_system_collections=False))

	look = Prices.find({})

	for each in look:
		print(each)

if __name__ == "__main__":
	main()