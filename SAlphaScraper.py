import time as sleeper
import requests
from bs4 import BeautifulSoup
import datetime
from pytz import timezone
import random

def getMonth(month):
	return {
		'Jan':'01',
		'Feb':'02',
		'Mar':'03',
		'Apr':'04',
		'May':'05',
		'Jun':'06',
		'Jul':'07',
		'Aug':'08',
		'Oct':'10',
		'Nov':'11',
		'Dec':'12'
	}[month.strip()]

def formatDate(timeSplit):
	if len(timeSplit) ==2:
		tz = timezone('EST')
		formattedTime = tz.localize(datetime.datetime.now())

		first = timeSplit[1].strip()[:5]
		if len(first.strip()) == 4:
			first = '0'+first.strip()
		second = timeSplit[1].strip()[5:].strip()

		if second =='PM' and int(first.split(':')[0]) <12:
			timeofday = str(int(first.split(':')[0])+12)+':'+first.split(':')[1]
		else:
			timeofday = first

		if timeSplit[0] == 'Today':
			formattedTime = formattedTime.strftime("%Y-%m-%d") + " "+ timeofday
		elif timeSplit[0] == 'Yesterday':
			formattedTime = formattedTime - datetime.timedelta(days=1)
			formattedTime = formattedTime.strftime("%Y-%m-%d")+ " "+ timeofday

	else:
		first = timeSplit[3].strip()[:5]
		if len(first.strip()) == 4:
			first = '0'+first.strip()
		second = timeSplit[3].strip()[5:].strip()

		if second =='PM' and int(first.split(':')[0]) <12:
			timeofday = str(int(first.split(':')[0])+12)+':'+first.split(':')[1]
		else:
			timeofday = first

		formattedTime = '2017-'+ getMonth(timeSplit[1])+'-'+ timeSplit[2].strip()+" "+timeofday.strip()
	return formattedTime


def getData(lastSearch):
	retData=[]

	for iterator in range(1,30):
		print('Iteration #'+str(iterator))
		url = 'https://seekingalpha.com/stock-ideas?page='+str(iterator)
		
		#'User-Agent': '/Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
		ua = {1:'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
		2:'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
		3:'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
		4:'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}
		headers = {'User-Agent':ua[random.randrange(1,5)]}
		r = requests.get(url, headers=headers)

		soup = BeautifulSoup(r.content, "html.parser")
		try:
			articles_list = soup.find_all('ul', {'id':'articles-list'})[0].find_all('div',{'class':'a-info'})
			count=0
			count2=0
			for listing in articles_list:
				count+=1
				try:
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
						if formattedDate > lastSearch:
							count2+=1
							articleData = [stock_mentions.get_text(), formattedDate, specific_author.get_text()]
							retData.append(articleData)
				except Exception:
					print('Lost an Article')
			print(count)
			print(count2)
			sleeper.sleep(10)
		except Exception:
			print("Lost a Page")
	return retData

if __name__ == '__main__':
	getData()






















