from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import random
import time


agents = [
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
]


userAgent = random.choice(agents)

headers = {
	'User-Agent': userAgent
}

link = "https://www.instagram.com/kushinii/"



browser = webdriver.PhantomJS()
browser.get(link)




SCROLL_PAUSE_TIME = 1.5

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")





linksList = []

#GET ALL POSTS LINK

while True:
	browser.execute_script("window.scrollTo(0, 100000);")
	time.sleep(SCROLL_PAUSE_TIME)
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')
	
	linksBlocksList = soup.findAll("div", {"class":"v1Nh3"})
	apendedCount = 0
	
	for link in linksBlocksList:
		link = link.find("a", href=True)
		if link['href'] not in linksList:
			linksList.append(link['href'])
			apendedCount +=1
	if apendedCount != 0:
		print("List appended for: %s" % apendedCount)
		continue
	else:
		print("Current page posts count: %s" % len(linksList))
		print("-------------------------HERE ARE THE LINKS--------------------------")
		print(linksList)
		break



posts = []
count = 0
outOf = len(linksList)

for postLink in linksList:
	print("Ready" + str(count) + "from" + str(outOf))
	postLink = "https://www.instagram.com" + postLink
	browser.get(postLink)
	time.sleep(SCROLL_PAUSE_TIME)
	postHtml = browser.page_source
	postSoup = BeautifulSoup(postHtml, 'html.parser')
	postElements = []
	postSoup = postSoup.findAll("li", {"class":"_-1_m6"})

	for element in postSoup:
		postVideos = element.find("video", {"class":"tWeCl"})
		postImages = element.find("img", {"class":"FFVAD"})

		if postVideos:
			element = {
				'type': 'video',
				'imageLink': postVideos['poster'],
				'videoLink': postVideos['src']
			};
			postElements.append(element)
		if postImages:
			element = {
				'type': 'image',
				'imageLink': postImages['src']
			}
			postElements.append(element)
	post = {
		'index': count,
		'postItems': postElements
	}
	posts.append(post)
	count += 1
	
print(posts)
print("------------------------------------------------")
print("HERE IS AN EXAMPLE OF A POST ELEMENTS DICTIONARY")
print("------------------------------------------------")
print(posts[0]['postItems'])
#IF VIDEO then CLASS == tWeCl
#ELSE FFVAD

#driver = webdriver.Firefox()
#driver.get(link)
#page = requests.get(link, headers=headers)
#time.sleep(10)

#linksList = linksBlocksList.findAll("a")




#f = open("parsing.html","w+")

#f.write(soup.prettify())
#f.close()