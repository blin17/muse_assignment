# Daily Muse Coding Assignment
Scrapes Muse API's jobs endpoint and answers 'How many jobs with the location "New York City Metro Area" were published from September 1st to 30th 2016?'


**Requirements**
- Python 2.7
- MYSQL 5.7.11

**Usage** 

1. Edit script to include paramters for your own db connection: 
	```
	db = mysql.connector.connect(host='localhost',user='root',password='082092', db='the_muse')
	```

2. Run script with following args: 
	```bash
	$ python main.py --pages=99
	```

	```
	optional arguments:
	--pages   Enter # pages to scrape Daily Muse Jobs endpoint
	```

**Production Ready Changes**
- [ ] Build separate classes for each table using Python ORM
- [ ] Build checker to see if API schema has changed
- [ ] Check for updates in result in addition to duplicates
- [ ] Handle DB exceptions without client seeing them
