from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests


from config import *

# Get Profile uuid of OctoBrowser
def fnGetUUID():
    response_octo = requests.request("GET", OCTO_SEARCH_URL, headers=OCTO_HEADER)
    data_uuid = response_octo.json()
    uuid = data_uuid.get('data')[0]['uuid']
    return uuid

# Get Debug Port
# Profile id is uuid from fnGetUUID()
def get_debug_port(profile_id):
    data = requests.post(
        f'{LOCAL_API}/start', json={'uuid': profile_id, 'headless': False, 'debug_port': True}
    ).json()
    return data['debug_port']

# Create webdriver
# port is from get_debug_port()
def get_webdriver(port):
    chrome_options = Options()
    chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
    # Change chrome driver path accordingly
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    return driver
