from urllib.parse import urlparse, unquote, urlsplit, parse_qs
from http.client import responses

import pandas as pd
import requests
from bs4 import BeautifulSoup


def list_rm_empty(lst):
    final = []
    for l in lst:
        if l == []:
            l = ' '
        final.append(l)
    return final

list_rm_empty([x.contents[0] for x in soup.find_all('h1')])

insydo2 = requests.get('https://www.insydo.com/category/nightlife/194')
insydo_soup = BeautifulSoup(insydo2.content, 'lxml')

[x.contents[0] for x in insydo_soup.find_all('h2')]



def seo_analyze(page):
    page_req = requests.get(page)
    page_text = page_req.text
    soup = BeautifulSoup(page_text, 'lxml')
    seo_elements = [
        ('title', soup.title.string),
        ('title_len', len(soup.title.string)),
        ('meta_description', soup.find_all(
            attrs={'name': 'description'})[0]['content']),
        ('h1', [x.contents for x in soup.find_all('h1')]),
        ('h2', [x.contents for x in soup.find_all('h2')]),
        ('h3', [x.contents for x in soup.find_all('h3')]),
        ('h4', [x.contents for x in soup.find_all('h4')]),
        ('status_code', page_req.status_code),
        ('status', responses[page_req.status_code]),
        ('response_time', page_req.elapsed.total_seconds()),
    ]
    seo_dict = {k: v for k, v in seo_elements}
    return seo_dict


d_urls = [
    'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity=d586&radius=50&zip=10022&sourceContext=RecentSearches_false_0&isRecentSearchView=true#listing=170536804_isFeatured',
    'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity=d586&radius=50&zip=10022&sourceContext=RecentSearches_false_0&isRecentSearchView=true#listing=175333441_isFeatured',
    'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity=d586&radius=50&zip=10022&sourceContext=RecentSearches_false_0&isRecentSearchView=true#listing=172868099_isFeatured',
    'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity=d586&radius=50&zip=10022&sourceContext=RecentSearches_false_0&isRecentSearchView=true#listing=177372388',
    'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity=d586&radius=50&zip=10022&sourceContext=RecentSearches_false_0&isRecentSearchView=true#listing=161422222',
]

danube = []

for page in d_urls:
    print('Analyzing', page)
    danube.append(seo_analyze(page))
danube[0]

carpage = d_urls[0]
car_req = requests.get(carpage)
carsoup = BeautifulSoup(car_req.content, 'lxml')
carh3 = carsoup.find_all('h3')

lst = [x.contents[0] for x in carh3[1:]]
tst = [x.contents for x in carh3]
','.join(tst)

carsoup.find_all('h3')