import codecs
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-javascript")

# Create the web browser
browser = webdriver.Chrome(options=chrome_options)

url = r"https://usp-data-models.broadband-forum.org/tr-181-2-15-1-usp.html#device215-data-model"

# Open browser
browser.get(url)

# Find all elements with class name "object"
objects = browser.find_elements(By.CLASS_NAME, "object")
# Find all elements with class name "mountpoint-object"
mountpoint_object = browser.find_elements(By.CLASS_NAME, "command")
# Declaration for all the lists
objectList = []
mountpoint_objectList = []

# The first object is unnecessary so here it is removed
objects = objects[1:]
mountpoint_object = mountpoint_object[1:]


def remove_non_breaking_hyphen(text):
    return text.replace('\xad', '')

breakObjLoop = False
breakMobjLoop = False

for obj in objects:
    # Find the nested elements with tag name "td" that contain the desired values
    parameters = obj.find_elements(By.TAG_NAME, "td")
    # Temp list to store the parameter values
    tempObjectList = []
    
    for parameter in parameters:
        if len(parameters) == 1:
            breakObjLoop = True
            break
        tempObjectList.append(remove_non_breaking_hyphen(parameter.text))
    
    if breakObjLoop:
        break
    
    objectList.append(tempObjectList)

for mobj in mountpoint_object:
    # Find the nested elements with tag name "td" that contain the desired values
    parameters = mobj.find_elements(By.TAG_NAME, "td")
    # Temp list to store the parameter values
    tempMountPointObjectList = []
    
    for index, parameter in enumerate(parameters):
        if index == 1 and remove_non_breaking_hyphen(parameter.text) == '-':
            breakMobjLoop = True
            break
        tempMountPointObjectList.append(remove_non_breaking_hyphen(parameter.text))
    
    if breakMobjLoop:
        break
    
    mountpoint_objectList.append(tempMountPointObjectList)

with open('information.csv', "w", newline='', encoding = "utf-8") as information:
    writer = csv.writer(information, quoting=csv.QUOTE_ALL)
    writer.writerow(['Name', 'Type', 'Write', 'Description', 'Object Default', 'Version'])
    writer.writerows(objectList)
    writer.writerows(mountpoint_objectList)