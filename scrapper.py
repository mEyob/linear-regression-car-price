import argparse
from cargurus import CarGurus
from truecar import TrueCar

URL_list = {
    'carguru':{
        'ToyotaCamry':['https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d292&zip=02169',70],
        'HondaAccord':['https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d585&zip=02169',66],
        'NissanAltima':['https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d237&zip=02169',52],
        'HyundaiSonata':['https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d96&zip=02169',35],
        'VWPassat':['https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d202&zip=02169',20],
        'FordFusion':['https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d845&zip=02169',36],
        'ChevroletMalibu':['https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d622&zip=02169',22]
        },
    'truecar':{
        'ToyotaCamry':['https://www.truecar.com/used-cars-for-sale/listings/toyota/camry/location-quincy-ma/',20],
        'HondaAccord':['https://www.truecar.com/used-cars-for-sale/listings/honda/accord/location-quincy-ma/',18],
        'NissanAltima':['https://www.truecar.com/used-cars-for-sale/listings/nissan/altima/location-quincy-ma/',14],
        'HyundaiSonata':['https://www.truecar.com/used-cars-for-sale/listings/hyundai/sonata/location-quincy-ma/',12],
        'VWPassat':['https://www.truecar.com/used-cars-for-sale/listings/volkswagen/passat/location-quincy-ma/',6],
        'FordFusion':['https://www.truecar.com/used-cars-for-sale/listings/ford/fusion/location-quincy-ma/',16],
        'ChevroletMalibu':['https://www.truecar.com/used-cars-for-sale/listings/chevrolet/malibu/location-quincy-ma/',7]
    }
}

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c","--carGurus", help='Scrape from cargurus.com',action='store_false')
    parser.add_argument("-t", "--trueCar", help="Scrape from truecar.com", action='store_true')

    args = parser.parse_args()

    if args.trueCar:
        website = 'truecar.com'
    else:
        website = 'cargurus.com'
    
    if website == 'truecar.com':
        for make_model, url in URL_list['truecar'].items():
            carlistings = TrueCar(make_model, url[0], url[1])
            carlistings.fetch_all_pages()
            carlistings.parse_all()
    else:
        for make_model, url in URL_list['carguru'].items():
            carlistings = CarGurus(make_model, url[0], url[1])
            carlistings.fetch_all_pages()
            carlistings.parse_all()

if __name__ == '__main__':
    main()





