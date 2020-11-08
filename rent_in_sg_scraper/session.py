import requests
from bs4 import BeautifulSoup


base_url = "https://rentinsingapore.com.sg/"
login_url = base_url + 'login'

data = {
    'utf8' : '✓',
    'authenticity_token' : '',
    'user[email]' : 'g.p8966891720@gmail.com',
    'user[password]' : 'Testing123',
    'commit' : 'Login'

}


def log_in(data):
    sess = requests.Session()
    r = sess.get(login_url)
    soup = BeautifulSoup(r.text, 'lxml')
    auth_token = soup.find('input', {'name' : 'authenticity_token'}).get('value')
    data['authenticity_token'] = auth_token
    # print(auth_token)
    login_req = sess.post(login_url, data=data)
    return sess

s = log_in(data)