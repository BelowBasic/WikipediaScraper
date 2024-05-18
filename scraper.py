import wikipedia
import re 
from bs4 import BeautifulSoup

def main():
    movie_name = input("movie name")
    #movie_name = "BeeMovie"
    infos = scraper(movie_name)
    print(infos)


def scraper(movie_name):
    """Gets Wikipedia Page and parses Infobox"""
    html=wikipedia.page(movie_name,auto_suggest=True,redirect=True).html()
    html_soup = BeautifulSoup(html,features="lxml")
    infobox_html = html_soup.find('table', class_='infobox').find_all('tr')
    infos = {}
    for x in infobox_html:
        th = x.find('th')
        if th is not None:            
            key = th.get_text().strip("\xa0")
            li = x.find_all('li')
            value = []
            if li is not None and li != []:
                for y in li:
                    value.append(y.get_text().strip("\xa0"))
            else:
                td = x.find_all('td')
                if td is not None:
                    for z in td:
                        value.append(z.get_text().strip("\xa0"))
            if value != []:
                infos.update({key : value})
    return infos



if __name__ == "__main__":
    main()

def html_scaper():
    return False