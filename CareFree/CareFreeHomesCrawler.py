"""
By Dallin Hull
dallinrichard@gmail.com
https://github.com/dallinhull

This API webcrawls carefreehomes.com and returns various information about presale homes and listed spec homes.
Information is gathered and processed via HTTP requests and BeautifulSoup.
Information includes location, price, sqft, bedroom count, bathroom count, etc.

Lastly, all selected info will be compiled into a list of lists.
The end goal is to make info easy to transfer via GoogleCloud to Google Sheets file [SEE ExportToCareFreeSheets.py]

"""

# Imports
import requests
from bs4 import BeautifulSoup

# Target competitor site
url = "https://www.carefreehomes.com/state/utah-new-homes/"

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
  }

# Initialize final list of lists
carefree_full_list = []
    
# Retrieve and parse HTML
def get_content(url, headers):
    
    response = requests.get(url, headers = headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    return soup

# Create a list of all community URLs
def get_community_list(soup):
    all_links = soup.find_all("a")
    all_links = list(set(all_links))
    
    href_list = []
    
    for link in all_links:
        href = link.get("href")
        href_list.append(href)
                
    href_list = list(set(href_list))
    
    community_string = "https://www.carefreehomes.com/communities/"
    community_list = []
    
    # Only keep hrefs of communities in href_list. Discard all other href values.
    for item in href_list:
        try:
            if community_string in item:
                if "#" in item:
                    continue
                elif "auburn" in item:
                    community_list.append(item)
                elif "cecita" in item:
                    community_list.append(item)
                elif "hawkeye" in item:
                    community_list.append(item)
                elif "sage" in item:
                    community_list.append(item)
                
        except TypeError:
            continue
            
    # Convert list to set (to remove duplicates) and convert back to list
    community_list = list(set(community_list))
      
    return community_list


# For each item in community_list, find and compiled a list of all listed presell home pages
def get_presell_list(communities, headers):
    community_list = communities
    presell_list = []
    
    for community in community_list:
        response = requests.get(community, headers=headers)
        community_content = response.text
        soup = BeautifulSoup(community_content, 'html.parser')
        
        all_links = soup.find_all("a")
        all_links = list(set(all_links))
        
        href_list = []
        
        for link in all_links:
            href = link.get("href")
            href_list.append(href)
                    
        href_list = list(set(href_list))
        
        presell_string = "https://www.carefreehomes.com/model/"
        
        for item in href_list:
            try:
                if presell_string in item:
                    presell_list.append(item)
                    
            except TypeError:
                continue
                
    # Convert list to set (to remove duplicates) and convert back to list
    presell_list = list(set(presell_list)) 
        
    return presell_list
        

# Identify relevant info about presell home, edit syntax, and compile in a list
def get_presell_info(presell_list, headers):
    full_presell_list = presell_list
    master_presell_list = []
    
    for presell in full_presell_list:
        home_full_url = presell
        response = requests.get(home_full_url, headers=headers)
        presell_content = response.text
        soup = BeautifulSoup(presell_content, 'html.parser')
        
        home_elements = soup.find_all(class_="row")
        home_elements_two = soup.find_all(class_="col-sm-3 model-detail")

        # Initialize a variable for each info category
        home_address = "Not Available"
        home_type = "None"        
        home_price = "none"
        home_bedrooms = "none"
        home_bathrooms = "none"
        home_sqft = "none"
        home_garages = "none"
        home_community = "none"
        home_RV = "none"
        home_city = "none"
        
        # Let the editing begin...
        if "sage" in presell:
            home_community = "Sage Haven at Desert Color"
            home_city = "St George"
            home_type = "Townhome"

        elif "desert" in presell:
            home_community = "Auburn Hills at Desert Color"
            home_city = "St George"
            home_type = "Townhome"
            
        elif "auburn" in presell:
            home_community = "Auburn Hills at Desert Color"
            home_city = "St George"
            home_type = "Townhome"

        elif "cecita" in presell:
            home_community = "Cecita Crest at Divario"
            home_city = "St George"
            home_type = "Single Family"

        elif "hawkeye" in home_address:
            home_community = "Hawkeye Pointe"
            home_city = "St George"
            home_type = "Single Family"
        
        else:
            home_community = "Hawkeye Pointe"
            home_city = "St George"

        for element in home_elements_two:
            if "$" in str(element):
                home_price = element.text
                home_price = home_price.replace('$', '')
                home_price = home_price.replace("Price", "")
                home_price = home_price.replace("\n", "")
                home_price = home_price[:20]
                home_price = home_price[13:]
        
        for element in home_elements:
            if "Square Foot" in str(element):
                home_sqft = element.text
                home_sqft = home_sqft.replace("Square Foot", "")
                home_sqft = home_sqft.replace("\n", "")
            elif "Bedrooms" in str(element):
                home_bedrooms = element.text
                home_bedrooms = home_bedrooms.replace(" Bedrooms", "")
                home_bedrooms = home_bedrooms.replace("Bedrooms", "")
                home_bedrooms = home_bedrooms.replace(" Beds", "")
                home_bedrooms = home_bedrooms.replace("\n", "")
            elif "Baths" in str(element):
                home_bathrooms = element.text
                home_bathrooms = home_bathrooms.replace("Baths", "")
                home_bathrooms = home_bathrooms.replace(" \n", "")
                home_bathrooms = home_bathrooms.replace("\n", "")
                home_bathrooms = home_bathrooms.replace(" 1/2", ".5")            
            elif "Garage" in str(element):
                home_garages = element.text
                home_garages = home_garages.replace('Car-Garage', '')
                home_garages = home_garages.replace("Garage", "")
                home_garages = home_garages.replace(" Car", "")
                home_garages = home_garages.replace("\n", "")
                if "R.V." in home_garages:
                   home_RV = "YES"
                   home_garages = home_garages.replace("R.V.", "")
                   home_garages = int(home_garages)
                   home_garages += 1
                else:
                    home_RV = "NO"
            elif "Level" in str(element):
                home_level = element.text
                home_level = home_level.replace("Level", "")
                home_level = home_level.replace("\n", "")
                
                
        master_presell_list.append([home_city, home_community, home_sqft, home_bedrooms, home_bathrooms, home_garages, home_RV, home_level, home_price, home_address, home_full_url])                
    return master_presell_list


# For each item in community_list, find and compiled a list of all available spec home pages
def get_spec_list(soup):
    
    all_links = soup.find_all("a")
    all_links = list(set(all_links))
    
    href_list = []
    
    for link in all_links:
        href = link.get("href")
        href_list.append(href)
                
    href_list = list(set(href_list))
        
    spec_string = "https://www.carefreehomes.com/move-in-ready/"
    spec_list =[]

    for item in href_list:
        try:
            if spec_string in item:
                spec_list.append(item)
                
        except TypeError:
            continue
    
    spec_list = list(set(spec_list))     
        
    return spec_list


# Identify relevant info about spec home, edit syntax, and compile in a list
def get_spec_info(spec_list, headers):
    full_spec_list = spec_list
    
    num = 1
    line = 1
    master_list = []
    
    for spec in full_spec_list:
        home_full_url = spec
        response = requests.get(home_full_url, headers=headers)
        spec_content = response.text
        soup = BeautifulSoup(spec_content, 'html.parser')
        
        home_elements = soup.find_all(class_="row two-lines")

        home_type = "None"        
        home_price = "none"
        home_bedrooms = "none"
        home_bathrooms = "none"
        home_sqft = "none"
        home_garages = "none"
        home_RV = "none"
        home_address = "Not Available"
        
        home_community = soup.find("span", {"class": "breadcrumb_last"}).text
        
        if "Sage" in home_community:
            home_community = "Sage Haven at Desert Color"
            home_city = "St George"
            home_type = "Townhome"

        elif "Auburn" in home_community:
            home_community = "Auburn Hills at Desert Color"
            home_city = "St George"
            home_type = "Townhome"

        elif "Cecita" in home_community:
            home_community = "Cecita Crest at Divario"
            home_city = "St George"
            home_type = "Single Family"

        elif "Hawkeye" in home_community:
            home_community = "Hawkeye Pointe"
            home_city = "St George"
            home_type = "Single Family"

        
        for element in home_elements:
            if "Square Foot" in str(element):
                home_sqft = element.text
                home_sqft = home_sqft.replace("Square Foot", "")
                home_sqft = home_sqft.replace("\n", "")
            elif "Bedrooms" in str(element):
                home_bedrooms = element.text
                home_bedrooms = home_bedrooms.replace(" Bedrooms", "")
                home_bedrooms = home_bedrooms.replace("Bedrooms", "")
                home_bedrooms = home_bedrooms.replace("\n", "")
            elif "Baths" in str(element):
                home_bathrooms = element.text
                home_bathrooms = home_bathrooms.replace("Baths", "")
                home_bathrooms = home_bathrooms.replace(" \n", "")
                home_bathrooms = home_bathrooms.replace("\n", "")
                home_bathrooms = home_bathrooms.replace(" 1/2", ".5")
            elif "$" in str(element):
                home_price = element.text
                home_price = home_price.replace('$', '')
                home_price = home_price.replace("Price", "")
                home_price = home_price.replace("\n", "")
                home_price = home_price[:7]               
            elif "Garage" in str(element):
                home_garages = element.text
                home_garages = home_garages.replace('Car-Garage', '')
                home_garages = home_garages.replace("Garage", "")
                home_garages = home_garages.replace("\n", "")
                if "R.V." in home_garages:
                   home_RV = "YES"
                   home_garages = home_garages.replace("R.V.", "")
                   home_garages = int(home_garages)
                   home_garages += 1
                else:
                    home_RV = "NO"
            elif "Level" in str(element):
                home_level = element.text
                home_level = home_level.replace('Level', '')
                home_level = home_level.replace("\n", "")
                 
        
        master_list.append([home_city, home_community, home_sqft, home_bedrooms, home_bathrooms, home_garages, home_RV, home_level, home_price, home_address, home_full_url])
        num+=1
        line+=1
    
    return master_list


def main_presell():
    master_presell_list = get_presell_info(
            get_presell_list(
                get_community_list(
                    get_content(url, headers)
                    ),
                headers),
            headers)
    return master_presell_list
    
def main_spec():
    master_spec_list = get_spec_info(
        get_spec_list(
            get_content(url, headers)
            ), headers)
    return master_spec_list

# Initialize variables for each "main_" function above.
carefree_presell_list = main_presell()
carefree_spec_list = main_spec()

# Count and add labels for presell list and spec list
carefree_full_list.append(["Buildable Plans", len(carefree_presell_list)])
for item in carefree_presell_list:
    carefree_full_list.append(item)
carefree_full_list.append(["Specs", len(carefree_spec_list)])
for item in carefree_spec_list:
    carefree_full_list.append(item)

# Print to verify    
for home in carefree_full_list:
    print(home)