import requests
import json
import argparse
import mysql.connector
from dateutil.parser import parse



def create_table_query(db_cursor, table_name, query):
	'''
	Checks to see if table exists. If it does not, then we create the table

	Args: connector cursor, table name, create table query
	Returns: None
	'''
	try:
		table_check_query = 'SELECT 1 FROM {0}'.format(table_name)
		db_cursor.execute(table_check_query)
	except mysql.connector.Error as err:
		if err.errno == 1146:
			cursor.execute(query)
		else:
			table_exception = 'Error creating {0} database'.format(table_name)
			raise Exception(table_exception)

def get_api_content(page):
	'''
	Retrieves Jobs from Muse API

	Args: page_num
	Returns: results
	'''
	url="https://api-v2.themuse.com/jobs?page={0}".format(page)
	content = requests.get(url).content
	results = json.loads(content)
	if 'error' in results:
		raise Exception('Muse API did not work')
	return results


# main
db = mysql.connector.connect(host='localhost',user='root',password='******', db='the_muse')
cursor = db.cursor(buffered=True)
parser = argparse.ArgumentParser(description='Process args for daily muse coding challenge')
parser.add_argument('--pages', type=int, 
					help='Enter # pages to scrape Daily Muse Jobs endpoint',
					required = False)
args = parser.parse_args()
pages = 0

if args.pages:
	print args.pages
	if args.pages < 1:
		raise Exception('Invalid # of pages number. Must be greater than 0')
	else:
		pages = args.pages



jobs_query = ("CREATE TABLE jobs("
						"id VARCHAR(255) NOT NULL PRIMARY KEY,"
						"company_id VARCHAR(255),"
						"contents TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,"
						"model_type VARCHAR(255),"
						"name VARCHAR(255),"
						"publication_date DATETIME,"
						"shortname VARCHAR(255),"
						"type VARCHAR(255)"
						");")
create_table_query(cursor, 'jobs', jobs_query)

companies_query = ('CREATE TABLE companies('
						'id VARCHAR(255) NOT NULL PRIMARY KEY,'
						'name VARCHAR(255),'
						'short_name VARCHAR(255)'
						');')
create_table_query(cursor, 'companies', companies_query)

job_categories_query = ('CREATE TABLE job_categories('
						'job_id VARCHAR(255),'
						'category VARCHAR(255),'
  						'PRIMARY KEY (job_id, category)'
						');')
create_table_query(cursor, 'job_categories', job_categories_query)

job_locations_query = ('CREATE TABLE job_locations('
						'job_id VARCHAR(255),'
						'location VARCHAR(255),'
  						'PRIMARY KEY (job_id, location)'
						');')
create_table_query(cursor, 'job_locations', job_locations_query)

	job_refs_query = ('CREATE TABLE job_refs('
					'job_id VARCHAR(255),'
					'landing_page VARCHAR(255),'
						'PRIMARY KEY (job_id, landing_page)'
					');')
create_table_query(cursor, 'job_refs', job_refs_query)

job_tags_query = ('CREATE TABLE job_tags('
				'job_id VARCHAR(255),'
				'tag_name VARCHAR(255),'
				'tag_short_name VARCHAR(255),'
					'PRIMARY KEY (job_id, tag_name)'
				');')
create_table_query(cursor,'job_tags', job_tags_query)


for page in range(pages):
	s = get_api_content(page)
	for result in s['results']:
		job_insert_query = ("INSERT INTO jobs (id,company_id,contents,model_type,name,publication_date ,shortname ,type) "
							"VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
		try:
			cursor.execute(job_insert_query, (result['id']
											, result['company']['id']
											, result['contents'].encode("utf-8")
											, result['model_type']
											, result['name']
											, parse(result['publication_date']).strftime('%Y-%m-%d %H:%M:%S')
											, result['short_name']
											, result['type']))
		except mysql.connector.Error as err:
			if err.errno != 1062:
				print err
		
		company_insert_query = ("INSERT INTO companies (id, name, short_name) VALUES (%s,%s,%s)")
		try:
			cursor.execute(company_insert_query, (result['company']['id']
												, result['company']['name']
												, result['company']['short_name']))
		except mysql.connector.Error as err:
			if err.errno != 1062:
				print err

		for item in result['categories']:
			categories_insert_query = ("INSERT INTO job_categories (job_id, category) VALUES (%s,%s)")
			try:
				cursor.execute(categories_insert_query, (result['id'], item['name']))
			except mysql.connector.Error as err:
				if err.errno != 1062:
					print err

		for item in result['locations']:
			categories_insert_query = ("INSERT INTO job_locations (job_id, location) VALUES (%s,%s)")
			try:
				cursor.execute(categories_insert_query, (result['id'], item['name']))
			except mysql.connector.Error as err:
				if err.errno != 1062:
					print err
		
		categories_insert_query = ("INSERT INTO job_refs (job_id, landing_page) VALUES (%s,%s)")
		try:
			cursor.execute(categories_insert_query, (result['id'], result['refs']['landing_page']))
		except mysql.connector.Error as err:
			print err
			if err.errno != 1062:
				print err

		for item in result['tags']:
			categories_insert_query = ("INSERT INTO job_tags (job_id, tag_name, tag_short_name) VALUES (%s,%s,%s)")
			try:
				cursor.execute(categories_insert_query, (result['id'], item['name'], item['short_name']))
			except mysql.connector.Error as err:
				if err.errno != 1062:
					print err

		for item in result['levels']:
			categories_insert_query = ("INSERT INTO job_levels (job_id, level_name, level_short_name) VALUES (%s,%s,%s)")
			try:
				cursor.execute(categories_insert_query, (result['id'], item['name'], item['short_name']))
			except mysql.connector.Error as err:
				if err.errno != 1062:
					print err


query = ('SELECT COUNT(*) FROM jobs j JOIN job_locations l ON j.id = l.job_id '
		'WHERE l.location = %s '
		'AND j.publication_date > %s '
		'AND j.publication_date < %s '
		)

cursor.execute(query, ('New York City Metro Area','2016-9-1','2016-9-30'))
print(cursor.fetchone())
db.commit()
cursor.close()
db.close()
