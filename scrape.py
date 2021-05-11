import requests as req
import os
from bs4 import BeautifulSoup
import math
import csv
import re


resp = req.get("https://webgate.ec.europa.eu/competition/transparency/public?lang=de")
soup = BeautifulSoup(resp.text, features="html.parser")
csrf_token = soup.find('input', {'name':'CSRFTOKEN'})['value']

resp = req.head("https://webgate.ec.europa.eu/competition/transparency/public?lang=de")
cookies = resp.headers['Set-Cookie']

post_url = 'https://webgate.ec.europa.eu/competition/transparency/public/search/results'
form_data  = 'CSRFTOKEN=' + csrf_token + '&resetSearch=true&countries=CountryAUT&aidMeasureTitle=covid&aidMeasureCaseNumber=&refNo=&beneficiaryMs-input=&beneficiaryNationalId=&beneficiaryName=&beneficiaryTypes-input=&regions-input=&sectors-input=&aidInstruments-input=&objectives-input=&nominalAmountFrom=&nominalAmountTo=&grantedAmountFrom=&grantedAmountTo=&currency=EUR&dateGrantedFrom=01%2F01%2F2020&dateGrantedTo=31%2F12%2F2021&grantingAuthorityNames-input=&entrustedEntities-input=&financialIntermediaries-input='
curl = 'curl -v -d "' + form_data + '" -X POST ' + post_url + " -H 'Cookie: " + cookies + "'"
pages_html = os.popen(curl).read()
soup = BeautifulSoup(pages_html, features="html.parser")
tags = soup.find_all('a')
pages = int(tags[-7].text)

pages = math.ceil(pages / 10)
urlbase = 'https://webgate.ec.europa.eu/competition/transparency/public/search/results?max=100&sort=beneficiary.name&order=asc&offset='
cookie = 'Cookie: ' + cookies

i = 1
offset = 0
while i <= pages:
	curl = "curl '" + urlbase + str(offset) + "' -H '" + cookie + "' -o raw" + str(i) + ".html"
	os.system(curl)
	i += 1
	offset += 100

i = 1
while i <= pages:
	filename = 'raw' + str(i) + '.html'
	file = open(filename)
	html = file.read()
	file.close() 

	soup = BeautifulSoup(html, features="html.parser")
	data = []
	table = soup.find('table')
	table_body = table.find('tbody')

	rows = table_body.find_all('tr')

	for row in rows:
	    cols = row.find_all('td')
	    cols = [re.sub('\s+',' ',ele.text) for ele in cols]
	    data.append([ele for ele in cols])

	with open('data.csv', 'a') as f:
	    write = csv.writer(f)
	    write.writerows(data)
	
	i += 1

