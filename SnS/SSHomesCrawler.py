import requests
from bs4 import BeautifulSoup

# Url for spec homes list
url = "https://sshomes.info/homes/"

# Header to mask bot
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
  }

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
           
    spec_string = "https://sshomes.info/homes/"

    spec_list =[]
    
    for item in href_list:
        try:
            if spec_string in item:
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
    master_list = []
    
    for spec in full_spec_list:
        # Get and parse HTML for each spec home
        home_full_url = spec
        response = requests.get(home_full_url, headers=headers)
        spec_content = response.text
        soup = BeautifulSoup(spec_content, 'html.parser')
        
        # use soup.find/soup.find_all to identify spec data via HTML tag and CSS class id
        multiple_elements = soup.find_all(class_="col-md-9")
        multiple_elements_plus = soup.find_all(class_="col-md-3")
        divided_text = ""
        home_bedrooms = ""
        home_bathrooms = ""
        home_garage = ""
        home_RV = ""
        home_sqft = ""
        home_community = ""
        home_floors = ""
        home_price = ""
        home_address = ""
        home_url = home_full_url
        
        

        for item in multiple_elements_plus:
            h2_tags = item.find_all("h2")
            for h2_tag in h2_tags:
                text = h2_tag.text
                if "$" in text:
                    text = text.replace("\n", "")
                    text = text.replace("\t", "")
                    text = text.replace("$", "")
                    text = text.replace("*", "")
                    if "-" in text:
                        text = text.split("-")
                        text = text[0]
                    home_price = text

        
        try:
            city_text = soup.find("h2", {"class": "margin-t-none margin-b-sm"}).text
            if "Washington" in city_text:
                home_city = "Washington"
            elif "Ivins" in city_text:
                home_city = "Ivins"
            elif "St George" in city_text:
                home_city = "St George"
            elif "St. George" in city_text:
                home_city = "St George"
            elif "Hurricane" in city_text:
                home_city = "Hurricane"
            else:
                home_city = "Other"
        except AttributeError:
            home_city = "BUG BUG BUG"
            
        if  home_city == "BUG BUG BUG":   
            try:
                city_text = soup.find("h2", {"class": "margin-b-none margin-t-none"}).text
                if "Washington" in city_text:
                    home_city = "Washington"
                elif "Ivins" in city_text:
                    home_city = "Ivins"
                elif "St George" in city_text:
                    home_city = "St George"
                elif "St. George" in city_text:
                    home_city = "St George"
                elif "Hurricane" in city_text:
                    home_city = "Hurricane"
                else:
                    home_city = "Other"
            except AttributeError:
                home_city = "BUG BUG BUG"
                
        street_address = soup.find("h2", {"class": "margin-b-none margin-t-none"}).text
        
        if street_address == city_text:
            home_address =  street_address
        else:
            home_address = f"{street_address}, {city_text}"
        

        # Narrow in on the spec info
        for element in multiple_elements:
            h4_tags = element.find_all("h4")
            for h4_tag in h4_tags:
                text = h4_tag.text
                if "Neighborhood: " in text:
                    neighborhood_text = text.replace("Neighborhood: ", "")
                    neighborhood_text = neighborhood_text.replace("\n", "")
                    neighborhood_text = neighborhood_text.replace("\t", "")
                    neighborhood_text = neighborhood_text.replace("\xa0", "")
                    home_community = neighborhood_text
                if "100" in text:
                    continue
                if "Bed" in text:
                    divided_text = text.replace("\t", "")
                    divided_text = divided_text.split(" •")
                    for item_order, item in enumerate(divided_text):
                        item = item.replace("\n", "")
                        item = item.replace("                                      ", "")
                        item = item.replace("\xa0", "")
                        item = item.replace("Bed", "")
                        item = item.replace("Bath", "")
                        item = item.replace("Garage", "")
                        item = item.replace("RV:", "")
                        item = item.replace("ft2", "")
                        divided_text[item_order] = item
                    home_bedrooms = divided_text[0]
                    home_bathrooms = divided_text[1]
                    home_garage = divided_text[2]
                    home_RV = divided_text[3]
                    home_sqft = divided_text[4]
                   
                    
        #         # Create a list of lists master_list[all data per spec][each item of data within spec]
        if home_price != "":

            master_list.append([home_city, home_community, home_sqft, home_bedrooms, home_bathrooms, home_garage, home_RV, home_price, home_address, home_url])
            num += 1
    master_list.insert(0,["Specs", len(master_list)])
      
    return master_list                


ss_spec_list = get_spec_info(get_spec_list(get_content(url, headers)), headers)        


# Run it
# def main():
#     get_spec_info(
#         get_spec_list(
#             get_content(url, headers)
#             ), headers)
    
    
# # Assign master_list to universal variable
# ss_spec_list = main()
for item in ss_spec_list:
    print(item)    


