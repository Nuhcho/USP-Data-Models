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

# Find all elements by CSS SELECTOR in order to add them to the list in the proper order.
objects = browser.find_elements(By.CSS_SELECTOR, ".object, .command")



# Declaration for all the lists
objectList = []


# The first two objects is unnecessary so here it is removed
objects = objects[2:]



#Method to remove the \xad at the end of each text
def remove_non_breaking_hyphen(text):
    return text.replace('\xad', '')

#For breaking out of nested for loops
breakObjLoop = False

for obj in objects:
    # Find the nested elements with tag name "td" that contain the desired values
    parameters = obj.find_elements(By.TAG_NAME, "td")
    # Temp list to store the parameter values
    tempObjectList = []
    #Contains a statement that checks for a the length of the parameter which causes the code to break out of all loops. This to prevent selenium from grabbing data beyond the table.
    for index, parameter in enumerate(parameters):
        if len(parameters) == 1 or (index == 1 and remove_non_breaking_hyphen(parameter.text) == '-'):
            breakObjLoop = True
            break
        tempObjectList.append(remove_non_breaking_hyphen(parameter.text))
    
    #Breaks out of nested for loop
    if breakObjLoop:
        break
    
    objectList.append(tempObjectList)


#Encoding changes the encoding type from cp1252 to utf-8 thus fixing the error for encoding special characters like apostrophes and commas
with open('information.csv', "w", newline='', encoding = "utf-8") as information:
    writer = csv.writer(information, quoting=csv.QUOTE_ALL)
    writer.writerow(['Name', 'Type', 'Write', 'Description', 'Object Default', 'Version'])
    #Sorts through the lists with these big lists and writes them in rows
    writer.writerows(objectList)
