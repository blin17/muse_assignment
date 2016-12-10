# Daily Muse Coding Assignment

## Usage

Run script with following args: 

  ```bash
  $ python main.py --pages=99
  ```

  ```
  optional arguments:
    --pages   Enter # pages to scrape Daily Muse Jobs endpoint
  ```

**Would Add**
- [ ] Instead of checking duplicates on job id, check against DB to see if there are any changes
- [ ] Build checker to see if API schema has changed
- [ ] Build separate classes for each table using Python ORM
- [ ] Handle DB exceptions without client seeing them
