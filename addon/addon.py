import xbmcaddon
import xbmcgui
import xbmc

#region Functions
# Get User Input via Keyboard/Onscreen Keyboard
def get_user_input():
    kb = xbmc.Keyboard('', 'Please enter the video title')
    kb.doModal() # Onscreen keyboard appears
    if not kb.isConfirmed():
        return ""
    query = kb.getText() # User input
    return query

#endregion

#region Main
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')


# Set a string variable to use
# line1 = "Hello World! We can write anything we want here Using Python"

# Launch a dialog box in kodi showing the string variable 'line1' as the contents
query = get_user_input() # User input via onscreen keyboard
if not query:
    xbmcgui.Dialog().ok(addonname, "No Input")
else:
    xbmcgui.Dialog().ok(addonname, query)
#endregion