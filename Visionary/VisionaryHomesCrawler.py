import requests
from bs4 import BeautifulSoup
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')

# Url for spec homes list
spec_url = "https://visionaryhomes.com/new-homes/st-george/available/"

# Url for presell homes list
presell_url = "https://visionaryhomes.com/new-homes/st-george/"

# Header to mask bot
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
  }

# Presells + Specs List
visionary_full_list = []

# Retrieve and parse HTML
def get_content(url, headers):
    
    response = requests.get(url, headers = headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup

# Create a list of all spec nhome URLs
def get_spec_list(soup):
    
    all_links = soup.find_all("a")
    all_links = list(set(all_links))
    
    href_list = []
    
    for link in all_links:
        href = link.get("href")
        href_list.append(href)
                
    href_list = list(set(href_list))
           
    spec_string = "/new-homes/ut"
    spec_list =[]

    for item in href_list:
        try:
            if spec_string in item:
                if "utah-county" not in item:
                    spec_list.append(item)
                
        except TypeError:
            continue
            #print("Stupid TypeError")
    
    spec_list = list(set(spec_list))     
        
    return spec_list
        
        
# Go into each spec URL, get/parse HTML, and org. specific data on each home into lists
def get_spec_info(spec_list, headers):
    full_spec_list = spec_list
    
    num = 1
    line = 1
    master_list = []
    
    for spec in full_spec_list:
        # Get and parse HTML for each spec home
        
        home_full_url = f"https://visionaryhomes.com{spec}"
        response = requests.get(home_full_url, headers=headers)
        spec_content = response.text
        soup = BeautifulSoup(spec_content, 'html.parser')
        
        # use soup.find/soup.find_all to identify spec data via HTML tag and CSS class id
        home_elements = soup.find_all(class_="pr-4 pr-3-sm")
        home_elements_community_floorplan = soup.find_all(class_= "favText spec")
        

        home_type = soup.find("p", {"class": "searchText detail"}).text
        if home_type is str:
            try:
                home_type = home_type
                    
            except AttributeError:
                home_type = "error"
                continue
                #print("Stupid TypeError")
        home_address = soup.find("h4", {"class": "bannerTitle"}).text
        home_price = soup.find("h4", {"class": "sub mapSub mb-0"}).text
        home_price = home_price.replace('Priced $', '')
        
        home_status = "Spec"
        home_levels = "To Be Coded"
        home_bedrooms = "blank"
        home_bathrooms = "blank"
        home_sqft = "blank"
        home_city = "blank"
        home_garages = "To Be Coded"
        home_community = "blank"
        
        if "st-george" in spec:
            home_city = "St George"
        elif "washington" in spec:
            home_city = "Washington"
        
        
        for element in home_elements:
            if "fas fa-ruler-triangle pr-2 pr-3-sm" in str(element):
                home_sqft = element.text
                continue
            elif "fas fa-bed-alt pr-2 pr-3-sm" in str(element):
                home_bedrooms = element.text
                continue
            elif "fas fa-bath pr-2 pr-3-sm" in str(element):
                home_bathrooms = element.text
            elif "fas fa-garage-car pr-2 pr-3-sm" in str(element):
                home_garages = element.text
                break
            
        for element in home_elements_community_floorplan:
            element = element.text
            element = element.upper()
            if "DIVARIO" in element:
                home_community = "Divario"
                continue
            elif "DESERT COLOR" in element:
                home_community = "Desert Color"
                continue
            elif "WARNER GATEWAY" in element:
                home_community = "Warner Gateway"
                continue
            elif "SONORAN" in element:
                home_levels = "1"
            elif "CLIFFROSE" in element:
                home_levels = "1"
            elif "AGAVE" in element:
                home_levels = "1"
            elif "SEDONA" in element:
                home_levels = "1"
            elif "PONDEROSA" in element:
                home_levels = "2"
            elif "ANASAZI" in element:
                home_levels = "2"
            elif "SAGUARO" in element:
                home_levels = "2"
            elif "ADENIUM" in element:
                home_levels = "1"
            elif "SIENNA" in element:
                home_levels = "1"
            elif "MESA" in element:
                home_levels = "1"
            elif "ARROYO" in element:
                home_levels = "2"
                
            
            
        
        # Create a list of lists master_list[all data per spec][each item of data within spec]
        if "Single Family" in home_type:
            master_list.append([home_status, home_city, home_community, home_sqft, home_bedrooms, home_bathrooms, home_garages, home_levels, home_price, home_address, home_full_url])
            num+=1
            line+=1

        

    return master_list

def get_presell_list(soup):
    
    # Find all SINGLE FAMILY HOMES
    # Find div elements with class="card-body z-1"
    card_body_elements = soup.find_all('div', {'class': 'card-body z-1'})
    #
    new_home_links = []
    
    # Extract all href values containing "/new-homes/ut" from 
    # communities with Single Family homes to new_home_links
    for card_body in card_body_elements:

        # Remove next line if you also want condos and townhomes
        if "Single Family" in card_body.text:

            for link in card_body.find_all('a'):
                href = link.get('href')
                if "/new-homes/ut" in href:
                    new_home_links.append(href)
        # Print the resulting list of links
    return new_home_links

def get_community_floor_plans(presell_list, headers):
    presells = presell_list
    total_presell_list = []
    
    desert_color_floorplan_string = re.compile("/new-homes/ut/st-george/desert-color-st-george/[a-zA-Z][a-zA-Z]*")
    divario_floorplan_string = re.compile("/new-homes/ut/st-george/divario/[a-zA-Z][a-zA-Z]*")    
    warner_gateway_floorplan_string = re.compile("/new-homes/ut/washington/warner-gateway/[a-zA-Z][a-zA-Z]*")          
        # "/new-homes/ut/st-george/desert-color-single-family-homes/saguaro/143877/" 
        # "/new-homes/ut/st-george/desert-color-single-family-homes/mojave/101386/"
    for presell in presells:
        if "desert-color" in presell:
            community_full_url = f"https://visionaryhomes.com{presell}"
            response = requests.get(community_full_url, headers=headers)
            community_content = response.text
            community_soup = BeautifulSoup(community_content, 'html.parser')
            
            all_links = community_soup.find_all("a", href=desert_color_floorplan_string)
            all_links = list(set(all_links))
        
            
            href_list = []
            
            for link in all_links:
                href = link.get("href")
                href_list.append(href)
                        
            href_list = list(set(href_list))           
            community_floorplan_list = href_list  

            for plan in community_floorplan_list:
                total_presell_list.append(plan)
                 
                
        elif "divario" in presell:
            community_full_url = f"https://visionaryhomes.com{presell}"
            response = requests.get(community_full_url, headers=headers)
            community_content = response.text
            community_soup = BeautifulSoup(community_content, 'html.parser')
            
            all_links = community_soup.find_all("a", href=divario_floorplan_string)
            all_links = list(set(all_links))

            
            href_list = []
            
            for link in all_links:
                print(link) #CURRENTLY GIVING ME NO LINKS!!!
                href = link.get("href")
                href_list.append(href)
                        
            href_list = list(set(href_list))  
            community_floorplan_list = href_list  

            for plan in community_floorplan_list:
                total_presell_list.append(plan) 
                
        elif "warner-gateway" in presell:
            community_full_url = f"https://visionaryhomes.com{presell}"
            response = requests.get(community_full_url, headers = headers)
            community_content = response.text
            community_soup = BeautifulSoup(community_content, 'html.parser')
            
            all_links = community_soup.find_all("a", href=warner_gateway_floorplan_string)
            all_links = list(set(all_links))
            
            href_list = []
            
            for link in all_links:
                href = link.get("href")
                href_list.append(href)
                        
            href_list = list(set(href_list))    
            community_floorplan_list = href_list  

            for plan in community_floorplan_list:
                total_presell_list.append(plan) 
                     
    return total_presell_list   
        
        # print(community_soup.find(class_='homeTypeText'))
        # community_plans = community_soup.find_all(class_='card oi-map-item plan-map-item vert-card')
        # print(community_plans)

def get_presell_info(presell_list, headers):
    full_presell_list = presell_list
    
    num = 1
    line = 1
    master_list = []
    
    for presell in full_presell_list:
        # Get and parse HTML for each spec home
        home_full_url = f"https://visionaryhomes.com{presell}"
        response = requests.get(home_full_url, headers=headers)
        presell_content = response.text
        soup = BeautifulSoup(presell_content, 'html.parser')
        
        # use soup.find/soup.find_all to identify spec data via HTML tag and CSS class id
        home_elements = soup.find_all(class_="pr-4 pr-3-sm")

        home_type = soup.find("p", {"class": "searchText detail"}).text
        home_price = soup.find("h4", {"class": "sub mapSub col-xs-12 my-0"}).text
        home_levels = soup.find("h4", {"class": "bannerTitle"}).text
        home_price = home_price.replace('Starting from $', '')
        home_status = "Buildable"
        home_city = "none"
        home_address = "none"
        home_bedrooms = "none"
        home_bathrooms = "none"
        home_sqft = "none"
        # home_levels = "To Be Coded"
        for element in home_elements:
            if "fas fa-garage-car pr-2 pr-3-sm" in str(element):
                home_garages = element.text
                home_garages = home_garages.replace(".0", "")
                home_garages = home_garages.replace(" - 3", '')
                home_garages = home_garages.replace(" - 4", '')
        
        if "divario" in presell:
            home_city = "St George"
            home_community = "Divario"
        elif "desert" in presell:
            home_city = "St George"
            home_community = "Desert Color"
        elif "warner" in presell:
            home_city = "Washington"
            home_community = "Warner Gateway"
        
        home_levels = home_levels.upper()
        if "SONORAN" in home_levels:
            home_levels = "1"
        elif "CLIFFROSE" in home_levels:
            home_levels = "1"
        elif "AGAVE" in home_levels:
            home_levels = "1"
        elif "SEDONA" in home_levels:
            home_levels = "1"
        elif "PONDEROSA" in home_levels:
            home_levels = "2"
        elif "ANASAZI" in home_levels:
            home_levels = "2"
        elif "SAGUARO" in home_levels:
            home_levels = "2"
        elif "ADENIUM" in home_levels:
            home_levels = "1"
        elif "SIENNA" in home_levels:
            home_levels = "1"
        elif "MESA" in home_levels:
            home_levels = "1"
        elif "ARROYO" in home_levels:
            home_levels = "2"
        
        for element in home_elements:
            if "fas fa-ruler-triangle pr-2 pr-3-sm" in str(element):
                home_sqft = element.text
                home_sqft = home_sqft.replace("Total Sq.Ft. ", "")
                continue
            if "fas fa-bed-alt pr-2 pr-3-sm" in str(element):
                home_bedrooms = element.text
                home_bedrooms = home_bedrooms.replace(' - 3', '')
                home_bedrooms = home_bedrooms.replace(' - 4', '')
                home_bedrooms = home_bedrooms.replace(' - 5', '')
                home_bedrooms = home_bedrooms.replace(' - 6', '')
                continue
            elif "fas fa-bath pr-2 pr-3-sm" in str(element):
                home_bathrooms = element.text
                home_bathrooms = home_bathrooms.replace(' - 2', '')
                home_bathrooms = home_bathrooms.replace(' - 1.5', '')
                home_bathrooms = home_bathrooms.replace(' - 3', '')
                home_bathrooms = home_bathrooms.replace(' - 2.5', '')
                home_bathrooms = home_bathrooms.replace(' - 3.5', '')
                break
        
        # Create a list of lists master_list[all data per spec][each item of data within spec]
        #if "Single Family" in home_type:
            master_list.append([home_status, home_city, home_community, home_sqft, home_bedrooms, home_bathrooms, home_garages, home_levels, home_price, home_full_url])
            num+=1
            line+=1

        

    return master_list

        # for plan in community_plans:
        
# Run it
def main_presell():
    master_presell_info_list = get_presell_info(
        get_community_floor_plans(
            get_presell_list(
                get_content(presell_url, headers), 
                ), 
            headers), 
        headers)
    print(master_presell_info_list)
    return master_presell_info_list

def main_spec():
    master_spec_info_list = get_spec_info(
        get_spec_list(
            get_content(spec_url, headers)
            ),headers)
    
    return master_spec_info_list
    
# Assign presells and specs to universal variable
visionary_presell_list = main_presell()
visionary_spec_list = main_spec()    


visionary_full_list.append(["Buildable Plans", len(visionary_presell_list)])
for item in visionary_presell_list:
    visionary_full_list.append(item)
visionary_full_list.append(["Specs", len(visionary_spec_list)])
for item in visionary_spec_list:
    visionary_full_list.append(item)

for item in visionary_full_list:
    print(item)




