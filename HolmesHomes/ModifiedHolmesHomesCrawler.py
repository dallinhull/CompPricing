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
url = "https://holmeshomes.com/search/?locations=st-george"

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
  }

# Initialize final list of lists
holmes_spec_list = []

# Retrieve and parse HTML
def get_content(url, headers):
    
    response = requests.get(url, headers = headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup

# Create a list of all spec home URLs
def get_homes_list(soup):
    info_class_list = []
    spec_list = []
    
    info_class_list = soup.find_all(class_="info")
    
    for item in info_class_list:
        info_text = item.text
        # if "$" in info_text:
        a_tags = item.find_all("a")
        a_tags = list(set(a_tags))
                       
        for a_tag in a_tags:
            href = a_tag.get("href")
            spec_list.append(href)
             
    return spec_list

# Cerate a list of home info for each spec home, compile lists
def get_homes_info(spec_list, headers):
    full_spec_list = spec_list
    num = 1
    master_spec_list = []
    master_presell_list = []
    master_full_list = []
    home_community = ""
    home_city = ""
    home_type = ""
    home_sqft = ""
    home_bedroom = ""
    home_bathroom = ""
    home_garage = ""
    home_price = ""
    home_level = "1"
    home_url = ""
    
    for spec in full_spec_list:
        response = requests.get(spec, headers=headers)
        spec_content = response.text
        soup = BeautifulSoup(spec_content, 'html.parser')
        
        # Home URL
        home_url = spec
        home_url = home_url.replace(" ", "")
        
        # Home Level
        level_class_list = soup.find_all(class_="uk-margin-medium")
        community_class_list = soup.find(class_="uk-h1-")
        for item in level_class_list:
            item_text = item.text
            if "Description" in item_text:
                if "2-story" in item_text:
                    home_level = 2
                elif "second story" in item_text:
                    home_level = 2
                else:
                    home_level = 1
            
            else:
                home_level = 1
        
        # Home Type
        home_type = soup.find("span", {'class': 'uk-text-medium uk-text-transform-none uk-text-small'}).text
        if home_type == "Townhome":
            home_level = "2"
        
        # Home Price
        home_price = soup.find('div', {'class': 'large-text uk-text-secondary uk-text-uppercase uk-text-semibold uk-text-right@s'}).text
        home_price = home_price.replace("Price:", "")
        home_price = home_price.replace(" ", "")
        home_price = home_price.replace("$", "")
        home_price = home_price.replace("\n", "")
        
        # Home City
        if "Washington" in soup.find('div', {'class': 'uk-grid uk-grid-small uk-child-width-1-2@s'}).text:
            home_city = "Washington"
        elif "St. George" in soup.find('div', {'class': 'uk-grid uk-grid-small uk-child-width-1-2@s'}).text:
            home_city = "St George"
        elif "Ivins" in soup.find('div', {'class': 'uk-grid uk-grid-small uk-child-width-1-2@s'}).text:
            home_city = "Ivins"
        elif "Hurricane" in soup.find('div', {'class': 'uk-grid uk-grid-small uk-child-width-1-2@s'}).text:
            home_city = "Hurricane"
        else:
            home_city = "Other"
            
        # Home Community
        community_info = soup.find('h2', {'class': 'uk-h1 uk-margin-small-bottom uk-text-white'})
        home_community = community_info.text
        if home_community == "Whitworth Estates":
            home_city = "Washington"
            
        
        # Home Bedroom, Bathroom, Garage, and SQFT Count
        info_class_list = soup.find_all(class_="info-icon")
    
        for item in info_class_list:
            info_text = item.text
            if "Bedroom" in info_text:
                home_bedroom = info_text
                home_bedroom = home_bedroom.replace("\n", "")
                home_bedroom = home_bedroom.replace("Bedrooms", "")
                
            elif "Bathroom" in info_text:
                home_bathroom = info_text
                home_bathroom = home_bathroom.replace("Bathrooms", "")
                home_bathroom = home_bathroom.replace("\n", "")
                
            elif "Garage" in info_text:
                home_garage = info_text
                home_garage = home_garage.replace("Garage", "")
                home_garage = home_garage.replace("Car", "")
                home_garage = home_garage.replace("\n", "")
                home_garage = home_garage.replace(" ", "")

            elif "Square Feet" in info_text:
                home_sqft = info_text
                home_sqft = home_sqft.replace("Square Feet", "")
                home_sqft = home_sqft.replace("\n", "")
                home_sqft = home_sqft.replace(" ", "")
                        
                  
        # Only append info for Single Family homes 
        if home_type != "Single Family":
            continue
        else:
            if home_price == "ContactAgent":
                master_presell_list.append([home_type, home_city, home_community, home_sqft, home_bedroom, home_bathroom, home_garage, home_level, home_price, home_url])
            else:
                master_spec_list.append([home_type, home_city, home_community, home_sqft, home_bedroom, home_bathroom, home_garage, home_level, home_price, home_url])
            num += 1 
    
    # Count and add labels for presell list and spec list    
    master_full_list.append(["Buildable Plans", len(master_presell_list)])
    for item in master_presell_list:
        master_full_list.append(item)
    master_full_list.append(["Specs", len(master_spec_list)])
    for item in master_spec_list:
        master_full_list.append(item)
    
    for home in master_full_list:
        print(home)
        
    return master_full_list


# Run
holmes_spec_list = get_homes_info(get_homes_list(get_content(url, headers)), headers)