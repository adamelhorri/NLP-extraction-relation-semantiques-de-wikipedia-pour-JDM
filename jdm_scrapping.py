

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

def check_relation(mot1, relation, mot2):
    url = f"https://www.jeuxdemots.org/rezo-ask.php?gotermsubmit=Demander&term1={mot1}&rel={relation}&term2={mot2}"
    
    # Setup retries and session
    session = requests.Session()
    retry = Retry(
        total=5,  # Number of retries
        backoff_factor=1,  # Time to wait between retries
        status_forcelist=[500, 502, 503, 504],  # Retry on these HTTP status codes
        raise_on_status=False  # Don't raise exceptions for these codes
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        response = session.get(url, timeout=10)  # 10 seconds timeout
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check if the content contains "oui"
        if "oui" in soup.get_text():
            return True
        return False
        
    except requests.exceptions.ConnectTimeout:
        print("Connection timed out.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False

# Example usage:
mot1 = "chien"
relation = "r_isa"
mot2 = "animal"
'''
result = check_relation(mot1, relation, mot2)
print(result)
'''
