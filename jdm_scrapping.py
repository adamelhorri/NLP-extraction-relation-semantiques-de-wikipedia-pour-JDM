
import requests
from bs4 import BeautifulSoup

def check_relation(mot1, relation, mot2):
    url = f"https://www.jeuxdemots.org/rezo-ask.php?gotermsubmit=Demander&term1={mot1}&rel={relation}&term2={mot2}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Check if the content contains "oui"
        if "oui" in soup.get_text():
            return True
    return False

# Example usage:
mot1 = "chien"
relation = "r_isa"
mot2 = "animal"
'''
result = check_relation(mot1, relation, mot2)
print(result)
'''
