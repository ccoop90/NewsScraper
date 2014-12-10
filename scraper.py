import readability
import datetime
import calendar
import csv
import time
from tld import get_tld
from readability import ParserClient
import re

domainToName = {"pbs" : "PBS","nytimes" : "NYT",	"washingtonpost" : "WaPo",	"wsj" : "WSJ",	"scientificamerican" : "SciAm",	"latimes" : "LA Times",	"thehill" : "The Hill",	"slate" : "Slate",	"politico" : "Politico",	"bloomberg" : "Bloomberg",	"nature" : "Nature",	"csmonitor" : "CSMonitor",	"nationaljournal" : "NatJo",	"reuters" : "Reuters",	"shanghaidaily" : "Shanghai Daily",	"vox" : "VOX",	"go" : "ABC News",	"mit" : "MIT News Office",	"technologyreview" : "MIT Technology Review",	"businessweek" : "Business Week",	"climatecentral" : "Climate Central",	"bbc" : "BBC",	"usnews" : "US News",	"theguardian" : "The Guardian",	"aljazeera" : "Al Jazeera",	"forbes" : "Forbes",	"npr" : "NPR",	"ap" :"AP",	"wcvb" : "WCVB",	"streetwise" : "Streetwise",	"bostonglobe" : "Boston Globe",	"nbcnews" : "NBC News",	"cnbc" : "CNBC",	"cnn" : "CNN",	"thehindubusinessline" : "The Hindu Business Line",	"smh" : "Sydney Morning Herald",	"cbc" : "CBC News",	"huffingtonpost" : "Huffington Post",	"dw" : "Deutsch Welle",	"cnbcafrica" : "CNBC Africa",	"economist" : "Economist",	"insideclimatenews" : "Inside Climate News",	"bizjourals" : "Business Journal",	"ipsnews" : "Inter Press Service",	"cbslocal" : "CBS Local",	"sciencemag" : "American Association for the Advancement of Science",	"scmp" : "South China Morning Post",	"economictimes" : "The Economic Times",	"trust" : "Thomson Reuters Foundation",	"latimes" : "Los Angeles Times",	"grist" : "Grist",	"marketplace" : "Marketplace",	"deccanchronicle" : "Deccan Chronicle",	"japantimes" : "The Japan Times",	"discovery" : "Discovery",	"india" : "Zee News",	"newrepublic" : "New Republic",	"indiatimes" : "The Times of India",	"ibtimes" : "International Business Times",	"indianexpress" : "The Indian Express",	"theatlantic" : "The Atlantic",	"energybiz" : "Energy Biz", "rtcc" : "Responding to Climate Change" }


monthdic = {"01" : "January", "02" : "February", "03" : "March", "04" : "April", "05" : "May", "06" : "June", "07" : "July", "08" : "August", "09" : "September", "10" : "October", "11" : "November", "12" : "December"}

results=[]

def timeconvert(date):
	try:
		x = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
		day = x[3:5]
		month = x[:2]
		year = x[6:]
		month2 = monthdic[month]
		date = '%s %s, %s' % (month2, day, year)
		return date
	except:
		return

def tounicode(text):
	try:
		return unicode(text).encode('utf-8')
	except:
		print text
		return text

def getDomainName(domain):
	try:
		return domainToName[domain]
	except KeyError:
		return domain

with open('url.csv') as csvfile:
	urls = csvfile.read().split('\r\n')
	for url in urls:
		article = " "
		try:
			parser_client = ParserClient('dab74f9def9312c90473befef4181cf66bab7321')
			parser_response = parser_client.get_article_content(url)
			s = parser_response.content['content']
			x = parser_response.content['date_published']
			title = parser_response.content['title']
			author = parser_response.content['author']
			article = re.sub('href', '', s)
			article1 = re.sub('<img.*?>', '', article)
			article2 = re.sub('<p>','<br>', article1)
			article3 = re.sub('</p>','<br />', article2)
		except:
			print 'fail', url
		results+=[(tounicode(url), tounicode(title), tounicode(author), tounicode(article3), timeconvert(x))]
output = time.strftime('articles-%x.html').replace('/', '_')
with open(output, 'w') as outputfile:
	for result in results:
		url, title, _, _, _ = result
		convert = get_tld(url, as_object=True)
		entry = '<b>%s</b>: <b>%s   <a href="%s">LINK</a></b><br />\r\n' % (getDomainName(convert.domain), title, url)
		outputfile.write(entry)
	outputfile.write('\r\n')
	for result in results:
		url, title, authors, text, time = result
		convert = get_tld(url, as_object=True)
		entry = ' <br/><b>%s</b>: <b>%s</b><br />\r\n<b>By: %s</b><br /><b>%s</b> <br /> %s\r\n\r\n' % (getDomainName(convert.domain), title, authors,tounicode(time), tounicode(text))
		outputfile.write(entry)