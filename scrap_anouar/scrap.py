import os
import re
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import random



def get_pages(count=2):
   

    pages = []

    driver = webdriver.Edge(executable_path="msedgedriver.exe")
    
    #https://www.lacentrale.fr/listing?co2Max=180&co2Min=100&critAirMax=5&doors=2%2C4%2C3%2C5&gearbox=AUTO&makesModelsCommercialNames=CITROEN%3BDACIA%3BPEUGEOT%3BRENAULT&options=&page={page_nb}&seats=4%2C5%2C7
    #https://www.lacentrale.fr/listing?makesModelsCommercialNames=&options=&page={page_nb}
    #https://www.lacentrale.fr/listing?co2Max=130&co2Min=110&critAirMax=5&doors=5&gearbox=MANUAL&makesModelsCommercialNames=CITROEN%3BDACIA%3BPEUGEOT%3BRENAULT&options=&page={page_nb}&seats=4
    #https://www.lacentrale.fr/listing?co2Max=130&co2Min=110&critAirMax=5&doors=5&energies=dies&gearbox=MANUAL&makesModelsCommercialNames=&options=&page={page_nb}&seats=5
    #https://www.lacentrale.fr/listing?co2Max=130&co2Min=110&doors=5&energies=ess&gearbox=MANUAL&makesModelsCommercialNames=&options=&page={page_nb}&seats=5
    #https://www.lacentrale.fr/listing?co2Max=130&co2Min=110&doors=5&energies=hyb&gearbox=MANUAL&makesModelsCommercialNames=&options=&page={page_nb}&seats=5
    #https://www.lacentrale.fr/listing?co2Max=110&doors=5&energies=elec&gearbox=AUTO&makesModelsCommercialNames=&options=&page={page_nb}&seats=5
    #https://www.lacentrale.fr/listing?co2Max=110&doors=3&energies=dies&gearbox=AUTO&makesModelsCommercialNames=&options=&page={page_nb}&seats=4
    #https://www.lacentrale.fr/listing?co2Max=110&doors=3&energies=ess&gearbox=AUTO&makesModelsCommercialNames=&options=&page={page_nb}&seats=4
    #https://www.lacentrale.fr/listing?co2Max=110&doors=3&energies=elec&gearbox=AUTO&makesModelsCommercialNames=&options=&page={page_nb}&seats=4
    #https://www.lacentrale.fr/listing?co2Max=110&doors=3&energies=dies&gearbox=MANUAL&makesModelsCommercialNames=&options=&page={page_nb}&seats=4
    #https://www.lacentrale.fr/listing?co2Max=180&co2Min=130&doors=5&energies=dies&gearbox=MANUAL&makesModelsCommercialNames=&options=&page={page_nb}&seats=5
    #https://www.lacentrale.fr/listing?co2Max=180&co2Min=130&doors=5&energies=ess&gearbox=MANUAL&makesModelsCommercialNames=&options=&page={page_nb}&seats=5
    
    
    # on recupere les pages
    for page_nb in range(2, count + 1):
        page_url = f"https://www.lacentrale.fr/listing?co2Max=180&co2Min=130&doors=5&energies=ess&gearbox=MANUAL&makesModelsCommercialNames=&options=&page={page_nb}&seats=5"
        driver.get(page_url)
        if page_nb == 2:
            time.sleep(15)
        else:
            time.sleep(random.randint(5, 8))
        pages.append(driver.page_source.encode("utf-8"))
    return pages


def get_driver(headless=False):
   
    if headless:
        driver = webdriver.Edge(executable_path="msedgedriver.exe")
    else:
        driver = webdriver.Edge()
    return driver

# on enregistre les pages
def save_pages(pages):
  
    os.makedirs("data", exist_ok=True)
    for page_nb, page in enumerate(pages):
        with open(f"data/page_{page_nb}.html", "wb") as f_out:
            f_out.write(page)

# on parse les pages
def parse_pages():
   
    results = pd.DataFrame()
    pages_paths = os.listdir("data")
    for pages_path in pages_paths:
        with open(os.path.join("data", pages_path), "rb") as f_in:
            page = f_in.read().decode("utf-8")
            results = results.append(parse_page(page))
    return results

# on prepare les donnees pour le dataframe
def parse_page(page):
  
    soup = BeautifulSoup(page, "html.parser")
    result = pd.DataFrame()

    
    result["Marque"] = [
        tag.text.strip() for tag in soup.find_all(attrs={"class": "searchCard__makeModel"})
    ]
    result["Model"] = [
        tag.text.strip() for tag in soup.find_all(attrs={"class": "searchCard__version"})
    ]
    
    result["Année"] = [
        tag.text.strip() for tag in soup.find_all(attrs={"class": "searchCard__year"})
    ]
    result["Kilométrage"] = [
        tag.text.strip() for tag in soup.find_all(attrs={"class": "searchCard__mileage"})
    ]
    
    result["Code Postal"] = [
       tag.text.strip() for tag in soup.find_all(attrs={"class": "searchCard__dptCont"})
    ]
    
    result["Prix"] = [
        tag.text.strip() for tag in soup.find_all(attrs={"class": "searchCard__fieldPrice"})
    ]

    return result

# on cas de besoin pour nettoyer les donnees du prix
#def clean_price(tag):
 #   text = tag.text.strip()
  #  price = int(text.replace("€", "").replace(" ", ""))
   # return price



# on lance le scraping avec le nombre de page souhaite
def main():
    pages = get_pages(count=80)
    save_pages(pages)

# go !
if __name__ == "__main__":
    main()