import json
from helper import image_to_str
from agent_listing_scrapper import listing_scrapper

def profile_scraper(profile_page, username, active_listing):
    agent_profile = {
        "username": username,
        "name" : None,
        "img" : None,
        "job_title" : None,
        "agency" : None,
        "phone_number" : None,
        "license_number" : None,
        "registration_number" : None,
        "website" : None,
        "description" : None,
        "services" : None,
        "regions_covered" : None,
        "properties_block" : None,
        "acitve_listing" : active_listing,
        "listings" : {
            "sale" : None,
            "rent" : None,
        }
    }
    agent_details = profile_page.find('div', {'class':'columned-content'})  # this column contains all the details of agent

    img_tag = agent_details.find('img', {'class':'media-object lazy lazy-bg'})
    if img_tag:
        img_url = img_tag.get('data-original')
        img_str = image_to_str(img_url)
        agent_profile['img'] = img_str
    
    name = agent_details.h3
    if name:
        agent_profile['name'] = name.text
    
    job_title = agent_details.find('div', {'class':'agent-job-title'})
    if job_title:
        agent_profile['job_title'] = job_title.text

    agency = agent_details.find('div', {'class':'agent-agency'})
    if agency:
        agent_profile['agency'] = agency.text

    phone_number = profile_page.find('span', {'class':'agent-details-phone-number hide'})
    if phone_number:
        agent_profile['phone_number'] = phone_number.text
    
    agent_licenses = agent_details.find('div', {'class':'agent-license'})
    if agent_licenses:
        lst = []
        for agent_license in agent_licenses.find_all('a'):
            lst.append(agent_license.text.split()[0])
        agent_profile['license_number'] = (lst[0] if lst[0] else None)
        agent_profile['registration_number'] = (lst[1]  if lst[1] else None)
        # print(lst)
    agent_website = agent_details.find('div', {'class': 'agent-website'})
    # print(agent_website)
    if agent_website:
      agent_website = agent_website.a.get('href')
      agent_profile['website'] = agent_website
    description = agent_details.find('div', {'class':'agent-details-description'})
    if description:
        description = description.text.split('\n')
        temp = ""
        for string in description: temp += string
        description = temp
        agent_profile['description'] = description 
    
    services = agent_details.find('div', {'class':'agent-services-block'})
    if services:
        services = services.find_all('li')[:-1]
        services_lst = [ ele.text for ele in services]
        agent_profile['services'] = services_lst
    
    regions_covered = agent_details.find('div', {'class':'agent-regions-block'})
    if regions_covered:
        regions_covered = regions_covered.find_all('li')[:-1]
        regions_covered_lst = [ ele.text for ele in regions_covered]
        agent_profile['regions_covered'] = regions_covered_lst

    properties_block = agent_details.find('div', {'class':'agent-properties-block'})
    if properties_block:
        properties_block = properties_block.find_all('li')[:-1]
        properties_block_lst = [ ele.text for ele in properties_block]
        agent_profile['properties_block'] = properties_block_lst

    listing_sale = None
    listing_rent = None
    # agent property listings 
    if active_listing:
        listing_sale = listing_scrapper(username, 'sale')
        listing_rent = listing_scrapper(username, 'rent')
    
    agent_profile['listings']['sale'] = listing_sale
    agent_profile['listings']['rent'] = listing_rent
    agent_profile = json.dumps(agent_profile, indent=4)
    # print(agent_profile)
    return agent_profile
