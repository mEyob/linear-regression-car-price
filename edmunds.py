import requests
import os
import time
import csv
from bs4 import BeautifulSoup

HERE = os.getcwd()

class Edmunds():

    def __init__(self, model, url, pages):
        self.model = model
        self.first_page = url 
        self.num_pages = pages
        self.page_path = os.path.join(HERE, 'html-files', self.model)

    def fetch_page(self, page_num):
        try:
            pagination = '' if page_num == 1 else '?pagenumber=' + str(page_num)
            url = self.first_page + pagination
            response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
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
            with open(os.path.join(self.page_path,  'Edmunds' + str(page)), 'w') as raw_html:
                response = self.fetch_page(page)
                if response:
                    raw_html.write(response)
                else:
                    problematic_pages += 1
            time.sleep(0.5)
        
        print("{}% of the pages retrieved successfully.".format((1 - (problematic_pages/self.num_pages)) * 100))
    
    def parse(self, raw_html, path):
        count = 0
        processed_listings = []
        for listing in raw_html.find_all('div', class_='srp-card-info'):
            try:
                listing_model = listing.find('a', class_='d-block').text.split()
                mileage = listing.find('span', class_='text-gray-darker').text.split()[0].replace(',','')
                price = listing.find('h3', class_='mb-0').text.replace('$', '').replace(',','')
                
                year, make, model, *detailed_model = listing_model[1:]
                detailed_model = ' '.join(detailed_model)

                processed_listings.append({
                    'Year': year, 
                    'Make': make, 
                    'Model': model, 
                    'Detailed_model': detailed_model, 
                    'Price': price, 
                    'Mileage': mileage,
                    'Website': 'ED'
                    })
                count += 1
            except Exception as e:
                print(e)
                print("Model or detail info not provided")
        if os.getenv("DEBUG"):
            print("{} listings processed".format(count))
        return count, processed_listings

    def header(self, path, csv_header):
        if not os.path.isfile(path):
            with open(path, 'w') as new_file:
                new_file.write(csv_header + '\n')

    def parse_all(self):
        total_listings = 0
        csv_path = os.path.join(HERE, 'car_listings.csv')
        csv_header = "Year,Make,Model,Detailed_model,Price,Mileage,Website"
        self.header(csv_path, csv_header)
        for page in os.listdir(self.page_path):
            if page.startswith('Edmund'):
                with open(os.path.join(self.page_path, page)) as html_file:
                    raw_html = BeautifulSoup(html_file.read(), 'lxml')
                    parsed = self.parse(raw_html, csv_path)
                    total_listings += parsed[0]
                with open(csv_path, 'a') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header.split(','))
                    for listing in parsed[1]:
                        csv_writer.writerow(listing)
        print('Total number of {} cars parsed {}'.format(self.model, total_listings))

if __name__ == "__main__":
    car = Edmunds('ToyotaCamry','https://www.edmunds.com/used-toyota-camry/',44)
    car.fetch_all_pages()
    car.parse_all()

