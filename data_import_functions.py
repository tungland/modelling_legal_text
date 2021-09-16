import requests
from bs4 import BeautifulSoup as bs
import re
from random import randint
from time import sleep
import pandas as pd

def get_links(path):
    # Get the document links from a webpage
    r = requests.get(path)
    soup = bs(r.content, 'lxml')
    links = soup.find_all('a', href=True)
    urls = []
    for link in links:
        urls.append(link['href'])

    legislation_2019 = []
    info_2019 = []

    for url in urls:
        l = re.compile(r".*legal-content/EN/TXT/\?uri=(OJ:L:.*):TOC")
        c = re.compile(r".*legal-content/EN/TXT/\?uri=(OJ:C:.*):TOC")    

        l_match = re.search(l, url)
        c_match = re.search(c, url)
        
        if l_match:
            legislation_2019.append(l_match.group(1))
        elif c_match:
            info_2019.append(c_match.group(1))


    return legislation_2019, info_2019

def page_loop(path, pages):
    # Loops through pages on path. Returns two lists
    legislation = []
    info = []
    for page in range(pages):
        # print(path[:-1] + str(int(url[-1:]) + page))
        urllink = path[:-1] + str(int(path[-1:]) + page)
        leg, inf = get_links(urllink)
        if leg == [] and inf == []:
            break
        legislation.append(leg)
        info.append(inf)
        sleep(randint(1,2))

    flat_inf = [item for sublist in info for item in sublist]
    flat_leg = [item for sublist in legislation for item in sublist]

    return flat_leg, flat_inf

def collect_entries(list_of_uris):
    # Collect text based on the uris of EU OJ entries
    dct = {}
    for i, uri in enumerate(list_of_uris):
        r = requests.get(f'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri={uri}:FULL&from=EN')
        soup = bs(r.content, 'xml')
        dct[i] = soup
        #sleep(randint(1, 2))
        sleep(1)
    df = pd.DataFrame.from_dict(dct, orient='index')
    return df