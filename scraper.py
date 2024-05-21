import wikipedia
# import re
import logging
from bs4 import BeautifulSoup


def main():
    # movie_name = input("Movie name: ")
    movie_name = "Bee movie"
    infos = scraper(movie_name, "film")
    print(infos)
    infos = scraper_de(movie_name, "film")
    print(infos)


def scraper(movie_name, media_type):
    """Gets Wikipedia Page and parses Infobox"""
    # Get Wikipedia page HTML
    search_result = wikipedia.search(movie_name + " " + media_type, suggestion=True)
    logging.debug(search_result)
    html = wikipedia.page(title=search_result[0][0], auto_suggest=False, redirect=False).html()
    # Initializes BeautifulSoup object of the HTML
    html_soup = BeautifulSoup(html, features="lxml")
    # Search for first instance of tables of class infobox and find all instances of "tr"
    infobox_html = html_soup.find('table', class_='infobox').find_all('tr')
    # Initializes an empty dictionary for the output data
    infos = {}
    # iterate through the infobox "tr"s
    for x in infobox_html:
        # find first instance of a "th" tag
        th = x.find('th')
        # checks if an instance of "th" is found
        if th is not None:
            if th["class"] == ["infobox-above", "summary"]:
                infos.update({"Title": th.get_text(strip=True).replace("\xa0", " ")})
            # create variable key with the text inside the th tag
            key = th.get_text(" ", strip=True)
            # find all instances of "li" tags
            li = x.find_all('li')
            # Initialize the list value
            value = []
            # If an instance of "li" exists iterate through them and add the text inside to the value list
            if li is not None and li != []:
                for y in li:
                    value.append(y.get_text(" ", strip=True).replace("\xa0", " "))
            # If no instance of "li" occurs search for instances of "td" and iterate through them
            # and add the text inside to the value list
            else:
                td = x.find_all('td')
                if td is not None:
                    for z in td:
                        value.append(z.get_text(" ", strip=True).replace("\xa0", " "))
            if value:
                infos.update({key: value})
        else:
            td = x.find('td', class_="infobox-image")
            if td is not None:
                infos.update({"Cover image": td.find("img")["src"].strip("//")})

    return infos


def scraper_de(movie_name, media_type):
    """Gets German Wikipedia Page and parses Infobox"""
    wikipedia.set_lang("de")
    # Get Wikipedia page HTML
    search_result = wikipedia.search(movie_name + " " + media_type, suggestion=True)
    logging.debug(search_result)
    html = wikipedia.page(title=search_result[0][0], auto_suggest=False, redirect=False).html()
    # Initializes BeautifulSoup object of the HTML
    html_soup = BeautifulSoup(html, features="lxml")
    # Search for first instance of tables of class infobox and find all instances of "tr"
    infobox_html = html_soup.find('table', class_='infobox').find_all('tr')
    # Initializes an empty dictionary for the output data
    infos = {}
    # iterate through the infobox "tr"s
    for x in infobox_html:
        # find first instance of a "th" tag
        th = x.find('th')
        # checks if an instance of "th" is found
        if th is not None:
            key = th.get_text(strip=True).replace("\xa0", " ")
            td = x.find('td')
            if td is not None:
                value = td.get_text(";", strip=True).replace("\xa0", " ")
                infos.update({key: value.split(";")})
    return infos


if __name__ == "__main__":
    main()


def html_scraper():
    return False
