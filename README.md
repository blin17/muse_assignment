# Daily Muse Coding Assignment
Scrapes Muse API's jobs endpoint and answers 'How many jobs with the location "New York City Metro Area" were published from September 1st to 30th 2016?'

**Usage**
Run script with following args: 

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
