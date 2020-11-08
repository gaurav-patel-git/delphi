import time, json
from bs4 import BeautifulSoup
from agent_profile_scraper_2 import profile_scraper 
from helper import (
    is_bot, 
    driver,
    )

agent_urls = []
last_ind = 0
scrapped_agents = []
with open('agent_files_2/agent_directory.json') as agent_directory, open('agent_files_2/profiles_statistics_2.json') as stat_f:
    content = json.load(agent_directory)
    agent_urls = content.get('agent_directory')

    stat_cont = json.load(stat_f)
    last_ind = stat_cont.get('last_scraped_ind')
    scrped_agents = stat_cont.get('scrped_agents')

base_url = "https://www.propertyguru.com.sg/"

for ind in range(last_ind, len(agent_urls)):
    dic = agent_urls[ind]
    agent_url = dic.get('loc')
    agent_img = dic.get('img')
    driver.get(agent_url)
    agent_profile_page_src = driver.page_source
    agent_profile_page = BeautifulSoup(agent_profile_page_src, 'lxml')
    if is_bot(agent_profile_page): 
        print('Bot Protection enabled get captcha done in 60 sec')
        time.sleep(60)
        continue

    print('Scraping profile ')
    agent_profile = profile_scraper(agent_profile_page, agent_url, agent_img)

    with open(f'agent_files_2/scraped_agents.json', 'a', encoding='utf-8') as save_data_f, open('agent_files_2/profiles_statistics_2.json', 'r+') as stat_f:
        save_data_f.write(',\n' )
        save_data_f.write(agent_profile)
        
        # writing agent username to stat file for record
        content = json.load(stat_f)
        content['last_scraped_ind'] = ind
        content['scraped_agents'].append(agent_url)
        stat_f.seek(0)
        json.dump(content, stat_f, indent=4)
        stat_f.truncate()


