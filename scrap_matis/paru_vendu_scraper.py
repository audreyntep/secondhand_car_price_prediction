from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import random
import requests
import re
import time
import csv


def get_user_agent():
    user_agent_strings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]

    return random.choice(user_agent_strings)

def putDataInList(i):
    data = []
    try :
        data.append(i.contents[3].contents[0])
    except:
        try:
            data.append(i.contents[0])
        except:
            data.append(None)
    return data


def getDataPage(page, header, content):
    dataPagelist = []
    try :
        response = requests.get(page, headers=header)
        content = response.content
    except:
        print('User requests not work')
    #html = urlopen(page)
    #bs = BeautifulSoup(html.read(), 'html.parser')
    try:
        bs = BeautifulSoup(content, 'html.parser')
        dataPage = bs.find_all('li', {'class':{'vers', 'kil', 'px', 'ann', 'en',
                                           'emiss', 'cons', 'vit', 'carro', 'puiss', 'por'}})
    except:
        print("find_all Not work or BeautifulSoup")
    dataPageelemts = list(dataPage)
    for i in dataPageelemts:
        dataPagelist.append(putDataInList(i))
    return dataPagelist


def getLinks(url):
    links = []
    try:
        response = requests.get(url, headers={'User-Agent': get_user_agent()})
        content = response.content
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(content, 'html.parser')
    except AttributeError as e:
        return None
    for link in bs.find_all('a', href=re.compile('(https://www.paruvendu.fr/a/voiture-occasion/)')):
        if 'href' in link.attrs:
            links.append(link.attrs['href'])
    return links

def getNextPage(url, n):
    try:
        response = requests.get(url, headers= {'User-Agent': get_user_agent()})
        content = response.content
    except:
        print("User agent in next_page failed")
        return None
    try:
        bs = BeautifulSoup(content, 'html.parser')
    except:
        print("Bs not work in getNextPage")
        return None
    next_page = bs.find('a', {'class':'page'})
    #return next_page.attrs['href']
    return 'https://www.paruvendu.fr/auto-moto/listefo/default/default?origine=affinage&tri=indiceQualite&ord=desc&np=&r=VO&trub=&ty=&r2=&codeINSEE=&lo=&pa=&ray=15&px0=&px1=&nrj=&co2=&critair=&a0=&a1=&km0=&km1=&npo=&tr=&fulltext=&codPro=&pf0=&pf1='+str(n)

def writeInCsv(data):
    csvFile = open('test.csv', 'w+')
    writer = csv.writer(csvFile)
    writer.writerows(data)
    csvFile.close()


links_page = []
data = []

url = 'https://www.paruvendu.fr/auto-moto/listefo/default/default?auto-typeRech=&reaf=1&r2=&px1=&md=&codeINSEE=&lo=&pa=&ray=15&r=VVO00000&r1=&trub=&nrj=&km1=&co2=&a0=&a1=&npo=0&tr=&pf0=&pf1=&fulltext=&codPro='
links_page = getLinks(url)
n = 1

while n :
    print(f"Page{n}", n)
    for page in links_page:
        time.sleep(3)
        data.append(getDataPage(page,
            header={'User-Agent': get_user_agent()}, content=None))
    n += 1
    next_page = getNextPage(url, n)
    if next_page == None:
        break
    links_page = getLinks(next_page) 
writeInCsv(data)
