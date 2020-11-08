import requests, base64, json
from bs4 import BeautifulSoup
from helper import agent_basic_details, get_property, last_ind, update_stat_file


with open('agents_url.json') as agent_f:
    agent_dict = json.load(agent_f).get('urls')
    
    last_ind = last_ind('scraping_stat.json')
    
    for ind in range(last_ind, len(agent_dict)):
        dic = agent_dict[ind]
        agent_url = dic.get('loc')
        print('==============================================================')
        print(agent_url)

        lst = agent_url.split('-')
        name = " ".join(lst[1:])  # extracting the name from the urls
        reg_num = lst[0].split('/')[-1]  # extracting the registration number from the urls
        r = requests.get(agent_url)   
        if r.status_code == 404:
            print('agent not found')
            update_stat_file('scraping_stat.json', ind, agent_url)
            continue
        profile_page = BeautifulSoup(r.text, 'lxml')
        details_card = profile_page.find('div', {'class':'col-md-4'})
        basic_details = agent_basic_details(details_card, reg_num)
        print(f'Listings found = {basic_details.get("total_listing")}')
        
        # scraping rent property details
        rent_ul = profile_page.find('ul', {'ng-show':"tab.active == 'rent'"})
        rent_properyt_details = get_property(rent_ul)
        
        sale_ul = profile_page.find('ul', {'ng-show':"tab.active == 'sale'"})
        sale_properyt_details = get_property(sale_ul)
              
        agent_profile = {
            "details" : basic_details,
            "sale" : sale_properyt_details,
            "rent" : rent_properyt_details
        }

        with open('agent_profiles.json', 'a', encoding='utf-8') as f:
            f.write(',\n')
            json.dump(agent_profile, f, indent=4)
            update_stat_file('scraping_stat.json', ind, agent_url)
