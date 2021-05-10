import os
from bs4 import BeautifulSoup
import csv
import re

####
# Example config (copy cookie header from browser)
urlbase = 'https://webgate.ec.europa.eu/competition/transparency/public/search/results?max=100&sort=beneficiary.name&order=asc&offset='
cookie = 'Cookie: WSC2SESSIONID=4upX0EJZojh9s44fh-85bNeZJV5j-GwwEDWmI6QADKtswc-GIufb!-924730375; dtCookie=-18$NA1I93E9HNBGHABCLULR6FTSFVKTOUDQ; rxVisitor=16204166952836PBBSFEB8DEM2H09U2DNBD2D51K1KAFI; dtSa=-; rxvt=1620418496357|1620416695294; dtPC=-18$416695215_448h-vMOMTKQWRWBNKPUAEGHUDUQMJCKTJCBHC-0e1; dtLatC=1; fontSize=1'
pages = 113
####

i = 1
offset = 0
while i <= pages:
	curl = "curl '" + urlbase + str(offset) + "' -H '" + cookie + "' -o " + str(i) + ".html"
	print(curl)
	os.system(curl)
	i += 1
	offset += 100

i = 1
while i <= pages:
	filename = str(i) + '.html'
	file = open(filename)
	html = file.read()
	file.close() 

	soup = BeautifulSoup(html)
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
