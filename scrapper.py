import argparse
from cargurus import CarGurus

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
    'cartrader':{
        'ToyotaCamry':['',],
        'HondaAccord':['',],
        'NissanAltima':['',],
        'HyundaiSonata':['',],
        'VWPassat':['',],
        'FordFusion':['',],
        'ChevroletMalibu':['',]
    }
}

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c","--carGurus", help='Scrape from cargurus.com',action='store_false')
    parser.add_argument("-t", "--carTrader", help="Scrape from cartrader.com", action='store_true')

    args = parser.parse_args()

    if args.carTrader:
        print('Here')
        website = 'cartrader.com'
    else:
        website = 'cargurus.com'
    
    if website == 'cargurus.com':
        for make_model, url in URL_list['carguru'].items():
            carlistings = CarGurus(make_model, url[0], url[1])
            carlistings.fetch_all_pages()
            carlistings.parse_all()

if __name__ == '__main__':
    main()





