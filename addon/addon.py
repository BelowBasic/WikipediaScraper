import xbmcaddon
import xbmcgui
import xbmc
import wikipedia
import logging
# import lxml
from bs4 import BeautifulSoup
logging.basicConfig(level=logging.DEBUG)
global_image_url = None


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
<<<<<<< HEAD

        if content is not "No Input":
            data = format_dict(content)
            data = data.replace("[", "").replace("]", "").replace("'", "")
        else:
            data = content

            logging.debug(data)

=======
        if not query:
            data = "No Input"
        else:
            if content is not None:
                data = format_dict(content)
                data = data.replace("[", "").replace("]", "").replace("'", "")
                logging.debug(data)
>>>>>>> main
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
<<<<<<< HEAD

        # Add an image from the globally  stored url
=======
        # Add an image from the global variable
>>>>>>> main
        if global_image_url:
            self.image = xbmcgui.ControlImage(1280-171-50, 720-260-50, 171, 260, global_image_url, 0, "99FFFFFF")
            self.addControl(self.image)
    def onAction(self, action):
        if action.getId() in [xbmcgui.ACTION_PREVIOUS_MENU, xbmcgui.ACTION_NAV_BACK]:
            self.close()
            logging.debug("Window closed by ACTION_NAV_BACK or ACTION_PREVIOUS_MENU")
# region Functions
def get_user_input():
    """Get User Input via Keyboard/Onscreen Keyboard"""
    kb = xbmc.Keyboard('', 'Please enter the video title')
    kb.doModal()  # Onscreen keyboard appears
    if not kb.isConfirmed():
        return ""
    query = kb.getText()  # User input
    return query


def scraper(movie_name, media_type):
    """Gets Wikipedia Page and parses Infobox"""
    if not query:
        infos = "No Input"
        return infos
    global global_image_url
    # Get Wikipedia page HTML
    search_result = wikipedia.search(movie_name + " " + media_type, suggestion=True)
    logging.debug(search_result)
    html = wikipedia.page(title=search_result[0][0], auto_suggest=False, redirect=False).html()
    # Initializes BeautifulSoup object of the HTML
    html_soup = BeautifulSoup(html, features="html.parser")
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
                logging.debug({"Cover image": td.find("img")["src"].strip("//")})
                global_image_url = 'https://' + td.find("img")["src"].strip("//")
                # brauchen wir nicht mehr oder?
                # infos.update({"Cover image": global_image_url})

    return infos


def scraper_de(movie_name, media_type):
    """Gets German Wikipedia Page and parses Infobox"""
    wikipedia.set_lang("de")
    # Get Wikipedia page HTML
    search_result = wikipedia.search(movie_name + " " + media_type, suggestion=True)
    if len(search_result) < 0:
        return "Movie Not Found"
    if len(search_result[0]) < 0:
        return "Movie Not Found"
    logging.debug(search_result)
    html = wikipedia.page(title=search_result[0][0], auto_suggest=False, redirect=False).html()
    # Initializes BeautifulSoup object of the HTML
    html_soup = BeautifulSoup(html, features="html.parser")
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
# end region

# region Main


addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

# Set a string variable to use
# line1 = "Hello World! We can write anything we want here Using Python"
# Launch a dialog box in kodi showing the string variable 'line1' as the contents
query = get_user_input()  # User input via onscreen keyboard
lang = xbmc.getLanguage(xbmc.ISO_639_1)

window = CustomWindow()
window.show()

while not xbmc.Monitor().waitForAbort(1):
    xbmc.sleep(100)

# end region