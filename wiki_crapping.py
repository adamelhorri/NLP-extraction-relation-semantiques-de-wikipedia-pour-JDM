from nltk.corpus import stopwords
from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List
import requests
from bs4 import BeautifulSoup
def get_wikipedia_summary(link: str, val: int) -> str:
    source = urlopen(link).read()
    soup = BeautifulSoup(source, 'lxml')

    cpt = 0
    paras = []
    for paragraph in soup.find_all('p'):
        if cpt >= val:
            break
        parent_div = paragraph.parent
        if parent_div.name == 'div' and 'mw-content-ltr' in parent_div.get('class', []):
            paras.append(paragraph.text)
            cpt += 1
    return " ".join(paras)


from typing import List
import requests
from bs4 import BeautifulSoup

def get_wikipedia_article_links(category_url: List[str]) -> List[str]:
    links = []  # Liste pour stocker les liens de chaque catégorie

    for url in category_url:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all('div', {'class': 'mw-category-group'}):
                for link in item.find_all('a'):
                    href = link.get('href')
                    # Vérification pour s'assurer que le lien est complet
                    if str(href).startswith('/wiki/')==True and (str(href).startswith('/wiki/Catégorie')==False or str(href).startswith('/wiki/Cat%C3%A9gorie')==False):
                        links.append("https://fr.wikipedia.org" + href)
        else:
            print(f"La requête a échoué pour l'URL : {url}")

    return links



def scrape_wikipedia_category(category_url: str, val: int,n: int) -> List[str]:
    article_links = get_wikipedia_article_links(category_url)
    summaries = []
    for link in article_links:
        summary = get_wikipedia_summary(link, val)
        summaries.append(summary)
        summaries=summaries[:n]
    return summaries
'''
a=scrape_wikipedia_category(["https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Chat"],3,20)
for i in a:
    print(i)
    print("************************************")
'''