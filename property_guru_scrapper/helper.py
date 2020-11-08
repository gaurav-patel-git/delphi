import json, time, requests, base64
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("user-data-dir=C:\\Users\\gp896\\AppData\\Local\Google\\Chrome\\User Data\Default")
    options.add_argument("user-data-dir=selenium_cookies")
    options.add_extension("extenstions/privacy_pass.crx")
    # your need to specify the location fo chromedriver directory
    driver = webdriver.Chrome(executable_path=r'driver/chromedriver.exe', options=options)
    return driver

driver = get_driver()    

def is_bot(parsed_page): return parsed_page.title.string == "Bot Protection"


def name_actv_lst(parsed_html):
    name_lst = []
    for name_tag in parsed_html.find_all('div', attrs={"class":"agent-info-name"}):
            name = name_tag.a.get('href')
            name = name.split('/')[2]  # extracting username form the anchor tag
            name_lst.append(name)
    active_listings = []
    for active_listing in parsed_html.find_all('div', {'class' : 'agent-info-listing hidden-xs'}):
        active_listing_lst = active_listing.text.split()
        active_listing_int = 0
        try: active_listing_int = int(active_listing_lst[0])  # ["1", "acitve", "listing"]
        except: pass
        active_listings.append(active_listing_int)
    return (name_lst, active_listings)

# url = "https://www.propertyguru.com.sg/property-agent-directory/city-south-west"
# driver.get(url)
# page_src = driver.page_source
# page = BeautifulSoup(page_src)
# names = name_extractor(page)
# print(names)

ua = UserAgent()
headers = {'User-Agent':ua.random}
def image_to_str(url):
    try:
        image_b = requests.get(url, headers=headers).content
        image_enc_b = base64.b64encode(image_b)         # it's type is byte not string but the representation is same as string 
        image_enc_ascii = image_enc_b.decode('ascii')   # even without decoding.  b'.......' just to remove b
        return image_enc_ascii
    except: return None
    

def get_username(stat_file_path):
    try:
        with open(stat_file_path, 'r+') as stat_file:
            content = json.load(stat_file)
            username_lst = content['username']
            return username_lst
    except FileNotFoundError:
        print("File Not Found")
        return None

def save_session(driver):
    executor_url = driver.command_executor._url
    session_id = driver.session_id    
    cur_session = {
        'exe_url' : executor_url,
        'sess_id' : session_id
    }
    with open('cur_browser.json', 'w') as f:
        json.dump(cur_session, f, indent=4)

def load_session(cur_browser_path):
    try:
        with open(cur_browser_path) as f:
            return json.load(f)
    except: return None

        
    
