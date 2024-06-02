import xbmcaddon
import xbmcgui
import xbmc
import wikipedia
import logging
# import lxml
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
global_image_url = None

# The method will receive a dictionary and return a string that is better suited for parsing in Kodi.
def format_dict(dictionary):
    formatted_output = ""
    stack = [(dictionary, 0)]  # (dict, indentation level)
    while stack:
        current_dict, indent = stack.pop()
        for key, value in current_dict.items():
            if isinstance(value, dict):
                formatted_output += "  " * indent + f"{key}:\n"
                stack.append((value, indent + 1))
            else:
                formatted_output += "  " * indent + f"{key}: {value}\n"
    return formatted_output



class CustomWindow(xbmcgui.Window):
    def __init__(self):
        super().__init__()

        if lang == "de-de":
            content = scraper_de(query, "Film")
        else:
            content = scraper(query, "Film")

        if not query:
            data = "No Input"
        else:
            if content is not None:
                data = format_dict(content)
                data = data.replace("[", "").replace("]", "").replace("'", "")

                logging.debug(data)

        # Set background color or image
        self.background = xbmcgui.ControlImage(0, 0, 1280, 720, 'special://home/addons/skin.estuary/background.jpg')
        self.addControl(self.background)

        # Add a text box to show the retrieved data
        self.textbox = xbmcgui.ControlTextBox(100, 100, 1080, 600, textColor='0xFFFFFFFF', font='font14')
        self.addControl(self.textbox)
        self.textbox.setText(data)

        # Add an image
        self.image = xbmcgui.ControlImage(300, 200, 200, 200,
                                          'special://home/addons/skin.estuary/media/default_icon.png')
        self.addControl(self.image)

        # Add an image from the global variable
        if global_image_url:
            self.image = xbmcgui.ControlImage(100, 100, 200, 200, global_image_url)
            self.addControl(self.image)

    def onAction(self, action):
        if action.getId() in [xbmcgui.ACTION_PREVIOUS_MENU, xbmcgui.ACTION_NAV_BACK]:
            self.close()
            logging.debug("Window closed by ACTION_NAV_BACK or ACTION_PREVIOUS_MENU")


# region Functions
def get_user_input():
    """Get User Input via Keyboard/Onscreen Keyboard"""
    kb = xbmc.Keyboard('', 'Please enter the video title')
    kb.doModal() # Onscreen keyboard appears
    if not kb.isConfirmed():
        return ""
    query = kb.getText()  # User input
    return query


def scraper(movie_name, media_type):

    """Gets the Wikipedia page and parses the infobox.

    Args:
        movie_name (str): The name of the movie to search for on Wikipedia.
        media_type (str): The type of media, such as "Film" or "TV series".

    Returns:
        dict: A dictionary containing information parsed from the Wikipedia infobox.
    """

    global global_image_url
    search_result = wikipedia.search(movie_name + " " + media_type, suggestion=True)
    logging.debug(search_result)
    html = wikipedia.page(title=search_result[0][0], auto_suggest=False, redirect=False).html()
    html_soup = BeautifulSoup(html, features="html.parser")
    infobox_html = html_soup.find('table', class_='infobox').find_all('tr')
    infos = {}
    for x in infobox_html:
        th = x.find('th')
        if th:
            if th["class"] == ["infobox-above", "summary"]:
                infos.update({"Title": th.get_text(strip=True).replace("\xa0", " ")})
            key = th.get_text(" ", strip=True)
            li = x.find_all('li')
            value = []
            if li:
                for y in li:
                    value.append(y.get_text(" ", strip=True).replace("\xa0", " "))
            else:
                td = x.find_all('td')
                if td:
                    for z in td:
                        value.append(z.get_text(" ", strip=True).replace("\xa0", " "))
            if value:
                infos.update({key: value})
        else:
            td = x.find('td', class_="infobox-image")
            if td:
                logging.debug({"Cover image": td.find("img")["src"].strip("//")})
                global_image_url = 'https://' + td.find("img")["src"].strip("//")
                infos.update({"Cover image": global_image_url})
    return infos


def scraper_de(movie_name, media_type):
    """Gets German Wikipedia Page and parses Infobox.
    
    The return value of wikipedia.search is a tuple containing two elements:

    A list of page titles matching the search query.
    A suggested title for the search query.

    """
    
    wikipedia.set_lang("de") 
    search_result = wikipedia.search(movie_name + " " + media_type, suggestion=True)
    if not search_result:
        return "Movie Not Found"
    
    html = wikipedia.page(title=search_result[0][0], auto_suggest=False, redirect=False).html()
    html_soup = BeautifulSoup(html, features="html.parser")
    infobox_html = html_soup.find('table', class_='infobox').find_all('tr')
    infos = {}
    for row in infobox_html:
        header = row.find('th')
        if header is not None:
            key = header.get_text(strip=True).replace("\xa0", " ")
            data = row.find('td')
            if data is not None:
                value = data.get_text(";", strip=True).replace("\xa0", " ")
                infos.update({key: value.split(";")})   
    return infos

# end region


# Initialize Kodi add-on information
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

# Prompt user for input
query = get_user_input()  # User input via onscreen keyboard
lang = xbmc.getLanguage(xbmc.ISO_639_1)

# Create and display custom window
window = CustomWindow()
window.show()

# Main loop to keep the add-on running
while not xbmc.Monitor().waitForAbort(1):
    xbmc.sleep(100)


