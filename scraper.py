import wikipedia
import re 
from bs4 import BeautifulSoup

def main():
   # movie_name = input("Movie name: ")
    movie_name = "Marnie"
    infos = scraper(movie_name,"film")
    print(infos)


def scraper(movie_name,media_type):
    """Gets Wikipedia Page and parses Infobox"""
    #Get Wikipedia page HTML
    search_result = wikipedia.search(movie_name + " " + media_type ,suggestion=True)
    print(search_result)
    html=wikipedia.page(title=search_result[0][0],auto_suggest=False,redirect=False).html()
    #Initalizes BeautifulSoup object of the HTML
    html_soup = BeautifulSoup(html,features="lxml")
    #Search for first instace of tables of class infobox and find all instaces of tr
    infobox_html = html_soup.find('table', class_='infobox').find_all('tr')
    #Ininitializes a empty dictionary for the output data
    infos = {}
    # iterate through the the infobox "tr"s
    for x in infobox_html:
        # find first instace of a "th" tag
        th = x.find('th')
        #checks if a instance of "th" is found
        if th is not None:
            if th["class"] == ["infobox-above","summary"]:
                infos.update({"Title" : th.get_text(strip=True)})
                # create variable key with the text inside the th tag     
            key = th.get_text(" ",strip=True)
                # find all instaces of "li" tags
            li = x.find_all('li')
                # Initialize the list value
            value = []
                # If an instace of "li" exists iterate through them and add the text inside to the value list
            if li is not None and li != []:
                for y in li:
                    value.append(y.get_text(" ",strip=True))
             # If no instace of "li" occures search for instances of "td" and iterate through them and add the text inside to the value list
            else:
                td = x.find_all('td')
                if td is not None:
                    for z in td:
                        value.append(z.get_text(" ",strip=True))
            if value != []:
                infos.update({key : value})
        else:
            td = x.find('td',class_="infobox-image")
            if td is not None:
                infos.update({"Cover image" : td.find("img")["src"].strip("//")})

    return infos



if __name__ == "__main__":
    main()

def html_scaper():
    return False