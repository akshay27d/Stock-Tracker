import pymongo
from pymongo import MongoClient
import datetime

def main():
	client = MongoClient('localhost', 27017)		#Connect to database
	db = client.StockTracker
	Count = db.Count
	Prices = db.Prices

	stock_to_enter = input('Stock to enter: ')


	'''Resetter'''
	# Count.delete_many({})			
	# post= {"name": stock_to_enter, "mentions": "1", "timestamps": [datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")]}
	# Count.insert_one(post)


	'''Update Count Collection'''
	check = Count.find_one({"name": stock_to_enter})		#Check if stock entry has been found before in 'Count'

	if check == None:						#Not mentioned before
		post= {"name": stock_to_enter, "mentions": "1", "timestamps": [datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")]}
		Count.insert_one(post)
		print("Check 1")
	else:									#Mentioned before
		countNum = check["mentions"]
		timesList = check["timestamps"]
		timesList.append(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"))
		Count.update_one({"name":stock_to_enter}, {"$set": {"mentions": str(int(countNum)+1), "timestamps":timesList}})
		print("Check 2")

	
	look = Count.find({})

	for each in look:
		print(each)

	

if __name__ == "__main__":
	main()


