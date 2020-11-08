import json, requests, base64
from fake_useragent import UserAgent

base_url = "https://www.99.co/"
location = "singapore/"
get_profile_url = base_url + "-/get_profile/"


ua = UserAgent()
headers = {'User-Agent':ua.random}
def image_to_str(url):
    try:
        image_b = requests.get(url, headers=headers).content
        image_enc_b = base64.b64encode(image_b)         # it's type is byte not string but the representation is same as string 
        image_enc_ascii = image_enc_b.decode('ascii')   # even without decoding.  b'.......' just to remove b
        return image_enc_ascii
    except: return None


def agent_basic_details(details_card, reg_num):
    details = {
        "name" : None,
        "total_listing" : None,
        "job_title" : None,
        "cea_reg_num" : None,
        "agency" : None,
        "contact" : None,
        "image" : None
    }

    name = details_card.find('h2', {'class':'agent-name'})
    details['name'] = name.get_text()

    img_url = details_card.find('img', {'class':'agent-profile-pic'})
    if img_url:
        img_url = f'https:{img_url.get("src")}'
        image_str = image_to_str(img_url)
        details['image'] = image_str
        # with open(f'{reg_num}.jpeg', 'wb') as f:
        #     image = requests.get(img_url)
        #     f.write(image.content)
        

    total_listing = details_card.find('h3', {'class':'primary-subtext text-center'})
    if total_listing:
        details['total_listing'] = int(total_listing.span.text)
    
    cea_reg_num = details_card.find('i', {'class':'fa fa-certificate icon-left'})
    if cea_reg_num:
        cea_reg_num = cea_reg_num.find_next_sibling()
        if cea_reg_num: details['cea_reg_num'] = cea_reg_num.get_text()
    
    agency = details_card.find('i', {'class':'fa fa-building icon-left'})
    if agency:
        agency = agency.find_next_sibling()
        if agency: details['agency'] = agency.get_text()
    
    contact = details_card.find('i', {'class':'fa fa-phone icon-left'})
    if contact:
        contact = contact.find_next_sibling()
        if contact: 
            contact = contact.get_text()
            contact = "".join(contact.split())
            details['contact'] = contact
    
    get_profile_url = f'https://www.99.co/-/get-profile/{reg_num}'
    api_call = requests.get(get_profile_url)
    if api_call.status_code == 200:
        api_call = json.loads(api_call.content)
        # print("api_call", api_call)
        details['job_title'] = api_call.get('job_title')
        details['achievements'] = api_call.get('achievements')
        details['bio'] = api_call.get('bio')
        details['start_year'] = api_call.get('start_year')
        details['description'] = api_call.get('description')
        details['languages'] = api_call.get('languages')
        details['education'] = api_call.get('education')
    return details

def property_scraper(property_id):
    json_res = requests.get(f'https://www.99.co/api/v1/web/listings/detail/{property_id}')
    json_res = json.loads(json_res.text)
    # print(json_res)
    data = json_res.get('data')

    property_details = {
        'basic_info' : {
            'title' : None,
            'summary' : {
                'bedrooms' : None,
                'bathrooms' : None,
                'unit_size' : None,
                'psf' : None
            },
            'address' : None,
            'address_type' : None,
            'postal_code' : None,
            'share_url' : None,
            'status' : None,
            'sub_title' : None,
            'sub_category' : None,
            'share_url' : None,
            'property_segment' : None,
            'video_viewing_available' : None,
            'coordinates' : None,
        },
        'key_details' : None,
        'amenities' : None,
        'description' : None,
        'grc_info' : None,
        'development_overview' : None,
        'enquiry_flags' : None
    }
    
    # Three primary keys
    info = data.get('info')
    sections = data.get('sections')
    
    # info key data
    if info:
        basic_info = property_details.get('basic_info')

        postal_code = info.get('postal_code')
        basic_info['postal_code'] = postal_code
        
        share_url = info.get('share_url')
        basic_info['share_url'] = share_url

        address = info.get('address_title')
        basic_info['address'] = address

        address_type = info.get('address_type')
        basic_info['address_type'] = address_type

        coordinates = info.get('coordinates')
        basic_info['coordinates'] = coordinates

        status = info.get('status')
        basic_info['status'] = status

        title = info.get('title')
        basic_info['title'] = title

        sub_title = info.get('subtitle')
        basic_info['sub_title'] = sub_title

        sub_category = info.get('sub_category')
        basic_info['sub_category'] = sub_category

        property_segment = info.get('property_segment')
        basic_info['property_segment'] = property_segment

        video_viewing_available = info.get('video_viewing_available')
        basic_info['video_viewing_available'] = video_viewing_available

    enquiry_flags = info.get('enquiry_flags')  # dictionary 
    property_details['enquiry_flags'] = enquiry_flags
    
    # sections key data
    if sections:
        amenities = sections.get('amenities')
        if amenities:
            amenities = amenities['data']['items']
            amenities_lst = []
            for a in amenities:
                amenities_lst.append(a['text'])
            property_details['amenities'] = amenities_lst

        facilities = sections.get('facilities')
        # print(facilities)
        if facilities:
            facilities = facilities['data']['items']
            facilities_lst = {}
            for f in facilities:
                facilities_lst[f['label']] = f['text']
            property_details['facilities'] = facilities_lst
        description = sections.get('description')
        if description:
            description = description.get('data').get('text')
            property_details['description'] = description

        summary = sections.get('summary')
        if summary:
            summary = summary.get('data')
            temp_dict = {}
            for item in summary.get('items'):
                temp_dict[item.get('icon_key')] = item.get('label')
            temp_dict['price'] = summary['price']
            basic_info['summary'].update(temp_dict)

    project_overview = sections.get('project_overview')
    if project_overview:
        project_overview = project_overview['data']['text_items']
        project_overview_dict = {}
        for overiew in project_overview:
            project_overview_dict[overiew['label']] = overiew['text']
        property_details['development_overview'] = project_overview_dict

    key_details = sections.get('key_details')
    if key_details:
        key_details = key_details['data']['items']
        key_details_dict = {}
        for detail in key_details:
            # print(detail)
            key_details_dict[detail['label']] = detail['text']
        property_details['key_details'] = key_details_dict

    grc_info = sections.get('grc_info')
    if grc_info:
        grc_info = grc_info['data']
        grc_info_dict = {
            'candidates' : grc_info['contestants'][0]['candidates'],
            'current_party' : grc_info['current_party'],
            'voters' : grc_info['voters'],
            'constituency_name' : grc_info['constituency_name'],
            'seats' : grc_info['seats']
        }
        property_details['grc_info'] = grc_info_dict
    
    return property_details

def get_property(ul):                
    # print(property_type, ul)
    if ul:
        property_ids = []
        a_tags = ul.find_all('a', {'data-click-id':'listing-card'})
        for a_tag in a_tags:
            property_id = a_tag.get('href').split('-')[-1]
            property_ids.append(property_id)
        property_details_lst = []
        for property_id in property_ids:
            property_details = property_scraper(property_id)
            property_details_lst.append(property_details)
        return property_details_lst
    return None


def last_ind(path):
    f = open(path)
    content = json.load(f)
    f.close()
    return content['last_scraped_ind']

def update_stat_file(path, ind, url):
    f = open(path, 'r+')
    content = json.load(f)
    content['last_scraped_ind'] = ind
    content['agents_scraped'].append(url)
    f.seek(0)
    json.dump(content, f, indent=4)
    f.close()


# lst = ['EfsFe2KJPGt28xjAQ2hEzV', 'AmciczjLZPfwgFsZ9ce4zR', 'wXdvU4owbNqybt6EpaS4Zj', 'eZsG3xwz8FwcqMJnbbSHpQ', 'kH7vhehV2S4dj9qJGZHJTj', 'RBP2QJPjs3uCM3YVAGdiyK', 'AZZtqYxkpkpmFyqLSf65Y9', 'ZbbKuGz2A5odaKLDyVFCLn', 'ABc4hgP6M3YUqxLdJUikXb', 'gCmyV7jEUEbcxRcvoXJwgD', 'EzSwDLFNJYgstJ5dXXxJfN', 'QrMakCpKQUQ7GqdvN8Rsnd', 'jwBPqDDSYKzW6r5NNJbVjN', '6a7VYN93zwDeFd2bvSKRXG', 'vs5ANVsfijTcXhFcEyoCnF', '84Cv7mcVHkz4DGvZq7gEHV']
# details = property_scraper('84Cv7mcVHkz4DGvZq7gEHV')
# print(json.dumps(details, indent=4))