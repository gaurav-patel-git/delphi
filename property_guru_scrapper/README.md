# [Property Guru Scrapper](https://www.propertyguru.com.sg/property-agent-directory)

Is scrape data of all the agents and listing even though the site is cloud flare protected with captcha. All the data is stored in [agent_files](agent_files/)

### Prerequists 
Make sure you have chrome drive compatiable with your chrome version availabe in the directory called ***driver***

### Callenges Faced
- [Propery Guru](https://www.propertyguru.com.sg/property-agent-directory) uses **CloudFlare** to protect their website from DDoS and bots so this project uses a chrome extension **privacy pass** which helps to bypaas captcha using earned passes. This extension is shipped along the project and gets installed when you run the script. 
- In order to use passes generated by privacy pass extenstion you need to specify **user-data-dir** in chromeoptions specified on get_driver function defined at helper.py. By default set to selenium_data.
- The profile picture of agents are converted to base64 string as we neede to transport images as string.
- Data integrity needed to be maintained so before scraping any agent it also checks in the current agent is already scrappd or not.

### Fire up the project
Please go through helper.py and agent_profile_getter.py. The code is self explanatory. 
```
pip install pipenv
pipenv install 
pipenv shell
python agent_profile_getter.py
```
### Output
Specify the area from where you want the agents.
Json output can be found at [here](agent_files/) in below format 
```
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
```
