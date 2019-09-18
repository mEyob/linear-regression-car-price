import requests
import os
import time
import csv
from bs4 import BeautifulSoup

HERE = os.getcwd()

class CarGurus():

	def __init__(self, model, url, pages):
		self.num_pages = pages
		self.model = model
		self.first_page = url
		self.page_path = os.path.join(HERE, 'html-files', self.model)

	def fetch_page(self, page_num):
		if page_num == 1:
			try:
				response = requests.get(self.first_page)
			except Exception as e:
				raise e
		else:
			try:
				response = requests.get(self.first_page + '#resultsPage=' + str(page_num))
			except:
				return None
		if response.status_code in range(200, 299):
			return response.text
	
	def fetch_all_pages(self):

		problematic_pages = 0
		if not os.path.exists(self.page_path):
			os.makedirs(self.page_path)
		for page in range(1, self.num_pages + 1):
			if os.getenv("DEBUG"):
				print("Fetching {} of {} Pages".format(page, self.num_pages))
			with open(os.path.join(self.page_path,  'Page' + str(page)), 'w') as raw_html:
				response = self.fetch_page(page)
				if response:
					raw_html.write(response)
				else:
					problematic_pages += 1
			time.sleep(0.5)
		
		print("{}% of the pages retrieved successfully.".format((1 - (problematic_pages/self.num_pages)) * 100))
	def header(self, path, csv_header):
		if not os.path.isfile(path):
			with open(path, 'w') as new_file:
				new_file.write(csv_header + '\n')
	def parse_all(self):
		total_listings = 0
		csv_path = os.path.join(HERE, 'car_listings.csv')
		csv_header = "Year,Make,Model,Detailed_model,Price,Mileage"
		self.header(csv_path, csv_header)
		for page in os.listdir(self.page_path):
			with open(os.path.join(self.page_path, page)) as html_file:
				raw_html = BeautifulSoup(html_file.read(), 'lxml')
				parsed = self.parse(raw_html, csv_path)
				total_listings += parsed[0]
			with open(csv_path, 'a') as csv_file:
				csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header.split(','))
				for listing in parsed[1]:
					csv_writer.writerow(listing)
		print('Total number of {} cars parsed {}'.format(self.model, total_listings))
	def parse(self, raw_html, path):
		count = 0
		processed_listings = []
		for listing in raw_html.find_all(['div','span'], class_="cg-dealFinder-result-wrap"):
			try:
				listing_model = listing.find(['div','span','h4'], class_="cg-dealFinder-result-model")
				listing_detail = listing.find(['div','span'], class_="cg-dealFinder-result-stats")
				
				listing_model = listing_model.text.split()[:-6]
				year = listing_model[0]
				make = listing_model[1]
				model = listing_model[2]
				detailed_model = ' '.join(listing_model[3:])

				listing_detail = listing_detail.text.split()
				price = listing_detail[1].replace('$','').replace(',','')
				mileage = listing_detail[3].replace(',','')

				processed_listings.append({
					'Year': year, 
					'Make': make, 
					'Model': model, 
					'Detailed_model': detailed_model, 
					'Price': price, 
					'Mileage': mileage
					})
				count += 1
			except:
				print("Model or detail info not provided")
		if os.getenv("DEBUG"):
			print("{} listings processed".format(count))
		return count, processed_listings

if __name__ == '__main__':
	# Testing the CarGurus class with Honda Accord
	url = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=forSaleTab_false_0&newSearchFromOverviewPage=true&inventorySearchWidgetType=AUTO&entitySelectingHelper.selectedEntity=d585&entitySelectingHelper.selectedEntity2=&zip=02169&distance=50&searchChanged=true&modelChanged=true&filtersModified=true&sortType=undefined&sortDirection=undefined'
	car = CarGurus('HondaAccord', url, 66)

	# car.fetch_all_pages()

	car.parse_all()

