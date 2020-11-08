from session import s
from bs4 import BeautifulSoup
import json


base_url = "https://rentinsingapore.com.sg/ID"


def scrape_room(room_id):
    room_details = {
    'room_id' : room_id,
    'title' : None,
    'street' : None,
    'price' : None,
    'owner' : None,
    'contact' : None,
    'description' : None,
    'details' : None,
    'location' : None
    }
    url = base_url + room_id
    r = s.get(url)
    room_page = BeautifulSoup(r.text, 'lxml')
    
    head_content = room_page.find('div', {'class':'intro-container intro-container__header'})
    if head_content:
        title = head_content.h1
        if title:
            title = title.get_text()
            room_details['title'] = title
        
        street = head_content.find('div', {'class':'room-street'})
        if street:
            street = street.get_text(strip=True)
            room_details['street'] =  street
        price = head_content.find('div', {'class':'room-price'})
        if price:
            price = price.get_text(strip=True)
            room_details['price'] = price
    
    contact = room_page.find('div', {'class':'btn btn-primary show-number'})
    if contact:
        contact = contact.find('span', {'class':'message-number__long'})
        if contact:
            room_details['contact'] = contact.get_text()
        else:
            contact = contact.find('span', {'class':'message-number__short'})
            if contact:
                room_details['contact'] = contact.get_text()
    
    owner = room_page.find('div', {'class':'message-container-owner'})
    if owner:
        owner = owner.get_text().split()
        owner = owner[1:]
        owner_name = "".join(owner)
        room_details['owner'] = owner_name

    description = room_page.find('p', {'class':'room-description container-show-description'})
    if description:
        description = description.get_text(strip=True)
        room_details['description'] = description
    
    details = room_page.find('div', {'class':'room-details container-show-details'})
    if details:
        details = details.find_all('li')
        temp = []
        for detail in details:
            temp.append(detail.text)
        room_details['details'] = temp

    location = room_page.find('div', {'class':'room-location container-show-location'})
    if location: 
        location = location.p
        if location:
            location = location.get_text(strip=True)
            room_details['location'] = location
    return json.dumps(room_details, indent=4, ensure_ascii=False)    

        
room_ids = []
last_ind = 0
scraped_room_ids = []
with open('room_ids.json', 'r') as f_id, open('scraping_stats.json', 'r+') as f_stat, open('room_scraped/rent_room_details.json', 'a', encoding='utf-8') as f_room_data:     
    room_ids = json.load(f_id)
    
    scraping_stat = json.load(f_stat)
    last_ind = scraping_stat['scraped_last_ind']
    scraped_room_ids = scraping_stat['scraped_room_ids']
    
    for ind in range(last_ind+1, len(room_ids)):
        room_id = room_ids[ind]
        print(f'Scraping room with id {room_id}, total rooms scraped {ind+1}')
        
        scraped_data = scrape_room(room_id)
        f_room_data.write(',\n')
        f_room_data.write(scraped_data)
        
        f_stat.seek(0)
        scraped_room_ids.append(room_id)
        stat_data = {
            "scraped_last_ind" : ind,
            "scraped_room_ids" : scraped_room_ids
        }
        json.dump(stat_data, f_stat, indent=4)

        

