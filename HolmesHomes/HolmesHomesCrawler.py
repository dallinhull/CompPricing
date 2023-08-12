import requests
from bs4 import BeautifulSoup

# Url for spec homes list
url = "https://holmeshomes.com/properties/marina-lot-5-move-in-ready/"

# Header to mask bot
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
  }

# Retrieve and parse HTML
def get_content(url, headers):
    
    response = requests.get(url, headers = headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    embedded_src = []
    
    embedded_div = soup.find('div', {'class': 'responsive-embed'})
    print(embedded_div)
    iframe = embedded_div.find("iframe")
    print(iframe)
    embedded_src.append(iframe['src'])
    print(embedded_src)
    
    for site in embedded_src:
        embedded_response = requests.get(site, headers=headers)
        embedded_site_content = embedded_response.text
        embedded_soup = BeautifulSoup(embedded_site_content, 'html.parser')
        text_soup = embedded_soup.text
        
        print(embedded_site_content)
        
        
        
    
get_content(url, headers)

   
