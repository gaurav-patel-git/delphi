import time, json
from bs4 import BeautifulSoup
from agent_profile_scraper import profile_scraper 
from helper import (
    is_bot, 
    get_username, 
    driver,
    name_actv_lst
    )

base_url = "https://www.propertyguru.com.sg/"

region = "city-south-west"
starting_page_number = 170
ending_page_number = 288  # you have to get the total number of pages in that particular region manually 
num = starting_page_number
while num < ending_page_number:
    print(f'Page Number: {num} and region is {region}')
    page_num = str(num)
    page_type = "property-agent-directory/"
    target_url = base_url + page_type + region + '/' + page_num
    driver.get(target_url)
    agent_name_page_src = driver.page_source
    agent_name_page = BeautifulSoup(agent_name_page_src, 'lxml')
    # print(agent_name_page.title.string)
    
    if is_bot(agent_name_page): 
        print('Bot Protection enabled get captcha done in 60 sec')
        time.sleep(60)
        continue
    
    # this part checks for agent already scrapped or not
    stat_file_path = 'agent_files/profiles_statistics.json'
    data = name_actv_lst(agent_name_page)
    agent_name_list = data[0]
    active_listings = data[1]
    scrapped_agent_lst = get_username(stat_file_path)  # list of agents already scrapped
    temp_name_list = []
    temp_actv_list = []
    for agent_name, actv_lstng in zip(agent_name_list, active_listings):
        if agent_name not in scrapped_agent_lst:
            temp_name_list.append(agent_name)
            temp_actv_list.append(actv_lstng)
        else: print(f'{agent_name} is already scrapped')
    agent_name_list = temp_name_list
    active_listings = temp_actv_list
        
    agent = "agent/"
    for agent_name, actv_lstng in zip(agent_name_list, active_listings):
        target_url = base_url + agent + agent_name
        print(target_url)
        driver.get(target_url)
        profile_page_src = driver.page_source
        profile_page = BeautifulSoup(profile_page_src, 'lxml')
        if is_bot(profile_page):
            print('Bot Protection enabled get captcha done in 60 sec')
            time.sleep(60)
            continue
        else:
            print('Scraping profile ')
            agent_profile = profile_scraper(profile_page, agent_name, actv_lstng)

            with open(f'agent_files/{region}.json', 'a') as profile_file, open(stat_file_path, 'r+') as stat_file:
                print(f'writing to agent profile from page number {num}' + '\n')
                profile_file.write(',\n' )
                profile_file.write(agent_profile)
                
                # writing agent username to stat file for record
                content = json.load(stat_file)
                content['username'].append(agent_name)
                stat_file.seek(0)
                json.dump(content, stat_file, indent=4)
                stat_file.truncate()
    num += 1