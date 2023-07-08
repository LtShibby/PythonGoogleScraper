import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

# Takes query and result and formats it into url
query = "Physical Therapists in Singapore"
search = query.replace(' ', '+')
results = 10
url = (f"https://www.google.com/search?q={search}&num={results}")

# Gets pages from requests and gets a list of links and headers from the pages
requests_results = requests.get(url)
soup_link = BeautifulSoup(requests_results.content, "html.parser")
soup_title = BeautifulSoup(requests_results.text,"html.parser")
links = soup_link.find_all("a")
heading_object=soup_title.find_all( 'h3' )
filePath = Path('scraperOutput.csv')
dataArray = []

# Creates dataArray formatting each link that is a URL to each title obtained from heading_object
# Unsure if it is supposed to do this or if each line should have each page title attached to its corresponding URL
for link in links:
  for info in heading_object:
    newLine = []
    get_title = info.getText()  # Gets title of current page
    link_href = link.get('href')  # Gets link from the current link
    if "url?q=" in link_href and not "webcache" in link_href: # Confirms the current link is a URL
        # Formats line and adds to dataArray
        newLine.append(get_title)
        newLine.append(link.get('href').split("?q=")[1].split("&sa=U")[0])
        dataArray.append(newLine)
        
# Converts data array to dataframe to write to the csv file        
df = pd.DataFrame(dataArray)
df.to_csv(filePath)
        