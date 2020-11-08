import json, time
from bs4 import BeautifulSoup
from helper import is_bot, driver



def listing_scrapper(username, listing_type, driver=driver):
    base_url = "https://www.propertyguru.com.sg/agent/"
    parameter = f'?listing_type={listing_type}'
    page_num = 1
    listings = []
    listing_dict_in = {
        "listing_title" : None,
        "listing_location" : None,
        "listing_price" : None,
        "listing_bed" : None,
        "listing_bath" : None,
        "listing_area" : None,
        "listing_property_type": None
    }
    while True:
        target_url = base_url + username + '/' + str(page_num) + parameter
        driver.get(target_url)
        page_src = driver.page_source
        parsed_page = BeautifulSoup(page_src, 'lxml')
        if is_bot(parsed_page):
            print('Bot detected waiting for 60 seconds')
            time.sleep(60)
            continue
        agent_listings = parsed_page.find('div', {'class':'listing-widget-new'})       
        if agent_listings:     
            agent_listings = agent_listings.find_all('div', {'class':'listing-card'})
            for listing in agent_listings:
                listing_dict = listing_dict_in
                img = listing.find('img')
                if img:
                    listing_img_url = img.get('data-original')     
                    # listing_img_str = image_to_str(listing_img_url)     
                    # agent_profile['lisgint_img'] = listing_img_str                                                       
                
                try:
                    listing_title = img.get('alt').split('-')[-1]
                    listing_dict['listing_title'] = listing_title
                except: pass
                
                listing_location = listing.find('span', {'itemprop':'streetAddress'})
                listing_dict['listing_location'] = (listing_location.text if listing_location else None)
                
                currency = listing.find('span', {'class':'currency'})
                price = listing.find('span', {'class':'price'})
                listing_dict['listing_price'] = (currency.text + price.text if currency and price else None)                            
                
                bed = listing.find('span', {'class':'bed'})
                listing_dict['listing_bed'] = (bed.get('title') if bed else None)
                
                bath = listing.find('span', {'class':'bath'})
                listing_dict['listing_bath'] = (bath.get('title') if bath else None)
                
            
                areas = listing.find_all('li', {'class':'listing-floorarea'})
                if areas:
                    area = []
                    for ele in areas:
                        area.append(ele.text)
                    listing_dict['listing_area'] = area
                try:
                    property_type_lst = listing.find('ul', {'class':'listing-property-type'}).find_all('li')
                    property_type = []
                    for ele in property_type_lst:
                        property_type.append(ele.text)
                    listing_dict['listing_property_type'] = property_type
                    # print(property_type)
                except: pass
                listings.append(listing_dict)
            page_num += 1
        else:
            return (listings if listings else None)
            break
# name = "murphy-lee-李国聪-67370"
# listing = listing_scrapper(name, 'rent', driver=driver)
# print(listing)