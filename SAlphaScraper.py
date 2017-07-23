import requests
from bs4 import BeautifulSoup
import datetime
from pytz import timezone

def getMonth(month):
	return str({
		'Jan':1,
		'Feb':2,
		'Mar':3,
		'Apr':4,
		'May':5,
		'Jun':6,
		'Jul':7,
		'Aug':8,
		'Sep':9,
		'Oct':10,
		'Nov':11,
		'Dec':12
	}[month.strip()])

def formatDate(timeSplit):
	if len(timeSplit) ==2:
		tz = timezone('EST')
		formattedTime = datetime.datetime.now(tz)
		if timeSplit[0] == 'Today':
			formattedTime = formattedTime.strftime("%Y-%m-%d")
		else:
			formattedTime = formattedTime - datetime.timedelta(days=1)
			formattedTime = formattedTime.strftime("%Y-%m-%d")

	else:
		formattedTime = '2017-'+ getMonth(timeSplit[1])+'-'+ timeSplit[2].strip()
	return formattedTime


def getData():
	url = 'https://seekingalpha.com/stock-ideas'
	r = requests.get(url)

	soup =BeautifulSoup(r.content, "html.parser")

	# found = soup.find_all('a', attrs={'price':'58.46'})
	articles_list = soup.find('ul', {'id':'articles-list'}).find_all('div', {'class':'a-info'})

	retData=[]

	for listing in articles_list:
		specific_article = listing.find_all('a', {'title': True})
		specific_author = listing.find('a', {'title': None})
		if listing.find('span', {'class': 'editors-pick-yellow-text'}) == None:
			specific_time = listing.find_all('span')[2]
		else:
			specific_time = listing.find_all('span')[4]

		for stock_mentions in specific_article:
			time = specific_time.get_text().replace('.',',')
			timeSplit= time.split(',')
			formattedDate = formatDate(timeSplit)
			articleData = [stock_mentions.get_text(), formattedDate, specific_author.get_text()]
			retData.append(articleData)
	
	return retData

if __name__ == '__main__':
	getData()






















